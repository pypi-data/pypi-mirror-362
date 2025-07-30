from collections import defaultdict
from itertools import groupby
from typing import Type, List, cast

from collections_extended import RangeMap
from pydantic import BaseModel, Field
from pymultirole_plugins.v1.processor import ProcessorParameters, ProcessorBase
from pymultirole_plugins.v1.schema import Document, Annotation, Category


class SegmentRenseignorParameters(ProcessorParameters):
    topic_as_category: bool = Field(
        True,
        description="Create categories out of topics",
        extra="advanced"
    )


def left_longest_match(a):
    return a.end - a.start, -a.start


class SegmentRenseignorProcessor(ProcessorBase):
    """Create segments from annotations ."""

    def process(
            self, documents: List[Document], parameters: ProcessorParameters
    ) -> List[Document]:
        params: SegmentRenseignorParameters = cast(SegmentRenseignorParameters, parameters)
        articles = []
        for document in documents:
            if document.annotations:
                englobs = defaultdict(list)
                seen = RangeMap()
                annotations = [a for a in document.annotations if a.status != "KO" and a.labelName != "sentence"]
                # Sort annotations by longest match to find embedded sub annotations
                sorted_annotations = sorted(annotations, key=left_longest_match, reverse=True)
                # attach sub annotations to their parent annotation as properties
                for a in sorted_annotations:
                    if a.start in seen and a.end - 1 in seen:
                        englob = seen.get(a.start)
                        englobs[(englob.start, englob.end)].append(a)
                    else:
                        seen[a.start:a.end] = a
                annotations2 = []
                for a in seen.values():
                    alist = englobs.get((a.start, a.end), None)
                    if alist is not None:
                        props = a.properties or {}
                        for suba in alist:
                            props[suba.labelName] = suba.text
                        a.properties = props
                    annotations2.append(a)

                sorted_annotations = sorted([
                    a
                    for a in annotations2
                ], key=lambda a: a.start)
                # Try to find the unique header containing renseignor number and date
                headers = [
                    a
                    for a in sorted_annotations
                    if a.labelName == "header"
                ]
                metadata = {}
                if len(headers) > 0:
                    if headers[0].properties:
                        for k, v in headers[0].properties.items():
                            if k == "date":
                                metadata["PUBLICATION DATE"] = v
                            elif k == "publication_slash_number":
                                metadata["PUBLICATION NUMBER"] = v
                    else:
                        pass
                docid = metadata.get("PUBLICATION NUMBER")
                subdocid = 0

                # Find boundaries of TOC and OURS to cut the useful part of text
                etocs = [
                    a
                    for a in sorted_annotations
                    if a.labelName == "etoc"
                ]
                bours = [
                    a
                    for a in sorted_annotations
                    if a.labelName == "bours"
                ]
                useful = Annotation(labelName="useful", start=etocs[0].end if len(etocs) > 0 else 0,
                                    end=bours[0].start if len(bours) > 0 else len(document.text))
                useful_text = document.text[useful.start:useful.end]

                # Shift useful annotations according to the useful part of text and try to group articles under a topic header
                shifted_annotations = []
                topic_annotations = []
                for a in sorted_annotations:
                    if a.end <= useful.end:
                        a.start -= useful.start
                        a.end -= useful.start
                        if a.start >= 0:
                            if a.labelName in ["footer", 'source']:
                                shifted_annotations.append(a)
                            elif a.labelName == "topic":
                                topic_annotations.append(a)
                sections = RangeMap()
                previous = 0
                topic = None
                for a in topic_annotations:
                    sections[previous:a.start] = (topic, previous, a.start)
                    previous = a.end
                    topic = a.text
                if topic is not None:
                    sections[previous:len(useful_text)] = (topic, previous, len(useful_text))

                def by_topic(a: Annotation):
                    ttuple = sections.get(a.start)
                    if ttuple is not None:
                        return ttuple
                    else:
                        return "toto"

                for k, g in groupby(shifted_annotations, by_topic):
                    if k is not None:
                        topic, tstart, tend = k
                        previous = tstart
                        tanns = list(g)
                        atext = ""
                        for a in tanns:
                            if a.labelName == "footer":
                                atext += useful_text[previous:a.start].strip()
                                previous = a.end
                            elif a.labelName == "source":
                                ametadata = {"TOPIC": topic}
                                acats = None
                                if params.topic_as_category:
                                    acats = [Category(label=topic)]
                                if a.properties is not None:
                                    for k, v in a.properties.items():
                                        if k == "date":
                                            ametadata["ARTICLE DATE"] = v
                                        elif k == "source_slash_name":
                                            ametadata["SOURCE NAME"] = v
                                ametadata.update(metadata)
                                atext += useful_text[previous:a.start].strip()
                                ititle = atext.find("...")
                                title = atext[0:ititle] if ititle > 0 else a.text
                                article = Document(identifier=f"{docid}-{subdocid}", title=title, text=atext,
                                                   categories=acats,
                                                   metadata=ametadata)
                                articles.append(article)
                                subdocid += 1
                                atext = ""
                                previous = a.end
            document.sentences = None
        return articles

    @classmethod
    def get_model(cls) -> Type[BaseModel]:
        return SegmentRenseignorParameters
