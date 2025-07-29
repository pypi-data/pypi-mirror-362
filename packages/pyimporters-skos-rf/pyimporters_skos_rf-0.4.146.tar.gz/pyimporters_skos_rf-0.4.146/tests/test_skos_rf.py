from pathlib import Path

from progress.bar import Bar
from pyimporters_plugins.base import Term

from pyimporters_skos_rf.skos_rf import SKOSRFKnowledgeParser, SKOSRFOptionsModel, RDFFormat


def test_xml():
    testdir = Path(__file__).parent
    source = Path(testdir, 'data/LL-RF-Terminologie-Paye_20210501.zip')
    parser = SKOSRFKnowledgeParser()
    options = SKOSRFOptionsModel(lang="fr", rdf_format=RDFFormat.xml)
    concepts = list(parser.parse(source, options.dict(), Bar('Processing')))
    assert len(concepts) == 1420
    ids = {c.identifier for c in concepts}
    # Check uniqueness of ids
    assert len(ids) == len(concepts)
    homme_id = 'https://revuefiduciaire.grouperf.com/referentiel/concept/thesaurus-paye#personne-physique-homme'
    homme = next(c for c in concepts if
                 c.identifier == homme_id)
    assert homme.identifier == homme_id
    assert homme.preferredForm == 'Homme'
    assert len(homme.properties['altForms']) == 1
    assert homme.properties['altForms'] == ['hommes']
    for c in concepts:
        assert "concept/" in c.identifier


def test_xml_all():
    testdir = Path(__file__).parent
    source = Path(testdir, 'data/LL-RF-Terminologie-Paye_20210501.zip')
    parser = SKOSRFKnowledgeParser()
    options = SKOSRFOptionsModel(lang="fr", rdf_format=RDFFormat.xml, TerminoConcept_only=False)
    concepts = list(parser.parse(source, options.dict(), Bar('Processing')))
    assert len(concepts) == 2330
    ids = {c.identifier for c in concepts}
    # Check uniqueness of ids
    assert len(ids) == len(concepts)
    homme_id = 'https://revuefiduciaire.grouperf.com/referentiel/concept/thesaurus-paye#personne-physique-homme'
    homme = next(c for c in concepts if
                 c.identifier == homme_id)
    assert homme.identifier == homme_id
    assert homme.preferredForm == 'Homme'
    assert len(homme.properties['altForms']) == 1
    assert homme.properties['altForms'] == ['hommes']


def test_standard_skosxml():
    testdir = Path(__file__).parent
    source = Path(testdir, 'data/lexicon.skos.rdf.zip')
    parser = SKOSRFKnowledgeParser()
    options = SKOSRFOptionsModel(lang="fr", rdf_format=RDFFormat.xml)
    concepts = list(parser.parse(source, options.dict(), Bar('Processing')))
    assert len(concepts) == 1
    c0: Term = concepts[0]
    assert c0.identifier == 'http://skos.um.es/unescothes/C02796'
    assert c0.preferredForm == 'Métier'
    assert len(c0.properties['altForms']) == 5
    assert set(c0.properties['altForms']) == {'Carrière', 'Occupation professionnelle', 'Profession',
                                              'Activité professionnelle', 'Poste'}
