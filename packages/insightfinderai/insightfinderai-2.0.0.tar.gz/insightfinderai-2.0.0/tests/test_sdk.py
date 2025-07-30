from insightfinderai import Client

# Initialize the client with all required parameters in one place
client = Client(
    session_name="test-gpt-llm1",   # Session name for chat and dynamic project name generation
    url="https://ai-stg.insightfinder.com",  # Base URL for the API
    username="mustafa",  # Can also be set via INSIGHTFINDER_USERNAME env var
    api_key="47b73a737d8a806ef37e1c6d7245b0671261faea",  # Can also be set via INSIGHTFINDER_API_KEY env var
    # enable_chat_evaluation=False  # Set to True to show evaluation and safety results in chat responses (default: True)
)

# Example 1: Simple chat
print("=== Example 1: Simple Chat ===")
response = client.chat("What is the capital of France? I think it's London.")
print(response)

print("\n" + "="*60 + "\n")

# Example 2: Batch chatting
print("=== Example 2: Batch Chat ===")
prompts = [
    "Hello, how are you?",
    "What's the capital of France?",
    "Tell me a joke"
]
responses = client.batch_chat(prompts)
for i, response in enumerate(responses, 1):
    print(f"\n--- Response {i} ---")
    print(response)

print("\n" + "="*60 + "\n")

# Example 3: Evaluation
print("=== Example 3: Evaluation ===")
eval_result = client.evaluate(
    prompt="What's the capital of India?",
    response="The capital of India is hindi"
)
print(eval_result)

print("\n" + "="*60 + "\n")

# Example 4: Batch evaluation
print("=== Example 4: Batch Evaluation ===")
pairs = [
    ("What's 2+2?", "2"),
    ("What's the capital of France?", "Paris"),
    ("Tell me about AI", "AI is artificial intelligence")
]
eval_results = client.batch_evaluate(pairs)
for i, result in enumerate(eval_results, 1):
    print(f"\n--- Evaluation {i} ---")
    print(result)

print("\n" + "="*60 + "\n")

# Example 5: Simple Chat with History Storage
print("\n=== Example 5: Chat with History Storage ===")
client.clear_chat_history()  # Start fresh

# Chat with history storage enabled
print(">>> First message with chat_history=True:")
response1 = client.chat("I'm planning a vacation to Japan", chat_history=True)
print(response1)

print("\n>>> Second message (builds on context):")
response2 = client.chat("What's the best time to visit?", chat_history=True)
print(response2)

print("\n" + "="*60 + "\n")

# Example 6: Conversation History Array
print("=== Example 6: Conversation History Array ===")
conversation = [
    {"role": "user", "content": "I need help with Python programming"},
    {"role": "assistant", "content": "I'd be happy to help! What specific Python topic would you like to learn about?"},
    {"role": "user", "content": "How do I work with lists?"}
]

response = client.chat(conversation, chat_history=True)
print(response)

print("\n" + "="*60 + "\n")

# Example 7: Save Chat History
print("=== Example 7: Save Chat History ===")

# Build a conversation
client.clear_chat_history()
print(">>> Building conversation...")
client.chat("Tell me about machine learning", chat_history=True)
client.chat("What are the main types of ML algorithms?", chat_history=True)
client.chat("Explain supervised learning", chat_history=True)

# Save conversation
print("\n>>> Saving conversation...")
saved_filename = client.save_chat_history("ml_conversation.json")
print(f"Saved to: {saved_filename}")

print("\n" + "="*60 + "\n")

# Example 8: Retrieve and Inspect Chat History
print("=== Example 8: Retrieve and Inspect Chat History ===")

# Build a sample conversation
client.clear_chat_history()
client.chat("Hello, I'm interested in learning about space", chat_history=True)
client.chat("Tell me about the solar system", chat_history=True)
client.chat("What's the largest planet?", chat_history=True)

# # Retrieve and display history
# print("Current conversation history:")
# history = client.retrieve_chat_history()
# for i, msg in enumerate(history, 1):
#     role_icon = "🧑" if msg['role'] == 'user' else "🤖"
#     print(f"  {i}. {role_icon} [{msg['role'].upper()}] {msg['content'][:50]}{'...' if len(msg['content']) > 50 else ''}")

# print("\n" + "="*60 + "\n")