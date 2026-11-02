---
name: text-preprocessor
description: Preprocess raw text by lowercasing, tokenizing (word or subword via BPE/SentencePiece), removing punctuation and numbers, lemmatizing with spaCy or stemming with Porter/Snowball, removing stopwords via NLTK, and extracting n-grams. Use this skill when cleaning text for NLP models, with optional spell correction, URL/email removal, and HTML stripping.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: data-engineering
tags: [nlp, tokenization, lemmatization, stopwords, bpe]
related: [data-engineering/image-dataset-loader, data-engineering/tabular-data-sampler]
prerequisites: []
outputs: [python]
difficulty: intermediate
estimated_tokens: 1300
permissions:
  read_files: true
  write_files: false
  network: false
  execute_code: true
language: en
last_reviewed: 2026-11-02
verified_against: []
---

# Text Preprocessor

## When To Use

- Raw text must be cleaned before being fed to a TF-IDF, count, or embedding model.
- Tokenization needs to be word-level or subword (BPE/SentencePiece).
- Lemmatization (spaCy) or stemming (Porter/Snowball) is required.
- Stopwords, URLs, emails, and HTML tags must be stripped.
- Optional steps like spell correction or n-gram extraction are needed.

## Workflow

1. Decide on the output form: token list or joined string.
2. Strip HTML (BeautifulSoup) if the source is web content.
3. Remove URLs and emails via regex before tokenization.
4. Lowercase the text (unless case preservation is requested).
5. Tokenize: word-level (regex/whitespace) or subword (BPE/SentencePiece).
6. Remove punctuation and numbers; keep alphabetic tokens unless told otherwise.
7. Apply lemmatization (spaCy) or stemming (Porter/Snowball).
8. Remove stopwords from a declared language list (NLTK).
9. Optionally extract n-grams (bigrams, trigrams) from the cleaned tokens.
10. Optionally run spell correction on the cleaned tokens.
11. Emit the cleaned token list or joined string plus a preprocessing manifest.

## Inputs

- Raw text (string, list of strings, or a file).
- Pipeline config: language, tokenization mode, lemmatize/stem, stopword list, n-gram size.

## Outputs

- A list of cleaned tokens (or joined string) per input text.
- A preprocessing manifest (JSON) listing the steps applied and parameters.

## Key Rules

- Stopword removal uses a declared language; never silently pick a default.
- Lemmatization and stemming are mutually exclusive; one or the other, not both.
- HTML stripping happens before tokenization so tags do not pollute tokens.
- URLs and emails are removed before tokenization to avoid splitting them mid-word.
- The manifest records every step and parameter so the pipeline is reproducible.
- Subword tokenizers (BPE/SentencePiece) skip stopword and lemmatize steps.

## Examples

```python
import re
import nltk
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, SnowballStemmer

try:
  nltk.data.find("corpora/stopwords")
except LookupError:
  nltk.download("stopwords")


URL_PATTERN = re.compile(r"https?://\S+|www\.\S+")
EMAIL_PATTERN = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
WORD_PATTERN = re.compile(r"[A-Za-z]+")


def StripHtml(text):
  # Remove HTML tags before tokenization so they never enter the vocabulary.
  return BeautifulSoup(text, "html.parser").get_text(separator=" ")


def RemoveUrlsAndEmails(text):
  # Drop URLs and emails in one pass.
  text = URL_PATTERN.sub(" ", text)
  text = EMAIL_PATTERN.sub(" ", text)
  return text


def Tokenize(text):
  # Word-level tokenizer keeping only alphabetic tokens.
  return WORD_PATTERN.findall(text.lower())


def RemoveStopwords(tokens, language="english"):
  # Drop stopwords declared for the target language.
  stopSet = set(stopwords.words(language))
  return [token for token in tokens if (token not in stopSet)]


def Stem(tokens, stemmerType="porter", language="english"):
  # Apply the chosen stemmer to the token list.
  if (stemmerType == "porter"):
    stemmer = PorterStemmer()
  else:
    stemmer = SnowballStemmer(language)
  return [stemmer.stem(token) for token in tokens]


def ExtractNgrams(tokens, n=2):
  # Build n-grams from the cleaned token list.
  return list(zip(*[tokens[i:] for i in range(n)]))


class TextPreprocessor:
  # Orchestrates the full pipeline driven by a config dict.
  def __init__(self, config):
    self.Config = config

  def Process(self, text):
    if (self.Config.get("StripHtml")):
      text = StripHtml(text)
    text = RemoveUrlsAndEmails(text)
    tokens = Tokenize(text)
    tokens = RemoveStopwords(tokens, self.Config.get("Language", "english"))
    if (self.Config.get("Stem")):
      tokens = Stem(tokens, self.Config["Stem"], self.Config.get("Language", "english"))
    if (self.Config.get("NgramSize")):
      tokens = tokens + [str(gram) for gram in ExtractNgrams(tokens, self.Config["NgramSize"])]
    if (self.Config.get("Output") == "string"):
      return " ".join(tokens)
    return tokens
```

## References

- NLTK: https://www.nltk.org
- spaCy: https://spacy.io
- SentencePiece: https://github.com/google/sentencepiece
- BeautifulSoup: https://www.crummy.com/software/BeautifulSoup/
