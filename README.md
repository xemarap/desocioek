# DeSocioEk

A Python package for generating a socioeconomic index and classifying areas at DeSO (Demographic Statistical Areas) level for all areas in Sweden. The package uses the [PxStatsPy](https://github.com/xemarap/pxstatspy) package to automatically fetch the relevant data with the Statistics Sweden (SCB) API.

## Installation

### Requirements

The DeSocioEk package requires:

- Python 3.7 or higher
- pandas
- numpy
- pxstatspy (not available on PyPI, must be installed from GitHub)

The package relies heavily on the PxStatsPy wrapper for accessing Statistics Sweden's API. Make sure to install PxStatsPy before installing DeSocioEk.

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
git clone https://github.com/xemarap/desocioek.git
cd desocioek

# Install in development mode
pip install -e .
```

## Usage

### Basic Usage

```python
from desocioek.deso_analyzer import DesoAnalyzer

# Create an analyzer instance
analyzer = DesoAnalyzer()

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

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

- Submit suggestions and report bugs
- Open a Pull Request
- Star the GitHub page

## License

This project is licensed under the [MIT License](https://github.com/xemarap/desocioek/blob/main/LICENSE.md)

## Acknowledgements

This project uses the following open source packages:
- [numpy](https://github.com/numpy)
- [pandas](https://github.com/pandas-dev/pandas)
- [pxstatspy](https://github.com/xemarap/pxstatspy)

The full license texts are available in the LICENSES directory.