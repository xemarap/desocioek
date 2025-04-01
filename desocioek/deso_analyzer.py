"""
DeSO Socioeconomic Analysis Package
Fetches data at DeSO level from Statistics Sweden (SCB) and performs
socioeconomic analysis similar to the RegSO level analysis.
"""

import pandas as pd
import numpy as np
from pxstatspy import PxAPI, PxAPIConfig, OutputFormat, OutputFormatParam

class DesoAnalyzer:
    """Class for fetching and analyzing DeSO level socioeconomic data"""
    
    def __init__(self, language="sv"):
        """
        Initialize the DesoAnalyzer with SCB API client
        
        Args:
            language: API language ("en" for English or "sv" for Swedish)
        """
        # Set up SCB API client
        config = PxAPIConfig(
            base_url="https://api.scb.se/OV0104/v2beta/api/v2",
            language=language
        )
        self.client = PxAPI(config)
        self.cache = {}  # Cache for storing fetched data
    
    def fetch_educational_level(self, years):
        """
        Fetch percentage of people with pre-high school education by DeSO
    
        Args:
            years: List of years to fetch data for
    
        Returns:
            DataFrame with educational level data as percentage (0-100)
        """
        table_id = "TAB5956"
    
        print(f"Fetching educational level data for years: {years}")
    
        # Convert years to strings if they are not already
        years_str = [str(year) for year in years]
    
        try:
            df = self.client.get_data_as_dataframe(
                table_id=table_id,
                value_codes={
                    "Tid": years_str,
                    "Region": ["*"],  # All regions
                    "UtbildningsNiva": ["*"],  # All education levels
                    "ContentsCode": ["000005MO"]
                },
                region_type="deso",  # Filter for DeSO regions only
                clean_colnames=True
            )
        
            # Filter for pre-high school education ("förgymnasial utbildning")
            print(f"Processing education data for {len(df)} rows")
        
            # Create a pivot table to calculate the percentage with pre-high school education
            # First, check if we need to filter the education level
            if 'utbildningsniva' in df.columns:
                # Filter for only pre-high school education rows
                pre_high_school = df[df['utbildningsniva'].str.contains('förgymnasial', case=False, na=False)]
            
                # Group by region and year
                regional_data = pre_high_school.groupby(['region_code', 'region', 'ar']).agg({
                    'befolkning': 'sum'  # Sum the population with pre-high school education
                }).reset_index()
            
                # Now get the total population by region and year
                total_pop = df.groupby(['region_code', 'region', 'ar']).agg({
                    'befolkning': 'sum'  # Sum all education levels
                }).reset_index()
            
                # Merge and calculate percentage
                merged = pd.merge(
                    regional_data,
                    total_pop,
                    on=['region_code', 'region', 'ar'],
                    suffixes=('_pre_high_school', '_total')
                )
            
                # Calculate percentage (0-100)
                merged['education_percentage'] = (merged['befolkning_pre_high_school'] / 
                                             merged['befolkning_total'] * 100)
            
                # Select only the needed columns
                result_df = merged[['region_code', 'region', 'ar', 'education_percentage']]
            
                # Cache the result
                self.cache["educational_level"] = result_df
            
                return result_df
            else:
                print("Warning: Expected column 'utbildningsniva' not found in data")
                print(f"Available columns: {df.columns.tolist()}")
                return None
        
        except Exception as e:
            print(f"Error fetching educational level data: {e}")
            import traceback
            print(traceback.format_exc())
            return None
   
    def fetch_economic_standard(self, years):
        """
        Fetch percentage of people with low economic standard by DeSO
    
        Args:
            years: List of years to fetch data for
    
        Returns:
            DataFrame with low economic standard data as percentage (0-100)
        """
        table_id = "TAB6436"
    
        print(f"Fetching economic standard data for years: {years}")
    
        # Convert years to strings if they are not already
        years_str = [str(year) for year in years]
    
        try:
            df = self.client.get_data_as_dataframe(
                table_id=table_id,
                value_codes={
                    "Tid": years_str,
                    "Region": ["*"],  # All regions
                    "Alder": ["tot"],  # Total age group
                    "ContentsCode": ["000007OQ"]
                },
                region_type="deso",  # Filter for DeSO regions only
                clean_colnames=True
            )
        
            print(f"Processing economic standard data for {len(df)} rows")
            print(f"Available columns in economic standard data: {df.columns.tolist()}")
        
            # This data should already be in percentage format (0-100), but we'll verify
            # and standardize the column names
        
            # Find the column that likely contains our percentage value
            percentage_cols = [col for col in df.columns if 'percentage' in col.lower() or 'andel' in col.lower()]
            value_cols = [col for col in df.columns if col not in ['region_code', 'region', 'ar', 'alder']]
        
            if percentage_cols:
                # Use the first percentage column we find
                percentage_col = percentage_cols[0]
            elif value_cols:
                # Use any remaining numeric column if we don't have an obvious percentage column
                percentage_col = value_cols[0]
            else:
                print("Warning: Could not identify a percentage column in economic standard data")
                return None
        
            # Create a standardized result dataframe
            result_df = df[['region_code', 'region', 'ar']].copy()
            result_df['low_economic_standard_percentage'] = df[percentage_col]
        
            # Verify the values are in percentage format (0-100)
            if result_df['low_economic_standard_percentage'].max() <= 1.0:
                # Convert from proportion to percentage
                print("Converting low economic standard from proportion to percentage")
                result_df['low_economic_standard_percentage'] *= 100
        
            # Cache the result
            self.cache["economic_standard"] = result_df
        
            return result_df
        
        except Exception as e:
            print(f"Error fetching economic standard data: {e}")
            import traceback
            print(traceback.format_exc())
            return None
    
    def fetch_unemployment_rate(self, years):
        """
        Fetch unemployment rate data by DeSO
    
        Args:
            years: List of years to fetch data for
    
        Returns:
            DataFrame with unemployment rate data as percentage (0-100)
        """
        table_id = "TAB5551"
    
        print(f"Fetching unemployment rate data for years: {years}")
    
        # Convert years to strings if they are not already
        years_str = [str(year) for year in years]
    
        try:
            df = self.client.get_data_as_dataframe(
                table_id=table_id,
                value_codes={
                    "Tid": years_str,
                    "Region": ["*"],  # All regions
                    "Kon": ["1+2"],  # Both men and women
                    "Alder": ["20-64"],  # Age group 20-64 years
                    "ContentsCode": ["0000079T", "0000077H"]
                },
                region_type="deso",  # Filter for DeSO regions only
                clean_colnames=True
            )
        
            print(f"Processing unemployment data for {len(df)} rows")
        
            # Check what columns are actually available
            print(f"Available columns in unemployment data: {df.columns.tolist()}")
        
            # Based on the sample data, we expect columns like:
            # region_code, region, kon, alder, ar, antal_arbetslosa, antal_sysselsatta_och_arbetslosa_arbetskraften
        
            # Pivot the data to calculate unemployment percentage
            # First, check if the expected columns exist
            if 'antal_arbetslosa' in df.columns and 'antal_sysselsatta_och_arbetslosa_arbetskraften' in df.columns:
                # Calculate unemployment rate as percentage (0-100)
                df['unemployment_rate_percentage'] = (df['antal_arbetslosa'] / 
                                                df['antal_sysselsatta_och_arbetslosa_arbetskraften'] * 100)
            
                # Group by region and year to handle any duplicates
                result_df = df.groupby(['region_code', 'region', 'ar']).agg({
                    'unemployment_rate_percentage': 'mean'  # Mean in case of multiple values
                }).reset_index()
            
                # Cache the result
                self.cache["unemployment_rate"] = result_df
            
                return result_df
            else:
                # Try to identify which columns might contain the needed data
                print("Warning: Expected columns not found in unemployment data")
            
                # Look for numeric columns that might contain the data
                numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
                print(f"Numeric columns: {numeric_cols}")
            
                return None
        
        except Exception as e:
            print(f"Error fetching unemployment rate data: {e}")
            import traceback
            print(traceback.format_exc())
            return None
    
    def fetch_all_indicators(self, years):
        """
        Fetch all three indicators required for socioeconomic index calculation
    
        Args:
            years: List of years to fetch data for
    
        Returns:
            Dictionary with DataFrames for each indicator
        """
        results = {}
    
        # Fetch all three indicators
        results["educational_level"] = self.fetch_educational_level(years)
        results["economic_standard"] = self.fetch_economic_standard(years)
        results["unemployment_rate"] = self.fetch_unemployment_rate(years)
    
        return results

    def calculate_socioeconomic_index(self, years):
        """
        Calculate socioeconomic index for DeSO regions based on the three indicators
    
        Args:
            years: List of years to calculate index for
    
        Returns:
            DataFrame with calculated socioeconomic index
        """
        # Fetch all indicators if not already in cache
        if not all(k in self.cache for k in ["educational_level", "economic_standard", "unemployment_rate"]):
            self.fetch_all_indicators(years)
        
        # Get DataFrames from cache
        education_df = self.cache.get("educational_level")
        economic_df = self.cache.get("economic_standard")
        unemployment_df = self.cache.get("unemployment_rate")
    
        # Check if all data is available
        if education_df is None or economic_df is None or unemployment_df is None:
            print("Error: Missing data for index calculation")
            return None
        
        # Prepare for merging - select only necessary columns
        education_df = education_df[["region_code", "region", "ar", "education_percentage"]]
        economic_df = economic_df[["region_code", "region", "ar", "low_economic_standard_percentage"]]
        unemployment_df = unemployment_df[["region_code", "region", "ar", "unemployment_rate_percentage"]]
    
        # Merge all three indicators on region_code and year
        merged_df = pd.merge(
            education_df, 
        economic_df, 
            on=["region_code", "region", "ar"],
            how="inner"
        )
    
        merged_df = pd.merge(
            merged_df,
            unemployment_df,
            on=["region_code", "region", "ar"],
            how="inner"
        )
    
        # Calculate socioeconomic index as the average of the three indicators
        merged_df["socioeconomic_index"] = (
            merged_df["education_percentage"] + 
            merged_df["low_economic_standard_percentage"] + 
            merged_df["unemployment_rate_percentage"]
        ) / 3

        # Rename region_code to deso and drop the duplicate region column
        merged_df = merged_df.rename(columns={"region_code": "deso"})
        merged_df = merged_df.drop(columns=["region"])
    
        return merged_df
    
    def classify_area_types(self, index_df, method="deso_statistics"):
        """
        Classify DeSO regions into area types based on socioeconomic index and
        add municipality and county information
    
        Args:
            index_df: DataFrame with calculated socioeconomic index
            method: Method to use for classification:
                - "regso_boundaries": Use the same boundaries as RegSO (future development)
                - "deso_statistics": Calculate boundaries based on DeSO statistics (default)
            
        Returns:
            DataFrame with area type classifications and geographic information
        """
        from desocioek.codes import get_kommun_name, get_lan_name
    
        result_df = index_df.copy()
    
        # Group by year to calculate statistics for each year
        for year, year_df in result_df.groupby("ar"):
            # Calculate statistics for the year
            mean = year_df["socioeconomic_index"].mean()
            std = year_df["socioeconomic_index"].std()
        
            # Get mask for this year
            year_mask = result_df["ar"] == year
        
            if method == "regso_boundaries":
                # For consistency with RegSO, use the RegSO boundaries
                # We would need to fetch the RegSO index statistics for this year
                # Here we're simulating it with hardcoded values based on the provided documents
                # In production, these should be fetched from the API
            
                # Example statistics from the document for 2022 (would need to be fetched for each year)
                regso_mean = 9.10  # From 2022 data in the document
                regso_std = 5.47   # From 2022 data in the document
            
                # Use RegSO statistics for boundaries
                result_df.loc[year_mask, "area_type"] = result_df.loc[year_mask].apply(
                    lambda row: self._get_area_type(row["socioeconomic_index"], regso_mean, regso_std),
                    axis=1
                )
            
            else:  # "deso_statistics"
                # Use DeSO statistics for boundaries
                result_df.loc[year_mask, "area_type"] = result_df.loc[year_mask].apply(
                    lambda row: self._get_area_type(row["socioeconomic_index"], mean, std),
                    axis=1
                )
            
        # Add description of area type
        result_df["area_type_description"] = result_df["area_type"].map({
            1: "Områden med stora socioekonomiska utmaningar",
            2: "Områden med socioekonomiska utmaningar",
            3: "Socioekonomiskt blandade områden",
            4: "Områden med goda socioekonomiska förutsättningar",
            5: "Områden med mycket goda socioekonomiska förutsättningar"
        })
    
        # Extract municipality and county codes from deso column
        # DeSO codes format: first 4 characters are municipality code, first 2 are county code
        if "deso" in result_df.columns:
            # Add kommun (municipality) name
            result_df["kommun"] = result_df["deso"].str[:4].apply(get_kommun_name)
        
            # Add län (county) name
            result_df["lan"] = result_df["deso"].str[:2].apply(get_lan_name)
    
        return result_df
    
    def _get_area_type(self, index_value, mean, std):
        """
        Determine area type based on index value, mean, and standard deviation
        
        Args:
            index_value: Socioeconomic index value
            mean: Mean of socioeconomic index
            std: Standard deviation of socioeconomic index
            
        Returns:
            Area type (1-5)
        """
        if index_value >= mean + 2*std:
            return 1  # Areas with major socioeconomic challenges
        elif index_value >= mean + std:
            return 2  # Areas with socioeconomic challenges
        elif index_value >= mean:
            return 3  # Socioeconomically mixed areas
        elif index_value >= mean - std:
            return 4  # Areas with good socioeconomic conditions
        else:
            return 5  # Areas with very good socioeconomic conditions