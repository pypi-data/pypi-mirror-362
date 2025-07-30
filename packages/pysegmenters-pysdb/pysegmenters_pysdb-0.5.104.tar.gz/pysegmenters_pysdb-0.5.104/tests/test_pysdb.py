from typing import List

import pytest
from pymultirole_plugins.v1.schema import Document

from pysegmenters_pysdb.pysdb_segmenter import PySDBSegmenter, PySDBSegmenterParameters


def test_rules_en():
    TEXT = """CLAIRSSON INTERNATIONAL REPORTS LOSS

Clairson International Corp. said it expects to report a net loss for its second quarter ended March 26.
The company doesn’t expect to meet analysts’ profit estimates of $3.9 to $4 million, or 76 cents a share to 79 cents a share, for its year ending Sept. 24, according to Pres. John Doe."""
    model = PySDBSegmenter.get_model()
    model_class = model.construct().__class__
    assert model_class == PySDBSegmenterParameters
    parameters = PySDBSegmenterParameters()
    segmenter = PySDBSegmenter()

    with pytest.raises(AttributeError) as excinfo:
        docs: List[Document] = segmenter.segment([Document(text=TEXT)], parameters)
    assert "None" in str(excinfo.value)

    with pytest.raises(AttributeError) as excinfo:
        docs: List[Document] = segmenter.segment([Document(text=TEXT, metadata={'language':'yy'})], parameters)
    assert "yy" in str(excinfo.value)

    docs: List[Document] = segmenter.segment([Document(text=TEXT, metadata={'language':'en'})], parameters)
    doc0 = docs[0]
    assert len(doc0.sentences) == 4
    sents = [doc0.text[s.start:s.end] for s in doc0.sentences]
    assert sents[0] == "CLAIRSSON INTERNATIONAL REPORTS LOSS"
    assert sents[
               1] == "Clairson International Corp. said it expects to report a net loss for its second quarter ended March 26."
    assert sents[
               2] == "The company doesn’t expect to meet analysts’ profit estimates of $3.9 to $4 million, or 76 cents a share to 79 cents a share, for its year ending Sept. 24, according to Pres."
    assert sents[3] == "John Doe."


