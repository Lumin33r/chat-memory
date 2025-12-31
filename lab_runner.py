#!/usr/bin/env python3
"""
Lab Runner for File-Based Session Storage System
This script demonstrates all the features of the SimpleSessionStore class.
"""

from session_store import SimpleSessionStore
import time

def print_separator(title):
    """Print a formatted separator with title."""
    print(f"\n{'='*60}")
    print(f" {title}")
    print(f"{'='*60}")

def print_session_summary(session):
    """Print a session summary in a formatted way."""
    print(f"\n🆔 Session ID: {session['session_id'][:8]}...")
    print(f"👤 User ID: {session.get('user_id', 'Anonymous')}")
    print(f"📅 Created: {session['created_at'][:19]}")
    print(f"🔄 Last Updated: {session['last_updated'][:19]}")
    print(f"💬 Messages: {session['message_count']}")

def print_message(message):
    """Print a message in a formatted way."""
    role_emoji = "👤" if message["role"] == "user" else "🤖"
    print(f"\n{role_emoji} {message['role'].upper()}: {message['content']}")
    print(f"   📅 {message['timestamp'][:19]}")

def main():
    """Main lab execution function."""
    print("🚀 Starting File-Based Session Storage Lab")

    # Initialize the session store
    store = SimpleSessionStore("session_storage")

    print_separator("1. Creating Sample Sessions")

    # Create some sample sessions
    session1 = store.create_session("user123", {"topic": "Python Help", "priority": "high"})
    session2 = store.create_session("user456", {"topic": "Docker Questions", "priority": "medium"})
    session3 = store.create_session("user123", {"topic": "General Chat", "priority": "low"})

    print_separator("2. Adding Messages to Sessions")

    # Add messages to session 1
    print(f"📝 Adding messages to session: {session1[:8]}...")
    store.add_message(session1, "user", "How do I create a virtual environment in Python?")
    store.add_message(session1, "assistant", "You can create a virtual environment using: python -m venv myenv")
    store.add_message(session1, "user", "How do I activate it?")
    store.add_message(session1, "assistant", "On Windows: myenv\\Scripts\\activate, On Unix: source myenv/bin/activate")

    # Add messages to session 2
    print(f"📝 Adding messages to session: {session2[:8]}...")
    store.add_message(session2, "user", "What is Docker?")
    store.add_message(session2, "assistant", "Docker is a platform for containerizing applications")
    store.add_message(session2, "user", "How do I run a container?")
    store.add_message(session2, "assistant", "Use: docker run image_name")

    # Add messages to session 3
    print(f"📝 Adding messages to session: {session3[:8]}...")
    store.add_message(session3, "user", "Hello!")
    store.add_message(session3, "assistant", "Hi there! How can I help you today?")

    print_separator("3. Retrieving Session Data")

    # Get complete session 1
    print(f"🔍 Retrieving complete session: {session1[:8]}...")
    session_data = store.get_session(session1)
    if session_data:
        print_session_summary(session_data)
        print("\n📨 Messages:")
        for message in session_data["messages"]:
            print_message(message)

    print_separator("4. Listing All Sessions")

    print("📋 All Sessions:")
    all_sessions = store.list_sessions()
    for session in all_sessions:
        print_session_summary(session)

    print("\n📋 Sessions for user123:")
    user_sessions = store.list_sessions("user123")
    for session in user_sessions:
        print_session_summary(session)

    print_separator("5. Testing Message Retrieval")

    # Get just messages from session 2
    print(f"📨 Messages from session: {session2[:8]}...")
    messages = store.get_session_messages(session2)
    for message in messages:
        print_message(message)

    print_separator("6. Testing Session Management")

    # Test session deletion
    print(f"🗑️  Deleting session: {session3[:8]}...")
    store.delete_session(session3)

    # List sessions again to confirm deletion
    print("\n📋 Sessions after deletion:")
    remaining_sessions = store.list_sessions()
    for session in remaining_sessions:
        print_session_summary(session)

    print_separator("7. Testing Error Handling")

    # Try to add message to non-existent session
    print("🧪 Testing error handling...")
    fake_session = "fake-session-id"
    store.add_message(fake_session, "user", "This should fail")

    # Try to get non-existent session
    fake_data = store.get_session(fake_session)
    print(f"Retrieved fake session: {fake_data}")

    print_separator("8. Final Statistics")

    stats = store.get_stats()
    print("📊 Session Store Statistics:")
    for key, value in stats.items():
        print(f"  {key}: {value}")

    print_separator("9. Testing Persistence")

    # Create a new store instance to test persistence
    print("🔄 Testing persistence by creating new store instance...")
    new_store = SimpleSessionStore("session_storage")

    # Try to retrieve existing session
    existing_session = new_store.get_session(session1)
    if existing_session:
        print(f"✅ Successfully retrieved persistent session: {session1[:8]}...")
        print(f"   Messages: {existing_session['message_count']}")
    else:
        print(f"❌ Failed to retrieve persistent session: {session1[:8]}...")

    print_separator("Lab Complete! 🎉")
    print("You've successfully implemented a file-based session storage system!")
    print("\nNext steps:")
    print("1. Try creating your own sessions with different metadata")
    print("2. Experiment with different message types and roles")
    print("3. Test the cleanup functionality with old sessions")
    print("4. Integrate this with your Flask application")
    print("5. Add Redis support as a stretch goal")

if __name__ == "__main__":
    main()
