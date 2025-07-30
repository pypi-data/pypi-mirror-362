import json
import logging
import os
import re
import sys
from collections import defaultdict, Counter
from concurrent.futures import as_completed
from datetime import timedelta
from pathlib import Path
from typing import List, Iterable

import pandas as pd
import pytest
import requests
from pyconverters_newsml.newsml import (
    NewsMLConverter,
    NewsMLParameters,
    get_mediatopics,
)
from pymongo import MongoClient, UpdateOne
from pymultirole_plugins.v1.schema import Document
from requests_cache import CachedSession
from requests_futures.sessions import FuturesSession
from reverso_api.context import ReversoContextAPI
from sklearn.model_selection import train_test_split
from starlette.datastructures import UploadFile
from tqdm import tqdm

testdir = Path(__file__).parent
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level="INFO",
    handlers=[logging.FileHandler(testdir / "tests.log"), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)
SCW_ADMIN_MONGO_PWD = os.getenv("SCW_ADMIN_MONGO_PWD")


def test_newsml_text():
    model = NewsMLConverter.get_model()
    model_class = model.construct().__class__
    assert model_class == NewsMLParameters
    converter = NewsMLConverter()
    parameters = NewsMLParameters(
        subjects_as_metadata="afpperson,afporganization,afplocation",
        keywords_as_categories=True,
    )
    testdir = Path(__file__).parent
    source = Path(testdir, "data/text_only.xml")
    with source.open("r") as fin:
        docs: List[Document] = converter.convert(
            UploadFile(source.name, fin, "text/xml"), parameters
        )
        assert len(docs) == 1
        doc0 = docs[0]
        assert doc0.metadata["nature"] == "text"
        assert doc0.metadata["language"] == "es"
        assert "Agence américaine d'information" in doc0.metadata["afporganization"]
        assert "New York" in doc0.metadata["afplocation"]
        assert len(doc0.categories) == 3


def test_newsml_pics():
    model = NewsMLConverter.get_model()
    model_class = model.construct().__class__
    assert model_class == NewsMLParameters
    converter = NewsMLConverter()
    parameters = NewsMLParameters(
        subjects_as_metadata="medtop,afpperson,afporganization,afplocation",
        subjects_code=True,
        mediatopics_as_categories=True,
        natures="text,picture,video",
    )
    testdir = Path(__file__).parent
    source = Path(testdir, "data/text_and_pics.xml")
    with source.open("r") as fin:
        docs: List[Document] = converter.convert(
            UploadFile(source.name, fin, "text/xml"), parameters
        )
        assert len(docs) == 6
        doc0 = docs[0]
        assert doc0.metadata["nature"] == "text"
        assert doc0.metadata["language"] == "fr"
        assert "20000579:national elections" in doc0.metadata["medtop"]
        assert "20000065:civil unrest" in doc0.metadata["medtop"]
        cat_labels = [cat.label for cat in doc0.categories]
        assert ["national elections" in cat_label for cat_label in cat_labels]
        assert ["civil unrest" in cat_label for cat_label in cat_labels]
        doc5 = docs[5]
        assert doc5.metadata["nature"] == "picture"
        assert doc5.metadata["language"] == "fr"
        assert "79588:Pascal Affi N'Guessan" in doc5.metadata["afpperson"]
        assert "1894:Abidjan" in doc5.metadata["afplocation"]
        cat_labels = [cat.label for cat in doc5.categories]
        assert ["national elections" in cat_label for cat_label in cat_labels]
        assert ["electoral system" in cat_label for cat_label in cat_labels]


def test_newsml_agenda():
    model = NewsMLConverter.get_model()
    model_class = model.construct().__class__
    assert model_class == NewsMLParameters
    converter = NewsMLConverter()
    parameters = NewsMLParameters()
    testdir = Path(__file__).parent
    source = Path(testdir, "data/agenda.xml")
    with source.open("r") as fin:
        docs: List[Document] = converter.convert(
            UploadFile(source.name, fin, "text/xml"), parameters
        )
        assert len(docs) == 1


