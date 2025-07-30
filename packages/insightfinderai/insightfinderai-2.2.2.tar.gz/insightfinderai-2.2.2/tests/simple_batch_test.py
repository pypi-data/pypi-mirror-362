#!/usr/bin/env python3
"""
Batch Chat Test - Multiple prompts at once
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

print("=== Batch Chat Test ===")

# Test 1: Small batch
print("\n--- Test 1: Small Batch Chat ---")
prompts = [
    "What is artificial intelligence?",
    "Explain machine learning",
    "What are neural networks?"
]

batch_result = client.batch_chat(prompts)
print(f"Number of responses: {len(batch_result.response)}")
print(f"Overall passed: {batch_result.is_passed}")

for i, response in enumerate(batch_result.response):
    print(f"\nResponse {i+1}: {response.response[:60]}...")

# Test 2: Batch with history
print("\n--- Test 2: Batch with History ---")
conversation_prompts = [
    "Hello, I'm learning programming",
    "What language should I start with?",
    "Can you give me an example?"
]

batch_with_history = client.batch_chat(conversation_prompts, enable_history=True)
print(batch_with_history)

for i, response in enumerate(batch_with_history.response):
    print(f"Response {i+1} history length: {len(response.history)}")

# Test 3: Check batch summary
print("\n--- Test 3: Batch Summary ---")
summary = batch_result.summary
print(f"Summary: {summary}")
