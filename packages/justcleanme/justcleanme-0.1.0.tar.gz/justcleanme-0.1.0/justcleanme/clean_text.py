import string
import html
import nltk
import emoji
from sklearn.feature_extraction.text import TfidfVectorizer
from textblob import TextBlob
from nltk.corpus import stopwords
# from sentence_transformers import SentenceTransformer

nltk.download('punkt')
nltk.download('stopwords')

class TextCleaner:
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
        # self.embed_model = SentenceTransformer('all-MiniLM-L6-v2')
    
    def count_words(self, text: str) -> int:
        return len(text.split())
    
    def remove_punctuation(self, text: str) -> str:
        return text.translate(str.maketrans('', '', string.punctuation))

    def remove_emojis(self, text: str) -> str:
        return emoji.replace_emoji(text, replace='')

    def remove_stopwords(self, text: str) -> str:
        words = text.split()
        filtered = [word for word in words if word.lower() not in self.stop_words]
        return ' '.join(filtered)

    def correct_spelling(self, text: str) -> str:
        return str(TextBlob(text).correct())

    def remove_html(self, text: str) -> str:
        return html.unescape(text)

    def convert_to_tfidf(self, texts: list) -> any:
        vectorizer = TfidfVectorizer()
        return vectorizer.fit_transform(texts)

    # def get_embeddings(self, texts: list) -> any:
    #     return self.embed_model.encode(texts)
