# Testing Guide: Lunar Times

## Overview

The Lunar Times project maintains a comprehensive test suite designed to ensure reliability, maintainability, and correctness of all functionality. Our testing approach emphasizes mock-based testing to avoid external dependencies and ensure consistent, fast test execution.

## Test Suite Statistics

- **Total Test Methods**: 22 unit tests
- **Functions Covered**: 6 (100% function coverage)
- **Test Framework**: pytest with unittest.TestCase
- **Test Location**: `tests/test_cli.py`
- **Mocking Strategy**: unittest.mock for external dependencies
- **Coverage Tool**: pytest-cov for line and branch coverage

## Functions Under Test

| Function | Purpose | Test Methods | Coverage |
|----------|---------|--------------|----------|
| `find_latlong()` | Geocoding city/state to coordinates | 3 tests | ✅ Success, failure, input formatting |
| `get_citystate()` | User input handling for location | 3 tests | ✅ Debug mode, interactive, input cleaning |
| `get_timezone()` | Timezone resolution from coordinates | 2 tests | ✅ Success cases, edge cases |
| `find_moon_data()` | Parse API response for moon times | 5 tests | ✅ Complete data, missing rise/set, edge cases |
| `print_moon_data()` | Format and display results | 4 tests | ✅ Normal/debug modes, timezones, N/A values |
| `main()` | Application entry point | 3 tests | ✅ Success, API errors, geocoding errors |
| **Integration** | End-to-end workflows | 2 tests | ✅ Full workflow, real API structure |

## Coverage Goals

Our coverage targets:

- **Line Coverage**: ≥90% (currently targeting 95%+)
- **Function Coverage**: 100% (all functions tested)
- **Branch Coverage**: ≥85% (all major code paths)
- **Edge Case Coverage**: All error conditions tested

## Running Tests

### Basic Test Execution
```bash
# Run all tests
make test

# Run with verbose output
uv run --extra dev python -m pytest tests/ -v

# Run specific test
uv run --extra dev python -m pytest tests/test_cli.py::TestMoonData::test_find_latlong_success -v
```

### With Coverage Reporting
```bash
# Run tests with coverage
make test-coverage

# Generate detailed coverage report
make coverage-report

# View coverage in browser
make coverage-html
```

### Development Testing
```bash
# Quick development checks (lint + test)
make quick-check

# Full quality pipeline
make check

# CI pipeline (format + check + build)
make ci
```

## Testing Philosophy

### 1. **Mock External Dependencies**
- All HTTP requests are mocked to avoid network dependencies
- Geocoding services (Nominatim) are mocked with realistic responses
- USNO Navy API calls are mocked with sample data structures
- No actual external API calls during testing

### 2. **Comprehensive Error Coverage**
- Network failures and HTTP errors
- Invalid user input (bad city/state combinations)
- Malformed API responses
- Missing data in API responses
- Edge cases in timezone handling

### 3. **Reproducible Results**
- All tests use fixed, predictable data
- No reliance on current date/time or external services
- Consistent test execution across environments
- Embedded test data instead of external files

### 4. **Real-World Data Structures**
- Test data based on actual API responses
- Realistic coordinate and timezone combinations
- Authentic moon phase data patterns
- Production-like error scenarios

## Test Categories

### Unit Tests (`TestMoonData` class)

**Geocoding Tests** (`find_latlong`)
- `test_find_latlong_success`: Valid city/state lookup
- `test_find_latlong_not_found`: Invalid location handling
- `test_find_latlong_input_formatting`: Input normalization

**User Input Tests** (`get_citystate`)
- `test_get_citystate_debug_mode`: Debug mode default values
- `test_get_citystate_interactive_mode`: User input simulation
- `test_get_citystate_input_cleaning`: Input sanitization

**Timezone Tests** (`get_timezone`)
- `test_get_timezone_success`: Coordinate to timezone conversion
- `test_get_timezone_edge_cases`: Boundary conditions

**Data Parsing Tests** (`find_moon_data`)
- `test_find_moon_data_complete`: Full moonrise/moonset data
- `test_find_moon_data_missing_rise`: Missing moonrise handling
- `test_find_moon_data_missing_set`: Missing moonset handling
- `test_find_moon_data_empty_moondata`: Empty API response
- `test_find_moon_data_time_formatting`: Time format validation

**Output Tests** (`print_moon_data`)
- `test_print_moon_data_normal_mode`: Standard output format
- `test_print_moon_data_debug_mode`: Debug mode output
- `test_print_moon_data_positive_offset`: Positive timezone offsets
- `test_print_moon_data_na_values`: Missing data display

**Application Tests** (`main`)
- `test_main_success`: Complete successful workflow
- `test_main_api_error`: API failure handling
- `test_main_geocoding_error`: Geocoding failure handling

### Integration Tests (`TestIntegration` class)

**End-to-End Tests**
- `test_api_request_parameters`: API request formatting
- `test_full_workflow_with_real_data`: Complete workflow with realistic data

## Mock Strategy Details

### External API Mocking

**Nominatim Geocoding API**
```python
@patch('geopy.geocoders.Nominatim.geocode')
def test_find_latlong_success(self, mock_geocode):
    # Mock successful geocoding response
    mock_location = MagicMock()
    mock_location.latitude = 32.0809
    mock_location.longitude = -106.42
    mock_geocode.return_value = mock_location
```

**USNO Navy API**
```python
@patch('requests.get')
def test_main_success(self, mock_get):
    # Mock API response with realistic data structure
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "properties": {"data": {"moondata": [...]}}
    }
```

