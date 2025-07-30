from spacy.matcher import Matcher
from spacy.tokens import Doc
from spacy.language import Language


@Language.factory(
    "rules_sentencizer",
    assigns=["token.is_sent_start", "doc.sents"],
    default_config={"split_patterns": None, "join_patterns": None},
)
def create_rules_sentencizer(nlp, name, split_patterns, join_patterns):
    return RuleSentencizer(nlp, name, split_patterns, join_patterns)


class RuleSentencizer(object):
    """
    Simple component that correct some over-segmentation errors of the sentencizer using exception rules.
    Each rule must have a IS_SENT_START token pattern and this sentence boundary is removed from the final output.
    For example the text
    "Une indemnité de 100. 000 Frs"
    is by default segmented after the 100. but it shouldn't
    With this simple rule:
    [{"IS_DIGIT": True}, {"IS_SENT_START": True, "IS_PUNCT" : True}, {"IS_DIGIT": True}]
    The sentence corrector does the trick.

    The component is initialized this way:
    overrides = defaultdict(dict)
    overrides["rules_sentencizer"]["split"] = [
        # Split on double line breaks
        [{"IS_SPACE": True, "TEXT": { "REGEX" : "[\n]{2,}" }}, {}],
        # Split on hard punctuation
        [{"IS_PUNCT": True, "TEXT" : { "IN" : [".", "!", "?"]}}, {}]
    ]
    overrides["rules_sentencizer"]["join"] = [
        # Une indemnité de 100. 000 Frs
        [{"IS_DIGIT": True}, {"IS_SENT_START": True, "IS_PUNCT" : True}, {"IS_DIGIT": True}]
    ]
    nlp = spacy.load(model)
    custom = RuleSentencizer(nlp, **overrides)
    nlp.add_pipe(custom)
    """

    def __init__(self, nlp, name, split_patterns, join_patterns):
        self.name = name
        if split_patterns:
            self.split_matcher = Matcher(nlp.vocab)
            self.split_matcher.add("split", split_patterns)
        else:
            self.split_matcher = None
        if join_patterns:
            self.join_matcher = Matcher(nlp.vocab)
            self.join_matcher.add("join", join_patterns)
        else:
            self.join_matcher = None

    def __call__(self, doc: Doc):
        if self.split_matcher:
            matches = self.split_matcher(doc)
            for match_id, start, end in matches:
                token = doc[end - 1]
                token.is_sent_start = True
                if end - 2 >= 0 and doc[end - 2].is_sent_start is True:
                    doc[end - 2].is_sent_start = False
        if self.join_matcher:
            matches = self.join_matcher(doc)
            for match_id, start, end in matches:
                # If there is a sent start in the match, just remove it
                for token in doc[start:end]:
                    if token.is_sent_start:
                        token.is_sent_start = False
        if doc.has_annotation("SENT_START"):
            # Trim starting spaces
            for sent in doc.sents:
                sentlen = len(sent)
                first_non_space = 0
                while first_non_space < sentlen and sent[first_non_space].is_space:
                    first_non_space += 1
                if first_non_space > 0 and first_non_space < sentlen:
                    sent[0].is_sent_start = False
                    sent[first_non_space].is_sent_start = True
        return doc
