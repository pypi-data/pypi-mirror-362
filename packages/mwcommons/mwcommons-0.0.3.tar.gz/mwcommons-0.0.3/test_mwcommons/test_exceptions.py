import unittest
from unittest.mock import Mock, patch

from mwcommons.exceptions import (
    GeneralException,
    InputDataError,
    ParameterError,
    SeverityLevel,
    SolutionError,
)


class TestGeneralException(unittest.TestCase):
    def test_initialization(self):
        """Test initialization of GeneralException."""
        test_message = "Test message"
        exc = GeneralException(test_message, SeverityLevel.ERROR)
        self.assertEqual(exc.msn, test_message)
        self.assertEqual(exc.severity_level, SeverityLevel.ERROR)

    @patch("traceback.format_exc")
    @patch("logging.Logger.log")
    def test_log_without_traceback(self, mock_log: Mock, mock_traceback: Mock):
        """Test log method without traceback."""
        exc = GeneralException("Test log message", SeverityLevel.WARNING)
        exc.log()
        mock_log.assert_called_once_with(SeverityLevel.WARNING.value, "Test log message")
        mock_traceback.assert_not_called()

    @patch("traceback.format_exc", return_value="Mocked Traceback")
    @patch("logging.Logger.log")
    def test_log_with_traceback(self, mock_logger: Mock, mock_traceback: Mock):
        """Test log method with traceback."""
        msn = "Test log message with traceback"
        exc = GeneralException(msn, SeverityLevel.ERROR)
        exc.log(with_traceback=True)
        traceback_msn = "Mocked Traceback"
        mock_logger.assert_has_calls(
            mock_logger.call(SeverityLevel.ERROR.value, msn),
            mock_logger.call(SeverityLevel.ERROR.value, traceback_msn),
        )
        assert mock_logger.call_count == 2
        mock_traceback.assert_called_once()
        assert mock_traceback.return_value == traceback_msn

    def test_exception_raised_with_non_severity_level_type(self):
        """Test exception raised when severity_level is not an instance of SeverityLevel."""
        with self.assertRaises(TypeError):
            GeneralException("Test message", 0)

    def test_log_traceback_without_exception(self):
        """Test log method with traceback but no exception raised."""
        exc = GeneralException("No exception raised", SeverityLevel.INFO)
        with patch("traceback.format_exc", return_value=""):
            with self.assertLogs() as log:
                exc.log(with_traceback=True)
        self.assertIn("No exception raised", log.output[0])


class TestParameterError(unittest.TestCase):
    def test_inherits_general_exception(self):
        """Test ParameterError inherits GeneralException."""
        exc = ParameterError("Parameter error occurred")
        self.assertIsInstance(exc, GeneralException)
        self.assertIsInstance(exc, ParameterError)
        self.assertEqual(exc.msn, "Parameter error occurred")
        self.assertEqual(exc.severity_level, SeverityLevel.ERROR)


class TestInputDataError(unittest.TestCase):
    def test_inherits_general_exception(self):
        """Test InputDataError inherits GeneralException."""
        exc = InputDataError("Input data error occurred")
        self.assertIsInstance(exc, GeneralException)
        self.assertIsInstance(exc, InputDataError)
        self.assertEqual(exc.msn, "Input data error occurred")
        self.assertEqual(exc.severity_level, SeverityLevel.ERROR)


class TestSolutionError(unittest.TestCase):
    def test_inherits_general_exception(self):
        """Test SolutionError inherits GeneralException."""
        exc = SolutionError("Solution error occurred")
        self.assertIsInstance(exc, GeneralException)
        self.assertIsInstance(exc, SolutionError)
        self.assertEqual(exc.msn, "Solution error occurred")
        self.assertEqual(exc.severity_level, SeverityLevel.ERROR)


if __name__ == "__main__":
    unittest.main()
