from unittest import mock

from pytest_message.plugin import pytest_addoption


def test_pytest_addoption_adds_correct_command_line_arguments():
    """Test the correct list of options are available in the command line."""
    expected_argument_names = ('--notify',)
    mock_parser = mock.MagicMock()
    mock_notify_group = mock_parser.getgroup.return_value

    pytest_addoption(mock_parser)

    mock_parser.getgroup.assert_called_once_with("notifying")
    added_argument_names = []

    for args, kwargs in mock_notify_group.addoption.call_args_list:
        added_argument_names.append(args[0] if args else kwargs.get("name"))
    assert tuple(added_argument_names) == expected_argument_names
