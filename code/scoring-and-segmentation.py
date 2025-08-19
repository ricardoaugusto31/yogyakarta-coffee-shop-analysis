"""
Phase 3: Scoring and Segmentation

This script quantifies the persona characteristics of each coffee shop by
implementing a sophisticated scoring model. It uses keyword weighting to
capture the significance of certain terms and Min-Max normalization to ensure
a fair, balanced comparison between the two persona scores.

Key Steps:
1.  Initialize NLP tools and load all necessary data.
2.  Apply the advanced text preprocessing pipeline from Phase 2.
3.  Calculate a weighted score for each individual review.
4.  Aggregate review scores to get a final score for each coffee shop.
5.  Normalize the final scores to a 0-1 scale.
6.  Generate and save the definitive 4-quadrant segmentation plot.
7.  Save the final scored and normalized data for the recommendation phase.
"""

# Import necessary libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re
import nltk
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from sklearn.preprocessing import MinMaxScaler

# =============================================================================
# 1. NLP TOOLKIT SETUP
# =============================================================================
try:
    nltk.data.find('corpora/stopwords')
except nltk.downloader.DownloadError:
    nltk.download('stopwords')

print("Initializing Sastrawi stemmer...")
factory = StemmerFactory()
stemmer = factory.create_stemmer()

stopwords_indonesian = set(nltk.corpus.stopwords.words('indonesian'))
custom_stopwords = {
    'yg', 'ga', 'gak', 'engga', 'nggak', 'nya', 'sih', 'saja', 'aja', 'kalo',
    'kalau', 'oke', 'banget', 'bgt', 'pas', 'biar', 'bikin', 'kok', 'tp',
    'tapi', 'udah', 'sdh', 'jgn', 'jangan', 'makin', 'pake', 'pakai', 'cuma',
    'trs', 'terus', 'emang', 'cukup', 'kurang', 'agak', 'lumayan', 'tempat', 'kopi'
}
stopwords_indonesian.update(custom_stopwords)
print("NLP tools are ready.")

# =============================================================================
# 2. DATA PREPARATION
# =============================================================================
SHOPS_FILE_PATH = 'datasets/coffee-shop-yogyakarta-indonesia.csv'
REVIEWS_FILE_PATH = 'datasets/coffee-shop-review-yogyakarta-indonesia.csv'

try:
    df_shops = pd.read_csv(SHOPS_FILE_PATH, delimiter=';')
    df_reviews = pd.read_csv(REVIEWS_FILE_PATH, delimiter=';', encoding='latin-1')
    print("Datasets successfully loaded.")
except FileNotFoundError as e:
    print(f"Error: {e}.")
    exit()

# Clean and prepare the main shops dataframe.
df_shops.dropna(subset=['RateStars'], inplace=True)
df_shops['RateStars'] = df_shops['RateStars'].astype(str).str.replace(',', '.', regex=False).astype(float)
# Extract a display name from the address field.
df_shops['OrganizationName'] = df_shops['OrganizationAddress'].apply(
    lambda x: x.split(',')[0] if isinstance(x, str) else 'Unknown'
)

# Merge and clean the combined dataframe.
df_merged = pd.merge(df_shops, df_reviews, left_on='Id', right_on='OrganizationId', how='left')
df_merged.dropna(subset=['ReviewTextOriginal'], inplace=True)
print("Data merging complete.")

# =============================================================================
# 3. ADVANCED TEXT PREPROCESSING
# =============================================================================
def preprocess_text_advanced(text):
    text = text.lower()
    text = re.sub(r'[^a-z\s]', '', text)
    text = stemmer.stem(text)
    words = [word for word in text.split() if word not in stopwords_indonesian]
    return " ".join(words)

print("Starting advanced text preprocessing...")
df_merged['CleanedReview'] = df_merged['ReviewTextOriginal'].apply(preprocess_text_advanced)
print("Advanced text preprocessing complete.")

# =============================================================================
# 4. ADVANCED SCORING (WEIGHTING & NORMALIZATION)
# =============================================================================
print("Calculating weighted and normalized scores...")

