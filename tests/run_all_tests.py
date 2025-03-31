"""
Script to run all test functions to verify the functionality
of the DesoAnalyzer class.
"""

from desocioek.deso_analyzer import DesoAnalyzer

def test_educational_level():
    """Test the fetch_educational_level function"""
    print("\n----- TESTING EDUCATIONAL LEVEL DATA -----")
    analyzer = DesoAnalyzer(language="sv")
    year = [2023]
    df = analyzer.fetch_educational_level(year)
    
    if df is not None:
        print(f"✓ Success! Fetched {len(df)} rows of educational level data")
        print("Sample data:")
        print(df.head(2))
        return True
    else:
        print("✗ Failed to fetch educational level data")
        return False

def test_economic_standard():
    """Test the fetch_economic_standard function"""
    print("\n----- TESTING ECONOMIC STANDARD DATA -----")
    analyzer = DesoAnalyzer(language="sv")
    year = [2023]
    df = analyzer.fetch_economic_standard(year)
    
    if df is not None:
        print(f"✓ Success! Fetched {len(df)} rows of economic standard data")
        print("Sample data:")
        print(df.head(2))
        return True
    else:
        print("✗ Failed to fetch economic standard data")
        return False

def test_unemployment_rate():
    """Test the fetch_unemployment_rate function"""
    print("\n----- TESTING UNEMPLOYMENT RATE DATA -----")
    analyzer = DesoAnalyzer(language="sv")
    year = [2023]
    df = analyzer.fetch_unemployment_rate(year)
    
    if df is not None:
        print(f"✓ Success! Fetched {len(df)} rows of unemployment rate data")
        print("Sample data:")
        print(df.head(2))
        return True
    else:
        print("✗ Failed to fetch unemployment rate data")
        return False

def test_index_calculation():
    """Test the calculate_socioeconomic_index function"""
    print("\n----- TESTING INDEX CALCULATION -----")
    analyzer = DesoAnalyzer(language="sv")
    year = [2023]
    df = analyzer.calculate_socioeconomic_index(year)
    
    if df is not None:
        print(f"✓ Success! Calculated index for {len(df)} areas")
        print("Sample data:")
        print(df.head(2))
        return True
    else:
        print("✗ Failed to calculate socioeconomic index")
        return False

def test_area_classification():
    """Test the classify_area_types function"""
    print("\n----- TESTING AREA CLASSIFICATION -----")
    analyzer = DesoAnalyzer(language="sv")
    year = [2023]
    index_df = analyzer.calculate_socioeconomic_index(year)
    
    if index_df is not None:
        classified_df = analyzer.classify_area_types(index_df)
        if classified_df is not None:
            print(f"✓ Success! Classified {len(classified_df)} areas")
            print("Sample data:")
            print(classified_df.head(2))
            
            # Print distribution of area types
            type_counts = classified_df.groupby(['ar', 'area_type']).size().reset_index(name='count')
            print("\nDistribution of area types:")
            print(type_counts)
            return True
    
    print("✗ Failed to classify areas by type")
    return False

if __name__ == "__main__":
    print("Running all DesoAnalyzer tests...")
    
    # Run all tests
    tests = [
        test_educational_level,
        test_economic_standard,
        test_unemployment_rate,
        test_index_calculation,
        test_area_classification
    ]
    
    # Track test results
    results = {}
    
    for test_func in tests:
        test_name = test_func.__name__
        result = test_func()
        results[test_name] = result
    
    # Print summary
    print("\n----- TEST SUMMARY -----")
    passed = sum(1 for result in results.values() if result)
    failed = len(results) - passed
    
    print(f"Tests passed: {passed}/{len(results)}")
    
    if failed > 0:
        print("Failed tests:")
        for name, result in results.items():
            if not result:
                print(f"  - {name}")
    else:
        print("All tests passed successfully!")