### Input/Output Mocking

**User Input Simulation**
```python
@patch('builtins.input')
def test_get_citystate_interactive_mode(self, mock_input):
    mock_input.side_effect = ['Austin', 'TX']
    # Test interactive input handling
```

**Output Capture**
```python
def captured_output(self):
    """Context manager to capture stdout for testing print functions."""
    new_out = io.StringIO()
    # ... capture and return output for verification
```

## Coverage Configuration

### Source Coverage
- **Source Directory**: `src/lunar_times/`
- **Excluded**: `tests/`, `*/__init__.py`
- **Minimum Coverage**: 90%
- **Report Formats**: Terminal, HTML

### Coverage Commands
```bash
# Basic coverage
pytest --cov=src/lunar_times

# With missing lines
pytest --cov=src/lunar_times --cov-report=term-missing

# Generate HTML report
pytest --cov=src/lunar_times --cov-report=html

# Combined terminal and HTML
make coverage-report
```

## Continuous Integration

### Pre-commit Checks
Our `make ci` pipeline runs:
1. Code formatting (black)
2. Linting (flake8) 
3. Type checking (mypy)
4. Full test suite
5. Coverage reporting
6. Build verification

### Quality Gates
- All tests must pass
- Coverage must meet minimum thresholds (90%+)
- No linting errors
- Type checking clean
- Documentation up to date

## Adding New Tests

### For New Functions
1. Add test class method following naming convention: `test_function_name_scenario`
2. Use appropriate mocking for external dependencies
3. Test both success and failure cases
4. Include edge cases and boundary conditions
5. Update this documentation

### Test Method Template
```python
def test_new_function_success(self):
    """Test new_function with valid input."""
    # Arrange
    test_input = "test_data"
    expected_output = "expected_result"
    
    # Act
    result = lunar_times.new_function(test_input)
    
    # Assert
    self.assertEqual(result, expected_output)
```

### Mocking Template
```python
@patch('module.external_dependency')
def test_function_with_external_call(self, mock_external):
    """Test function that calls external service."""
    # Arrange
    mock_external.return_value = "mocked_response"
    
    # Act & Assert
    result = lunar_times.function_name()
    self.assertEqual(result, "expected_result")
    mock_external.assert_called_once()
```

## Test Maintenance

### Regular Tasks
- Run full test suite before each commit
- Update test data when API responses change
- Review coverage reports for gaps
- Update mocks when external APIs change
- Keep documentation synchronized with tests

### Debugging Failed Tests
```bash
# Run single failing test with verbose output
uv run --extra dev python -m pytest tests/test_cli.py::TestClass::test_method -v -s

# Run with debugging
uv run --extra dev python -m pytest tests/test_cli.py::TestClass::test_method --pdb

# Show local variables on failure
uv run --extra dev python -m pytest tests/test_cli.py --tb=long

# Coverage for specific test
uv run --extra dev python -m pytest tests/test_cli.py::TestClass::test_method --cov=src/lunar_times --cov-report=term-missing
```

## Testing Best Practices

### Do's
- ✅ Mock all external dependencies
- ✅ Test both success and failure paths
- ✅ Use descriptive test method names
- ✅ Keep tests focused and atomic
- ✅ Use realistic test data
- ✅ Verify expected side effects
- ✅ Test edge cases and boundary conditions
- ✅ Maintain high coverage (>90%)

### Don'ts
- ❌ Don't make actual API calls in tests
- ❌ Don't rely on external files for test data
- ❌ Don't test multiple things in one test method
- ❌ Don't ignore failing tests
- ❌ Don't skip testing error conditions
- ❌ Don't hardcode environment-specific values
- ❌ Don't ignore coverage drops

## Performance Considerations

- **Fast Execution**: All tests run in <5 seconds
- **No Network Delays**: All external calls mocked
- **Isolated Tests**: No shared state between tests
- **Minimal Setup**: Simple test data initialization

## Coverage Analysis

### Expected Coverage Results
Based on our test suite, we expect:

- **find_latlong()**: 100% (all branches covered)
- **get_citystate()**: 95%+ (debug and interactive modes)
- **get_timezone()**: 100% (straightforward function)
- **find_moon_data()**: 100% (all data scenarios)
- **print_moon_data()**: 95%+ (all output formats)
- **main()**: 90%+ (main entry point with error handling)

### Coverage Gaps
Monitor these areas for potential coverage improvements:
- Exception handling in network edge cases
- Uncommon timezone edge cases
- Complex user input validation scenarios

## Future Testing Improvements

### Planned Enhancements
- [ ] Property-based testing with Hypothesis
- [ ] Performance benchmarking tests
- [ ] Integration tests with test containers
- [ ] Mutation testing for test quality assessment
- [ ] Automated test generation for new functions

### Coverage Expansion
- [ ] Branch coverage reporting
- [ ] Performance regression testing
- [ ] Security testing for input validation
- [ ] Memory usage testing

---

## Quick Reference

| Command | Purpose |
|---------|---------|
| `make test` | Run full test suite |
| `make test-coverage` | Run tests with coverage |
| `make coverage-report` | Generate detailed coverage report |
| `make coverage-html` | Open coverage report in browser |
| `make quick-check` | Run lint + test (fast development check) |
| `make ci` | Full CI pipeline (format + check + build) |

For detailed development workflows, see [docs/USAGE.md](USAGE.md). 