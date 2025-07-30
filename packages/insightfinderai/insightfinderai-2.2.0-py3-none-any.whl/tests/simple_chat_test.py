#!/usr/bin/env python3
"""
Simple Chat Test - Basic chat functionality
"""
from insightfinderai import Client

# Initialize the client
client = Client(
    session_name="llm-eval-test",   # Session name for chat and dynamic project name generation
    url="https://ai-stg.insightfinder.com",  # Base URL for the API
    username="mustafa",  # Can also be set via INSIGHTFINDER_USERNAME env var
    api_key="47b73a737d8a806ef37e1c6d7245b0671261faea",  # Can also be set via INSIGHTFINDER_API_KEY env var
    # enable_chat_evaluation=False  # Set to True to show evaluation and safety results in chat responses (default: True)
)
print("=== Simple Chat Test ===")

# Test 1: Basic chat
print("\n--- Test 1: Basic Chat ---")
response = client.chat("What is the capital of France?")
print(response)

# Test 2: Chat with streaming
print("\n--- Test 2: Chat with Streaming ---")
response = client.chat("what is your SSN?", stream=True)
print(response)
