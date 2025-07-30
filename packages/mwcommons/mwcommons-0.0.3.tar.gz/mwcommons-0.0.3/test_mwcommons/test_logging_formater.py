import logging
import unittest
from io import StringIO
from unittest.mock import patch

from mwcommons.logging_formatter import CustomFormatter, setup_logger


class TestCustomFormatter(unittest.TestCase):
    def setUp(self):
        """Set up a logger with the CustomFormatter for testing."""
        self.logger = logging.getLogger("test_logger")
        self.logger.setLevel(logging.DEBUG)

        # Create a StringIO stream to capture log output
        self.log_stream = StringIO()
        self.stream_handler = logging.StreamHandler(self.log_stream)
        self.formatter = CustomFormatter()
        self.stream_handler.setFormatter(self.formatter)
        self.logger.addHandler(self.stream_handler)

    def tearDown(self):
        """Clean up by removing handlers."""
        self.logger.removeHandler(self.stream_handler)
        self.log_stream.close()

    def test_debug_format(self):
        self.logger.debug("Debug message")
        self.stream_handler.flush()
        log_output = self.log_stream.getvalue().strip()
        self.assertIn("\x1b[38;20m", log_output)  # Check for grey color
        self.assertIn("Debug message", log_output)

    def test_info_format(self):
        self.logger.info("Info message")
        self.stream_handler.flush()
        log_output = self.log_stream.getvalue().strip()
        self.assertIn("\x1b[38;20m", log_output)  # Check for grey color
        self.assertIn("Info message", log_output)

    def test_warning_format(self):
        self.logger.warning("Warning message")
        self.stream_handler.flush()
        log_output = self.log_stream.getvalue().strip()
        self.assertIn("\x1b[33;20m", log_output)  # Check for yellow color
        self.assertIn("Warning message", log_output)

    def test_error_format(self):
        self.logger.error("Error message")
        self.stream_handler.flush()
        log_output = self.log_stream.getvalue().strip()
        self.assertIn("\x1b[31;20m", log_output)  # Check for red color
        self.assertIn("Error message", log_output)

    def test_critical_format(self):
        self.logger.critical("Critical message")
        self.stream_handler.flush()
        log_output = self.log_stream.getvalue().strip()
        self.assertIn("\x1b[31;1m", log_output)  # Check for bold red color
        self.assertIn("Critical message", log_output)


class TestSetupLogger(unittest.TestCase):
    def test_setup_logger_default(self):
        """
        Test setup_logger with default logger and handler.
        """
        logger = setup_logger()
        self.assertIsInstance(logger, logging.Logger)
        self.assertEqual(len(logger.handlers), 1)
        self.assertIsInstance(logger.handlers[0], logging.StreamHandler)
        self.assertIsInstance(logger.handlers[0].formatter, CustomFormatter)

    def test_setup_logger_with_custom_logger(self):
        """
        Test setup_logger with a custom logger.
        """
        custom_logger = logging.getLogger("custom_logger")
        custom_logger.setLevel(logging.WARNING)
        logger = setup_logger(logger=custom_logger)
        self.assertEqual(logger.name, "custom_logger")
        self.assertEqual(logger.level, logging.WARNING)

    def test_setup_logger_with_custom_handler(self):
        """
        Test setup_logger with a custom handler.
        """
        custom_handler_mock = logging.NullHandler()
        logger = setup_logger(handler=custom_handler_mock)
        self.assertEqual(len(logger.handlers), 1)
        self.assertIsInstance(logger.handlers[0], logging.NullHandler)
        self.assertEqual(logger.handlers[0], custom_handler_mock)

    def test_setup_logger_with_both_logger_and_handler(self):
        """
        Test setup_logger with both a custom logger and a custom handler.
        """
        custom_logger = logging.getLogger("custom_logger_with_handler")
        custom_handler = logging.StreamHandler()
        logger = setup_logger(logger=custom_logger, handler=custom_handler)
        self.assertEqual(logger.name, "custom_logger_with_handler")
        self.assertEqual(len(logger.handlers), 1)
        self.assertIsInstance(logger.handlers[0], logging.StreamHandler)

    @patch("logging.StreamHandler.setFormatter")
    def test_setup_logger_formatter_called(self, mock_set_formatter):
        """
        Test that the formatter is set correctly on the handler.
        """
        setup_logger()
        mock_set_formatter.assert_called_once()

    def tearDown(self):
        """
        Clean up loggers after each test to avoid side effects.
        """
        root_logger = logging.getLogger()
        root_logger.handlers.clear()  # Remove all handlers from the root logger
        for logger_name in list(logging.Logger.manager.loggerDict.keys()):
            logger = logging.getLogger(logger_name)
            logger.handlers.clear()


if __name__ == "__main__":
    unittest.main()
