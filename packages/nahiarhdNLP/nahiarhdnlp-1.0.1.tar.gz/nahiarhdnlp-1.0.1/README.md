# nahiarhdNLP

[![PyPI version](https://badge.fury.io/py/nahiarhdNLP.svg)](https://badge.fury.io/py/nahiarhdNLP)
[![Python Version](https://img.shields.io/pypi/pyversions/nahiarhdNLP.svg)](https://pypi.org/project/nahiarhdNLP/)
[![GitHub](https://img.shields.io/github/stars/nahiarhdNLP/nahiarhdNLP?style=social)](https://github.com/nahiarhdNLP/nahiarhdNLP)

**nahiarhdNLP** is an advanced Python library for Indonesian Natural Language Processing (NLP), providing easy-to-use tools for text preprocessing, normalization, tokenization, stemming, spell correction, and customizable pipelines.

---

## Installation

```bash
pip install nahiarhdNLP
```

---

## Features

- **Preprocessing**: Clean text from HTML, URLs, stopwords, slang, emoji, mentions, hashtags, numbers, punctuation, extra spaces, and special characters.
- **Tokenization**: Split sentences into tokens/words.
- **Stemming**: Convert words to their root form (using Sastrawi).
- **Spell Correction**: Automatic spelling correction.
- **Pipeline**: Chain multiple preprocessing functions easily.
- **Normalization**: Replace slang, emoji, and informal words with formal equivalents.

---

## Quick Usage Example

### Basic Preprocessing

```python
from nahiarhdNLP import preprocessing

text = "Halooo emg siapa yg nanya? 😀 <a href='#'>link</a> @user #trending 123"
cleaned = preprocessing.cleaning.text_cleaner.clean_text(text)
print(cleaned)
```

### Custom Preprocessing Pipeline

```python
from nahiarhdNLP.preprocessing import (
    pipeline, remove_html, remove_url, remove_mentions, remove_hashtags,
    remove_numbers, replace_word_elongation, emoji_to_words, replace_slang,
    remove_stopwords, remove_punctuation, remove_extra_spaces, to_lowercase
)

custom_pipe = pipeline([
    remove_html, remove_url, remove_mentions, remove_hashtags, remove_numbers,
    replace_word_elongation, emoji_to_words, replace_slang, remove_stopwords,
    remove_punctuation, remove_extra_spaces, to_lowercase
])

result = custom_pipe("Halooo emg siapa yg nanya? 😀 <a href='#'>link</a> @user #trending 123")
print(result)
```

### Spell Correction

```python
from nahiarhdNLP.preprocessing import correct_spelling
print(correct_spelling("sya suka mkn nasi"))  # "saya suka makan nasi"
```

### Stemming

```python
from nahiarhdNLP.preprocessing import stem_text
print(stem_text("bermain-main dengan senang"))  # "main dengan senang"
```

---

## Requirements

- Python 3.7+
- pandas, fsspec, huggingface_hub, sastrawi, datasets, rich

---

## Testing

```bash
pytest tests/
```

---

## Directory Structure

```
nahiarhdNLP/
├── main.py
├── requirements.txt
├── README.md
├── src/
│   ├── preprocessing/
│   ├── mydatasets/
└── tests/
```

---

## Contribution

Contributions are welcome! Please fork the repository, create a new branch, and submit a pull request.

---

## License

MIT License

---

## Acknowledgments

- Stopwords dataset from HuggingFace
- Emoji dataset from HuggingFace
- Slang dataset from HuggingFace
- Sastrawi for Indonesian stemming
