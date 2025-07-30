import random
import threading
import time


class SessionManager:
    def __init__(
        self, expiry_seconds: int = 3600, check_expiry: bool = True
    ):  # 1 hour default
        self._sessions: dict[int, float] = {}  # session_id -> last_access_time
        self._lock = threading.Lock()
        self._expiry_seconds = expiry_seconds
        self._cleanup_thread = None
        if check_expiry:
            self._cleanup_thread = threading.Thread(
                target=self._cleanup_expired_sessions, daemon=True
            )
            self._cleanup_thread.start()

    def generate_session_id(self) -> int:
        """Generate a new 64-bit random session ID."""
        while True:
            # Generate a random 64-bit integer
            session_id = random.getrandbits(64)
            with self._lock:
                # Make sure it's unique
                if session_id not in self._sessions:
                    self._sessions[session_id] = time.time()
                    return session_id

    def get_session_info(self, session_id: int | None) -> str:
        """Get session info string."""
        if session_id is None:
            return "No session"
        with self._lock:
            if session_id in self._sessions:
                last_access = self._sessions[session_id]
                age = time.time() - last_access
                return f"Session {session_id} (age: {age:.1f}s)"
            return f"Unknown session {session_id}"

    def touch_session(self, session_id: int) -> bool:
        """Update the last access time of a session. Returns True if session exists."""
        current_time = time.time()
        with self._lock:
            if session_id in self._sessions:
                # Check if session has expired
                last_access = self._sessions[session_id]
                if current_time - last_access > self._expiry_seconds:
                    del self._sessions[session_id]
                    return False
                self._sessions[session_id] = current_time
                return True
            return False

    def session_exists(self, session_id: int) -> bool:
        """Check if a session exists and is not expired."""
        current_time = time.time()
        with self._lock:
            if session_id in self._sessions:
                last_access = self._sessions[session_id]
                if current_time - last_access > self._expiry_seconds:
                    del self._sessions[session_id]
                    return False
                return True
            return False

    def _cleanup_expired_sessions(self):
        """Cleanup expired sessions periodically."""
        while True:
            time.sleep(60)  # Check every minute
            current_time = time.time()
            with self._lock:
                expired = [
                    sid
                    for sid, last_access in self._sessions.items()
                    if current_time - last_access > self._expiry_seconds
                ]
                for sid in expired:
                    del self._sessions[sid]
