#!/usr/bin/env python3
"""
Test suite for SimpleSessionStore
Run with: python -m pytest test_session_store.py -v
"""

import pytest
import tempfile
import os
import shutil
from session_store import SimpleSessionStore

@pytest.fixture
def temp_store():
    """Create a temporary session store for testing."""
    temp_dir = tempfile.mkdtemp()
    store = SimpleSessionStore(temp_dir)
    yield store

    # Cleanup
    shutil.rmtree(temp_dir)

def test_create_session(temp_store):
    """Test creating a new session."""
    session_id = temp_store.create_session("test_user", {"topic": "test"})

    assert session_id is not None
    assert len(session_id) > 0

    # Verify session was created
    session_data = temp_store.get_session(session_id)
    assert session_data is not None
    assert session_data["user_id"] == "test_user"
    assert session_data["metadata"]["topic"] == "test"

def test_add_message(temp_store):
    """Test adding messages to a session."""
    session_id = temp_store.create_session("test_user")

    # Add a message
    success = temp_store.add_message(session_id, "user", "Hello world")
    assert success == True

    # Verify message was added
    messages = temp_store.get_session_messages(session_id)
    assert len(messages) == 1
    assert messages[0]["content"] == "Hello world"
    assert messages[0]["role"] == "user"

def test_get_session(temp_store):
    """Test retrieving a session."""
    session_id = temp_store.create_session("test_user")
    temp_store.add_message(session_id, "user", "Test message")

    session_data = temp_store.get_session(session_id)
    assert session_data is not None
    assert session_data["session_id"] == session_id
    assert len(session_data["messages"]) == 1

def test_list_sessions(temp_store):
    """Test listing all sessions."""
    # Create multiple sessions
    temp_store.create_session("user1")
    temp_store.create_session("user2")
    temp_store.create_session("user1")

    all_sessions = temp_store.list_sessions()
    assert len(all_sessions) == 3

    user1_sessions = temp_store.list_sessions("user1")
    assert len(user1_sessions) == 2

def test_delete_session(temp_store):
    """Test deleting a session."""
    session_id = temp_store.create_session("test_user")

    # Verify session exists
    assert temp_store.get_session(session_id) is not None

    # Delete session
    success = temp_store.delete_session(session_id)
    assert success == True

    # Verify session is gone
    assert temp_store.get_session(session_id) is None

def test_empty_message_validation(temp_store):
    """Test validation of empty messages."""
    session_id = temp_store.create_session("test_user")

    # Try to add empty message
    success = temp_store.add_message(session_id, "user", "")
    assert success == False

def test_nonexistent_session(temp_store):
    """Test operations on non-existent sessions."""
    fake_id = "fake-session-id"

    # Try to get non-existent session
    session = temp_store.get_session(fake_id)
    assert session is None

    # Try to add message to non-existent session
    success = temp_store.add_message(fake_id, "user", "Hello")
    assert success == False

def test_session_persistence(temp_store):
    """Test that sessions persist across store instances."""
    session_id = temp_store.create_session("test_user")
    temp_store.add_message(session_id, "user", "Persistent message")

    # Create new store instance pointing to same directory
    new_store = SimpleSessionStore(temp_store.storage_dir)

    # Verify session still exists
    session_data = new_store.get_session(session_id)
    assert session_data is not None
    assert len(session_data["messages"]) == 1
    assert session_data["messages"][0]["content"] == "Persistent message"

def test_get_stats(temp_store):
    """Test statistics functionality."""
    # Create some sessions with messages
    session1 = temp_store.create_session("user1")
    temp_store.add_message(session1, "user", "Message 1")
    temp_store.add_message(session1, "assistant", "Response 1")

    session2 = temp_store.create_session("user2")
    temp_store.add_message(session2, "user", "Message 2")

    stats = temp_store.get_stats()
    assert stats["total_sessions"] == 2
    assert stats["total_messages"] == 3
    assert stats["average_messages_per_session"] == 1.5

def test_message_metadata(temp_store):
    """Test adding messages with metadata."""
    session_id = temp_store.create_session("test_user")

    # Add message with metadata
    metadata = {"confidence": 0.95, "source": "user_input"}
    success = temp_store.add_message(session_id, "user", "Test message", metadata)
    assert success == True

    # Verify metadata was saved
    messages = temp_store.get_session_messages(session_id)
    assert len(messages) == 1
    assert messages[0]["metadata"]["confidence"] == 0.95
    assert messages[0]["metadata"]["source"] == "user_input"

def test_session_metadata(temp_store):
    """Test creating sessions with metadata."""
    metadata = {"topic": "Python Help", "priority": "high", "tags": ["beginner", "python"]}
    session_id = temp_store.create_session("test_user", metadata)

    session_data = temp_store.get_session(session_id)
    assert session_data["metadata"]["topic"] == "Python Help"
    assert session_data["metadata"]["priority"] == "high"
    assert "beginner" in session_data["metadata"]["tags"]

def test_multiple_messages(temp_store):
    """Test adding multiple messages to a session."""
    session_id = temp_store.create_session("test_user")

    # Add multiple messages
    messages = [
        ("user", "Hello"),
        ("assistant", "Hi there!"),
        ("user", "How are you?"),
        ("assistant", "I'm doing well, thanks!")
    ]

    for role, content in messages:
        success = temp_store.add_message(session_id, role, content)
        assert success == True

    # Verify all messages were added
    retrieved_messages = temp_store.get_session_messages(session_id)
    assert len(retrieved_messages) == 4

    # Verify message order and content
    for i, (role, content) in enumerate(messages):
        assert retrieved_messages[i]["role"] == role
        assert retrieved_messages[i]["content"] == content
        assert retrieved_messages[i]["id"] == i + 1

def test_session_cleanup(temp_store):
    """Test cleaning up old sessions."""
    # This test would require time manipulation to be comprehensive
    # For now, just test the method exists and doesn't crash
    removed_count = temp_store.cleanup_old_sessions(days_old=7)
    assert isinstance(removed_count, int)
    assert removed_count >= 0
