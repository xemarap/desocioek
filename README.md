# DeSocioEk

A Python package for analyzing socioeconomic data at DeSO (Demographic Statistical Areas) level using the Statistics Sweden (SCB) API.

## Installation

### Prerequisites

Since pxstatspy is not yet available on PyPI, you'll need to install it from GitHub first:

```bash
# Install pxstatspy from GitHub
pip install git+https://github.com/xemarap/pxstatspy.git
```
After installing pxstatspy you can install desocioek from GitHub with:

```bash
# Install desocioek from GitHub
pip install git+https://github.com/xemarap/desocioek.git
```

### Development Installation

To install the package in development mode you can use this, but make sure pxstatspy is installed first:

```bash
# Clone the repository
git clone https://github.com/yourusername/desocioek.git
cd desocioek

# Install in development mode
pip install -e .
```

## Usage

### Basic Usage

```python
from desocioek.deso_analyzer import DesoAnalyzer

# Create an analyzer instance
analyzer = DesoAnalyzer(language="sv")

# Analyze data for the specified years
years = [2023]

# Calculate socioeconomic index
index_df = analyzer.calculate_socioeconomic_index(years)

# Classify areas by type
classified_df = analyzer.classify_area_types(index_df)

# Save results
classified_df.to_csv("deso_classifications.csv", index=False)
```

### Available Functions

- `fetch_educational_level(years)`: Fetch educational level data
- `fetch_economic_standard(years)`: Fetch economic standard data
- `fetch_unemployment_rate(years)`: Fetch unemployment rate data
- `calculate_socioeconomic_index(years)`: Calculate the socioeconomic index
- `classify_area_types(index_df)`: Classify areas into socioeconomic types

## Running Examples

```bash
# Run examples
python -m examples.run_deso_analyzer
```

## Running Tests

```bash
# Run all tests
python -m tests.run_all_tests

# Run a specific test
python -m tests.test_fetch_education
```

## License

[MIT](https://github.com/xemarap/desocioek/blob/main/LICENSE.md)