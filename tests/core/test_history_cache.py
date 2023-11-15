from unittest.mock import patch
from commandeft.constants.consts import Models
from commandeft.core.history_cache import HistoryCache


def test_history_cache_append():
    model = Models.GPT_4
    history_cache = HistoryCache(model)

    # Mock the num_tokens_from_messages method to return a fixed value.
    with patch.object(history_cache, "num_tokens_from_messages", return_value=100):
        # Call the append method with a mock message.
        message = {"role": "user", "content": "This is a test message."}
        history_cache.append(message)

    # Check if the cache has the appended message.
    assert len(history_cache.cache) == 1
    assert history_cache.cache[0] == message

    # Check if the size has been updated correctly.
    assert history_cache.size == 100


def test_history_cache_clear():
    # Test the clear method.

    # Create a HistoryCache object with a mock model and cache.
    model = Models.GPT_3_5_TURBO
    history_cache = HistoryCache(model)
    history_cache.cache = [{"role": "user", "content": "Message 1"}, {"role": "assistant", "content": "Response 1"}]
    history_cache._HistoryCache__size = 200

    # Call the clear method.
    history_cache.clear()

    # Check if the cache is empty and size is reset.
    assert len(history_cache.cache) == 0
    assert history_cache.size == 0


def test_history_cache_num_tokens_from_messages():
    # Test the num_tokens_from_messages method.

    # Create a HistoryCache object with a mock model.
    model = Models.GPT_3_5_TURBO
    history_cache = HistoryCache(model)

    # Create a list of mock messages.
    messages = [
        {"role": "user", "content": "Message 1"},
        {"role": "assistant", "content": "Response 1", "name": "Assistant"},
        {"role": "user", "content": "Message 2"},
    ]

    # Call the num_tokens_from_messages method.
    num_tokens = history_cache.num_tokens_from_messages(messages)

    # Check if the number of tokens is calculated correctly.
    assert num_tokens == 26  # The expected number of tokens may vary based on the model.


def test_history_cache_is_empty():
    # Test the is_empty method when the cache is empty.

    # Create a HistoryCache object with a mock model.
    model = Models.GPT_3_5_TURBO
    history_cache = HistoryCache(model)

    # Check if the cache is empty.
    assert history_cache.is_empty() is True


def test_history_cache_is_not_empty():
    # Test the is_empty method when the cache is not empty.

    # Create a HistoryCache object with a mock model and cache.
    model = Models.GPT_3_5_TURBO
    history_cache = HistoryCache(model)
    history_cache.cache = [{"role": "user", "content": "Message 1"}]

    # Check if the cache is not empty.
    assert history_cache.is_empty() is False


def test_history_cache_get_cache():
    # Test the get_cache method.

    # Create a HistoryCache object with a mock model and cache.
    model = Models.GPT_3_5_TURBO
    history_cache = HistoryCache(model)
    history_cache.cache = [{"role": "user", "content": "Message 1"}, {"role": "assistant", "content": "Response 1"}]

    # Get the cache and check its content.
    cache = history_cache.get_cache()
    assert cache == [{"role": "user", "content": "Message 1"}, {"role": "assistant", "content": "Response 1"}]


def test_history_cache_max_tokens_reached():
    # Test the behavior when the maximum token size is reached.

    # Create a HistoryCache object with a mock model and cache.
    model = Models.GPT_3_5_TURBO
    history_cache = HistoryCache(model)

    # Mock the num_tokens_from_messages method to return a value below the maximum tokens.
    with patch.object(history_cache, "num_tokens_from_messages", return_value=1000):
        # Append a message to the cache.
        message = {"role": "user", "content": "This is a test message."}
        history_cache.append(message)

    # Check if the cache has the appended message.
    assert len(history_cache.cache) == 1
    assert history_cache.cache[0] == message

    # Check if the size has been updated correctly.
    assert history_cache.size == 1000

    # Mock the num_tokens_from_messages method to return a value that exceeds the maximum tokens.
    with patch.object(history_cache, "num_tokens_from_messages", return_value=5000):
        # Append a message to the cache, which should trigger reset.
        message = {"role": "user", "content": "Another test message."}
        history_cache.append(message)

    # Check if the cache is empty and size is reset.
    assert len(history_cache.cache) == 0
    assert history_cache.size == 0