APP_EF_URI = "https://vital.kairntech.com"
APP_EF_URI3 = "https://sherpa-entityfishing.kairntech.com"
APP_EF_URI2 = "https://cloud.science-miner.com/nerd"


class EntityFishingClient:
    def __init__(self, base_url=APP_EF_URI):
        self.base_url = base_url[0:-1] if base_url.endswith("/") else base_url
        self.dsession = requests.Session()
        self.dsession.headers.update(
            {"Content-Type": "application/json", "Accept": "application/json"}
        )
        self.dsession.verify = False
        self.ksession = CachedSession(
            cache_name="ef_cache",
            backend="sqlite",
            cache_control=True,  # Use Cache-Control headers for expiration, if available
            expire_after=timedelta(
                weeks=1
            ),  # Otherwise expire responses after one week
            allowable_methods=[
                "GET"
            ],  # Cache POST requests to avoid sending the same data twice
        )
        self.ksession.headers.update(
            {"Content-Type": "application/json", "Accept": "application/json"}
        )
        self.ksession.verify = False
        self.fsession = FuturesSession(session=self.ksession)
        self.disamb_url = "/service/disambiguate/"
        self.kb_url = "/service/kb/concept/"
        self.term_url = "/service/kb/term/"

    def disamb_query(
        self, text, lang, minSelectorScore, entities=None, sentences=None, segment=False
    ):
        disamb_query = {
            "text": text.replace("\r\n", " \n"),
            "entities": entities,
            "sentences": sentences,
            "language": {"lang": lang},
            "mentions": ["wikipedia"],
            "nbest": False,
            "sentence": segment,
            "customisation": "generic",
            "minSelectorScore": minSelectorScore,
        }
        try:
            resp = self.dsession.post(
                self.base_url + self.disamb_url, json=disamb_query, timeout=(60, 300)
            )
            if resp.ok:
                return resp.json()
            else:
                resp.raise_for_status()
        except BaseException:
            logger.warning("An exception was thrown!", exc_info=True)
        return {}

    def disamb_terms_query(
        self,
        termVector,
        lang,
        minSelectorScore,
        entities=None,
        sentences=None,
        segment=False,
    ):
        disamb_query = {
            "termVector": termVector,
            "entities": entities,
            "sentences": sentences,
            "language": {"lang": lang},
            "mentions": ["wikipedia"],
            "nbest": False,
            "sentence": segment,
            "customisation": "generic",
            "minSelectorScore": minSelectorScore,
        }
        resp = self.dsession.post(
            self.base_url + self.disamb_url, json=disamb_query, timeout=(30, 300)
        )
        if resp.ok:
            return resp.json()
        else:
            return {}

    def get_kb_concept(self, qid):
        try:
            resp = self.ksession.get(
                self.base_url + self.kb_url + qid, timeout=(30, 300)
            )
            if resp.ok:
                return resp.json()
            else:
                resp.raise_for_status()
        except BaseException:
            logger.warning("An exception was thrown!", exc_info=True)
        return {}

    def get_kb_concepts(self, qids: Iterable):
        futures = [self.fsession.get(self.base_url + self.kb_url + qid) for qid in qids]
        concepts = {qid: None for qid in qids}
        for future in as_completed(futures):
            try:
                resp = future.result()
                if resp.ok:
                    concept = resp.json()
                    if "wikidataId" in concept:
                        concepts[concept["wikidataId"]] = concept
                else:
                    resp.raise_for_status()
            except BaseException:
                logger.warning("An exception was thrown!", exc_info=True)
        return concepts

    def compute_fingerprint(self, docid, yeardir, fingerprints):
        jsondir = yeardir / "json"
        tokens = []
        result = None
        if jsondir.exists():
            filename = docid2filename(docid)
            jsonfile = jsondir / f"{filename}.json"
            if jsonfile.exists():
                with jsonfile.open("r") as jfin:
                    result = json.load(jfin)
            else:
                logger.warning(f"Can't find file {jsonfile}")
        else:
            logger.warning(f"Can't find dir {jsondir}")
            # result = self.disamb_query(text, lang, 0.2, None, None)
        if result is not None:
            entities = (
                [entity for entity in result["entities"] if "wikidataId" in entity]
                if "entities" in result
                else []
            )
            qids = {entity["wikidataId"] for entity in entities}
            concepts = self.get_kb_concepts(qids)
            for entity in entities:
                qid = entity["wikidataId"]
                tokens.append(qid)
                concept = concepts[qid]
                if concept is not None:
                    if "statements" in concept:
                        finger_sts = list(
                            filter(
                                lambda st: st["propertyId"] in fingerprints and isinstance(st["value"], str),
                                concept["statements"],
                            )
                        )
                        if finger_sts:
                            fingerprint = {
                                st["value"]
                                for st in finger_sts
                                if st["value"].startswith("Q")
                            }
                            tokens.extend(fingerprint)
            return " ".join(tokens)
        return None


