"""
Phase 4: Final Recommendations and Conclusion

This script translates the quantitative scores from Phase 3 into actionable,
human-readable recommendations. It loads the final segmented data, identifies
the top-performing coffee shops within each key segment, and prints a
formatted summary of the findings.

Key Steps:
1.  Load the final scored and segmented dataset.
2.  Classify each coffee shop into one of four segments based on median scores.
3.  Identify and rank the top 3 coffee shops in the primary segments.
4.  Print the final recommendations to the console.
"""

# Import necessary libraries
import pandas as pd

# =============================================================================
# 1. LOAD FINAL SCORED DATA
# =============================================================================
SCORES_FILE_PATH = 'output/stage-3-scoring/coffee_shop_scores_final.csv'

try:
    df_scores = pd.read_csv(SCORES_FILE_PATH)
    print(f"Final scores loaded successfully from: {SCORES_FILE_PATH}")
except FileNotFoundError:
    print(f"Error: File not found at {SCORES_FILE_PATH}.")
    print("Please ensure the Phase 3 script has been run successfully.")
    exit()

# =============================================================================
# 2. CLASSIFY COFFEE SHOPS INTO SEGMENTS
# =============================================================================
# Calculate the median values to be used as robust quadrant dividers.
median_nugas = df_scores['Nugas_Score_Normalized'].median()
median_nongkrong = df_scores['Nongkrong_Score_Normalized'].median()

def assign_segment(row):
    """Assigns a segment label to a coffee shop based on its scores."""
    is_nugas_high = row['Nugas_Score_Normalized'] >= median_nugas
    is_nongkrong_high = row['Nongkrong_Score_Normalized'] >= median_nongkrong

    if is_nugas_high and is_nongkrong_high:
        return 'All-Rounder'
    elif is_nugas_high and not is_nongkrong_high:
        return 'Productivity Hub'
    elif not is_nugas_high and is_nongkrong_high:
        return 'Social Hotspot'
    else:
        return 'General Purpose'

# Apply the classification function to create the 'Segment' column.
df_scores['Segment'] = df_scores.apply(assign_segment, axis=1)
print("Coffee shops have been classified into segments.")

# =============================================================================
# 3. IDENTIFY TOP SHOPS IN EACH SEGMENT
# =============================================================================
def get_top_shops_in_segment(df, segment_name, top_n=3):
    """Filters, sorts by rating and review count, and returns the top N shops."""
    return df[df['Segment'] == segment_name].sort_values(
        by=['RateStars', 'ReviewsTotalCount'],
        ascending=[False, False]
    ).head(top_n)

# Extract the top performers for the key segments.
top_nugas_shops = get_top_shops_in_segment(df_scores, 'Productivity Hub')
top_nongkrong_shops = get_top_shops_in_segment(df_scores, 'Social Hotspot')
top_all_rounder_shops = get_top_shops_in_segment(df_scores, 'All-Rounder')

# =============================================================================
# 4. PRESENT FINAL RECOMMENDATIONS
# =============================================================================
# Note: The original dataset lacks a clean 'Name' column.
# 'OrganizationName' is an extract from the address and is used as a proxy.

print("\n\n" + "="*60)
print("      FINAL RECOMMENDATIONS: TOP COFFEE SHOPS IN YOGYAKARTA")
print("="*60 + "\n")

# --- Recommendations for "Productivity Hub" ---
print("✅ FOR PRODUCTIVITY & STUDY (Productivity Hubs)")
print("-" * 60)
print("The following coffee shops scored highest for a productive environment:\n")
for i, (index, row) in enumerate(top_nugas_shops.iterrows(), 1):
    print(f"  🏆 #{i}: {row['OrganizationName']}")
    print(f"     - Rating: {row['RateStars']} ⭐ | Reviews: {int(row['ReviewsTotalCount'])}")
    print(f"     - Productivity Score (Norm.): {row['Nugas_Score_Normalized']:.2f}\n")

# --- Recommendations for "Social Hotspot" ---
print("🤳 FOR SOCIALIZING & GATHERINGS (Social Hotspots)")
print("-" * 60)
print("The following coffee shops are best suited for social activities:\n")
for i, (index, row) in enumerate(top_nongkrong_shops.iterrows(), 1):
    print(f"  🏆 #{i}: {row['OrganizationName']}")
    print(f"     - Rating: {row['RateStars']} ⭐ | Reviews: {int(row['ReviewsTotalCount'])}")
    print(f"     - Social Score (Norm.): {row['Nongkrong_Score_Normalized']:.2f}\n")

# --- Recommendations for "All-Rounders" ---
print("🌟 FOR THE BEST OF BOTH WORLDS (All-Rounders)")
print("-" * 60)
print("These coffee shops are great for both productivity and socializing:\n")
for i, (index, row) in enumerate(top_all_rounder_shops.iterrows(), 1):
    print(f"  🏆 #{i}: {row['OrganizationName']}")
    print(f"     - Rating: {row['RateStars']} ⭐ | Reviews: {int(row['ReviewsTotalCount'])}")
    print(f"     - Productivity Score (Norm.): {row['Nugas_Score_Normalized']:.2f}")
    print(f"     - Social Score (Norm.): {row['Nongkrong_Score_Normalized']:.2f}\n")

print("="*60)
print("                          END OF ANALYSIS")
print("="*60)

# Save the fully classified dataframe for potential further use.
df_scores.to_csv('output/final_segmented_shops.csv', index=False)
print("\nComplete dataframe with segment classifications saved to 'final_segmented_shops.csv'")