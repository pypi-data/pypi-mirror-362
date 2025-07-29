from collections import defaultdict
from enum import Enum
from pathlib import Path
from typing import Type, Dict, Any, Generator, Union, List

from fastapi import Query
from progress.bar import Bar
from pydantic import BaseModel
from pydantic.dataclasses import dataclass
from pyimporters_plugins.base import KnowledgeParserBase, Term, KnowledgeParserOptions, maybe_archive
from rdflib import Graph, RDF, SKOS, URIRef
from rdflib.resource import Resource


class RDFFormat(str, Enum):
    xml = 'xml'
    n3 = 'n3'
    turtle = 'turtle'
    nt = 'nt'
    json_ld = 'json-ld'


@dataclass
class SKOSRFOptions(KnowledgeParserOptions):
    """
    Options for the RDF knowledge import
    """
    rdf_format: RDFFormat = Query(RDFFormat.xml, description="RDF format")
    TerminoConcept_only: bool = Query(True, description="Only import terms that are related to a TerminoConcept")


SKOSRFOptionsModel = SKOSRFOptions.__pydantic_model__


class SKOSRFKnowledgeParser(KnowledgeParserBase):
    def parse(self, source: Path, options: Union[KnowledgeParserOptions, Dict[str, Any]], bar: Bar) \
            -> Generator[Term, None, None]:
        options = SKOSRFOptions(**options) if isinstance(options, dict) else options
        bar.max = 20
        bar.start()
        g = Graph()
        with maybe_archive(source) as file:
            thes = g.parse(file=file, format=options.rdf_format)
            namespaces = dict(thes.namespaces())
            SRM_NS = namespaces.get('srm', None)
            bar.next(20)
            bar.max = len(list(thes.subjects(predicate=RDF.type, object=SKOS.Concept)))
            # To deduplicate concepts (same identifier)
            concepts = defaultdict(list)
            for curi in thes[:RDF.type:SKOS.Concept]:
                bar.next()
                c = Resource(g, curi)
                # status = uri2value(c, "status", SRM_NS)
                # workStatus = uri2value(c, "workStatus", SRM_NS)
                terminoConcepts = list(c.objects(URIRef("TerminoConcept", base=SRM_NS)))

                if SRM_NS is None or terminoConcepts or not options.TerminoConcept_only:
                    identifier = str(terminoConcepts[0].identifier) if terminoConcepts else str(curi)
                    variants = list(
                        c.objects(URIRef("syntacticVariantAllowed", base=SRM_NS)))
                    variants.extend(
                        c.objects(URIRef("abbreviationAllowed", base=SRM_NS)))
                    variants.extend(
                        c.objects(URIRef("acronymAllowed", base=SRM_NS)))

                    concept: Term = None
                    for prefLabel in c.objects(SKOS.prefLabel):
                        if prefLabel.language.startswith(options.lang):
                            concept: Term = Term(identifier=identifier, preferredForm=prefLabel.value)
                    for altLabel in c.objects(SKOS.altLabel):
                        if altLabel.language.startswith(options.lang):
                            variants.append(altLabel)
                    if concept:
                        if variants or terminoConcepts:
                            concept.properties = {}
                            if variants:
                                concept.properties['altForms'] = [v.value for v in variants]
                        concepts[identifier].append(concept)
            for identifier, duplicates in concepts.items():
                if len(duplicates) > 1:
                    altforms = set()
                    duplicate: Term = None
                    for i, duplicate in enumerate(duplicates):
                        if i > 0 and duplicate.preferredForm is not None:
                            altforms.add(duplicate.preferredForm)
                        if duplicate.properties and 'altForms' in duplicate.properties:
                            altforms.update(duplicate.properties['altForms'])
                    if duplicates[0].properties is None:
                        duplicates[0].properties = {}
                    if altforms:
                        duplicates[0].properties['altForms'] = list(altforms)
                yield duplicates[0]

    @classmethod
    def get_schema(cls) -> KnowledgeParserOptions:
        return SKOSRFOptions

    @classmethod
    def get_model(cls) -> Type[BaseModel]:
        return SKOSRFOptionsModel

    @classmethod
    def get_extensions(cls) -> List[str]:
        return ["xml", "zip", "rdf", "jsonld", "ttl", "nt", "n3"]


def uri2value(concept, uri, base=None):
    val = None
    vals = list(concept.objects(URIRef(uri, base=base)))
    if vals:
        qname = vals[0].qname()
        toks = qname.split(":")
        if len(toks) == 2:
            val = toks[1]
    return val
