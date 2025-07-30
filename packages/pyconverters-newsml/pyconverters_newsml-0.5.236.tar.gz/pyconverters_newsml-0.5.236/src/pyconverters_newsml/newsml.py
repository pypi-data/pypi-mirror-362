import xml.etree.ElementTree as ET
from collections import defaultdict, namedtuple
from functools import lru_cache
from pathlib import Path
from typing import List, cast, Type

import pandas as pd
from inscriptis import get_text
from pydantic import BaseModel, Field
from pymultirole_plugins.util import comma_separated_to_list
from pymultirole_plugins.v1.converter import ConverterParameters, ConverterBase
from pymultirole_plugins.v1.schema import Document, Category
from starlette.datastructures import UploadFile


# _home = os.path.expanduser('~')
# xdg_cache_home = os.environ.get('XDG_CACHE_HOME') or os.path.join(_home, '.cache')


class NewsMLParameters(ConverterParameters):
    subjects_as_metadata: str = Field(
        "",
        description="Comma-separated list of subjects (medtop,afpperson,afporganization,afplocation) to retrieve as metadata.",
    )
    subjects_code: bool = Field(
        False, description="If true, use code as subject metadata. If false use name."
    )
    mediatopics_as_categories: bool = Field(
        False, description="whether to add mediatopics mediatopics as categories."
    )
    keywords_as_categories: bool = Field(
        False, description="whether to add slug keywords as categories."
    )
    natures: str = Field(
        "text",
        description="Comma-separated list of natures (text,video,picture,graphic) to retrieve.",
    )


class NewsMLConverter(ConverterBase):
    """NewsML converter ."""

    def convert(
        self, source: UploadFile, parameters: ConverterParameters
    ) -> List[Document]:  # noqa: C901
        params: NewsMLParameters = cast(NewsMLParameters, parameters)

        docs = []
        root = ET.parse(source.file)
        for el in root.iter():
            _, _, el.tag = el.tag.rpartition("}")
        subjects_filter = comma_separated_to_list(params.subjects_as_metadata.strip())
        natures_filter = comma_separated_to_list(params.natures.strip())
        itemSet = root.find("itemSet")
        for newsItem in itemSet.iter("newsItem"):
            metadatas = {}
            text = ""
            itemMeta = newsItem.find("itemMeta")
            lang = newsItem.get("{http://www.w3.org/XML/1998/namespace}lang")
            metadatas["language"] = lang
            ver = newsItem.get("version")
            metadatas["version"] = ver
            guid = newsItem.get("guid")
            metadatas["versionCreated"] = itemMeta.findtext("versionCreated")
            if itemMeta.find("firstCreated"):
                metadatas["firstCreated"] = itemMeta.findtext("firstCreated")
            contentMeta = newsItem.find("contentMeta")
            contentSet = newsItem.find("contentSet")
            genre = get_genre(contentMeta)
            if genre is not None:
                metadatas["genre"] = get_genre(contentMeta)
            title = get_title(contentMeta)
            categories = []
            slug = get_slug(contentMeta)
            if slug:
                metadatas["slug"] = slug
                if params.keywords_as_categories:
                    keywords = get_keywords(contentMeta)
                    categories.extend(
                        [Category(label=kw) for kw in keywords if len(kw.strip()) > 0]
                    )
            if params.subjects_as_metadata.strip() or params.mediatopics_as_categories:
                topics = get_mediatopics()
                subjects = get_subjects(contentMeta, topics)
                for stype, sdict in subjects.items():
                    if subjects_filter[0] == "all" or stype in subjects_filter:
                        metadatas[stype] = (
                            [f"{k}:{v}" for k, v in sdict.items()]
                            if params.subjects_code
                            else list(sdict.values())
                        )
                    cats = defaultdict(list)

                    if params.mediatopics_as_categories and stype == "medtop":
                        for code in sdict:
                            medtop = topics.get(code, None)
                            if medtop and medtop.levels[0] != code:
                                cats[medtop.levels[0]].append(code)
                        categories.extend(
                            [
                                Category(
                                    label=f"{k} ({topics[k].label})", labelName=f"{k}"
                                )
                                for k in cats.keys()
                            ]
                        )
                        for key, tlist in cats.items():
                            hiers = {}
                            for t in tlist:
                                hier = "/".join(topics[t].levels)
                                hiers[hier] = topics[t].label
                            hierkeys = sorted(hiers.keys(), key=len)
                            for hierkey in hierkeys:
                                for h in list(hiers.keys()):
                                    if h != hierkey and hierkey.startswith(h):
                                        del hiers[h]
                            leveln = [
                                Category(
                                    label=f"{k} ({v})", labelName=k.replace("/", "_")
                                )
                                for k, v in hiers.items()
                            ]
                            categories.extend(leveln)
            itemClass = itemMeta.find("itemClass")
            qcode = itemClass.get("qcode")
            if qcode.startswith("ninat:"):
                nature = qcode[len("ninat:") :]
                metadatas["nature"] = nature
                if nature == "text":
                    text = get_textbody(contentSet, title)
                elif nature in ["video", "picture", "graphic"]:
                    text = get_alttext(contentMeta, title)
                else:
                    print(f"Unknown nature: {nature}")
            if nature in natures_filter:
                doc = Document(
                    identifier=guid,
                    text=text,
                    title=title,
                    metadata=metadatas,
                    categories=categories,
                )
                doc.properties = {"fileName": source.filename}
                docs.append(doc)
        return docs

    @classmethod
    def get_model(cls) -> Type[BaseModel]:
        return NewsMLParameters


