# Simple test script to try just one function
from desocioek.deso_analyzer import DesoAnalyzer

# Create analyzer instance
analyzer = DesoAnalyzer()

# Test with just one year to start
year = [2023]
print(f"Testing fetch_educational_level for {year}")

# Try to fetch educational level data
education_df = analyzer.fetch_educational_level(year)

if education_df is not None:
    print(f"Success! Fetched {len(education_df)} rows")
    print("\nSample data:")
    print(education_df.head())
    
    # Show data types and summary statistics
    print("\nData types:")
    print(education_df.dtypes)
    
    print("\nSummary statistics:")
    print(education_df.describe())
else:
    print("Failed to fetch education data")