from pysbd import Segmenter
from spacy.language import Language
from spacy.tokens import Doc


@Language.factory(
    "pysbd_sentencizer",
    assigns=["token.is_sent_start", "doc.sents"],
    default_config={},
)
def create_pysbd_sentencizer(nlp, name):
    return PySBDSentencizer(nlp, name)


class PySBDSentencizer(object):
    def __init__(self, nlp, name):
        self.name = name
        self.seg = Segmenter(language=nlp.lang, clean=False,
                             char_span=True)

    def __call__(self, doc: Doc):
        sents_char_spans = self.seg.segment(doc.text)
        start_token_ids = [sent.start for sent in sents_char_spans]
        for token in doc:
            token.is_sent_start = (True if token.idx in start_token_ids else False)
        if doc.has_annotation("SENT_START"):
            # Trim starting spaces
            for sent in doc.sents:
                sentlen = len(sent)
                first_non_space = 0
                while first_non_space < sentlen and sent[first_non_space].is_space:
                    first_non_space += 1
                if 0 < first_non_space < sentlen:
                    sent[0].is_sent_start = False
                    sent[first_non_space].is_sent_start = True
        return doc
