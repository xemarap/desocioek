import pandas as pd
from desocioek.deso_analyzer import DesoAnalyzer

# Create an analyzer instance
analyzer = DesoAnalyzer()

# Define the years to analyze
years_to_analyze = [2020, 2021, 2022, 2023]

# Initialize a list to hold all the DataFrames
all_classified_dfs = []

# Process each year individually
for year in years_to_analyze:
    print(f"\n{'='*50}")
    print(f"Processing year: {year}")
    print(f"{'='*50}")
    
    try:
        # Clear the analyzer's cache to ensure we're fetching fresh data
        analyzer.cache = {}
        
        # Convert year to string as expected by the API
        year_str = str(year)
        
        # Directly modify how we call the fetch methods to ensure we get data for the specific year
        print(f"Fetching data for year {year}...")
        
        # Create a new analyzer instance for each year to avoid any caching issues
        year_analyzer = DesoAnalyzer()
        
        # Calculate the socioeconomic index for just this one year
        print(f"Calculating socioeconomic index for {year}...")
        index_df = year_analyzer.calculate_socioeconomic_index([year])
        
        if index_df is not None and not index_df.empty:
            # Verify the data contains the correct year
            if 'ar' in index_df.columns:
                actual_years = sorted(index_df['ar'].unique())
                print(f"Index data contains years: {actual_years}")
                
                # Force the year if needed (shouldn't be necessary, but just in case)
                if str(year) not in [str(y) for y in actual_years]:
                    print(f"Warning: Forcing year to {year} as it wasn't found in data")
                    index_df['ar'] = year
            
            # Display summary of the index data
            print(f"Socioeconomic index summary statistics:")
            print(index_df['socioeconomic_index'].describe())
            
            # Classify areas
            print(f"Classifying areas for {year}...")
            classified_df = year_analyzer.classify_area_types(index_df)
            
            if classified_df is not None and not classified_df.empty:
                print(f"Successfully classified {len(classified_df)} areas for year {year}")
                
                # Print distribution of area types to verify the data looks reasonable
                area_type_counts = classified_df.groupby('area_type').size().reset_index(name='count')
                print("Area type distribution:")
                print(area_type_counts)
                
                # Save individual year results
                year_filename = f"deso_classifications_{year}.csv"
                classified_df.to_csv(year_filename, index=False)
                print(f"Saved results for {year} to {year_filename}")
                
                # Add to our list of all DataFrames
                all_classified_dfs.append(classified_df)
            else:
                print(f"Warning: Could not classify areas for year {year}")
        else:
            print(f"Warning: Could not calculate index for year {year}")
    
    except Exception as e:
        print(f"Error processing year {year}: {e}")
        import traceback
        traceback.print_exc()

# Merge all DataFrames
if all_classified_dfs:
    # Concatenate all yearly DataFrames
    merged_df = pd.concat(all_classified_dfs, ignore_index=True)
    
    print(f"\n{'='*50}")
    print(f"Merged results summary:")
    print(f"{'='*50}")
    print(f"Total records: {len(merged_df)}")
    
    # Show distribution by year
    year_counts = merged_df.groupby('ar').size().reset_index(name='count')
    print("\nRecords by year:")
    print(year_counts)
    
    # Show area type distribution by year
    area_type_by_year = merged_df.groupby(['ar', 'area_type']).size().reset_index(name='count')
    print("\nArea type distribution by year:")
    print(area_type_by_year)
    
    # Compare index values for the same areas across years
    print("\nComparing index values across years for a sample DESO area:")
    if len(merged_df['ar'].unique()) > 1:
        # Get a sample area that appears in all years
        sample_areas = merged_df.groupby('deso').filter(lambda x: len(x['ar'].unique()) >= len(years_to_analyze))['deso'].unique()
        
        if len(sample_areas) > 0:
            sample_area = sample_areas[0]
            sample_data = merged_df[merged_df['deso'] == sample_area].sort_values('ar')
            print(f"Area {sample_area} across years:")
            print(sample_data[['deso', 'ar', 'socioeconomic_index', 'area_type']])
    
    # Save merged results
    merged_filename = "deso_classifications_all_years.csv"
    merged_df.to_csv(merged_filename, index=False)
    print(f"\nSaved merged results to {merged_filename}")