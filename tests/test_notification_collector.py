import pytest
from unittest.mock import patch, MagicMock
from clutchtimealerts.notifications.base import Notification
from clutchtimealerts.notification_collector import NotificationCollector


class MockNotification(Notification):
    COMMON_NAME = "mock_notification"


class MockPlugin(Notification):
    COMMON_NAME = "mock_plugin"


class NotANotification:
    pass


@pytest.fixture
def collector():
    """Fixture to create a fresh instance of NotificationCollector."""
    return NotificationCollector()


def make_fake_ep(name, plugin_class):
    ep = MagicMock()
    ep.name = name
    ep.load.return_value = plugin_class
    return ep


@pytest.fixture(autouse=True)
def disable_plugins(monkeypatch):
    monkeypatch.setattr(
        NotificationCollector, "_iter_plugin_entrypoints", lambda self: []
    )


def test_folder_path_module_path(collector):
    """Test the _folder_path_module_path method."""
    folder_path = "clutchtimealerts/notifications"
    expected_module_path = "clutchtimealerts.notifications"
    result = collector._folder_path_module_path(folder_path)
    assert result == expected_module_path


@patch("os.listdir")
@patch("importlib.import_module")
def test_collect_notifications_success(mock_import_module, mock_listdir, collector):
    """
    Test collect_notifications successfully collects Notification subclasses
    and populates dictionaries.
    """
    mock_listdir.return_value = ["mock_notification.py"]
    mock_module = MagicMock()
    mock_module.MockNotification = MockNotification
    mock_import_module.return_value = mock_module

    folder_path = "src/clutchtimealerts/notifications"
    collector.collect_notifications(folder_path)

    assert "MockNotification" in collector.classname_dict
    assert collector.classname_dict["MockNotification"] == MockNotification
    assert "mock_notification" in collector.common_name_dict
    assert collector.common_name_dict["mock_notification"] == MockNotification


@patch("os.listdir")
@patch("importlib.import_module")
def test_collect_notifications_import_error(
    mock_import_module, mock_listdir, collector
):
    """
    Test collect_notifications skips modules that cannot be imported.
    """
    mock_listdir.return_value = ["invalid_module.py"]
    mock_import_module.side_effect = ImportError("Mocked import error")

    folder_path = "src/clutchtimealerts/notifications"
    collector.collect_notifications(folder_path)

    assert len(collector.classname_dict) == 0
    assert len(collector.common_name_dict) == 0


@patch("os.listdir")
@patch("importlib.import_module")
def test_collect_notifications_no_notification_subclasses(
    mock_import_module, mock_listdir, collector
):
    """
    Test collect_notifications handles modules with no Notification subclasses.
    """
    mock_listdir.return_value = ["module_without_notifications.py"]
    mock_module = MagicMock()
    mock_import_module.return_value = mock_module

    folder_path = "src/clutchtimealerts/notifications"
    collector.collect_notifications(folder_path)

    assert len(collector.classname_dict) == 0
    assert len(collector.common_name_dict) == 0


@patch("os.listdir")
@patch("importlib.import_module")
def test_collect_notifications_skips_non_python_files(
    mock_import_module, mock_listdir, collector
):
    """
    Test collect_notifications skips non-Python files in the folder.
    """
    mock_listdir.return_value = ["README.md", "mock_notification.py"]
    mock_module = MagicMock()
    mock_module.MockNotification = MockNotification
    mock_import_module.return_value = mock_module

    folder_path = "src/clutchtimealerts/notifications"
    collector.collect_notifications(folder_path)

    assert "MockNotification" in collector.classname_dict
    assert collector.classname_dict["MockNotification"] == MockNotification
    assert "mock_notification" in collector.common_name_dict
    assert collector.common_name_dict["mock_notification"] == MockNotification

    assert len(collector.classname_dict) == 1
    assert len(collector.common_name_dict) == 1


def test_collect_plugin_notifications_success(monkeypatch):
    collector = NotificationCollector()

    # Enable plugin mocks JUST for this test
    monkeypatch.setattr(
        collector,
        "_iter_plugin_entrypoints",
        lambda: [make_fake_ep("mock_plugin", MockPlugin)],
    )

    collector._collect_plugin_notifications()

    assert "MockPlugin" in collector.classname_dict
    assert collector.common_name_dict["mock_plugin"] == MockPlugin


def test_collect_plugin_notifications_ignores_invalid(monkeypatch, collector):
    bad_ep = make_fake_ep("bad", NotANotification)
    monkeypatch.setattr(collector, "_iter_plugin_entrypoints", lambda: [bad_ep])

    collector._collect_plugin_notifications()

    assert collector.classname_dict == {}
    assert collector.common_name_dict == {}
