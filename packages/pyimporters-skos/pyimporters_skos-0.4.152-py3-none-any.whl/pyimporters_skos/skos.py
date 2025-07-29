from collections import defaultdict
from enum import Enum
from pathlib import Path
from typing import Type, Dict, Any, Generator, Union, List

from fastapi import Query
from progress.bar import Bar
from pydantic import BaseModel
from pydantic.dataclasses import dataclass
from pyimporters_plugins.base import KnowledgeParserBase, KnowledgeParserOptions, Term, maybe_archive
from rdflib import Graph, RDF, SKOS, URIRef
from rdflib.resource import Resource


class RDFFormat(str, Enum):
    xml = 'xml'
    n3 = 'n3'
    turtle = 'turtle'
    nt = 'nt'
    json_ld = 'json-ld'


@dataclass
class SKOSOptions(KnowledgeParserOptions):
    """
    Options for the RDF knowledge import
    """
    rdf_format: RDFFormat = Query(RDFFormat.xml, description="RDF format")
    concept_class: str = Query("http://www.w3.org/2004/02/skos/core#Concept", description="")


SKOSOptionsModel = SKOSOptions.__pydantic_model__


class SKOSKnowledgeParser(KnowledgeParserBase):
    def parse(self, source: Path, options: Union[KnowledgeParserOptions, Dict[str, Any]], bar: Bar) \
            -> Generator[Term, None, None]:
        options = SKOSOptions(**options) if isinstance(options, dict) else options
        bar.max = 100
        bar.start()
        g = Graph()
        mode = "rb" if options.rdf_format in [RDFFormat.nt, RDFFormat.json_ld] else "r"
        with maybe_archive(source, mode=mode) as file:
            bar.next(10)
            thes = g.parse(file=file, format=options.rdf_format)
            bar.next(10)
            concept_class = URIRef(options.concept_class)
            bar.max = len(list(thes.subjects(predicate=RDF.type, object=concept_class)))
            for curi in thes[:RDF.type:concept_class]:
                bar.next()
                c = Resource(g, curi)
                concept: Term = None
                for prefLabel in c.objects(SKOS.prefLabel):
                    if prefLabel.language is None or options.lang == 'xx' or prefLabel.language.startswith(
                            options.lang):
                        concept: Term = Term(identifier=str(curi), preferredForm=prefLabel.value)
                if concept:
                    props = defaultdict(list)
                    for altLabel in c.objects(SKOS.altLabel):
                        if altLabel.language is None or options.lang == 'xx' or altLabel.language.startswith(
                                options.lang):
                            props['altForms'].append(altLabel.value)
                    if props:
                        concept.properties = props
                    yield concept

    @classmethod
    def get_schema(cls) -> KnowledgeParserOptions:
        return SKOSOptions

    @classmethod
    def get_model(cls) -> Type[BaseModel]:
        return SKOSOptionsModel

    @classmethod
    def get_extensions(cls) -> List[str]:
        return ["xml", "zip", "rdf", "skos", "jsonld", "ttl", "nt", "n3"]