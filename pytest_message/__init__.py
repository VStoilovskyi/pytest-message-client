"""Package contains pytest notification plugin"""

from .slack_listener import SlackListener
from .notifier import notify


__all__ = ['SlackListener', 'notify']
