# pylint: disable=W0621
import pytest
from dspacelogs import loganalyzer

# --- Sample data for tests ---
SAMPLE_LOG_DATA = """
127.0.0.1 - - [01/Jan/2025:10:00:00 +0100] "GET /home" 200 1024 "" "Chrome"
127.0.0.1 - - [01/Jan/2025:10:00:10 +0100] "GET /home" 200 1024 "" "Chrome"
127.0.0.1 - - [01/Jan/2025:10:00:20 +0100] "GET /home" 200 1024 "" "Chrome"
88.88.88.88 - - [01/Jan/2025:10:00:30 +0100] "GET /error" 404 512 "" "Firefox"
88.88.88.88 - - [01/Jan/2025:10:00:40 +0100] "GET /error" 404 512 "" "Firefox"
127.0.0.1 - - [01/Jan/2025:10:01:15 +0100] "GET /admin" 200 2048 "" "Chrome"
"""


@pytest.fixture
def log_file(tmp_path):
    """Creates a temporary log file for tests."""
    file_path = tmp_path / "test_access.log"
    file_path.write_text(SAMPLE_LOG_DATA)
    return str(file_path)


class TestLogAnalyzer:
    """A collection of tests for the LogAnalyzer class."""

    # C0116: Missing method docstring (Pylint warning) - docstring moved from function comment
    def test_data_loading(self, log_file):
        """Test 1: Verifies that data is loaded correctly."""
        analyzer = loganalyzer(log_file_path=log_file)
        assert analyzer.load_data() is True
        assert analyzer.valid
        assert len(analyzer) == 6

    def test_top_requests(self, log_file):
        """Test 2: Verifies that the most frequent request is found correctly."""
        analyzer = loganalyzer(log_file_path=log_file)
        analyzer.load_data()
        top_reqs = analyzer.get_top_requests(n=1)
        assert top_reqs.iloc[0]["Requested address"] == "GET /home"
        assert top_reqs.iloc[0]["Number of accesses"] == 3

    def test_suspicious_activity(self, log_file):
        """Test 3: Verifies that suspicious activity is detected correctly."""
        analyzer = loganalyzer(log_file_path=log_file, suspicious_threshold=2)
        analyzer.load_data()
        suspicious_df = analyzer.get_suspicious_activity()
        assert not suspicious_df.empty
        assert len(suspicious_df["ip"].unique()) == 1
        assert suspicious_df.iloc[0]["ip"] == "127.0.0.1"
