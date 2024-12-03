import pytest
from widgets.spinner_widget import SpinnerWidget
from unittest.mock import patch, call
import time


@pytest.fixture
def spinner():
    """Fixture to initialize SpinnerWidget."""
    return SpinnerWidget()

@patch("sys.stdout.write")
def test_spinner_stops(mock_stdout, spinner):
    """Test that the spinner stops and clears the terminal line."""
    spinner.start("Processing")
    time.sleep(0.5)  # Allow the spinner to run for a bit
    spinner.stop()

    # Ensure the spinner stopped
    spinner._thread.join()  # Ensure the thread finishes
    assert not spinner._running

    # Check if the clear line code was written
    mock_stdout.assert_any_call("\r\033[K")


def test_multiple_starts(spinner):
    """Test that calling start multiple times does not create multiple spinners."""
    spinner.start("Task 1")
    spinner.start("Task 2")  # This should not overwrite the first spinner
    assert spinner._running is True
    spinner.stop()
    assert spinner._running is False


@patch("sys.stdout.write")
def test_spinner_clear_on_stop(mock_stdout, spinner):
    """Test that the spinner clears its output on stop."""
    spinner.start("Cleaning up")
    time.sleep(0.5)  # Allow the spinner to run
    spinner.stop()

    # Check if the spinner cleared the output
    mock_stdout.assert_any_call("\r\033[K")