def test_rules_hi():
    TEXT = """यूएन महासभा में ईरानी राष्ट्रपति इब्राहिम रईसी का वार और चीन की अहम घोषणा ईरान के नए राष्ट्रपति इब्राहिम रईसी ने संयुक्त राष्ट्र महासभा के पहले संबोधन में अमेरिका को जमकर निशाने पर लिया है.
रईसी ने कहा कि ईरान पर प्रतिबंध को अमेरिका जंग की तरह इस्तेमाल कर रहा है. रईसी ने यूएन में अपने पूर्ववर्ती हसन रूहानी से भी ज़्यादा सख़्त रुख़ अपनाया.
रईसी ने पिछले महीने ही राष्ट्रपति पद की शपथ ली थी. इब्राहिम रईसी ईरान की सुप्रीम कोर्ट के पूर्व चीफ़ जस्टिस हैं और उन्हें रूढ़िवादी माना जाता है.
रईसी ने यूएन महासभा को तेहरान से वर्चुअली संबोधित किया. उन्होंने कहा, ''दुनिया के कई देशों के साथ अमेरिका प्रतिबंध को हथियार के तौर पर इस्तेमाल कर रहा है. कोविड महामारी के वक़्त में इस तरह की आर्थिक सज़ा मानवता के ख़िलाफ़ अपराध है.'' रईसी ने कहा, ''हमारे क्षेत्र अमेरिका न केवल अधिनायकवादी व्यवहार कर रहा है बल्कि पश्चिमी पहचान थोपने में लगा हुआ है. लेकिन उसे इसमें नाकामी ही हाथ लगी है. इराक़ और अफ़ग़ानिस्तान से अमेरिका ख़ुद गया नहीं बल्कि उसे वहाँ से निकाला गया है. अमेरिकी सैनिकों को अफ़ग़ानिस्तान से निकलना पड़ा और इराक़ से भी ऐसा ही करना पड़ रहा है.'' अमेरिका को निशाने पर लेते हुए रईसी ने इसी साल छह जनवरी को अमेरिका के कैपिटल हिल ट्रंप समर्थकों की हिंसा का भी हवाला दिया है. रईसी ने कहा, ''कैपिटल से काबुल तक स्पष्ट संदेश है कि अमेरिकी अधिनायकवादी सिस्टम की कोई साख है. वो चाहे अमेरिका के भीतर हो या बाहर.'' ईरान के राष्ट्रपति ने कहा, ''पश्चिमी तौर-तरीक़ों को थोपने की कोशिश नाकाम हो गई है. इराक़ और अफ़ग़ानिस्तान से ये साबित हो गया है. दुनिया को अमेरिकी नारों से कोई फ़र्क़ नहीं पड़ता है. वो चाहे ट्रंप का अमेरिका फर्स्ट हो या बाइडन का अमेरिका बैक.'' रईसी ने ईरान में 1979 की इस्लामिक क्रांति की तारीफ़ की और इसे धार्मिक लोकतंत्र से भी जोड़ा. उन्होंने पश्चिम में आतंकवाद में हुई बढ़ोतरी को अध्यात्म में आई गिरावट से भी जोड़ा. रईसी ने अपने संबोधन में कहा कि अमेरिका से बातचीत तभी शुरू हो सकती है जब कोई ठोस नतीजे की उम्मीद होगी और प्रतिबंध हटाए जाएंगे. उन्होंने कहा कि ईरान अमेरिकी सरकार के वादों पर भरोसा नहीं कर सकती है.
अमेरिकी अख़बार वॉशिंगटन पोस्ट के अनुसार, अमेरिकी विदेश मंत्रालय के एक अधिकारी ने कहा है कि उन्होंने रईसी के भाषण को सुना है लेकिन वे चाहते हैं कि ईरान अपने परमाणु कार्यक्रम पर कुछ ठोस करे.
रईसी ने कहा कि ईरान के रक्षा सिद्धांत में परमाणु हथियार और प्रतिरोधक नीति (डेटरेंस पॉलिसी) की कोई जगह नहीं है. अमेरिकी राष्ट्रपति जो बाइडन ने यूएन महासभा को संबोधित करते मंगलवार को कहा था कि अमेरिका अपने रुख़ पर कायम है कि वो ईरान को परमाणु हथियार हासिल नहीं करने देगा."""
    model = PySDBSegmenter.get_model()
    model_class = model.construct().__class__
    assert model_class == PySDBSegmenterParameters
    segmenter = PySDBSegmenter()
    parameters = PySDBSegmenterParameters()
    docs: List[Document] = segmenter.segment([Document(text=TEXT, metadata={'language':'hi'})], parameters)
    doc0 = docs[0]
    assert len(doc0.sentences) == 6
    # sents = [doc0.text[s.start:s.end] for s in doc0.sentences]


def test_rules_fr():
    TEXT = """ARTICLE I
Chapitre 1
chapitre bla, bla, bla, bla, bla, bla
Chapitre 2
chapitre bla, bla, bla, bla, bla, bla
ARTICLE II
Chapitre 1
chapitre bla, bla, bla, bla, bla, bla
Chapitre 2
chapitre bla, bla, bla, bla, bla, bla
"""
    model = PySDBSegmenter.get_model()
    model_class = model.construct().__class__
    assert model_class == PySDBSegmenterParameters
    segmenter = PySDBSegmenter()
    parameters = PySDBSegmenterParameters()
    docs: List[Document] = segmenter.segment([Document(text=TEXT, metadata={'language':'fr'})], parameters)
    doc0 = docs[0]
    assert len(doc0.sentences) == 10
    sents = [doc0.text[s.start:s.end] for s in doc0.sentences]
    assert sents[0].startswith("ARTICLE")
    assert sents[1].startswith("Chapitre")
    assert sents[2].startswith("chapitre")
    assert sents[3].startswith("Chapitre")
    assert sents[4].startswith("chapitre")
    assert sents[5].startswith("ARTICLE")
    assert sents[6].startswith("Chapitre")
    assert sents[7].startswith("chapitre")
    assert sents[8].startswith("Chapitre")
    assert sents[9].startswith("chapitre")


