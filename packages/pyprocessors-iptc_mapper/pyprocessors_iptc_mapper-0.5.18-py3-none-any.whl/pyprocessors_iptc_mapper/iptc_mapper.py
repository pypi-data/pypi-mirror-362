from collections import namedtuple
from functools import lru_cache
from itertools import groupby
from pathlib import Path
from typing import Type, cast, List, Dict

import pandas as pd
from log_with_context import add_logging_context, Logger
from pydantic import BaseModel, Field
from pymultirole_plugins.v1.processor import ProcessorParameters, ProcessorBase
from pymultirole_plugins.v1.schema import Document, Category

logger = Logger("pymultirole")


class IPTCMapperParameters(ProcessorParameters):
    label2iptc_mapping: Dict[str, str] = Field(None, description="Label to iptc mediatopic mapping",
                                               extra="key:label")
    filter_root_only_categories: bool = Field(True, description="Filter root IPTC categories if no leaf is assigned")


def is_iptc_category(cat: Category):
    ok = "0123456789_"
    return all(c in ok for c in cat.labelName)


def remove_root_only(iptc_categories):
    iptc_root_names = set(c[0:c.index('_')] for c in iptc_categories.keys() if '_' in c)
    categories = [v for k, v in iptc_categories.items() if k[0:len('00000000')] in iptc_root_names]
    return categories


class IPTCMapper(ProcessorBase):
    """Create categories from annotations"""

    def process(
            self, documents: List[Document], parameters: ProcessorParameters
    ) -> List[Document]:  # noqa: C901
        params: IPTCMapperParameters = cast(IPTCMapperParameters, parameters)
        topics = get_mediatopics()
        mapping = {k: topics.get(v, None) for k, v in params.label2iptc_mapping.items()} if (params.label2iptc_mapping and len(
            params.label2iptc_mapping) > 0) else {}
        for document in documents:
            with add_logging_context(docid=document.identifier):
                iptc_categories = {}
                mapped_categories = {}
                sorted_categories = sorted(document.categories or [], key=lambda c: c.labelName, reverse=True)
                for is_iptc, group in groupby(sorted_categories, is_iptc_category):
                    if is_iptc:
                        iptc_categories.update({c.labelName: c for c in group})
                    else:
                        for c in group:
                            if c.labelName in mapping:
                                mediatopic = mapping[c.labelName]
                                clabel = f"{mediatopic.path.replace('_', '/')} ({mediatopic.label})"
                                mapped_categories[mediatopic.path] = Category(labelName=mediatopic.path, label=clabel, score=c.score)
                categories = remove_root_only(iptc_categories) if params.filter_root_only_categories else list(iptc_categories.values())
                for k, mapped_category in mapped_categories.items():
                    if k not in iptc_categories:
                        categories.append(mapped_category)
                document.categories = categories
        return documents

    @classmethod
    def get_model(cls) -> Type[BaseModel]:
        return IPTCMapperParameters


Mediatopic = namedtuple("Mediatopic", ["label", "code", "path"])


@lru_cache(maxsize=None)
def get_mediatopics():
    iptc = Path(__file__).parent / "IPTC-MediaTopic-NewsCodes.xlsx"
    topics = {}
    iptc_codes = pd.read_excel(iptc, header=1).fillna(value="")
    levels = [None] * 6
    for index, row in iptc_codes.iterrows():
        topic_url = row["NewsCode-QCode (flat)"]
        topic_code = topic_url[len("medtop:"):]
        for lev in range(0, 6):
            level = f"Level{lev + 1}/NewsCode"
            level_url = row[level]
            if level_url:
                level_code = level_url[len("medtop:"):]
                levels[lev] = level_code
                break
        path = "_".join(levels[0: lev + 1])
        topics[topic_code] = Mediatopic(
            label=row["Name (en-GB)"], code=topic_code, path=path
        )
    return topics
