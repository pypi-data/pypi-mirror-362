import json
import os
from datetime import datetime
from typing import Dict, Optional

class StateManager:
    def __init__(self, state_file: str = "config/alert_state.json"):
        self.state_file = state_file
        self.state = self._load_state()

    def _load_state(self) -> Dict[str, str]:
        """Load the state from file or create empty state if file doesn't exist"""
        if os.path.exists(self.state_file):
            with open(self.state_file, 'r') as f:
                return json.load(f)
        return {}

    def _save_state(self) -> None:
        """Save the current state to file"""
        # Ensure directory exists
        os.makedirs(os.path.dirname(self.state_file), exist_ok=True)
        with open(self.state_file, 'w') as f:
            json.dump(self.state, f, indent=4)

    def get_last_processed_time(self, alert_name: str) -> Optional[datetime]:
        """Get the last processed timestamp for an alert"""
        timestamp_str = self.state.get(alert_name)
        if timestamp_str:
            return datetime.fromisoformat(timestamp_str)
        return None

    def update_last_processed_time(self, alert_name: str, timestamp: datetime) -> None:
        """Update the last processed timestamp for an alert"""
        self.state[alert_name] = timestamp.isoformat()
        self._save_state() 