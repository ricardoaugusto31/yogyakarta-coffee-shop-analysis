"""
Phase 2: Persona Analysis via Word Clouds

This script utilizes advanced NLP techniques to analyze customer reviews,
aiming to visually represent two key user personas: 'Productivity Hub' (Nugas)
and 'Social Hotspot' (Nongkrong). It employs NLTK for stopwords and Sastrawi
for stemming to ensure high-quality text processing.

Key Steps:
1.  Initialize NLTK stopwords and the Sastrawi stemmer.
2.  Load and merge the primary shop and review datasets.
3.  Apply an advanced text preprocessing pipeline to clean the review text.
4.  Generate and save distinct Word Clouds for each persona.
"""

# Import necessary libraries
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import re
import nltk
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

# =============================================================================
# 1. NLP TOOLKIT SETUP
# =============================================================================
# Ensure NLTK stopwords are available locally.
try:
    nltk.data.find('corpora/stopwords')
except nltk.downloader.DownloadError:
    print("Downloading NLTK stopwords for Indonesian...")
    nltk.download('stopwords')

# Initialize the Sastrawi stemmer for Bahasa Indonesia.
print("Initializing Sastrawi stemmer...")
factory = StemmerFactory()
stemmer = factory.create_stemmer()

# Combine NLTK's standard stopwords with a custom list of slang and common terms.
stopwords_indonesian = set(nltk.corpus.stopwords.words('indonesian'))
custom_stopwords = {
    'yg', 'ga', 'gak', 'engga', 'nggak', 'nya', 'sih', 'saja', 'aja', 'kalo',
    'kalau', 'oke', 'banget', 'bgt', 'pas', 'biar', 'bikin', 'kok', 'tp',
    'tapi', 'udah', 'sdh', 'jgn', 'jangan', 'makin', 'pake', 'pakai', 'cuma',
    'trs', 'terus', 'emang', 'cukup', 'kurang', 'agak', 'lumayan', 'ya'
}
stopwords_indonesian.update(custom_stopwords)
print("NLP tools are ready with custom stopwords.")

# =============================================================================
# 2. DATA PREPARATION
# =============================================================================
SHOPS_FILE_PATH = 'datasets/coffee-shop-yogyakarta-indonesia.csv'
REVIEWS_FILE_PATH = 'datasets/coffee-shop-review-yogyakarta-indonesia.csv'

try:
    df_shops = pd.read_csv(SHOPS_FILE_PATH, delimiter=';')
    # Specify 'latin-1' encoding to handle potential character issues in reviews.
    df_reviews = pd.read_csv(REVIEWS_FILE_PATH, delimiter=';', encoding='latin-1')
    print("Datasets successfully loaded.")
except FileNotFoundError as e:
    print(f"Error: {e}. Please ensure dataset files are in the correct path.")
    exit()

# Merge the two dataframes.
df_merged = pd.merge(df_shops, df_reviews, left_on='Id', right_on='OrganizationId', how='left')
df_merged.dropna(subset=['ReviewTextOriginal'], inplace=True)
print("Data merging complete.")

# =============================================================================
# 3. ADVANCED TEXT PREPROCESSING
# =============================================================================
def preprocess_text_advanced(text):
    """
    A text cleaning pipeline that applies lowercasing, punctuation removal,
    stemming, and stopword removal.
    """
    text = text.lower()
    text = re.sub(r'[^a-z\s]', '', text) # Keep only letters and spaces
    text = stemmer.stem(text)
    words = [word for word in text.split() if word not in stopwords_indonesian]
    return " ".join(words)

print("Starting advanced text preprocessing on all reviews (this may take a while)...")
df_merged['CleanedReview'] = df_merged['ReviewTextOriginal'].apply(preprocess_text_advanced)
print("Advanced text preprocessing complete.")

# =============================================================================
# 4. PERSONA-BASED WORD CLOUD GENERATION
# =============================================================================
# Keywords are in their stemmed (root) form for accurate matching.
nugas_keywords_stemmed = ['tugas', 'kerja', 'wifi', 'colok', 'tenang', 'nyaman', 'laptop', 'produktif', 'konsen', 'sendiri']
nongkrong_keywords_stemmed = ['nongkrong', 'kumpul', 'teman', 'asyik', 'suasana', 'betah', 'instagram', 'estetik', 'ramai', 'seru', 'bareng']

# Create a text corpus for each persona by filtering reviews.
nugas_text_corpus = " ".join(review for review in df_merged[df_merged['CleanedReview'].str.contains('|'.join(nugas_keywords_stemmed))]['CleanedReview'])
nongkrong_text_corpus = " ".join(review for review in df_merged[df_merged['CleanedReview'].str.contains('|'.join(nongkrong_keywords_stemmed))]['CleanedReview'])

print("Generating improved Word Clouds...")

# Define common words to exclude specifically from the word clouds for better focus.
wordcloud_stopwords = set(['tempat', 'kopi', 'enak'])

# --- Word Cloud for "Productivity Hub" Persona ---
wordcloud_nugas = WordCloud(
    width=800, height=400, background_color='white',
    colormap='viridis', stopwords=wordcloud_stopwords
).generate(nugas_text_corpus)

plt.figure(figsize=(10, 8))
plt.imshow(wordcloud_nugas, interpolation='bilinear')
plt.axis('off')
plt.title('Word Cloud: "Productivity Hub" Persona', fontsize=16, pad=20)
plt.savefig('output/stage-2-persona/wordcloud_nugas.png')
print("Visualization 'wordcloud_nugas.png' has been saved.")

# --- Word Cloud for "Social Hotspot" Persona ---
wordcloud_nongkrong = WordCloud(
    width=800, height=400, background_color='white',
    colormap='plasma', stopwords=wordcloud_stopwords
).generate(nongkrong_text_corpus)

plt.figure(figsize=(10, 8))
plt.imshow(wordcloud_nongkrong, interpolation='bilinear')
plt.axis('off')
plt.title('Word Cloud: "Social Hotspot" Persona', fontsize=16, pad=20)
plt.savefig('output/stage-2-persona/wordcloud_nongkrong.png')
print("Visualization 'wordcloud_nongkrong.png' has been saved.")

print("\nPhase 2 Analysis Complete.")