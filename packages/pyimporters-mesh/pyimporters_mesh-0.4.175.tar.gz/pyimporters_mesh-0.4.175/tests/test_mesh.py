from pathlib import Path

from progress.bar import Bar
from pyimporters_plugins.base import Term

from pyimporters_mesh.mesh import MeSHKnowledgeParser, MeSHOptionsModel


def test_mesh():
    testdir = Path(__file__).parent
    source = Path(testdir, 'data/small.zip')
    parser = MeSHKnowledgeParser()
    options = MeSHOptionsModel()
    concepts = list(parser.parse(source, options.dict(), Bar('Processing')))
    assert len(concepts) == 3
    c0: Term = concepts[0]
    assert c0.identifier == 'D000001'
    assert c0.preferredForm == 'Calcimycin'
    assert len(c0.properties['altForms']) == 5
    assert set(c0.properties['altForms']) == {'A-23187', 'A 23187', 'A23187', 'Antibiotic A23187', 'A23187, Antibiotic'}
    assert len(c0.properties['TreeNumber']) == 1


def test_mesh_branch():
    testdir = Path(__file__).parent
    source = Path(testdir, 'data/small.zip')
    parser = MeSHKnowledgeParser()
    options = MeSHOptionsModel(branches="J")
    concepts = list(parser.parse(source, options.dict(), Bar('Processing')))
    assert len(concepts) == 1
