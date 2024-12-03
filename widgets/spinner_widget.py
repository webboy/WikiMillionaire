import sys
import threading
import time


class SpinnerWidget:
    """
    A class to display a spinning loader in the terminal.
    """

    def __init__(self):
        self._text = None
        self._spinner = ["|", "/", "-", "\\"]
        self._running = False
        self._thread = None

    def start(self, text: str = ""):
        """
        Start the spinner with optional text.
        :param text: Additional text to display alongside the spinner.
        """
        if self._running:
            return  # Prevent multiple spinners

        self._running = True
        self._text = text
        self._thread = threading.Thread(target=self._spin, daemon=True)
        self._thread.start()

    def _spin(self):
        """
        Private method to handle the spinner animation.
        """
        while self._running:
            for char in self._spinner:
                sys.stdout.write(f"\r{char} {self._text}")
                sys.stdout.flush()
                time.sleep(0.2)
        sys.stdout.write("\r")  # Clear the spinner line

    def stop(self):
        """
        Stop the spinner and clear the text from the terminal.
        """
        self._running = False
        if self._thread:
            self._thread.join()
        sys.stdout.write("\r\033[K")  # Clear the line
        sys.stdout.flush()