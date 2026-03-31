import json
import os

STATE_FILE = ".craft_listen_state.json"

def load_state():
    """Load application state from file."""
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}
    return {}

def save_state(state):
    """Save application state to file."""
    try:
        with open(STATE_FILE, 'w') as f:
            json.dump(state, f, indent=2)
    except IOError:
        pass  # Fail silently if we can't save state

def should_show_welcome():
    """Check if the welcome message should be shown."""
    state = load_state()
    return not state.get('has_seen_welcome', False)

def mark_welcome_as_seen():
    """Mark the welcome message as seen."""
    state = load_state()
    state['has_seen_welcome'] = True
    save_state(state)
