import io
from collections import defaultdict, namedtuple
from enum import Enum
from functools import lru_cache
from itertools import groupby
from pathlib import Path
from typing import Type
import pandas as pd
import spacy
from collections_extended import RangeMap
from pydantic import Field, BaseModel
from pymultirole_plugins.v1.formatter import FormatterBase, FormatterParameters
from pymultirole_plugins.v1.schema import Document, Annotation, Category
from spacy.training.iob_utils import biluo_tags_from_offsets
from starlette.responses import Response


class OutputFormat(str, Enum):
    xlsx = "xlsx"


class CompareWith(str, Enum):
    METADATA = "METADATA"
    CREATOR = "CREATOR"


class AFPQualityParameters(FormatterParameters):
    format: OutputFormat = Field(OutputFormat.xlsx, description="Output format")
    compare: CompareWith = Field(
        CompareWith.METADATA,
        description="Compare with metadata (no position) or annotations created by different systems",
    )
    text: bool = Field(True, description="Add text of document as separate sheet")


class AFPQualityFormatter(FormatterBase):
    """AFPQuality formatter."""

    def format(self, document: Document, parameters: FormatterParameters) -> Response:
        """Parse the input document and return a formatted response.

        :param document: An annotated document.
        :param options: options of the parser.
        :returns: Response.
        """
        parameters: AFPQualityParameters = parameters
        try:
            dfs = {}

            if parameters.compare == CompareWith.METADATA:
                columns = ["Code", "Name", "True", "Pred"]
                # categories
                cats_true, cats_pred = parse_categories(document)
                dfs["medtop"] = classification_report(cats_true, cats_pred)

                # annotations
                ann_groups = group_annotations_withterms(document, by_label)
                for subject in ["afpperson", "afplocation", "afporganization"]:
                    anns_true = [
                        tuple(subj.split(":", maxsplit=1))
                        for subj in document.metadata.get(subject, [])
                    ]
                    anns_pred = ann_groups.get(subject, [])
                    dfs[subject] = classification_report(anns_true, anns_pred)
            else:
                nlp = get_nlp(document.metadata.get("lang", "en"))
                # Tokenize with spacy
                doc = nlp(document.text)
                # annotations
                ann_groups = group_annotations(document, by_creator)
                columns = ["Tokens"].extend(ann_groups.keys())
                tags = {"Tokens": [t.text for t in doc]}
                for group, anns in ann_groups.items():
                    entities = [(a.start, a.end, a.labelName) for a in anns]
                    tags[group] = biluo_tags_from_offsets(doc, entities)
                dfs["biluo"] = pd.DataFrame.from_dict(tags)

            resp: Response = None
            filename = f"file.{parameters.format.value}"
            if document.properties and "fileName" in document.properties:
                filepath = Path(document.properties["fileName"])
                filename = f"{filepath.stem}.{parameters.format.value}"
            if parameters.format == OutputFormat.xlsx:
                bio = io.BytesIO()
                writer = pd.ExcelWriter(bio, engine="openpyxl")
                if parameters.text:
                    text_df = pd.DataFrame.from_records(
                        [(document.identifier, document.text)], columns=["Id", "Text"]
                    )
                    text_df.to_excel(
                        writer, index=False, sheet_name="text", columns=["Id", "Text"]
                    )
                for subject, df in dfs.items():
                    df.to_excel(
                        writer,
                        index=False,
                        sheet_name=subject,
                        columns=columns,
                    )

                writer.save()
                writer.close()
                resp = Response(
                    content=bio.getvalue(),
                    media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                )
                resp.headers["Content-Disposition"] = f"attachment; filename={filename}"
            return resp
        except BaseException as err:
            raise err

    @classmethod
    def get_model(cls) -> Type[BaseModel]:
        return AFPQualityParameters


def classification_report(y_true, y_pred):
    y_true = pd.DataFrame.from_records(list(y_true), columns=["Code", "Name"])
    y_pred = pd.DataFrame.from_records(list(y_pred), columns=["Code", "Name"])
    y_all = pd.concat([y_pred, y_true]).drop_duplicates(subset=["Code"])

    def compute_truth(code, codes):
        return 1 if code in list(codes) else 0

    y_all["True"] = y_all["Code"].map(lambda x: compute_truth(x, y_true["Code"]))
    y_all["Pred"] = y_all["Code"].map(lambda x: compute_truth(x, y_pred["Code"]))
    return y_all.sort_values("Code")


def parse_categories(doc: Document):
    topics = get_mediatopics()
    medtops_true = [
        medtop.split(":", maxsplit=1)[0] for medtop in doc.metadata.get("medtop", [])
    ]
    cats_true = set()
    for t in medtops_true:
        levels = topics[t].levels
        if len(levels) == 1 or levels[0]:
            cats_true.add((t, topics[t].label))
    medtops_pred = set()
    if doc.categories:
        for cat in doc.categories:
            medtops_pred.update(cat.labelName.split("_"))
    cats_pred = [(t, topics[t].label) for t in medtops_pred]
    return cats_true, cats_pred


def group_annotations_withterms(doc: Document, keyfunc):
    groups = defaultdict(list)
    if doc.annotations:
        for k, g in groupby(sorted(doc.annotations, key=keyfunc), keyfunc):
            afpterms = set()
            for a in g:
                if a.terms:
                    afpterms.update(
                        [
                            (t.identifier[len(k) + 1:], t.preferredForm)
                            for t in a.terms
                            if t.identifier.startswith(k)
                        ]
                    )
            groups[k] = list(afpterms)
    return groups


def group_annotations(doc: Document, keyfunc):
    def get_sort_key(a: Annotation):
        return a.end - a.start, -a.start

    groups = defaultdict(list)
    for k, g in groupby(sorted(doc.annotations, key=keyfunc), keyfunc):
        sorted_group = sorted(g, key=get_sort_key, reverse=True)
        dedup = []
        seen_offsets = RangeMap()
        for ann in sorted_group:
            # Check for end - 1 here because boundaries are inclusive
            if seen_offsets.get(ann.start) is None and seen_offsets.get(ann.end - 1) is None:
                dedup.append(ann)
                seen_offsets[ann.start:ann.end] = ann
        groups[k] = dedup

    return groups


def by_label(a: Annotation):
    return a.labelName


def by_creator(a: Annotation):
    return a.createdBy or "True"


def by_len_and_alpha_str(k: str):
    return len(k), k


def by_len_and_alpha_cat(c: Category):
    return len(c.labelName), c.labelName


Mediatopic = namedtuple("Mediatopic", ["label", "levels"])


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
        for k in range(lev + 1, 6):
            levels[k] = None
        topics[topic_code] = Mediatopic(
            label=row["Name (en-GB)"], levels=levels[0: lev + 1].copy()
        )
    return topics


@lru_cache(maxsize=None)
def get_nlp(lang: str, ttl_hash=None):
    del ttl_hash
    nlp = spacy.blank(lang)
    return nlp
