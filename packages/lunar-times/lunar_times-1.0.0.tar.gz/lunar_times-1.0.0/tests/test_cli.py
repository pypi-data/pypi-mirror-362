import unittest
from unittest.mock import patch, MagicMock
import sys
import io
from contextlib import contextmanager

# Import the module to test
from lunar_times import cli as moon_data


class TestMoonData(unittest.TestCase):
    """
    Test suite for the Lunar Times functions.

    This module contains comprehensive unit tests for all functionality in the
    lunar times calculator application.
    """

    def setUp(self):
        """Set up test fixtures before each test method."""
        # Sample API response for testing
        self.sample_api_response = {
            "apiversion": "4.0.1",
            "geometry": {"coordinates": [-106.44, 32.04], "type": "Point"},
            "properties": {
                "data": {
                    "moondata": [
                        {"phen": "Rise", "time": "22:58"},
                        {"phen": "Set", "time": "13:08"},
                        {"phen": "Upper Transit", "time": "05:33"},
                    ],
                    "tz": -6.0,
                    "year": 2024,
                    "month": 10,
                    "day": 22,
                }
            },
        }

    @contextmanager
    def captured_output(self):
        """Context manager to capture stdout for testing print functions."""
        new_out = io.StringIO()
        old_out = sys.stdout
        try:
            sys.stdout = new_out
            yield sys.stdout
        finally:
            sys.stdout = old_out

    def test_find_latlong_success(self):
        """Test find_latlong with valid city and state."""
        with patch("lunar_times.cli.Nominatim") as mock_nominatim:
            # Setup mock
            mock_geolocator = MagicMock()
            mock_nominatim.return_value = mock_geolocator

            mock_location = MagicMock()
            mock_location.latitude = 30.2672
            mock_location.longitude = -97.7431
            mock_geolocator.geocode.return_value = mock_location

            # Test
            lat, lng = moon_data.find_latlong("Austin", "TX")

            # Assertions
            self.assertEqual(lat, 30.2672)
            self.assertEqual(lng, -97.7431)
            mock_nominatim.assert_called_once_with(
                user_agent="lunar_times_app"
            )
            mock_geolocator.geocode.assert_called_once_with("Austin, TX")

    def test_find_latlong_not_found(self):
        """Test find_latlong with invalid city and state."""
        with patch("lunar_times.cli.Nominatim") as mock_nominatim:
            # Setup mock to return None (location not found)
            mock_geolocator = MagicMock()
            mock_nominatim.return_value = mock_geolocator
            mock_geolocator.geocode.return_value = None

            # Test and assert exception
            with self.assertRaises(ValueError) as context:
                moon_data.find_latlong("InvalidCity", "XX")

            self.assertIn(
                "Could not find coordinates for InvalidCity, XX",
                str(context.exception),
            )

    def test_find_latlong_input_formatting(self):
        """Test find_latlong handles various input formats correctly."""
        with patch("lunar_times.cli.Nominatim") as mock_nominatim:
            mock_geolocator = MagicMock()
            mock_nominatim.return_value = mock_geolocator

            mock_location = MagicMock()
            mock_location.latitude = 40.7128
            mock_location.longitude = -74.0060
            mock_geolocator.geocode.return_value = mock_location

            # Test with various formats
            test_cases = [
                ("new york", "ny"),
                ("New York", "NY"),
                ("NEW YORK", "NEW YORK"),
            ]

            for city, state in test_cases:
                lat, lng = moon_data.find_latlong(city, state)
                self.assertEqual(lat, 40.7128)
                self.assertEqual(lng, -74.0060)

    @patch("sys.argv", ["lunar_times.cli.py", "-d"])
    def test_get_citystate_debug_mode(self):
        """Test get_citystate in debug mode."""
        city, state = moon_data.get_citystate()
        self.assertEqual(city, "El Paso")
        self.assertEqual(state, "TX")

    @patch("sys.argv", ["lunar_times.cli.py"])
    @patch("builtins.input", side_effect=["austin", "tx"])
    def test_get_citystate_interactive_mode(self, mock_input):
        """Test get_citystate in interactive mode."""
        city, state = moon_data.get_citystate()
        self.assertEqual(city, "Austin")
        self.assertEqual(state, "TX")

    @patch("sys.argv", ["lunar_times.cli.py"])
    @patch("builtins.input", side_effect=[" new york ", " ny "])
    def test_get_citystate_input_cleaning(self, mock_input):
        """Test get_citystate properly cleans and formats input."""
        city, state = moon_data.get_citystate()
        self.assertEqual(city, "New York")
        self.assertEqual(state, "NY")

    def test_get_timezone_success(self):
        """Test get_timezone with valid coordinates."""
        with patch(
            "lunar_times.cli.TimezoneFinder"
        ) as mock_tz_finder_class, patch(
            "lunar_times.cli.pytz.timezone"
        ) as mock_pytz_timezone:

            # Setup mocks
            mock_tz_finder = MagicMock()
            mock_tz_finder_class.return_value = mock_tz_finder
            mock_tz_finder.timezone_at.return_value = "America/Chicago"

            mock_tz = MagicMock()
            mock_pytz_timezone.return_value = mock_tz
            mock_tz.utcoffset.return_value.total_seconds.return_value = (
                -21600
            )  # -6 hours

            # Test
            tz_label, offset = moon_data.get_timezone(30.2672, -97.7431)

            # Assertions
            self.assertEqual(tz_label, "America/Chicago")
            self.assertEqual(offset, -6.0)
            mock_tz_finder.timezone_at.assert_called_once_with(
                lng=-97.7431, lat=30.2672
            )

    def test_get_timezone_edge_cases(self):
        """Test get_timezone with edge case coordinates."""
        with patch(
            "lunar_times.cli.TimezoneFinder"
        ) as mock_tz_finder_class, patch(
            "lunar_times.cli.pytz.timezone"
        ) as mock_pytz_timezone:

            mock_tz_finder = MagicMock()
            mock_tz_finder_class.return_value = mock_tz_finder
            mock_tz_finder.timezone_at.return_value = "UTC"

            mock_tz = MagicMock()
            mock_pytz_timezone.return_value = mock_tz
            mock_tz.utcoffset.return_value.total_seconds.return_value = 0

            # Test with extreme coordinates
            tz_label, offset = moon_data.get_timezone(90.0, 180.0)
            self.assertEqual(tz_label, "UTC")
            self.assertEqual(offset, 0.0)

    def test_find_moon_data_complete(self):
        """Test find_moon_data with complete moonrise and moonset data."""
        moonrise, moonset = moon_data.find_moon_data(self.sample_api_response)
        self.assertEqual(moonrise, "10:58 PM")
        self.assertEqual(moonset, "01:08 PM")

    def test_find_moon_data_missing_rise(self):
        """Test find_moon_data when moonrise data is missing."""
        test_data = {
            "properties": {
                "data": {
                    "moondata": [
                        {"phen": "Set", "time": "13:08"},
                        {"phen": "Upper Transit", "time": "05:33"},
                    ]
                }
            }
        }

        moonrise, moonset = moon_data.find_moon_data(test_data)
        self.assertEqual(moonrise, "N/A")
        self.assertEqual(moonset, "01:08 PM")

    def test_find_moon_data_missing_set(self):
        """Test find_moon_data when moonset data is missing."""
        test_data = {
            "properties": {
                "data": {
                    "moondata": [
                        {"phen": "Rise", "time": "22:58"},
                        {"phen": "Upper Transit", "time": "05:33"},
                    ]
                }
            }
        }

        moonrise, moonset = moon_data.find_moon_data(test_data)
        self.assertEqual(moonrise, "10:58 PM")
        self.assertEqual(moonset, "N/A")

    def test_find_moon_data_empty_moondata(self):
        """Test find_moon_data with empty moondata array."""
        test_data = {"properties": {"data": {"moondata": []}}}

        moonrise, moonset = moon_data.find_moon_data(test_data)
        self.assertEqual(moonrise, "N/A")
        self.assertEqual(moonset, "N/A")

    def test_find_moon_data_time_formatting(self):
        """Test find_moon_data time format conversion."""
        test_cases = [
            ("00:00", "12:00 AM"),
            ("12:00", "12:00 PM"),
            ("01:30", "01:30 AM"),
            ("13:45", "01:45 PM"),
            ("23:59", "11:59 PM"),
        ]

        for input_time, expected_output in test_cases:
            test_data = {
                "properties": {
                    "data": {
                        "moondata": [{"phen": "Rise", "time": input_time}]
                    }
                }
            }

            moonrise, moonset = moon_data.find_moon_data(test_data)
            self.assertEqual(moonrise, expected_output)
            self.assertEqual(moonset, "N/A")

    @patch("sys.argv", ["lunar_times.cli.py"])
    def test_print_moon_data_normal_mode(self):
        """Test print_moon_data in normal mode."""
        with self.captured_output() as output:
            moon_data.print_moon_data(
                "2024-01-15", "America/Chicago", -6.0, "10:58 PM", "01:08 PM"
            )

        output_lines = output.getvalue().strip().split("\n")
        self.assertEqual(len(output_lines), 3)  # 1 header + 2 data lines
        self.assertIn("Timezone: America/Chicago -6.0", output_lines[0])
        self.assertIn("2024-01-15", output_lines[0])
        self.assertIn("RISE: 10:58 PM", output_lines[1])
        self.assertIn("SET: 01:08 PM", output_lines[2])

    @patch("sys.argv", ["lunar_times.cli.py", "-d"])
    def test_print_moon_data_debug_mode(self):
        """Test print_moon_data in debug mode."""
        with self.captured_output() as output:
            moon_data.print_moon_data(
                "2024-01-15", "America/Denver", -6.0, "10:28 PM", "08:52 AM"
            )

        output_lines = output.getvalue().strip().split("\n")
        self.assertEqual(len(output_lines), 4)  # debug + header + data
        self.assertIn("Running in debug mode", output_lines[0])
        self.assertIn("El Paso, TX", output_lines[0])

    def test_print_moon_data_positive_offset(self):
        """Test print_moon_data with positive timezone offset."""
        with self.captured_output() as output:
            moon_data.print_moon_data(
                "2024-01-15", "Europe/London", 1.0, "10:58 PM", "01:08 PM"
            )

        output_text = output.getvalue()
        self.assertIn("+1.0", output_text)

    def test_print_moon_data_na_values(self):
        """Test print_moon_data with N/A values."""
        with self.captured_output() as output:
            moon_data.print_moon_data(
                "2024-01-15", "America/Chicago", -6.0, "N/A", "N/A"
            )

        output_text = output.getvalue()
        self.assertIn("RISE: N/A", output_text)
        self.assertIn("SET: N/A", output_text)

    @patch("lunar_times.cli.get_citystate")
    @patch("lunar_times.cli.find_latlong")
    @patch("lunar_times.cli.get_timezone")
    @patch("lunar_times.cli.requests.get")
    @patch("lunar_times.cli.find_moon_data")
    @patch("lunar_times.cli.print_moon_data")
    @patch("lunar_times.cli.datetime.date")
    def test_main_success(
        self,
        mock_date,
        mock_print,
        mock_find_moon,
        mock_requests,
        mock_get_tz,
        mock_find_ll,
        mock_get_cs,
    ):
        """Test main function with successful execution."""
        # Setup mocks
        mock_get_cs.return_value = ("Austin", "TX")
        mock_find_ll.return_value = (30.2672, -97.7431)
        mock_get_tz.return_value = ("America/Chicago", -6.0)
        mock_date.today.return_value.strftime.return_value = "2024-01-15"

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = self.sample_api_response
        mock_requests.return_value = mock_response

        mock_find_moon.return_value = ("10:58 PM", "01:08 PM")

        # Test
        moon_data.main()

        # Assertions
        mock_get_cs.assert_called_once()
        mock_find_ll.assert_called_once_with("Austin", "TX")
        mock_get_tz.assert_called_once_with(30.2672, -97.7431)
        mock_requests.assert_called_once()
        mock_find_moon.assert_called_once_with(self.sample_api_response)
        mock_print.assert_called_once_with(
            "2024-01-15", "America/Chicago", -6.0, "10:58 PM", "01:08 PM"
        )

    @patch("lunar_times.cli.get_citystate")
    @patch("lunar_times.cli.find_latlong")
    @patch("lunar_times.cli.get_timezone")
    @patch("lunar_times.cli.requests.get")
    @patch("lunar_times.cli.datetime.date")
    def test_main_api_error(
        self, mock_date, mock_requests, mock_get_tz, mock_find_ll, mock_get_cs
    ):
        """Test main function with API error."""
        # Setup mocks
        mock_get_cs.return_value = ("Austin", "TX")
        mock_find_ll.return_value = (30.2672, -97.7431)
        mock_get_tz.return_value = ("America/Chicago", -6.0)
        mock_date.today.return_value.strftime.return_value = "2024-01-15"

        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_requests.return_value = mock_response

        # Test and assert exception
        with self.assertRaises(ConnectionError) as context:
            moon_data.main()

        self.assertIn(
            "Failed to retrieve moon data. Status code: 500",
            str(context.exception),
        )

    @patch("lunar_times.cli.get_citystate")
    @patch("lunar_times.cli.find_latlong")
    def test_main_geocoding_error(self, mock_find_ll, mock_get_cs):
        """Test main function with geocoding error."""
        # Setup mocks
        mock_get_cs.return_value = ("InvalidCity", "XX")
        mock_find_ll.side_effect = ValueError(
            "Could not find coordinates for InvalidCity, XX"
        )

        # Test and assert exception
        with self.assertRaises(ValueError) as context:
            moon_data.main()

        self.assertIn(
            "Could not find coordinates for InvalidCity, XX",
            str(context.exception),
        )

    def test_api_request_parameters(self):
        """Test that API request includes correct parameters."""
        with patch("lunar_times.cli.get_citystate") as mock_get_cs, patch(
            "lunar_times.cli.find_latlong"
        ) as mock_find_ll, patch(
            "lunar_times.cli.get_timezone"
        ) as mock_get_tz, patch(
            "lunar_times.cli.requests.get"
        ) as mock_requests, patch(
            "lunar_times.cli.find_moon_data"
        ) as mock_find_moon, patch(
            "lunar_times.cli.print_moon_data"
        ), patch(
            "lunar_times.cli.datetime.date"
        ) as mock_date:

            # Setup mocks
            mock_get_cs.return_value = ("Austin", "TX")
            mock_find_ll.return_value = (30.27, -97.74)
            mock_get_tz.return_value = ("America/Chicago", -6.0)
            mock_date.today.return_value.strftime.return_value = "2024-01-15"

            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = self.sample_api_response
            mock_requests.return_value = mock_response
            mock_find_moon.return_value = ("10:58 PM", "01:08 PM")

            # Test
            moon_data.main()

            # Check API call parameters
            expected_params = {
                "date": "2024-01-15",
                "coords": " 30.27, -97.74",
                "tz": "-6.0",
                "dst": "false",
            }

            mock_requests.assert_called_once_with(
                moon_data.url, params=expected_params
            )


