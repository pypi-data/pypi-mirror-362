from collections import defaultdict
from pathlib import Path
from typing import Type, Dict, Any, Generator, Union, List

from collections_extended import setlist
from fastapi import Query
from lxml import etree
from progress.bar import Bar
from pydantic import BaseModel
from pydantic.dataclasses import dataclass
from pyimporters_plugins.base import KnowledgeParserBase, KnowledgeParserOptions, Term, maybe_archive


@dataclass
class MeSHOptions(KnowledgeParserOptions):
    """
    Options for the MeSH knowledge import
    """
    branches: str = Query(None,
                          description="""Comma-separated list of branches to import,
                                         for example 'B,C' to import only descriptors
                                         belonging to the Organisms & Diseases categories""")


MeSHOptionsModel = MeSHOptions.__pydantic_model__

# The top-level categories in the MeSH descriptor hierarchy are:
MESH_CATEGORIES = {
    "A": "Anatomy",
    "B": "Organisms",
    "C": "Diseases",
    "D": "Chemicals and Drugs",
    "E": "Analytical, Diagnostic and Therapeutic Techniques and Equipment",
    "F": "Psychiatry and Psychology",
    "G": "Biological Sciences",
    "H": "Physical Sciences",
    "I": "Anthropology, Education, Sociology and Social Phenomena",
    "J": "Technology and Food and Beverages",
    "K": "Humanities",
    "L": "Information Science",
    "M": "Persons",
    "N": "Health Care",
    "V": "Publication Characteristics",
    "Z": "Geographic Locations",
}


class MeSHKnowledgeParser(KnowledgeParserBase):
    def parse(self, source: Path, options: Union[KnowledgeParserOptions, Dict[str, Any]], bar: Bar) \
            -> Generator[Term, None, None]:
        options = MeSHOptions(**options) if isinstance(options, dict) else options
        allowed_branches = [b.strip() for b in options.branches.split(",") if
                            b.strip() in MESH_CATEGORIES] if options.branches else list(MESH_CATEGORIES.keys())
        with maybe_archive(source) as file:
            mesh = etree.parse(file)
            bar.max = int(mesh.xpath("count(//DescriptorRecord)"))
        bar.start()

        with maybe_archive(source, mode='rb') as file:
            mesh = etree.iterparse(file, events=("end",), tag=['DescriptorRecord'])
            for event, record in mesh:
                bar.next()
                dui = record.findtext("DescriptorUI")
                norm = record.findtext("./DescriptorName/String")
                labels = setlist()
                props = defaultdict(list)
                labels.add(norm)
                for concept in record.iterfind("./ConceptList/Concept"):
                    for term in concept.iterfind("./TermList/Term"):
                        tname = term.findtext("String")
                        labels.add(tname)
                labels.remove(norm)
                cats = setlist()
                branches = setlist()
                for tnumber in record.iterfind("./TreeNumberList/TreeNumber"):
                    number = tnumber.text
                    props['TreeNumber'].append(number)
                    branches.add(number[0])
                    cats.add(MESH_CATEGORIES[number[0]])
                props['Category'] = list(cats)
                props['Branch'] = list(branches)
                props['altForms'] = list(labels)

                record.clear()
                if intersection(allowed_branches, props['Branch']):
                    term: Term = Term(identifier=dui, preferredForm=norm, properties=props)
                    yield term

    @classmethod
    def get_schema(cls) -> KnowledgeParserOptions:
        return MeSHOptions

    @classmethod
    def get_model(cls) -> Type[BaseModel]:
        return MeSHOptionsModel

    @classmethod
    def get_extensions(cls) -> List[str]:
        return ["xml", "zip"]


# Python program to illustrate the intersection
# of two lists using set() method
def intersection(lst1, lst2):
    return list(set(lst1) & set(lst2))
