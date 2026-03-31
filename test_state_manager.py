#!/usr/bin/env python3
"""Test the state manager functionality."""

import os
import json
from state_manager import should_show_welcome, mark_welcome_as_seen, load_state, STATE_FILE

def test_state_manager():
    """Test state manager functions."""
    # Clean up any existing state file
    if os.path.exists(STATE_FILE):
        os.remove(STATE_FILE)

    # Test 1: First time user should see welcome
    assert should_show_welcome() == True, "First time user should see welcome"
    print("✓ Test 1 passed: First time user should see welcome")

    # Test 2: After marking as seen, should not show welcome
    mark_welcome_as_seen()
    assert should_show_welcome() == False, "After marking as seen, should not show welcome"
    print("✓ Test 2 passed: After marking as seen, should not show welcome")

    # Test 3: State file should exist and contain correct data
    assert os.path.exists(STATE_FILE), "State file should exist"
    state = load_state()
    assert state.get('has_seen_welcome') == True, "State should have has_seen_welcome set to True"
    print("✓ Test 3 passed: State file exists with correct data")

    # Test 4: Verify state persists after reload
    state = load_state()
    assert state.get('has_seen_welcome') == True, "State should persist"
    print("✓ Test 4 passed: State persists after reload")

    # Clean up
    if os.path.exists(STATE_FILE):
        os.remove(STATE_FILE)

    print("\n✓ All tests passed!")

if __name__ == "__main__":
    test_state_manager()
