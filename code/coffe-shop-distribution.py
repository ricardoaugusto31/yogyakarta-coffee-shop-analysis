"""
Phase 1: Exploratory Data Analysis (EDA)

This script conducts the initial exploration of the Yogyakarta coffee shop dataset.
Its primary goal is to establish a foundational understanding of the dataset's
characteristics, focusing on the distribution, quality, and geographic density
of coffee shops.

Key Steps:
1.  Load the primary dataset from a CSV file.
2.  Perform essential data cleaning and type conversion.
3.  Generate and save three key visualizations:
    - Geographical distribution scatter plot.
    - Rating distribution count plot.
    - Location concentration heatmap.
"""

# Import necessary libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# =============================================================================
# 1. DATA LOADING
# =============================================================================
# Define the file path for better project management.
FILE_PATH = 'datasets/coffee-shop-yogyakarta-indonesia.csv'

try:
    # Load the dataset, specifying the semicolon delimiter.
    df_shops = pd.read_csv(FILE_PATH, delimiter=';')
    print(f"Dataset successfully loaded from: {FILE_PATH}")
except FileNotFoundError:
    print(f"Error: File not found at the specified path: {FILE_PATH}")
    exit()

# =============================================================================
# 2. DATA CLEANING
# =============================================================================
print("Starting data cleaning process...")

# Drop records with null values in critical columns required for analysis.
initial_rows = len(df_shops)
df_shops.dropna(subset=['RateStars', 'OrganizationLatitude', 'OrganizationLongitude'], inplace=True)
print(f"Handling missing values: {initial_rows - len(df_shops)} rows were dropped.")

# Standardize and convert data types for numerical columns read as text.
# The decimal comma (,) is replaced with a period (.) to enable float conversion.
for col in ['RateStars', 'OrganizationLatitude', 'OrganizationLongitude']:
    df_shops[col] = df_shops[col].astype(str).str.replace(',', '.', regex=False).astype(float)

print("Data cleaning and type conversion complete.")

# =============================================================================
# 3. EXPLORATORY VISUALIZATION
# =============================================================================
print("Generating visualizations...")

# A. Geographical Distribution Scatter Plot
plt.figure(figsize=(10, 10))
sns.scatterplot(
    x='OrganizationLongitude',
    y='OrganizationLatitude',
    data=df_shops,
    hue='RateStars',      # Color-code points by rating
    palette='viridis',    # Use a colorblind-friendly palette
    alpha=0.7,
    s=50
)
plt.title('Geographical Distribution of Coffee Shops in Yogyakarta', fontsize=16, pad=20)
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.legend(title='Star Rating')
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.savefig('output/stage-1-distribution/geographical_distribution.png')
print("Visualization 'geographical_distribution.png' has been saved.")

# B. Rating Distribution Count Plot
plt.figure(figsize=(12, 7))

# Calculate rating frequencies and sort by the rating value for a logical x-axis order.
rating_counts = df_shops['RateStars'].value_counts().sort_index()

# Create a bar plot to show the count of shops for each unique rating.
ax = sns.countplot(
    x='RateStars',
    data=df_shops,
    palette='viridis',
    order=rating_counts.index  # Enforce logical sorting
)

plt.title('Rating Distribution of Coffee Shops in Yogyakarta', fontsize=16, pad=20)
ax.set_xlabel('Star Rating', fontsize=12)
ax.set_ylabel('Number of Coffee Shops', fontsize=12)
ax.tick_params(axis='x', rotation=45)
ax.grid(axis='y', linestyle='--', alpha=0.6)

# Add data labels above each bar for precise counts.
for p in ax.patches:
    ax.annotate(f'{int(p.get_height())}',
                (p.get_x() + p.get_width() / 2., p.get_height()),
                ha='center', va='center',
                xytext=(0, 9),
                textcoords='offset points')

plt.tight_layout()
plt.savefig('output/stage-1-distribution/rating_distribution.png')
print("Visualization 'rating_distribution.png' has been saved.")

# C. Location Concentration Heatmap (Hexbin Plot)
plt.figure(figsize=(12, 10))
plt.hexbin(
    x=df_shops['OrganizationLongitude'],
    y=df_shops['OrganizationLatitude'],
    gridsize=30,      # Adjust bin size to control the aggregation level
    cmap='plasma'     # Use a distinct color map for heatmaps
)
plt.colorbar(label='Number of Coffee Shops per Area')
plt.title('Concentration Map of Coffee Shops in Yogyakarta', fontsize=16, pad=20)
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.tight_layout()
plt.savefig('output/stage-1-distribution/concentration_heatmap.png')
print("Visualization 'concentration_heatmap.png' has been saved.")

print("\nPhase 1 Analysis Complete. All visualizations have been saved.")