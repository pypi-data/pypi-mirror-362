# textcleaner_partha/preprocess.py

import os
import re
import json
import spacy
import contractions
import importlib.resources as pkg_resources
from autocorrect import Speller
from bs4 import BeautifulSoup

# Lazy initialization
_nlp = None
_spell = None
_abbrev_map = None

ABBREV_DIR = pkg_resources.files("textcleaner_partha").joinpath("abbreviation_mappings")

def get_nlp():
    global _nlp
    if _nlp is None:
        try:
            _nlp = spacy.load("en_core_web_sm")
        except OSError:
            raise OSError("Model 'en_core_web_sm' not found. Run: python -m spacy download en_core_web_sm")
    return _nlp

def get_spell():
    global _spell
    if _spell is None:
        _spell = Speller()
    return _spell

def load_abbreviation_mappings():
    global _abbrev_map

    if _abbrev_map is None:
        _abbrev_map = {}

    if os.path.exists(ABBREV_DIR):
        for fname in os.listdir(ABBREV_DIR):
            if fname.endswith(".json"):
                path = os.path.join(ABBREV_DIR, fname)
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        _abbrev_map.update({k.lower(): v for k, v in data.items()})
                except Exception as e:
                        print(f"[textcleaner warning] Failed to load {fname}: {e}")

    return _abbrev_map

def expand_abbreviations(text):
    abbr_map = load_abbreviation_mappings()

    def replace_abbr(match):
        word = match.group(0)
        return abbr_map.get(word.lower(), word)

    return re.sub(r'\b\w+\b', replace_abbr, text)

def remove_html_tags(text):
    soup = BeautifulSoup(text, "html.parser")
    return soup.get_text()

def remove_emojis(text):
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F680-\U0001F6FF"  # transport & map symbols
        "\U0001F1E0-\U0001F1FF"  # flags
        "\U00002700-\U000027BF"  # dingbats
        "\U0001F900-\U0001F9FF"  # supplemental symbols and pictographs
        "\U0001FA70-\U0001FAFF"  # extended pictographs
        "\U00002600-\U000026FF"  # miscellaneous symbols
        "]+",
        flags=re.UNICODE
    )
    return emoji_pattern.sub(r'', text)

def remove_extra_whitespace(text):
    return re.sub(r'\s+', ' ', text).strip()

def remove_punctuation(text):
    return re.sub(r'[^\w\s]', '', text)

def correct_spellings(text):
    spell = get_spell()
    return ' '.join([spell(w) for w in text.split()])

def expand_contractions(text):
    return contractions.fix(text)

def preprocess(
    text,
    lowercase=True,
    remove_html=True,
    remove_emoji=True,
    remove_whitespace=True,
    remove_punct=False,
    expand_contraction=True,
    expand_abbrev=True,
    correct_spelling=True,
    lemmatise=True,
    verbose=False,
):
    if lowercase:
        text = text.lower()

    if remove_html:
        text = remove_html_tags(text)

    if remove_emoji:
        text = remove_emojis(text)

    if expand_abbrev:
        try:
            text = expand_abbreviations(text)
        except Exception as e:
            if verbose:
                print(f"[textcleaner warning] Abbreviation expansion skipped: {e}")

    if expand_contraction:
        text = expand_contractions(text)

    if correct_spelling:
        try:
            text = correct_spellings(text)
        except Exception as e:
            if verbose:
                print(f"[textcleaner warning] Spelling correction skipped: {e}")

    if remove_punct:
        text = remove_punctuation(text)

    if remove_whitespace:
        text = remove_extra_whitespace(text)

    if lemmatise:
        doc = get_nlp()(text)
        tokens = [
            token.lemma_ for token in doc
            if token.is_alpha
            and not token.is_stop
            and not token.is_punct
            and not token.like_num
            and token.pos_ in {"NOUN", "VERB", "ADJ", "ADV"}
        ]
        return ' '.join(tokens)

    return text

def get_tokens(
    text,
    lowercase=True,
    remove_html=True,
    remove_emoji=True,
    remove_whitespace=True,
    remove_punct=False,
    expand_contraction=True,
    expand_abbrev=True,
    correct_spelling=True,
    lemmatise=True,
    verbose=False,
):
    """Return the list of tokens after full preprocessing pipeline (minus joining)."""

    text = preprocess(
                        text,
                        lowercase=lowercase,
                        remove_html=remove_html,
                        remove_emoji=remove_emoji,
                        remove_whitespace=remove_whitespace,
                        remove_punct=remove_punct,
                        expand_contraction=expand_contraction,
                        expand_abbrev=expand_abbrev,
                        correct_spelling=correct_spelling,
                        lemmatise=False,
                        verbose=verbose,
                    )

    doc = get_nlp()(text)

    if lemmatise:
        tokens = [token.lemma_ for token in doc if not token.is_space]
    else:
        tokens = [token.text for token in doc if not token.is_space]

    return tokens
