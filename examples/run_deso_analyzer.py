# Import the DesoAnalyzer class
from desocioek.deso_analyzer import DesoAnalyzer

# Create an analyzer instance
# You can use either "sv" (Swedish) or "en" (English) for the language
analyzer = DesoAnalyzer(language="sv")

# Define the years you want to analyze
years = [2023]

#---------------RUN ANALYSIS-------------------
# Get data and calculate the socioeconomic index
print("\n--- Calculating Socioeconomic Index ---")
index_df = analyzer.calculate_socioeconomic_index(years)
if index_df is not None:
    print(f"Calculated socioeconomic index for {len(index_df)} areas")
    print(index_df.head())


# Classify areas by socioeconomic type
print("\n--- Classifying Areas by Type ---")
if index_df is not None:
    classified_df = analyzer.classify_area_types(index_df)
    print(f"Classified {len(classified_df)} areas into socioeconomic types")
    
    # Display sample data with new columns
    print("\nSample data with municipality and county information:")
    print(classified_df[['deso', 'kommun', 'lan', 'area_type', 'area_type_description', 'socioeconomic_index']].head())
    
    # Get summary statistics by area type
    print("\nSummary by area type:")
    area_type_summary = classified_df.groupby(['ar', 'area_type']).agg({
        'deso': 'count',  # Changed from region_code to deso
        'socioeconomic_index': ['mean', 'min', 'max']
    })
    print(area_type_summary)
    
    # Save the classified results
    classified_file = "deso_area_classifications.csv"
    classified_df.to_csv(classified_file, index=False)
    print(f"\nClassification results saved to {classified_file}")