# Define weighted keywords to score reviews more accurately.
# High-impact words receive a higher weight.
nugas_weights = {
    'tugas': 3, 'kerja': 3, 'wifi': 3, 'colok': 3, 'laptop': 2, 'produktif': 2,
    'konsen': 2, 'tenang': 1, 'nyaman': 1, 'sendiri': 1, 'buku': 1, 'belajar': 2
}
nongkrong_weights = {
    'nongkrong': 3, 'kumpul': 3, 'teman': 3, 'bareng': 3, 'asyik': 2, 'suasana': 2,
    'betah': 1, 'instagram': 2, 'estetik': 2, 'ramai': 1, 'seru': 2, 'obrol': 2, 'santai': 1
}

def calculate_weighted_score(text, weights):
    """Calculates a score for a text based on a dictionary of weighted keywords."""
    return sum(weights.get(word, 0) for word in text.split())

# Apply the weighted scoring function to each review.
df_merged['skor_nugas_review'] = df_merged['CleanedReview'].apply(lambda x: calculate_weighted_score(x, nugas_weights))
df_merged['skor_nongkrong_review'] = df_merged['CleanedReview'].apply(lambda x: calculate_weighted_score(x, nongkrong_weights))

# Aggregate scores by summing them up for each coffee shop.
shop_scores = df_merged.groupby('Id').agg({
    'OrganizationName': 'first', 'RateStars': 'first', 'ReviewsTotalCount': 'first',
    'skor_nugas_review': 'sum', 'skor_nongkrong_review': 'sum'
}).reset_index()

shop_scores.rename(columns={
    'skor_nugas_review': 'Total_Skor_Nugas', 'skor_nongkrong_review': 'Total_Skor_Nongkrong'
}, inplace=True)

# Normalize the aggregated scores to a 0-1 scale for fair comparison.
scaler = MinMaxScaler()
shop_scores[['Nugas_Score_Normalized', 'Nongkrong_Score_Normalized']] = scaler.fit_transform(
    shop_scores[['Total_Skor_Nugas', 'Total_Skor_Nongkrong']]
)
print("Scoring and normalization complete.")

# =============================================================================
# 5. VISUALIZATION AND SAVING
# =============================================================================
print("Generating final 4-quadrant segmentation plot...")

x_col, y_col = 'Nugas_Score_Normalized', 'Nongkrong_Score_Normalized'

# Use the median as a robust divider for segmentation.
median_nugas_norm = shop_scores[x_col].median()
median_nongkrong_norm = shop_scores[y_col].median()

plt.figure(figsize=(12, 12))
sns.scatterplot(
    x=x_col, y=y_col, data=shop_scores,
    hue='RateStars', size='ReviewsTotalCount',
    sizes=(50, 1000), palette='viridis', alpha=0.8
)

# Add quadrant lines based on the median.
plt.axvline(median_nugas_norm, color='grey', linestyle='--')
plt.axhline(median_nongkrong_norm, color='grey', linestyle='--')

plt.title('Coffee Shop Segmentation (Normalized Scores)', fontsize=18, pad=20)
plt.xlabel('Productivity Score (Normalized)', fontsize=12)
plt.ylabel('Social Score (Normalized)', fontsize=12)
plt.legend(title='Rating & Review Count', bbox_to_anchor=(1.05, 1), loc='upper left')

# Add quadrant annotations in the corners for clarity.
x_min, x_max = plt.xlim()
y_min, y_max = plt.ylim()
margin = 0.04

plt.text(x_max - margin, y_max - margin, 'All-Rounder', ha='right', va='top', fontsize=12, color='green', weight='bold')
plt.text(x_max - margin, y_min + margin, 'Productivity Hub', ha='right', va='bottom', fontsize=12, color='blue', weight='bold')
plt.text(x_min + margin, y_max - margin, 'Social Hotspot', ha='left', va='top', fontsize=12, color='red', weight='bold')
plt.text(x_min + margin, y_min + margin, 'General Purpose', ha='left', va='bottom', fontsize=12, color='grey', weight='bold')

plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.savefig('output/stage-3-scoring/scoring_segmentation.png')
print("Visualization 'scoring_segmentation.png' has been saved.")

# Save the final data for the next phase.
shop_scores.to_csv('output/stage-3-scoring/coffee_shop_scores_final.csv', index=False)
print("Final dataframe with scores has been saved.")
print("\nPhase 3 Analysis Complete.")