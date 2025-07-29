import unittest
from unittest.mock import patch, mock_open, MagicMock
import tempfile
import os
import logging

from jbussdieker.service import cli


class TestCLI(unittest.TestCase):
    def setUp(self):
        # Set up logging to capture output
        self.log_capture = []
        self.original_logging_info = logging.info
        self.original_logging_debug = logging.debug

        def mock_info(msg):
            self.log_capture.append(("INFO", msg))

        def mock_debug(msg):
            self.log_capture.append(("DEBUG", msg))

        logging.info = mock_info
        logging.debug = mock_debug

    def tearDown(self):
        # Restore original logging
        logging.info = self.original_logging_info
        logging.debug = self.original_logging_debug

    def test_get_systemd_unit_path(self):
        """Test that the systemd unit path is correct."""
        expected_path = "/etc/systemd/system/jbussdieker.service"
        self.assertEqual(cli.get_systemd_unit_path(), expected_path)

    def test_get_systemd_unit_content(self):
        """Test that the systemd unit content is properly formatted."""
        content = cli.get_systemd_unit_content()

        # Check that it contains all required sections
        self.assertIn("[Unit]", content)
        self.assertIn("[Service]", content)
        self.assertIn("[Install]", content)

        # Check for specific content
        self.assertIn("Description=jbussdieker service", content)
        self.assertIn("Type=simple", content)
        self.assertIn(
            "ExecStart=/home/jbussdieker/.local/bin/jbussdieker service", content
        )
        self.assertIn("WantedBy=multi-user.target", content)

    @patch("builtins.open", new_callable=mock_open)
    def test_install_systemd_service(self, mock_file):
        """Test that the systemd service installation writes the correct content."""
        cli.install_systemd_service()

        # Verify the file was opened with correct path
        mock_file.assert_called_once_with(
            "/etc/systemd/system/jbussdieker.service", "w"
        )

        # Verify the content was written
        mock_file().write.assert_called_once()
        written_content = mock_file().write.call_args[0][0]

        # Check that the written content matches our expected content
        expected_content = cli.get_systemd_unit_content()
        self.assertEqual(written_content, expected_content)

    @patch("time.sleep")
    def test_run_service(self, mock_sleep):
        """Test that the service runs and logs correctly."""
        # Clear log capture
        self.log_capture.clear()

        # Mock time.sleep to raise an exception after first call to break the infinite loop
        call_count = 0

        def mock_sleep_with_limit(seconds):
            nonlocal call_count
            if call_count == 0:
                call_count += 1
                # First call to sleep - let it pass
                pass
            else:
                # Second call to sleep - raise exception to break the loop
                raise StopIteration("Test complete")

        mock_sleep.side_effect = mock_sleep_with_limit

        # This should raise StopIteration after one iteration
        with self.assertRaises(StopIteration):
            cli.run_service()

        # Check that logging was called correctly
        # We expect 3 log messages: INFO "Starting service", DEBUG "running...", and another DEBUG "running..."
        self.assertEqual(len(self.log_capture), 3)
        self.assertEqual(self.log_capture[0], ("INFO", "Starting service"))
        self.assertEqual(self.log_capture[1], ("DEBUG", "running..."))
        self.assertEqual(self.log_capture[2], ("DEBUG", "running..."))

        # Verify time.sleep was called twice (once for each iteration)
        self.assertEqual(mock_sleep.call_count, 2)
        mock_sleep.assert_called_with(1)

    def test_main_with_install_command(self):
        """Test that main function calls install_systemd_service when command is 'install'."""
        args = MagicMock()
        args.command = "install"
        config = MagicMock()

        with patch.object(cli, "install_systemd_service") as mock_install:
            cli.main(args, config)
            mock_install.assert_called_once()

    def test_main_without_command(self):
        """Test that main function calls run_service when no command is specified."""
        args = MagicMock()
        args.command = None
        config = MagicMock()

        with patch.object(cli, "run_service") as mock_run:
            cli.main(args, config)
            mock_run.assert_called_once()

    def test_main_with_other_command(self):
        """Test that main function calls run_service when command is not 'install'."""
        args = MagicMock()
        args.command = "some_other_command"
        config = MagicMock()

        with patch.object(cli, "run_service") as mock_run:
            cli.main(args, config)
            mock_run.assert_called_once()

    def test_register_function(self):
        """Test that the register function sets up the parser correctly."""
        # Create a mock subparsers object
        mock_subparsers = MagicMock()
        mock_parser = MagicMock()
        mock_subparsers.add_parser.return_value = mock_parser

        # Call the register function
        cli.register(mock_subparsers)

        # Verify the parser was added with correct arguments
        mock_subparsers.add_parser.assert_called_once_with("service", help="Service")

        # Verify subparsers were created
        mock_parser.add_subparsers.assert_called_once_with(
            dest="command", help="Subcommands"
        )

        # Verify the install subcommand was added
        mock_subparsers_instance = mock_parser.add_subparsers.return_value
        mock_subparsers_instance.add_parser.assert_called_once_with(
            "install", help="Install the systemd service"
        )

        # Verify the default function was set
        mock_parser.set_defaults.assert_called_once_with(func=cli.main)


if __name__ == "__main__":
    unittest.main()