def docid2filename(docid):  # noqa
    if docid.startswith("urn:"):
        parts = docid.split(":")
        filename = parts[-1]
    elif docid.startswith("http:"):
        parts = docid.split("/")
        filename = parts[-1]
    else:
        filename = None
    return filename


@pytest.fixture(scope="session")
def get_mongo():
    REMOTE_MONGO = False
    if REMOTE_MONGO:
        from ssh_pymongo import MongoSession

        session = MongoSession(
            host="sherpa-scw.kairntech.com",
            port=22,
            user="oterrier",
            key="/home/olivier/.ssh/id_rsa",
            uri=f"mongodb://admin:{SCW_ADMIN_MONGO_PWD}@localhost:27017/",
        )
        mongo = session.connection
    else:
        mongo_uri = "mongodb://localhost:27017/"
        mongo = MongoClient(mongo_uri)
    return mongo


@pytest.mark.skip(reason="Not a test")
def test_consolidate_cats(get_mongo):  # noqa
    dbname = "afp_iptc_health"
    root = "07000000"
    topics = get_mediatopics()
    count_min = 50
    root_topics = {k: v for k, v in topics.items() if v.levels[0] == root}
    counts = defaultdict(int)
    db = get_mongo[dbname]
    for doc in db.documents.find():
        if doc["categories"]:
            for cat in doc["categories"]:
                labels = cat["labelName"].split("_")
                for label in labels:
                    counts[label] += 1
    for level in range(5, 1, -1):
        logger.info(f"Consolidating level {level}")
        level_topics = {k: v for k, v in root_topics.items() if len(v.levels) == level}
        level_conso = []
        for code in level_topics:
            topic = level_topics[code]
            count = counts[code]
            if 0 < count < count_min:
                level_conso.append(topic)
        for t in level_conso:
            logger.info(f"Dropping {t.label}")
            parentCode = t.levels[-2]
            parent = root_topics[parentCode]
            parentName = "_".join(parent.levels)
            labelName = "_".join(t.levels)
            cat_filter = {"categories.labelName": labelName}
            cat_rename = {"$set": {"categories.$.labelName": parentName}}
            result = db.documents.update_many(cat_filter, cat_rename)
            if result.acknowledged:
                logger.info(
                    "%d document categories consolidated" % result.modified_count
                )


@pytest.mark.skip(reason="Not a test")
def test_titles_lang(get_mongo):  # noqa
    dbname = "afp_iptc_politics"
    db = get_mongo[dbname]
    pipeline = [
        {"$match": {"metadata.nature": "text"}},
        {
            "$group": {
                "_id": {"lang": "$metadata.language"},
                "docs": {"$push": "$$ROOT"},
            }
        },
    ]
    results = db.documents.aggregate(pipeline, allowDiskUse=True)
    titles = defaultdict(dict)
    for result in results:
        lang = result["_id"]["lang"]
        cat = result["_id"]["cat"]
        cats = titles[cat]
        if lang not in cats:
            cats[lang] = []
        for doc in result["docs"]:
            cats[lang].append(doc["title"])
    datadir = Path(__file__).parent / "data"
    tsource = datadir / "politics_train.tsv"
    dsource = datadir / "politics_dev.tsv"
    with tsource.open("w") as tfout:
        with dsource.open("w") as dfout:
            for cat, cats in titles.items():
                for lang, ltitles in cats.items():
                    if len(ltitles) > 2:
                        train, test = train_test_split(
                            ltitles, train_size=min(10, len(ltitles) - 1), shuffle=True
                        )
                        for t in train:
                            t = (
                                t.replace("\t", " ")
                                .replace("\n", " ")
                                .replace("\r", "")
                            )
                            tfout.write(f"{cat}\t{t}\n")
                        for t in test:
                            t = (
                                t.replace("\t", " ")
                                .replace("\n", " ")
                                .replace("\r", "")
                            )
                            dfout.write(f"{cat}\t{t}\n")


