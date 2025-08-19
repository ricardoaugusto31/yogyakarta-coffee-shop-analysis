"""
Phase 1: Exploratory Data Analysis (EDA) - Yogyakarta Coffee Shop Landscape

This script performs the first stage of analysis on the Yogyakarta coffee shop dataset.
The main objective is to gain a high-level understanding of the distribution,
quality, and geographical concentration of coffee shops, which will serve as a
foundation for further, more detailed analysis.

The script covers the following steps:
1. Load the dataset from a CSV file.
2. Perform essential data cleaning on critical columns.
3. Generate and save three key visualizations:
   - A scatter plot for geographical distribution.
   - A count plot for rating distribution.
   - A hexbin plot (heatmap) for location concentration.
"""

# Import necessary libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# =============================================================================
# 1. DATA LOADING
# =============================================================================
# Define the file path for easier management and modification.
# Ensure this path matches your project's directory structure.
FILE_PATH = 'datasets/coffee-shop-yogyakarta-indonesia.csv'

try:
    # Load the dataset using a semicolon (;) as the delimiter.
    df_shops = pd.read_csv(FILE_PATH, delimiter=';')
    print(f"Dataset successfully loaded from: {FILE_PATH}")
except FileNotFoundError:
    print(f"Error: File not found at the specified path: {FILE_PATH}")
    print("Please ensure the folder and file names are correct.")
    exit()

# =============================================================================
# 2. DATA CLEANING
# =============================================================================
print("Starting data cleaning process...")

# Drop rows with missing values in critical columns (rating & coordinates).
# These columns are essential for the analysis, so records without them are dropped.
initial_rows = len(df_shops)
df_shops.dropna(subset=['RateStars', 'OrganizationLatitude', 'OrganizationLongitude'], inplace=True)
print(f"Handling missing values: {initial_rows - len(df_shops)} rows were dropped.")

# Standardize and convert data types for numerical columns read as text.
# The decimal comma (,) is replaced with a period (.) to allow float conversion.
for col in ['RateStars', 'OrganizationLatitude', 'OrganizationLongitude']:
    df_shops[col] = df_shops[col].astype(str).str.replace(',', '.', regex=False).astype(float)

print("Data cleaning and type conversion complete.")

# =============================================================================
# 3. EXPLORATORY DATA ANALYSIS & VISUALIZATION
# =============================================================================
print("Generating visualizations...")

# A. Geographical Distribution Scatter Plot
plt.figure(figsize=(10, 10))
sns.scatterplot(
    x='OrganizationLongitude',
    y='OrganizationLatitude',
    data=df_shops,
    hue='RateStars',      # Color-code points by their rating
    palette='viridis',    # Use a colorblind-friendly palette
    alpha=0.7,            # Set marker transparency
    s=50                  # Set marker size
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

# Calculate the frequency of each rating and sort by the rating value (index).
# This ensures the x-axis is ordered logically from lowest to highest rating.
rating_counts = df_shops['RateStars'].value_counts().sort_index()

# Create a bar plot showing the count of coffee shops for each unique rating.
ax = sns.countplot(
    x='RateStars',
    data=df_shops,
    palette='viridis',
    order=rating_counts.index  # Enforce the logical sorting
)

plt.title('Rating Distribution of Coffee Shops in Yogyakarta', fontsize=16, pad=20)
ax.set_xlabel('Star Rating', fontsize=12)
ax.set_ylabel('Number of Coffee Shops', fontsize=12)
ax.tick_params(axis='x', rotation=45)
ax.grid(axis='y', linestyle='--', alpha=0.6)

# Add data labels on top of each bar for clarity.
for p in ax.patches:
    ax.annotate(f'{int(p.get_height())}',
                (p.get_x() + p.get_width() / 2., p.get_height()),
                ha='center', va='center',
                xytext=(0, 9),
                textcoords='offset points')

plt.tight_layout()
plt.savefig('output/stage-1-distribution/rating_distribution.png')
print("Visualization 'rating_distribution.png' has been saved.")

# C. Location Concentration Heatmap
plt.figure(figsize=(12, 10))
plt.hexbin(
    x=df_shops['OrganizationLongitude'],
    y=df_shops['OrganizationLatitude'],
    gridsize=30,      # Adjust the number of bins to control aggregation level
    cmap='plasma'     # Use a distinct color map for the heatmap
)
plt.colorbar(label='Number of Coffee Shops per Area')
plt.title('Concentration Map of Coffee Shops in Yogyakarta', fontsize=16, pad=20)
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.tight_layout()
plt.savefig('output/stage-1-distribution/concentration_heatmap.png')
print("Visualization 'concentration_heatmap.png' has been saved.")

print("\nPhase 1 Analysis Complete. All visualizations have been saved.")