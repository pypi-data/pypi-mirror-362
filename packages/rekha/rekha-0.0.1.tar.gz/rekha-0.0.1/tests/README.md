# Rekha Test Suite

This directory contains a comprehensive test suite for the Rekha visualization library. The tests are organized into several modules, each focusing on different aspects of the library.

## Test Files

### 1. `test_basic.py` (Original Tests)
- **Purpose**: Basic functionality tests that were already present
- **Coverage**: 
  - Line plot creation
  - Scatter plot creation
  - Bar plot creation
  - Histogram creation
  - Dark mode functionality
  - Color grouping
  - Theme application
  - Subplot creation
- **Status**: ✅ All tests passing

### 2. `test_plots.py` (New Comprehensive Plot Tests)
- **Purpose**: Comprehensive testing of all plot types and features
- **Coverage**:
  - All plot functions (line, scatter, bar, histogram, heatmap, box, cdf)
  - Different data types (DataFrame, dict, arrays, lists)
  - Customization options (labels, titles, figsize, colors, themes)
  - Error handling and edge cases
  - Plot methods (save, show, update_layout, add_annotation)
- **Key Features Tested**:
  - Plot creation with various data sources
  - Color and size mapping
  - Custom labels and titles
  - Dark mode and theme integration
  - Grid and layout options
  - Grayscale friendly mode
  - Time series data handling

### 3. `test_theme.py` (Theme System Tests)
- **Purpose**: Testing the theme and color system
- **Coverage**:
  - Theme constants (REKHA_COLORS, REKHA_DARK_COLORS)
  - Color palette structure and validation
  - Theme application and persistence
  - Light vs dark mode differences
  - Theme integration with plots
- **Key Features Tested**:
  - Color hex format validation
  - Theme consistency across plots
  - Plot-level vs global theme settings
  - Font and grid settings
  - Color cycle configuration

### 4. `test_utils.py` (Utility Function Tests)
- **Purpose**: Testing utility functions for data processing and color management
- **Coverage**:
  - Data preparation and validation
  - Color palette generation
  - Color mapping to categories
  - Layout utilities (subplots)
- **Key Features Tested**:
  - Data preparation with various input types
  - Color palette generation for light/dark modes
  - Category color mapping with custom orders
  - Subplot creation and configuration
  - Error handling for invalid inputs

### 5. `test_base.py` (BasePlot Class Tests)
- **Purpose**: Testing the core BasePlot class functionality
- **Coverage**:
  - Class initialization with various parameters
  - Data preparation methods
  - Theme application
  - Plot customization methods
  - Error handling
- **Key Features Tested**:
  - Initialization with different data types
  - Custom font sizes and styling
  - Grid and layout settings
  - Color mapping and category ordering
  - Method availability and functionality

### 6. `test_integration.py` (Integration Tests)
- **Purpose**: Testing interactions between different components
- **Coverage**:
  - Cross-component integration
  - Data type compatibility
  - Performance testing
  - Error handling consistency
- **Key Features Tested**:
  - Theme consistency across plot types
  - Color mapping consistency
  - Large dataset handling
  - Memory management
  - Error recovery

## Running the Tests

### Prerequisites
```bash
pip install pytest matplotlib numpy pandas
```

### Running All Tests
```bash
pytest tests/ -v
```

### Running Specific Test Files
```bash
pytest tests/test_basic.py -v
pytest tests/test_plots.py -v
pytest tests/test_theme.py -v
pytest tests/test_utils.py -v
pytest tests/test_base.py -v
pytest tests/test_integration.py -v
```

### Running Specific Test Cases
```bash
pytest tests/test_basic.py::TestBasicPlots::test_line_plot_creation -v
```

## Test Configuration

### `conftest.py`
- Configures matplotlib for headless testing
- Suppresses warnings during test execution
- Sets up non-interactive plotting backend

### `.gitignore`
- Excludes test artifacts and temporary files
- Prevents generated plots from being committed

## Test Coverage Areas

1. **Plot Creation**: All plot types (line, scatter, bar, histogram, heatmap, box, cdf)
2. **Data Handling**: DataFrames, dictionaries, numpy arrays, lists
3. **Customization**: Themes, colors, labels, titles, sizing
4. **Error Handling**: Invalid inputs, missing data, malformed parameters
5. **Integration**: Component interactions, consistency checks
6. **Performance**: Large datasets, memory management

## Notes

- Some tests may fail if the actual implementation differs from expected behavior
- The test suite is designed to be comprehensive and may need adjustment based on the specific implementation details
- Tests use matplotlib's 'Agg' backend for headless execution
- All tests clean up matplotlib figures to prevent memory leaks

## Future Enhancements

- Add tests for additional plot types as they are implemented
- Include performance benchmarks
- Add tests for export functionality
- Include accessibility testing
- Add tests for interactive features 