@pytest.mark.skip(reason="Not a test")
def test_clean_slugs(get_mongo):  # noqa
    hapax_min = 2
    dbname = "afp_slug_en"
    db = get_mongo[dbname]
    nb_docs, counter = count_documents_per_cats(db)

    counts = defaultdict(list)
    for (label, count) in counter.most_common():
        res = re.search(r"^(.+)_([0-9]+)$", label)
        if res:
            lab = res.group(1)
            counts[lab].append((label, count))
        else:
            counts[label].append((label, count))
    for label, lcounts in counts.items():
        if len(lcounts) > 1:
            total = sum([x[1] for x in lcounts])
            lcounts.sort(key=lambda x: x[1])
            labs = [lab[0] for lab in lcounts]
            lab = labs.pop()
            rename_documents_cats(db, lab, labs)
            if total <= hapax_min:
                delete_documents_label(db, lab)
        else:
            total = lcounts[0][1]
            if re.match(r"^[0-9]+$", label) or total <= hapax_min:
                delete_documents_label(db, label)


@pytest.mark.skip(reason="Not a test")
def test_cleanplus_slugs(get_mongo):
    trans_dict = {'_': '', '0': '', '1': '', '2': '', '3': '', '4': '', '5': '', '6': '', '7': '', '8': '', '9': ''}
    mytable = str.maketrans(trans_dict)
    # noqa
    dbname = "afp_slug_en"
    db = get_mongo[dbname]
    nb_docs, counter = count_documents_per_cats(db)

    counts = defaultdict(list)
    for (label, count) in counter.most_common():
        lab = label.translate(mytable)
        if lab:
            counts[lab].append((label, count))
    translations = []
    for label, lcounts in counts.items():
        if len(lcounts) > 1:
            lcounts.sort(key=lambda x: x[1])
            labs = [lab[0] for lab in lcounts]
            lab = labs.pop()
            for ll in labs:
                translations.append(
                    {
                        "name": ll,
                        "to": {"name": lab},
                    }
                )
    testdir = Path(__file__).parent
    source = Path(testdir, dbname + "_plus.json")
    with source.open("w") as fout:
        json.dump(translations, fout, indent=2)


def rename_documents_cats(db, label, labels, doit=True):
    if doit:
        db.documents.update_many(
            {"categories.labelName": {"$in": labels}},
            {"$set": {"categories.$.labelName": label}},
        )
        db.labels.delete_many({"name": {"$in": labels}})


def delete_documents_label(db, label, doit=True):  # noqa
    if doit:
        db.documents.update_many({}, {"$pull": {"categories": {"labelName": label}}})
        db.labels.delete_one({"name": label})


def short_lang(lang):
    return lang[0:2] if len(lang) > 2 else lang


DEEPL_API_KEY = os.environ.get("DEEPL_API_KEY")


def get_translator(auth_key):
    import deepl
    translator = deepl.Translator(auth_key)
    return translator


