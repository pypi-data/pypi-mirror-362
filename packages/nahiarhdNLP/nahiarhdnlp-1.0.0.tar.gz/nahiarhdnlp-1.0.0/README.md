# nahiarhdNLP

[![PyPI version](https://badge.fury.io/py/nahiarhdNLP.svg)](https://badge.fury.io/py/nahiarhdNLP)
[![Python Version](https://img.shields.io/pypi/pyversions/nahiarhdNLP.svg)](https://pypi.org/project/nahiarhdNLP/)
[![Test](https://github.com/nahiarhdNLP/nahiarhdNLP/workflows/Test/badge.svg)](https://github.com/nahiarhdNLP/nahiarhdNLP/actions)
[![Lint](https://github.com/nahiarhdNLP/nahiarhdNLP/workflows/Lint/badge.svg)](https://github.com/nahiarhdNLP/nahiarhdNLP/actions)
[![codecov](https://codecov.io/gh/nahiarhdNLP/nahiarhdNLP/branch/main/graph/badge.svg)](https://codecov.io/gh/nahiarhdNLP/nahiarhdNLP)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

**Bahasa** | [English](README.md)

nahiarhdNLP adalah library python advanced yang bertujuan untuk memudahkan proyek NLP anda dengan fitur-fitur yang selalu up-to-date.

## Installation

nahiarhdNLP dapat diinstall dengan mudah dengan menggunakan pip:

```bash
$ pip install nahiarhdNLP
```

Atau clone repository ini:

```bash
git clone https://github.com/nahiarhdNLP/nahiarhdNLP.git
cd nahiarhdNLP
pip install -r requirements.txt
```

## Preprocessing

Modul `nahiarhdNLP.preprocessing` menyediakan beberapa fungsi umum untuk menyiapkan dan melakukan transformasi terhadap data teks mentah untuk digunakan pada konteks tertentu.

### Generics

#### remove_html

Menghapus html tag yang terdapat di dalam teks

```python
>>> from src.preprocessing import remove_html
>>> remove_html("website <a href='https://google.com'>google</a>")
"website google"
```

#### remove_url

Menghapus url yang terdapat di dalam teks

```python
>>> from src.preprocessing import remove_url
>>> remove_url("retrieved from https://gist.github.com/gruber/8891611")
"retrieved from "
```

#### remove_stopwords

Stopwords merupakan kata yang diabaikan dalam pemrosesan dan biasanya disimpan di dalam stop lists. Stop list ini berisi daftar kata umum yang mempunyai fungsi tapi tidak mempunyai arti.

Menghapus stopwords yang terdapat di dalam teks. List stopwords bahasa Indonesia didapatkan dari dataset HuggingFace.

```python
>>> from src.preprocessing import remove_stopwords
>>> remove_stopwords("siapa yang suruh makan?!!")
"suruh makan?!!"
```

#### replace_slang

Mengganti kata gaul (slang) menjadi kata formal tanpa mengubah makna dari kata tersebut. List kata gaul (slang words) bahasa Indonesian didapatkan dari dataset HuggingFace.

```python
>>> from src.preprocessing import replace_slang
>>> replace_slang("emg siapa yg nanya?")
"memang siapa yang bertanya?"
```

#### replace_word_elongation

Word elongation adalah tindakan untuk menambahkan huruf ke kata, biasanya di akhir kata.

Menghandle word elongation:

```python
>>> from src.preprocessing import replace_word_elongation
>>> replace_word_elongation("kenapaaa?")
"kenapaa?"
```

### Fungsi Pembersihan Individual

#### remove_mentions

Menghapus mentions (@username) dari teks.

```python
>>> from src.preprocessing import remove_mentions
>>> remove_mentions("Halo @user123 dan @admin, apa kabar?")
"Halo dan , apa kabar?"
```

#### remove_hashtags

Menghapus hashtags (#tag) dari teks.

```python
>>> from src.preprocessing import remove_hashtags
>>> remove_hashtags("Hari ini #senin #libur #weekend")
"Hari ini"
```

#### remove_numbers

Menghapus angka dari teks.

```python
>>> from src.preprocessing import remove_numbers
>>> remove_numbers("Saya berumur 25 tahun dan punya 3 anak")
"Saya berumur tahun dan punya anak"
```

#### remove_punctuation

Menghapus tanda baca dari teks.

```python
>>> from src.preprocessing import remove_punctuation
>>> remove_punctuation("Halo, apa kabar?! Semoga sehat selalu...")
"Halo apa kabar Semoga sehat selalu"
```

#### remove_extra_spaces

Menghapus spasi berlebih dari teks.

```python
>>> from src.preprocessing import remove_extra_spaces
>>> remove_extra_spaces("Halo    dunia   yang    indah")
"Halo dunia yang indah"
```

#### remove_special_chars

Menghapus karakter khusus yang bukan alfanumerik atau spasi.

```python
>>> from src.preprocessing import remove_special_chars
>>> remove_special_chars("Halo @#$%^&*() dunia!!!")
"Halo () dunia!!!"
```

#### remove_whitespace

Membersihkan karakter whitespace (tab, newline, dll).

```python
>>> from src.preprocessing import remove_whitespace
>>> remove_whitespace("Halo\n\tdunia\r\nyang indah")
"Halo dunia yang indah"
```

#### to_lowercase

Mengubah teks menjadi huruf kecil.

```python
>>> from src.preprocessing import to_lowercase
>>> to_lowercase("HALO Dunia Yang INDAH")
"halo dunia yang indah"
```

### Emoji

Preproses teks yang mengandung emoji.

#### emoji_to_words

Mengubah emoji yang berada dalam sebuah teks menjadi kata-kata yang sesuai dengan emoji tersebut.

```python
>>> from src.preprocessing import emoji_to_words
>>> emoji_to_words("emoji 😀😁")
"emoji wajah_gembira wajah_gembira_dengan_mata_bahagia"
```

#### words_to_emoji

Mengubah kata-kata dengan kode emoji menjadi emoji.

```python
>>> from src.preprocessing import words_to_emoji
>>> words_to_emoji("emoji wajah_gembira")
"emoji 😀"
```

### Pipelining

Membuat pipeline dari sequence fungsi preprocessing:

```python
>>> from src.preprocessing import pipeline, replace_word_elongation, replace_slang
>>> pipe = pipeline([replace_word_elongation, replace_slang])
>>> pipe("Knp emg gk mw makan kenapaaa???")
"Kenapa memang tidak mau makan kenapa??"
```

### Preprocessing All-in-One

Fungsi `preprocess` menyediakan preprocessing lengkap dengan berbagai opsi:

```python
>>> from src.preprocessing import preprocess
>>> preprocess("Halooo emg siapa yg nanya? 😀")
"halo wajah_gembira"
```

Dengan opsi kustomisasi:

```python
>>> from src.preprocessing import preprocess
>>> preprocess(
...     "Halooo emg siapa yg nanya? 😀",
...     remove_html_tags=True,
...     remove_urls=True,
...     remove_stopwords_flag=True,
...     replace_slang_flag=True,
...     replace_elongation=True,
...     convert_emoji=True,
...     to_lowercase=True
... )
"halo wajah_gembira"
```

## Fungsi Tambahan

### Tokenization

```python
>>> from src.preprocessing import tokenize
>>> tokenize("Saya suka makan nasi")
['Saya', 'suka', 'makan', 'nasi']
```

### Text Cleaning

```python
>>> from src.preprocessing import clean_text
>>> clean_text("Halooo!!! @user #trending https://example.com 😀")
"haloo!!"
```

### Spell Correction

```python
>>> from src.preprocessing import correct_spelling
>>> correct_spelling("sya suka mkn nasi")
"saya suka makan nasi"
```

### Stemming

```python
>>> from src.preprocessing import stem_text
>>> stem_text("bermain-main dengan senang")
"main dengan senang"
```

## Advanced Usage

### Menggunakan Kelas Langsung

Jika Anda memerlukan kontrol lebih lanjut, Anda dapat menggunakan kelas-kelas secara langsung:

```python
from src.preprocessing import TextCleaner, StopwordRemover, SlangNormalizer

# Inisialisasi dengan opsi kustom
cleaner = TextCleaner(
    remove_urls=True,
    remove_mentions=True,
    remove_hashtags=True,
    lowercase=True
)

stopword_remover = StopwordRemover(language="indonesian")
slang_normalizer = SlangNormalizer(language="indonesian")

# Gunakan
text = "Halooo @user ini contoh teks!!! https://example.com"
cleaned = cleaner.clean(text)
no_stopwords = stopword_remover.remove_stopwords(cleaned)
formal = slang_normalizer.normalize(no_stopwords)
```

### Pipeline Kustom

```python
from src.preprocessing import pipeline
from src.preprocessing import (
    remove_html,
    remove_url,
    replace_word_elongation,
    emoji_to_words,
    replace_slang,
    remove_stopwords,
    # Fungsi-fungsi individual
    remove_mentions,
    remove_hashtags,
    remove_numbers,
    remove_punctuation,
    remove_extra_spaces,
    to_lowercase
)

# Buat pipeline kustom
custom_pipe = pipeline([
    remove_html,
    remove_url,
    remove_mentions,
    remove_hashtags,
    remove_numbers,
    replace_word_elongation,
    emoji_to_words,
    replace_slang,
    remove_stopwords,
    remove_punctuation,
    remove_extra_spaces,
    to_lowercase
])

# Gunakan
result = custom_pipe("Halooo emg siapa yg nanya? 😀 <a href='#'>link</a> @user #trending 123")
print(result)
```

### Penggunaan Fungsi Individual

```python
from src.preprocessing import (
    remove_mentions,
    remove_hashtags,
    remove_numbers,
    remove_punctuation,
    remove_extra_spaces,
    to_lowercase
)

# Gunakan fungsi individual
text = "Halo @user123 #trending! Saya berumur 25 tahun..."
text = remove_mentions(text)  # "Halo #trending! Saya berumur 25 tahun..."
text = remove_hashtags(text)  # "Halo ! Saya berumur 25 tahun..."
text = remove_numbers(text)   # "Halo ! Saya berumur tahun..."
text = remove_punctuation(text)  # "Halo  Saya berumur tahun"
text = remove_extra_spaces(text)  # "Halo Saya berumur tahun"
text = to_lowercase(text)     # "halo saya berumur tahun"
```

## Requirements

- Python 3.7+
- datasets
- requests
- rich (untuk output yang menarik)

Untuk fitur tambahan:

- Sastrawi (untuk stemming): `pip install Sastrawi`
- pyspellchecker (untuk spell correction): `pip install pyspellchecker`

## Testing

Untuk menjalankan semua test:

```bash
pytest tests/
```

## Demo

Untuk melihat demo lengkap library:

```bash
python main.py
```

## Directory Structure

```
nahiarhdNLP/
├── main.py                    # Demo aplikasi
├── requirements.txt           # Dependencies
├── README.md                  # Dokumentasi
├── src/
│   ├── __init__.py           # Main module
│   ├── preprocessing/         # Modul preprocessing
│   │   ├── __init__.py       # Export semua fungsi
│   │   ├── utils.py          # Fungsi wrapper utama
│   │   ├── cleaning/         # Pembersihan teks
│   │   ├── normalization/    # Normalisasi teks
│   │   ├── linguistic/       # Pemrosesan linguistik
│   │   └── tokenization/     # Tokenisasi
│   └── mydatasets/           # Dataset loader
└── tests/                    # Unit tests
```

## Kontribusi

Kontribusi sangat diterima! Silakan fork repository ini, buat branch baru, dan submit pull request.

## License

MIT License

## Acknowledgments

- Dataset stopwords dari HuggingFace
- Dataset emoji dari HuggingFace
- Dataset slang dari HuggingFace
- Sastrawi untuk stemming bahasa Indonesia