class TestIntegration(unittest.TestCase):
    """
    Integration tests that test the application with minimal mocking.

    These tests use real API responses but mock the network calls to ensure
    reproducible test results.
    """

    def test_full_workflow_with_real_data(self):
        """Test complete workflow using real API response structure."""
        # Real API response structure for testing
        real_api_response = {
            "apiversion": "4.0.1",
            "geometry": {"coordinates": [-106.44, 32.04], "type": "Point"},
            "properties": {
                "data": {
                    "closestphase": {
                        "day": 24,
                        "month": 10,
                        "phase": "Last Quarter",
                        "time": "02:03",
                        "year": 2024,
                    },
                    "curphase": "Waning Gibbous",
                    "day": 22,
                    "day_of_week": "Tuesday",
                    "fracillum": "66%",
                    "moondata": [
                        {"phen": "Upper Transit", "time": "05:33"},
                        {"phen": "Set", "time": "13:08"},
                        {"phen": "Rise", "time": "22:58"},
                    ],
                    "tz": -6.0,
                    "year": 2024,
                }
            },
            "type": "Feature",
        }

        # Test moon data parsing with real response
        moonrise, moonset = moon_data.find_moon_data(real_api_response)
        self.assertEqual(moonrise, "10:58 PM")
        self.assertEqual(moonset, "01:08 PM")


if __name__ == "__main__":
    # Run tests with verbose output
    unittest.main(verbosity=2)
