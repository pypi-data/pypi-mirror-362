import re
from pathlib import Path
from typing import Type, Dict, Any, Generator, Union, List

import obonet
from collections_extended import setlist
from fastapi import Query
from progress.bar import Bar
from pydantic import BaseModel
from pydantic.dataclasses import dataclass
from pyimporters_plugins.base import KnowledgeParserBase, KnowledgeParserOptions, Term, maybe_archive


@dataclass
class OBOOptions(KnowledgeParserOptions):
    """
    Options for the OBO knowledge import
    """
    synonym_scopes: str = Query(None,
                                description="""Comma-separated list of synonym scopes to consider among
                                         [EXACT, BROAD, NARROW, RELATED], default is all""")
    namespaces: str = Query(None,
                            description="""Comma-separated list of namespaces to consider, default is all""")


SYN_SCOPES = ['EXACT', 'BROAD', 'NARROW', 'RELATED']

OBOOptionsModel = OBOOptions.__pydantic_model__


class OBOKnowledgeParser(KnowledgeParserBase):
    def __init__(self):
        self.syn_re = re.compile('^"([^"]+)" ([A-Z]+) .*$')

    def parse(self, source: Path, options: Union[KnowledgeParserOptions, Dict[str, Any]], bar: Bar) \
            -> Generator[Term, None, None]:
        options = OBOOptions(**options) if isinstance(options, dict) else options
        allowed_scopes = [s.strip() for s in options.synonym_scopes.split(",") if
                          s.strip() in SYN_SCOPES] if options.synonym_scopes else SYN_SCOPES
        allowed_namespaces = [s.strip() for s in options.namespaces.split(",")] if options.namespaces else None

        with maybe_archive(source) as file:
            g = obonet.read_obo(file)
            bar.max = len(g)
            bar.start()
            for id_, data in g.nodes(data=True):
                bar.next()
                if 'name' in data:
                    norm = data['name']
                    props = {}
                    if 'namespace' in data:
                        props['namespace'] = data['namespace']
                    if allowed_namespaces is None or props.get('namespace', None) in allowed_namespaces:
                        term: Term = Term(identifier=id_, preferredForm=norm)
                        labels = setlist()
                        if 'synonym' in data:
                            for syn in data['synonym']:
                                m = self.syn_re.match(syn)
                                syn = m.group(1)
                                scope = m.group(2)
                                if scope in allowed_scopes:
                                    labels.add(syn)
                            props['altForms'] = list(labels)
                        if 'xref' in data:
                            wikidatas = [xref[len('Wikidata:'):] for xref in data['xref'] if
                                         xref.startswith('Wikidata:')]
                            if wikidatas:
                                props['wikidataId'] = wikidatas[0]
                        if props:
                            term.properties = props
                        yield term

    @classmethod
    def get_schema(cls) -> KnowledgeParserOptions:
        return OBOOptions

    @classmethod
    def get_model(cls) -> Type[BaseModel]:
        return OBOOptionsModel

    @classmethod
    def get_extensions(cls) -> List[str]:
        return ["obo", "zip"]
