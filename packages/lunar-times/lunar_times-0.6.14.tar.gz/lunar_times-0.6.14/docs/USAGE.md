# Usage Guide: Lunar Times

This guide provides detailed instructions and examples for using the Lunar Times application.

## Table of Contents
- [Basic Usage](#basic-usage)
- [Command-Line Options](#command-line-options)
- [Input Formats](#input-formats)
- [Output Interpretation](#output-interpretation)
- [Common Use Cases](#common-use-cases)
- [Error Handling](#error-handling)
- [Tips and Best Practices](#tips-and-best-practices)
- [Troubleshooting](#troubleshooting)

## Basic Usage

### Interactive Mode

Run the application without any flags to enter interactive mode:

```bash
make run
```

You'll be prompted to enter a city and state:

```
Enter the city: Austin
Enter the state: TX
```

### Debug Mode

Use debug mode to automatically use El Paso, TX as the location:

```bash
make run-debug
```

### Alternative: Direct Commands

You can also run the application directly:

```bash
# Interactive mode
lunar-times

# Debug mode
lunar-times -d

# Run the command-line tool
uv run lunar-times
uv run lunar-times -d
```

## Command-Line Options

| Make Target | Description | Example |
|-------------|-------------|---------|
| `make run` | Interactive mode - prompts for city and state | `make run` |
| `make run-debug` | Debug mode - uses El Paso, TX as default location | `make run-debug` |

### Alternative uv Commands

| Option | Description | Example |
|--------|-------------|---------|
| (none) | Interactive mode - prompts for city and state | `uv run lunar-times` |
| `-d` | Debug mode - uses El Paso, TX as default location | `uv run lunar-times -d` |

## Input Formats

### City Names
- **Capitalization**: Not case-sensitive (automatically converted to Title Case)
- **Spaces**: Supported for multi-word cities
- **Special Characters**: Basic punctuation supported

✅ **Valid Examples:**
```
austin          → Austin
new york        → New York
st. louis       → St. Louis
san francisco   → San Francisco
```

### State Names
- **Abbreviations**: 2-letter state codes (automatically converted to uppercase)
- **Full Names**: Full state names are supported
- **Capitalization**: Not case-sensitive

✅ **Valid Examples:**
```
tx      → TX
TX      → TX
texas   → TEXAS
Texas   → TEXAS
ca      → CA
california → CALIFORNIA
```

### Supported Locations
The application works with locations that can be found by OpenStreetMap's Nominatim service:
- All US states and territories
- Major cities worldwide
- International locations (city, country format may work)

## Output Interpretation

### Standard Output Format
```
# Moon rise/set times in (Timezone: America/Chicago -6.0) on 2024-01-15:
-  RISE: 10:45 PM
-  SET: 11:30 AM
```

### Output Components

1. **Header Line**: Contains timezone information and date
   - `Timezone: America/Chicago` - IANA timezone identifier
   - `-6.0` - UTC offset in hours
   - `2024-01-15` - Date in YYYY-MM-DD format

2. **Rise Time**: When the moon rises above the horizon
   - Format: 12-hour time with AM/PM
   - `N/A` if moon doesn't rise on this date

3. **Set Time**: When the moon sets below the horizon
   - Format: 12-hour time with AM/PM
   - `N/A` if moon doesn't set on this date

### Special Cases

**Moon doesn't rise/set on the given date:**
```
# Moon rise/set times in (Timezone: America/New_York -5.0) on 2024-01-15:
-  RISE: N/A
-  SET: 02:30 PM
```

**Debug mode indication:**
```
Running in debug mode. Defaulting to city (El Paso, TX)
# Moon rise/set times in (Timezone: America/Denver -6.0) on 2024-01-15:
-  RISE: 10:28 PM
-  SET: 08:52 AM
```

## Common Use Cases

### 1. Photography Planning
```bash
$ make run
Enter the city: Yosemite Valley
Enter the state: CA
# Moon rise/set times in (Timezone: America/Los_Angeles -8.0) on 2024-01-15:
-  RISE: 09:45 PM
-  SET: 10:15 AM
```

### 2. Astronomical Observation
```bash
$ make run
Enter the city: Flagstaff
Enter the state: AZ
# Moon rise/set times in (Timezone: America/Phoenix -7.0) on 2024-01-15:
-  RISE: 11:22 PM
-  SET: 09:30 AM
```

### 3. Outdoor Activities
```bash
$ make run
Enter the city: Moab
Enter the state: UT
# Moon rise/set times in (Timezone: America/Denver -6.0) on 2024-01-15:
-  RISE: 10:55 PM
-  SET: 08:45 AM
```

### 4. Quick Testing/Development
```bash
$ make run-debug
Running in debug mode. Defaulting to city (El Paso, TX)
# Moon rise/set times in (Timezone: America/Denver -6.0) on 2024-01-15:
-  RISE: 10:28 PM
-  SET: 08:52 AM
```

## Error Handling

### Location Not Found
```
$ make run
Enter the city: InvalidCity
Enter the state: XX
ValueError: Could not find coordinates for Invalidcity, XX
```

**Solutions:**
- Check spelling of city name
- Use common city names or nearby major cities
- Try different state abbreviations
- Use full state names instead of abbreviations

### Network Issues
```
ConnectionError: Failed to retrieve lunar data. Status code: 500
```

**Solutions:**
- Check internet connection
- Verify firewall settings allow HTTPS traffic
- Try again later (API may be temporarily unavailable)
- Test with debug mode to isolate the issue

### API Service Unavailable
```
ConnectionError: Failed to retrieve lunar data. Status code: 503
```

**Solutions:**
- The USNO Navy API may be under maintenance
- Try again in a few minutes
- Check the USNO website for service status

## Tips and Best Practices

### 1. Use Proper City Names
- Use commonly recognized city names
- For small towns, try nearby larger cities
- Use the city name as it appears on maps

### 2. State Abbreviations
- Use standard 2-letter state codes (TX, CA, NY)
- Both uppercase and lowercase work
- Full state names are also supported

### 3. Development and Testing
- Use debug mode (`-d`) for consistent testing
- Debug mode always uses El Paso, TX
- Great for development and automated testing

### 4. Timezone Awareness
- Output times are in local timezone for the location
- UTC offset is displayed for reference
- Consider daylight saving time changes

### 5. Performance Optimization
- Each run makes fresh API calls
- No caching between runs
- Typical response time: 1-3 seconds

## Troubleshooting

### Common Issues and Solutions

#### 1. ModuleNotFoundError
```
ModuleNotFoundError: No module named 'requests'
```
**Solution**: Install dependencies
```bash
make install
```

#### 2. Application Hangs
**Symptoms**: Application doesn't respond after entering location
**Solutions**:
- Check internet connection
- Verify firewall allows outbound HTTPS
- Try debug mode to test basic functionality

#### 3. Incorrect Timezone
**Symptoms**: Times seem wrong for the location
**Solutions**:
- Verify the location is correct
- Check if daylight saving time is in effect
- Compare with known astronomical sources

#### 4. City Not Found
**Symptoms**: "Could not find coordinates" error
**Solutions**:
- Try nearby larger cities
- Use alternative city names
- Check spelling and state abbreviation

### Testing Your Installation

#### Basic Functionality Test
```bash
make run-debug
```
Expected output should show El Paso, TX lunar data.

#### Interactive Mode Test
```bash
make run
# Enter: New York
# Enter: NY
```
Should show New York lunar data with Eastern timezone.

#### Error Handling Test
```bash
make run
# Enter: InvalidCity
# Enter: XX
```
Should display a clear error message.

## Advanced Usage

### Terminal Color Configuration

By default, the Makefile displays colored output for better readability. If you prefer no colors or encounter display issues:

```bash
# Disable colors for a single command
NO_COLOR=1 make run

# Disable colors permanently for your session
export NO_COLOR=1
make run
```

**When to use NO_COLOR:**
- Terminal doesn't support ANSI colors
- Screen readers or accessibility tools
- Plain text output for logging
- Personal preference

### Automated Testing
For development or automated testing:
```bash
# Test basic functionality
make run-debug

# Test with known good location (using direct uv for piping)
echo -e "Austin\nTX" | uv run lunar-times
```

### Integration with Other Tools
The application outputs to stdout, making it suitable for:
- Shell scripting
- Automated reports
- Integration with other applications

### Example Shell Script
```bash
#!/bin/bash
# Get lunar data for multiple cities
# Note: Using uv directly for piping input; make targets work best interactively
cities=("Austin:TX" "Denver:CO" "Seattle:WA")

for city_state in "${cities[@]}"; do
    IFS=':' read -r city state <<< "$city_state"
    echo "=== $city, $state ==="
    echo -e "$city\n$state" | uv run lunar-times
    echo
done
```

## Getting Help

### Debug Information
When reporting issues, include:
- Command used
- Input provided
- Error message (if any)
- Operating system
- Python version
- Internet connectivity status

### Support Resources
- Check [SETUP.md](SETUP.md) for installation issues
- Review [FAILURE.md](FAILURE.md) for known issues
- Verify [ARCH.md](ARCH.md) for technical details

### Testing Locations
For troubleshooting, try these known working locations:
- Austin, TX
- New York, NY
- Los Angeles, CA
- Chicago, IL
- Denver, CO

---

*For installation instructions, see [SETUP.md](SETUP.md)*
*For architecture details, see [ARCH.md](ARCH.md)*
*For project information, see [README.md](../README.md)* 