@pytest.mark.skip(reason="Not a test")
def test_translate_slugs(get_mongo):  # noqa
    import enchant
    from deepl import DeepLException
    from thefuzz import process, fuzz

    langs = ["fr_FR_LRG", "en_US", "es", "pt_PT", "de_DE", "ar"]
    deeplangs = ["FR", "EN-US", "ES", "PT-PT", "DE", "AR"]
    language = "en_US"
    langid = langs.index(language)
    translator = get_translator(DEEPL_API_KEY)
    broker = enchant.Broker()
    broker.describe()
    dicts = {}
    dbname = "afp_slug_" + short_lang(language)

    for lang in langs:
        dicts[lang] = enchant.Dict(lang)
    db = get_mongo[dbname]
    labelnames = get_labels(db)
    labels = labelnames.inverse
    translations = []
    candidate_labels = list(labels.keys())
    candidate_labels.extend(labels.values())
    for label in labels:
        if not dicts[language].check(label):
            print(f"Label {label} does not exist in {language}")
            found = False
            for il, l in enumerate(langs):
                if il != langid:
                    if dicts[l].check(label):
                        print(f"Label {label} does exist in {l}")
                        try:
                            if language == "ar":
                                api = ReversoContextAPI(source_text=label, source_lang=short_lang(l), target_lang="ar")
                                for source_word, trans_label, frequency, part_of_speech, inflected_forms in api.get_translations():
                                    break
                            else:
                                trans_label = translator.translate_text(
                                    label,
                                    source_lang=short_lang(l).upper(),
                                    target_lang=deeplangs[langid],
                                ).text
                            closest = process.extractOne(
                                trans_label,
                                candidate_labels,
                                scorer=fuzz.UQRatio,
                                score_cutoff=90,
                            )
                            if closest:
                                closest_label = closest[0]
                                closest_score = closest[1]
                                iclosest = candidate_labels.index(closest_label)
                                if iclosest < len(labels):
                                    closest_name = labels[closest_label]
                                else:
                                    closest_name = closest_label
                                    closest_label = labelnames[closest_name]
                                if closest_label != label:
                                    print(
                                        f"Move label {label} to {closest_name}/{closest_label} with score {closest_score}"
                                    )
                                    found = True
                                    translations.append(
                                        {
                                            "name": labels[label],
                                            "label": label,
                                            "to": {
                                                "name": closest_name,
                                                "label": closest_label,
                                                "score": closest_score,
                                            },
                                        }
                                    )
                                    break
                        except DeepLException:
                            print(sys.exc_info())
                            exit(-1)
            if not found:
                print(f"Can't move {label} to a known label")
                translations.append({"name": labels[label], "label": label})

    testdir = Path(__file__).parent
    source = Path(testdir, dbname + ".json")
    with source.open("w") as fout:
        json.dump(translations, fout, indent=2)


@pytest.mark.skip(reason="Not a test")
def test_apply_translate_slugs(get_mongo):  # noqa
    language = "en"
    plus = ''
    # plus = '_plus'
    dbname = "afp_slug_" + language
    testdir = Path(__file__).parent
    source = Path(testdir, f"{dbname}{plus}_reviewed.json")
    with source.open("r") as fin:
        translations = json.load(fin)
    db = get_mongo[dbname]

    for translation in translations:
        from_name = translation['name']
        to_name = translation.get('to', {}).get('name', None)
        if to_name:
            rename_documents_cats(db, to_name, [from_name])


@pytest.mark.skip(reason="Not a test")
def test_downsampling_cats(get_mongo):  # noqa
    dbname = "afp_iptc_health"
    db = get_mongo[dbname]
    nb_docs, counter = count_documents_per_cats(db)
    # max_docs = int(nb_docs / 10)
    max_docs = 1000
    # min_docs = 50
    # small_cats = [k for (k, v) in counter.most_common() if v < min_docs]
    big_cats = [k for (k, v) in counter.most_common(50) if v > max_docs]
    for label in big_cats:
        nb = counter[label]
        if nb > max_docs:
            # delete_topcat_if_leave(db, label)
            # delete_documents_for_cat(db, label, (nb - max_docs))
            nb_docs, counter = count_documents_per_cats(db)


