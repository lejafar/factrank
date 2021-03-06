import re
import unicodedata
import logging

import spacy

logger = logging.getLogger(__name__)


class Tokenize:

    def __init__(self):
        self.nlp = spacy.load('nl_core_news_sm')
        self.sentence_regex = re.compile(
            r' ?((?:[A-Z@#\d]|[\"][^\n]+?[\"] ?)(?:[\"\(][^\n]{1,30}?[\"\)]|\.{3}|[^?!\.\n]|\.[^ \nA-Z\"]){0,200}(?:!|\?|\n|\.{1})) ?'
        )

    @staticmethod
    def clean_text(text):
        # normalize unicode equivalence
        text = unicodedata.normalize('NFC', text)
        text = re.sub(r"\r", "", text)
        # normalize single quotes
        text = re.sub(r"’", "'", text)
        text = re.sub(r"‘", "'", text)
        # normalize double quotes
        text = re.sub(r"”", "\"", text)
        text = re.sub(r"„", "\"", text)
        text = re.sub(r"“", "\"", text)
        # replace linebreak by punctuation when followed by linebreak
        text = re.sub(r"(\"|\')\n", r"\g<1>.", text)
        # normalize dash
        text = re.sub(r"—", "-", text)
        text = re.sub(r"–", "-", text)
        # replace double punctuations
        text = re.sub(r"\?+", "?", text)
        text = re.sub(r"\!+", "!", text)
        text = re.sub(r"\,", ",", text)
        # different whitespace representations
        text = re.sub(r" ", " ", text)
        text = re.sub(r"­", " ", text)
        # remove unwanted stuff
        text = re.sub(r"^ +", "", text)
        text = re.sub(r"\n", " ", text)
        text = re.sub(r"\n$", "", text)
        text = re.sub(r"§", "", text)
        # clean dirt
        text = re.sub(r"…", "...", text)
        text = re.sub(r"[\*\n\\…\=•\[\]\|]", "", text)
        # clean excessive whitespace
        text = re.sub(r" +", " ", text).strip()

        if text:
            # clean leading twitter dirt
            while text.strip().split()[0][0] in {'#', '@'}:
                text = re.sub(r"^[@#][^ ]* *", "", text)
            # clean trailing twitter dirt
            while text.strip().split()[-1][0] in {'#', '@'}:
                text = re.sub(r" *[@#][^ ]* *([.?!]) *$", r"\g<1>", text)

        return text

    def clean_sentence_for_inference(self, sentence):
        sentence = Tokenize.clean_text(sentence)
        # remove unclosed brackets/quotes
        sentence = re.sub(r"^ *\( ?(?!.*\))", "", sentence)  # remove unclosed brackets
        sentence = re.sub(r"^ *\' ?(?!.*\')", "", sentence)  # remove single quotes
        sentence = re.sub(r"^ *\" ?(?!.*\")", "", sentence)  # remove double quotes
        # remove unwanted stuff
        sentence = re.sub(r"^ +", "", sentence)
        sentence = re.sub(r"[A-Z ]+: <<", "", sentence)
        # remove point at the end of sentence
        sentence = re.sub(r"\.$", "", sentence)
        # remove quotes when apparent at both ends
        sentence = re.sub(r"^\'(.*)\'$", r"\g<1>", sentence)  # single quotes
        sentence = re.sub(r"^\"(.*)\"$", r"\g<1>", sentence)  # double quotes
        # clean twitter dirt
        sentence = re.sub(r"@#", "", sentence)
        # tag digits with NUM
        sentence = self.tag_numeral(sentence)
        return sentence

    def tag_numeral(self, sentence):
        replace_values = {
            token.text: f"{token.text} {token.pos_}" for token in self.nlp(sentence) if token.pos_ in {'NUM'}
        }
        sentence = " ".join([replace_values.get(word, word) for word in sentence.split()])
        return sentence

    def tokenize(self, sentence):
        return [
            tok.text
            for tok in self.nlp.tokenizer(self.clean_sentence_for_inference(sentence).lower())
            if tok.text != " "
        ]

    def sentencize(self, text):
        text = self.clean_text(text)
        for sentence in self.sentence_regex.findall(text):
            if len(sentence.split()) < 3 or len(sentence.split()) > 50:
                continue  # too long / too short
            if sentence.count("\"") % 2:
                continue  # unclosed quotes
            if sentence.count("(") and sentence.count("(") - sentence.count(")"):
                continue  # unclosed brackets
            if sentence.count('#') > len(sentence.split()) / 2:
                continue  # probably too many hashtags
            yield sentence.strip()
