import json
from pathlib import Path
from typing import List

from dirty_equals import IsPartialDict, HasLen, Contains, IsList
from pyannotators_acronyms.acronyms import AcronymsAnnotator, AcronymsParameters
from pymultirole_plugins.v1.schema import Document, Sentence


def test_acronyms():
    sents = [
        "Le comité d'établissement (CE) s'est réuni.",
        "Les technologies de l'information et de la communication (TIC) prennent diverses formes : Internet, ordinateur, téléphone portable, modem, progiciels, etc.",
        "Les représentants du MoDem (Mouvement Démocrate) à la région, élus en 2015 sur la liste de M. Wauquiez, avaient annoncé en mars qu'ils quittaient la majorité, sans pour autant rejoindre l'opposition.",
        "Y compris dans la majorité, la vice-présidente du groupe LREM (La République En Marche) Sophie Beaudouin-Hubière a écrit au Premier ministre LREM Jean Castex pour dénoncer une décision d'autant plus injuste que les règles de distanciation ont été bien respectées DANS ces commerces.",
        "Ce CE n'est pas ambigu.",
        "Le Conseil d'Etat (CE) est une autre possibilité pour CE.",
        "La vice-présidente Les Républicains (LR) de l'Assemblée nationale Annie Genevard a aussi pointé le désarroi des petits commerçants, la situation accentuant le risque réel de dépérissement de nos centres-villes.",
        "Aide directe ou préfinancement du CESU ? Cette aide peut prendre la forme, en pratique, d'une aide financière directe versée aux salariés ou de chèques emploi-service universel (CESU).",
        "Exonération ZRR et ZRU : nouveaux formulaires \n\nLes embauches effectuées dans les zones de revitalisation rurale (ZRR) et de redynamisation urbaine (ZRU)",
        "L'employeur doit inviter les syndicats intéressés à négocier le protocole d'accord préélectoral en vue de l'élection d'un comité social et économique (CSE).",
        "Ce CE là est ambigu.",
        "Le Comité d'hygiène, de sécurité et des conditions de travail (CHSCT) se réunira demain"
    ]
    text = ""
    sentences = []
    for sent in sents:
        sstart = len(text)
        text += sent + "\n\n"
        send = len(text)
        sentences.append(Sentence(start=sstart, end=send))
    doc = Document(text=text, sentences=sentences, metadata={'language': 'fr'})
    annotator = AcronymsAnnotator()
    parameters = AcronymsParameters()
    docs: List[Document] = annotator.annotate([doc], parameters)
    doc0 = docs[0]
    acros = ["CE", "TIC", "MoDem", "LREM", "LR", "CESU", "ZRR", "CSE", "CHSCT"]
    expands = [
        "comité d'établissement",
        "technologies de l'information et de la communication",
        "Mouvement Démocrate",
        "La République En Marche",
        "Conseil d'Etat",
        "Les Républicains",
        "chèques emploi-service universel",
        "zones de revitalisation rurale",
        "comité social et économique",
        "Comité d'hygiène, de sécurité et des conditions de travail"
    ]
    assert len(doc0.annotations) == 24
    shorts = [a.text for a in doc0.annotations if a.label == "Acronym"]
    assert shorts == HasLen(len(acros), ...)
    assert shorts == Contains(*acros)
    assert shorts != Contains("ZRU", "DANS")
    longs = [a.text for a in doc0.annotations if a.label == "Expanded"]
    assert longs == HasLen(len(expands), ...)
    assert longs == Contains(*expands)
    ce1 = doc0.annotations[0]
    assert ce1.dict() == IsPartialDict(
        label="Acronym",
        text="CE",
        terms=IsList(IsPartialDict(preferredForm="comité d'établissement"), length=1),
    )
    ce1_1 = doc0.annotations[9]
    assert ce1_1.dict() == IsPartialDict(
        label="Acronym",
        text="CE",
        terms=IsList(IsPartialDict(preferredForm="comité d'établissement"), length=1),
    )
    ce2 = doc0.annotations[10]
    assert ce2.dict() == IsPartialDict(
        label="Acronym",
        text="CE",
        terms=IsList(IsPartialDict(preferredForm="Conseil d'Etat"), length=1),
    )
    ce1_2_1 = doc0.annotations[12]
    assert ce1_2_1.dict() == IsPartialDict(label="Acronym", text="CE", terms=HasLen(2))
    ce1_2_2 = doc0.annotations[21]
    assert ce1_2_2.dict() == IsPartialDict(label="Acronym", text="CE", terms=HasLen(2))

    parameters.short_label = "short"
    parameters.long_label = "long"
    docs: List[Document] = annotator.annotate([doc], parameters)
    doc0 = docs[0]
    labels = list(set([a.labelName for a in doc0.annotations]))
    assert labels == IsList("short", "long", check_order=False)


def test_ifpen():
    testdir = Path(__file__).parent
    source = Path(testdir, "data/ifpen_en-document-2023_en.json")
    with source.open("r") as fin:
        jdoc = json.load(fin)
        doc = Document(**jdoc)
    annotator = AcronymsAnnotator()
    parameters = AcronymsParameters()
    docs: List[Document] = annotator.annotate([doc], parameters)
    doc0 = docs[0]
    assert len(doc0.annotations) > 0