@pytest.mark.skip(reason="Not a test")
def test_downsampling_kw(get_mongo):  # noqa
    dbname = "afp_iptc_health"
    db = get_mongo[dbname]
    pipeline = [
        {
            # '$match': {
            #     'text': re.compile(r"covid|coronavirus(?i)")
            # }
            "$match": {"text": re.compile(r"فيروس كورونا|كوفيد")}
        },
        {
            "$match": {
                "categories.labelName": {
                    "$in": [
                        "07000000_20000446_20000448_20000451",
                        "07000000_20000446_20000448_20000449_20001218",
                        "07000000_20000446_20000448_20000449",
                        "07000000_20000446_20000448_20000451",
                    ]
                }
            }
        },
        {
            "$project": {
                "identifier": 1,
                "items": {
                    "$filter": {
                        "input": "$categories",
                        "as": "item",
                        "cond": {
                            "$in": [
                                "$$item.labelName",
                                [
                                    "07000000_20000446_20000448_20000451",
                                    "07000000_20000446_20000448_20000449_20001218",
                                    "07000000_20000446_20000448_20000449",
                                    "07000000_20000446_20000448_20000451",
                                ],
                            ]
                        },
                    }
                },
                "categories": 1,
                "nb_cats": {"$size": "$categories"},
            }
        },
        {
            "$project": {
                "identifier": 1,
                "items": 1,
                "categories": 1,
                "nb_cats": 1,
                "nb_items": {"$size": "$items"},
            }
        },
        {"$sort": {"nb_cats": 1, "nb_items": 1}},
    ]
    cursor = db.documents.aggregate(pipeline)
    rows = pd.DataFrame(list(cursor))
    if len(rows):
        to_delete = rows[(rows["nb_cats"] == rows["nb_items"])]
        to_remove = list(to_delete["_id"])
        result = db.documents.delete_many({"_id": {"$in": to_remove}})
        if result.acknowledged:
            logger.info(f"{result.deleted_count} docs deleted")
    del rows
    cursor.close()


@pytest.mark.skip(reason="Not a test")
def test_downsampling_pandemic(get_mongo):  # noqa
    dbname = "afp_iptc_health"
    pandemic_topics = [
        "07000000_20000446_20000448_20000451",
        "07000000_20000446_20000448_20000449_20001218",
        "07000000_20000446_20000448_20000449",
        "07000000_20000446_20000448_20000451",
        "07000000_20000480",
        "07000000_20000464_20000476_20000477",
    ]
    db = get_mongo[dbname]
    pipeline = [
        {
            "$match": {
                "categories.labelName": {
                    "$in": ["07000000_20000446_20000448_20000449_20001218"]
                }
            }
        },
        {
            "$project": {
                "identifier": 1,
                "items": {
                    "$filter": {
                        "input": "$categories.labelName",
                        "as": "item",
                        "cond": {"$in": ["$$item", pandemic_topics]},
                    }
                },
                "cats": "$categories.labelName",
                "nb_cats": {"$size": "$categories"},
            }
        },
        {
            "$project": {
                "identifier": 1,
                "items": 1,
                "cats": 1,
                "nb_cats": 1,
                "nb_items": {"$size": "$items"},
            }
        },
        {"$sort": {"nb_cats": 1, "nb_items": 1}},
    ]
    cursor = db.documents.aggregate(pipeline)
    rows = pd.DataFrame(list(cursor))
    if len(rows):
        to_delete = rows[(rows["nb_cats"] == rows["nb_items"])]
        to_remove = list(to_delete["identifier"])
        result = db.documents.delete_many({"identifier": {"$in": to_remove}})
        if result.acknowledged:
            logger.info(f"{result.deleted_count} docs deleted")
        result = db.altTexts.delete_many({"documentIdentifier": {"$in": to_remove}})
        if result.acknowledged:
            logger.info(f"{result.deleted_count} alts deleted")
    del rows
    cursor.close()


