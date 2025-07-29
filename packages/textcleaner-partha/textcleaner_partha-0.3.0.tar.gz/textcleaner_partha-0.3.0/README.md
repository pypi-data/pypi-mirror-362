# 🧹 textcleaner-partha

[![PyPI version](https://img.shields.io/pypi/v/textcleaner-partha?color=blue)](https://pypi.org/project/textcleaner-partha/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

A lightweight and reusable text preprocessing package for NLP tasks.
It cleans text by removing HTML tags and emojis, expanding contractions, correcting spelling, and performing lemmatization using spaCy.

## ✨ Features
	•	✅ HTML tag and emoji removal
	•	✅ Contraction expansion (e.g., “can’t” → “cannot”)
	•	✅ Abbreviation expansion (e.g., “asap” → “as soon as possible”)
	•	✅ Spelling correction with autocorrect
	•	✅ Lemmatization using spaCy (en_core_web_sm)
	•	✅ Filters out stopwords, punctuation, numbers
	•	✅ Retains only nouns, verbs, adjectives, and adverbs
	•	✅ Returns tokens in a text


## 🚀 Installation

### From PyPI:

```bash
pip install textcleaner-partha
```

Install directly from GitHub:

```bash
pip install git+https://github.com/partha6369/textcleaner.git
```

## 🧠 Usage

```python
from textcleaner_partha import preprocess

text = "I can't believe it's already raining! 😞 <p>Click here</p>"

# Default usage (all features enabled)
cleaned = preprocess(text)
print(cleaned)

# Custom usage with optional features disabled
cleaned_partial = preprocess(
    text,
    lemmatise=False,            # Skip spaCy processing (lemmatisation, POS filtering)
    correct_spelling=False,     # Skip spelling correction
    expand_contraction=False    # Skip contraction expansion
)
print(cleaned_partial)
```

```python
from textcleaner_partha import get_tokens

text = "I can't believe it's already raining! 😞 <p>Click here</p>"

# Default usage (all features enabled)
tokens = get_tokens(text)
print(tokens)

# Custom usage with optional features disabled
tokens_partial = get_tokens(
    text,
    lemmatise=False,            # Skip spaCy processing (lemmatisation, POS filtering)
    correct_spelling=False,     # Skip spelling correction
    expand_contraction=False    # Skip contraction expansion
)
print(tokens_partial)
```

## 🔧 Parameters

The preprocess() and get_tokens() functions offer flexible control over each text cleaning step. You can selectively enable or disable operations using the parameters below:

```python
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
)
```

```python
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
)
```

## 📦 Dependencies

	•	spacy
	•	autocorrect
	•	contractions

You can install them manually or via the included requirements.txt:
```bash
pip install -r requirements.txt
```

And download the required spaCy model:
```bash
python -m spacy download en_core_web_sm
```


## 📄 License

MIT License © Dr. Partha Majumdar
