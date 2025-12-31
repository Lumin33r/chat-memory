import json
import os
import uuid
from datetime import datetime
from typing import List, Dict, Optional

class SimpleSessionStore:
    """
    A simple session storage system using JSON files for persistence.

    Features:
    - Create and manage conversation sessions
    - Add messages to sessions with timestamps
    - Retrieve complete conversation history
    - List all active sessions
    - Clean up old sessions
    """

    def __init__(self, storage_dir: str = "sessions"):
        """
        Initialize the session store.

        Args:
            storage_dir: Directory to store session files
        """
        self.storage_dir = storage_dir
        self._ensure_storage_dir()

    def _ensure_storage_dir(self):
        """Create storage directory if it doesn't exist."""
        if not os.path.exists(self.storage_dir):
            os.makedirs(self.storage_dir)
            print(f"✅ Created storage directory: {self.storage_dir}")

    def _get_session_file(self, session_id: str) -> str:
        """Get the file path for a session."""
        return os.path.join(self.storage_dir, f"{session_id}.json")

    def create_session(self, user_id: str = None, metadata: Dict = None) -> str:
        """
        Create a new session.

        Args:
            user_id: Optional user identifier
            metadata: Additional session metadata

        Returns:
            Session ID string
        """
        session_id = str(uuid.uuid4())
        session_data = {
            "session_id": session_id,
            "user_id": user_id,
            "created_at": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat(),
            "message_count": 0,
            "metadata": metadata or {},
            "messages": []
        }

        # Save the session
        self._save_session(session_id, session_data)
        print(f"✅ Created session: {session_id}")
        return session_id

    def add_message(self, session_id: str, role: str, content: str,
                   metadata: Dict = None) -> bool:
        """
        Add a message to a session.

        Args:
            session_id: Session to add message to
            role: Message role ('user' or 'assistant')
            content: Message content
            metadata: Additional message metadata

        Returns:
            True if successful, False otherwise
        """
        if not content.strip():
            print("❌ Message content cannot be empty")
            return False

        session_data = self.get_session(session_id)
        if not session_data:
            print(f"❌ Session {session_id} not found")
            return False

        message = {
            "id": len(session_data["messages"]) + 1,
            "role": role.strip().lower(),
            "content": content.strip(),
            "timestamp": datetime.now().isoformat(),
            "metadata": metadata or {}
        }

        session_data["messages"].append(message)
        session_data["message_count"] = len(session_data["messages"])
        session_data["last_updated"] = datetime.now().isoformat()

        # Save the updated session
        self._save_session(session_id, session_data)
        print(f"✅ Added message to session {session_id}")
        return True

    def get_session(self, session_id: str) -> Optional[Dict]:
        """
        Retrieve a complete session.

        Args:
            session_id: Session to retrieve

        Returns:
            Session data dictionary or None if not found
        """
        session_file = self._get_session_file(session_id)
        if not os.path.exists(session_file):
            return None

        try:
            with open(session_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"❌ Error loading session {session_id}: {e}")
            return None

    def get_session_messages(self, session_id: str) -> List[Dict]:
        """
        Get just the messages from a session.

        Args:
            session_id: Session to get messages from

        Returns:
            List of message dictionaries
        """
        session_data = self.get_session(session_id)
        if session_data:
            return session_data.get("messages", [])
        return []

    def list_sessions(self, user_id: str = None) -> List[Dict]:
        """
        List all sessions, optionally filtered by user.

        Args:
            user_id: Optional user filter

        Returns:
            List of session summaries
        """
        sessions = []

        for filename in os.listdir(self.storage_dir):
            if filename.endswith('.json'):
                session_id = filename[:-5]  # Remove .json extension
                session_data = self.get_session(session_id)

                if session_data:
                    # Apply user filter if specified
                    if user_id is None or session_data.get("user_id") == user_id:
                        summary = {
                            "session_id": session_data["session_id"],
                            "user_id": session_data.get("user_id"),
                            "created_at": session_data["created_at"],
                            "last_updated": session_data["last_updated"],
                            "message_count": session_data["message_count"]
                        }
                        sessions.append(summary)

        # Sort by last updated (most recent first)
        sessions.sort(key=lambda x: x["last_updated"], reverse=True)
        return sessions

    def delete_session(self, session_id: str) -> bool:
        """
        Delete a session and its file.

        Args:
            session_id: Session to delete

        Returns:
            True if successful, False otherwise
        """
        session_file = self._get_session_file(session_id)
        if os.path.exists(session_file):
            try:
                os.remove(session_file)
                print(f"✅ Deleted session: {session_id}")
                return True
            except OSError as e:
                print(f"❌ Error deleting session {session_id}: {e}")
                return False
        else:
            print(f"❌ Session {session_id} not found")
            return False

    def cleanup_old_sessions(self, days_old: int = 7) -> int:
        """
        Remove sessions older than specified days.

        Args:
            days_old: Remove sessions older than this many days

        Returns:
            Number of sessions removed
        """
        from datetime import timedelta

        cutoff_date = datetime.now() - timedelta(days=days_old)
        removed_count = 0

        for filename in os.listdir(self.storage_dir):
            if filename.endswith('.json'):
                session_id = filename[:-5]
                session_data = self.get_session(session_id)

                if session_data:
                    created_date = datetime.fromisoformat(session_data["created_at"])
                    if created_date < cutoff_date:
                        if self.delete_session(session_id):
                            removed_count += 1

        print(f"✅ Cleaned up {removed_count} old sessions")
        return removed_count

    def _save_session(self, session_id: str, session_data: Dict):
        """Save session data to file."""
        session_file = self._get_session_file(session_id)
        try:
            with open(session_file, 'w', encoding='utf-8') as f:
                json.dump(session_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"❌ Error saving session {session_id}: {e}")

    def get_stats(self) -> Dict:
        """Get statistics about all sessions."""
        sessions = self.list_sessions()
        total_messages = sum(s["message_count"] for s in sessions)

        return {
            "total_sessions": len(sessions),
            "total_messages": total_messages,
            "storage_directory": self.storage_dir,
            "average_messages_per_session": total_messages / len(sessions) if sessions else 0
        }