@pytest.mark.skip(reason="Not a test")
def test_compute_fingerprint(get_mongo):  # noqa
    ef_client = EntityFishingClient()
    fingerprints = "P31,P279,P361,P106,P452,P1566"
    # fingerprints = "P31,P279,P361,P106,P1566"
    dbname = "afp_iptc_politics"
    db = get_mongo[dbname]
    nb_docs = db.documents.count_documents({"metadata.language": "ar"})

    def compute_fingerprint(row):
        lang = row.lang
        year = row.year
        docid = row.identifier
        yeardir = Path(
            f"/media/olivier/DATA/corpora/AFP/POC/POC_KAIRNTECH_CORPUS_{lang.upper()}_PARSED/{lang}/{year}"
        )
        if yeardir.exists() and lang in ["en", "fr", "de", "ar", "es", "pt"]:
            fingerprint = ef_client.compute_fingerprint(docid, yeardir, fingerprints)
            return fingerprint
        else:
            logger.error(f"Year dir {str(yeardir)} does not exist")
        return pd.NA

    start_at = 0
    for skip in tqdm(range(start_at, nb_docs, 100)):
        pipeline = [
            {
                "$match": {
                    "metadata.language": {"$in": ["en", "fr", "de", "ar", "es", "pt"]}
                }
            },
            {
                "$project": {
                    "identifier": 1,
                    "lang": "$metadata.language",
                    "year": {"$substr": ["$metadata.versionCreated", 0, 4]},
                }
            },
            {"$sort": {"_id": 1}},
            {"$skip": skip},
            {"$limit": 100},
        ]
        cursor = db.documents.aggregate(pipeline)
        rows = pd.DataFrame(list(cursor))
        rows["fingerprint"] = rows.apply(lambda x: compute_fingerprint(x), axis=1)
        updates = []
        for i, doc in rows.iterrows():
            if not pd.isna(doc.fingerprint):
                updates.append(
                    UpdateOne(
                        {"_id": doc._id},
                        {"$set": {"metadata.fingerprint": doc.fingerprint}},
                    )
                )
        if updates:
            db.documents.bulk_write(updates, ordered=False)
            # result = db.documents.bulk_write(updates, ordered=False)
            # logger.info("%d documents modified" % (result.modified_count + result.upserted_count,))
        del rows
        cursor.close()
        print(skip)


def chunks(seq, size=1000):  # noqa
    return (seq[pos: pos + size] for pos in range(0, len(seq), size))


def count_documents_per_cats(db):  # noqa
    nb_docs = 0
    counts = defaultdict(int)
    for doc in db.documents.find():
        if doc["categories"]:
            nb_docs += 1
            for cat in doc["categories"]:
                label = cat["labelName"]
                counts[label] += 1
    return nb_docs, Counter(counts)


def get_labels(db):  # noqa
    from bidict import bidict
    labels = {}
    for doc in db.labels.find():
        labels[doc["name"]] = doc["label"]
    return bidict(labels)


def delete_documents_for_cat(db, label, limit):  # noqa
    aggreg = [
        {"$match": {"categories.labelName": label}},
        {"$project": {"nb_cats": {"$size": "$categories"}}},
        {"$sort": {"nb_cats": 1}},
        {"$match": {"nb_cats": 1}},
        {"$limit": limit},
    ]
    results = list(db.documents.aggregate(aggreg))
    if results:
        to_remove = [d["_id"] for d in results]
        result = db.documents.delete_many({"_id": {"$in": to_remove}})
        if result.acknowledged:
            logger.info(f"{result.deleted_count} docs deleted for category {label}")


def delete_topcat_if_leave(db, label):  # noqa
    aggreg = [
        {"$match": {"categories.labelName": re.compile(r"^" + label + "_")}},
        {"$match": {"categories.labelName": label}},
        {"$project": {"_id": 1, "categories": 1, "nb_cats": {"$size": "$categories"}}},
        {"$sort": {"nb_cats": 1}},
    ]
    results = list(db.documents.aggregate(aggreg))
    if results:
        updates = []
        for doc in results:
            categories = [cat for cat in doc["categories"] if cat["labelName"] != label]
            updates.append(
                UpdateOne({"_id": doc["_id"]}, {"$set": {"categories": categories}})
            )
        if updates:
            result = db.documents.bulk_write(updates, ordered=False)
            logger.info(
                "%d documents modified"
                % (result.modified_count + result.upserted_count,)
            )
