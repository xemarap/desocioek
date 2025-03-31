# DeSocioEk - Socioeconomic Index and Area Classification Methods

This document outlines the methodology used in the DeSocioEk package for calculating the socioeconomic index and classifying areas (DeSO - Demographic Statistical Areas) based on this index. The calculation methods follow the official methodology used by Statistics Sweden (SCB). However, the indicator "C. Percentage of People Unemployed (Ages 20-65)" is different from the SCB implementation on RegSO level, which uses "Percentage of People with Economic Assistance and/or Long-term Unemployment (Ages 20-65)". This is due to the lack of public availability of the exact same indicators on DeSO level.

## 1. Socioeconomic Index Calculation

The socioeconomic index is a composite measure based on three indicators that reflect different aspects of socioeconomic conditions. Each indicator is weighted equally, and the index is calculated as the average of these three indicators.

### 1.1 Indicators

The three indicators used in the calculation are:

#### A. Percentage of People with Pre-High School Education (Ages 25-65)

This indicator measures the percentage of residents aged 25-65 in a DeSO area whose highest level of education is pre-high school education ("förgymnasial utbildning"). This includes education of less than nine years or the equivalent of nine years of schooling. This data is fetched from Statistics Sweden using the table ID `TAB5956`.

#### B. Percentage of People with Low Economic Standard (All Ages)

This indicator measures the percentage of residents of all ages in a DeSO area who live in households with low economic standard. Low economic standard is defined as having a disposable income less than 60% of the national median disposable income. This data is fetched from Statistics Sweden using the table ID `TAB6436`.

#### C. Percentage of People Unemployed (Ages 20-65)

This indicator measures the percentage of residents aged 20-65 in a DeSO area who has the status unemployed. This data is fetched from Statistics Sweden using the table ID `TAB5551`.

### 1.2 Calculation Method

For each DeSO area, the socioeconomic index is calculated as follows:

```
Socioeconomic Index = (Indicator A + Indicator B + Indicator C) / 3
```

Where:
- Indicator A: Percentage with pre-high school education (0-100)
- Indicator B: Percentage with low economic standard (0-100)
- Indicator C: Percentage of people unemployed (0-100)

The index value is on a scale from 0 to 100, where higher values indicate worse socioeconomic conditions:
- 0 represents the best possible socioeconomic conditions
- 100 represents the worst possible socioeconomic conditions

## 2. Area Classification

After calculating the socioeconomic index, DeSO areas are classified into five area types based on how many standard deviations their index values are from the mean.

### 2.1 Classification Method

The package currently supports one method for classification. Later versions may add RegSO boundaries for consistency with RegSO index.

#### DeSO Statistics Method

This method calculates boundaries based on the distribution of socioeconomic index values across DeSO areas for the given year. This method uses the mean (μ) and standard deviation (σ) of the socioeconomic index values calculated specifically for DeSO areas.

### 2.2 Area Type Definitions

The five area types are defined as follows:

1. **Areas with Major Socioeconomic Challenges** (`Index ≥ μ + 2σ`)
   - These areas have socioeconomic conditions that are at least 2 standard deviations worse than the mean.

2. **Areas with Socioeconomic Challenges** (`μ + σ ≤ Index < μ + 2σ`)
   - These areas have socioeconomic conditions between 1 and 2 standard deviations worse than the mean.

3. **Socioeconomically Mixed Areas** (`μ ≤ Index < μ + σ`)
   - These areas have socioeconomic conditions between the mean and 1 standard deviation worse than the mean.

4. **Areas with Good Socioeconomic Conditions** (`μ - σ ≤ Index < μ`)
   - These areas have socioeconomic conditions between the mean and 1 standard deviation better than the mean.

5. **Areas with Very Good Socioeconomic Conditions** (`Index < μ - σ`)
   - These areas have socioeconomic conditions at least 1 standard deviation better than the mean.

## 3. Implementation in DeSocioEk

### 3.1 Data Retrieval

The package uses the [PxStatsPy](https://github.com/xemarap/pxstatspy) wrapper to access Statistics Sweden's API and fetch the necessary data for each indicator:

```python
def fetch_educational_level(self, years):
    """Fetch percentage of people with pre-high school education by DeSO"""
    table_id = "TAB5956"
    # ... API calls and data processing ...

def fetch_economic_standard(self, years):
    """Fetch percentage of people with low economic standard by DeSO"""
    table_id = "TAB6436"
    # ... API calls and data processing ...

def fetch_unemployment_rate(self, years):
    """Fetch unemployment rate data by DeSO"""
    table_id = "TAB5551"
    # ... API calls and data processing ...
```

### 3.2 Index Calculation

The socioeconomic index is calculated by combining the three indicators:

```python
def calculate_socioeconomic_index(self, years):
    """Calculate socioeconomic index for DeSO regions"""
    # Fetch all indicators
    education_df = self.fetch_educational_level(years)
    economic_df = self.fetch_economic_standard(years)
    unemployment_df = self.fetch_unemployment_rate(years)
    
    # Merge indicators and calculate index
    merged_df["socioeconomic_index"] = (
        merged_df["education_percentage"] + 
        merged_df["low_economic_standard_percentage"] + 
        merged_df["unemployment_rate_percentage"]
    ) / 3
    
    return merged_df
```

### 3.3 Area Classification

Areas are classified based on their index values and the selected classification method:

```python
def classify_area_types(self, index_df, method="deso_statistics"):
    """Classify DeSO regions into area types"""
    # For each year in the data
    for year, year_df in result_df.groupby("ar"):
        # Calculate statistics for the year
        mean = year_df["socioeconomic_index"].mean()
        std = year_df["socioeconomic_index"].std()
        
        # Apply classification function to each row
        result_df.loc[year_mask, "area_type"] = result_df.loc[year_mask].apply(
            lambda row: self._get_area_type(row["socioeconomic_index"], mean, std),
            axis=1
        )
    
    return result_df

def _get_area_type(self, index_value, mean, std):
    """Determine area type based on index value, mean, and standard deviation"""
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
```

## 4. Important Considerations

When analyzing socioeconomic index data and area classifications, consider the following:

1. **Relative Measure**: The area type classification is a relative measure that compares areas within a specific year. Changes in an area's classification over time may be due to changes in its own conditions or changes in other areas.

2. **Absolute Measure**: The socioeconomic index itself is an absolute measure that directly reflects the conditions within an area. For tracking changes in a specific area over time, the index value is more appropriate than the area type.

3. **Demographic Factors**: Different demographic compositions can affect the indicators. For example, areas with high concentrations of students might show higher rates of low economic standard due to students' typically lower incomes.

4. **Border Effects**: In municipalities near national borders, income earned in neighboring countries may not be fully captured in Swedish income statistics, potentially affecting the low economic standard indicator.

5. **Population Size**: DeSO areas vary in population size, which can affect the stability of the indicators and the resulting index, especially in areas with very small populations.

6. **Data Quality**: There may be data quality issues such as missing values or reporting delays that can affect the accuracy of the indicators and the resulting index.

## 5. References

This methodology is based on Statistics Sweden's approach to socioeconomic index calculation and area classification. For more information, refer to:

- Statistics Sweden (SCB) documentation on RegSO and DeSO classifications
- "Indelning i områdestyper efter socioekonomiskt index" (SCB, 2025-01-13)
- Government commission on integration data (Regeringsuppdraget Registerdata för integration)