Mediatopic = namedtuple("Mediatopic", ["label", "levels"])


def get_subjects(contentMeta, topics):
    subjects = defaultdict(dict)
    for subject in contentMeta.iter("subject"):
        qcode = subject.get("qcode")
        if qcode is not None:
            type, code = qcode.split(":")
            if type == "medtop":
                subj = topics.get(code, None)
                if subj is None:
                    print(f"Unknown media topics code: {code}, ignoring")
                else:
                    subjects[type][code] = subj.label
            elif type in ["afpperson", "afplocation", "afporganization"]:
                sname = subject.findtext("name")
                if sname is not None and sname != "-":
                    subjects[type][code] = sname
        else:
            pass
    return subjects


def get_keywords(contentMeta):
    keywords = set()
    for keyword in contentMeta.iter("keyword"):
        if keyword.text:
            keywords.add(keyword.text)
    return list(keywords)


def get_title(contentMeta):
    title = None
    for headline in contentMeta.iter("headline"):
        if not title or not headline.get("role"):
            title = get_text(headline.text or "")
    return title


def get_slug(contentMeta):
    slug = None
    for slugline in contentMeta.iter("slugline"):
        if not slug:
            slug = get_text(slugline.text or "")
    return slug


def get_genre(contentMeta):
    for genre in contentMeta.iter("genre"):
        qcode = genre.get("qcode")
        if qcode is not None:
            type, code = qcode.split(":")
            if type == "afpgenre":
                return code
    return None


def get_textbody(contentSet, title, sep="\n\n"):
    texts = [title] if title else []
    inlineXML = contentSet.find("inlineXML")
    html = inlineXML.find("html")
    if html:
        htmlText = ET.tostring(html, encoding="unicode")
        text = get_text(htmlText)
        if text not in texts:
            texts.append(text)
    return sep.join(texts)


def get_alttext(contentMeta, title, sep="\n\n"):
    texts = [title] if title else []
    for desc in contentMeta.iter("description"):
        text = get_text(desc.text or "")
        if text not in texts:
            texts.append(text)
    return sep.join(texts)


@lru_cache(maxsize=None)
def get_mediatopics():
    iptc = Path(__file__).parent / "IPTC-MediaTopic-NewsCodes.xlsx"
    topics = {}
    iptc_codes = pd.read_excel(iptc, header=1).fillna(value="")
    levels = [None] * 6
    for index, row in iptc_codes.iterrows():
        topic_url = row["NewsCode-QCode (flat)"]
        topic_code = topic_url[len("medtop:") :]

        for lev in range(0, 6):
            level = f"Level{lev + 1}/NewsCode"
            level_url = row[level]
            if level_url:
                level_code = level_url[len("medtop:") :]
                levels[lev] = level_code
                break
        for k in range(lev + 1, 6):
            levels[k] = None
        topics[topic_code] = Mediatopic(
            label=row["Name (en-GB)"], levels=levels[0 : lev + 1].copy()
        )
    return topics
