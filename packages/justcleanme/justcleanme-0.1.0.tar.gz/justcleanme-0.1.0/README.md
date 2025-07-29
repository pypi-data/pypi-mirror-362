# simpletextcleaner

Simple NLP preprocessing: word count, remove punctuation, emojis, stopwords, HTML, fix spelling, TF-IDF, embeddings.

## Usage

```python
from simpletextcleaner import TextCleaner

cleaner = TextCleaner()
text = "Hello 🌟 <b>world!</b> I'm learning NLP!!!"

print(cleaner.count_words(text))
print(cleaner.remove_punctuation(text))
print(cleaner.remove_emojis(text))
print(cleaner.remove_stopwords(text))
print(cleaner.correct_spelling("Ths is a spleling errr"))
print(cleaner.remove_html(text))
print(cleaner.convert_to_tfidf([text, "More examples here"]))
print(cleaner.get_embeddings(["This is a test."]))

