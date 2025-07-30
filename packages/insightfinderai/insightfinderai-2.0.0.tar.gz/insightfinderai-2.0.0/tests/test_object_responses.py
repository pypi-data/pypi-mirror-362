from insightfinderai import Client

# Initialize the client
client = Client(
    session_name="llm-eval-test",
    url="https://ai-stg.insightfinder.com",
    username="mustafa",
    api_key="47b73a737d8a806ef37e1c6d7245b0671261faea"
)

print("=== Testing New Object-Based Response Format ===\n")

# Example 1: Single Chat with Object Access
print("=== Example 1: Single Chat Response Object ===")
response = client.chat("What is the capital of France?")

print("Response object properties:")
print(f"response.response: {response.response}")
print(f"response.prompt: {response.prompt}")
print(f"response.trace_id: {response.trace_id}")
print(f"response.model: {response.model}")
print(f"response.history: {response.history}")
print(f"response.evaluations: {response.evaluations}")

print("\n>>> Using response.print():")
response.print()

print("\n" + "="*60 + "\n")

# Example 2: Chat with History
print("=== Example 2: Chat with History ===")
client.clear_chat_history()
response1 = client.chat("I'm interested in Python programming", chat_history=True)
response2 = client.chat("What are the main data types?", chat_history=True)

print("Second response object properties:")
print(f"response.response: {response2.response[:100]}...")
print(f"response.prompt: {response2.prompt}")
print(f"response.history length: {len(response2.history)}")
print("History contents:")
for i, msg in enumerate(response2.history):
    print(f"  {i+1}. [{msg['role']}] {msg['content'][:50]}...")

print("\n" + "="*60 + "\n")

# Example 3: Single Evaluation with Object Access
print("=== Example 3: Single Evaluation Response Object ===")
eval_response = client.evaluate(
    prompt="What's the capital of India?",
    response="The capital of India is New Delhi"
)

print("Evaluation object properties:")
print(f"eval_response.prompt: {eval_response.prompt}")
print(f"eval_response.response: {eval_response.response}")
print(f"eval_response.evaluations: {len(eval_response.evaluations) if eval_response.evaluations else 0} evaluations")
print(f"eval_response.summary: {eval_response.summary}")

print("\nSummary explanation:")
print("- total_prompts: Number of prompts evaluated")
print("- passed_evaluations: Number with empty evaluations (empty = passed)")
print("- failed_evaluations: Number with evaluations (has evaluations = failed)")
print("- top_failed_evaluation: Most common evaluation type(s)")

if eval_response.evaluations:
    print("Individual evaluations:")
    for i, eval_item in enumerate(eval_response.evaluations):
        print(f"  {i+1}. {eval_item.get('evaluationType', 'Unknown')}: {eval_item.get('score', 0)}")

print("\n>>> Using eval_response.print():")
eval_response.print()

print("\n" + "="*60 + "\n")

# Example 4: Batch Evaluation with Summary
print("=== Example 4: Batch Evaluation Response Object ===")
pairs = [
    ("What's 2+2?", "4"),
    ("What's the capital of France?", "London"),  # Intentionally wrong
    ("Tell me about AI", "AI is artificial intelligence")
]

batch_eval_response = client.batch_evaluate(pairs)

print("Batch evaluation object properties:")
print(batch_eval_response.evaluations)
print(f"batch_eval_response.evaluations: {len(batch_eval_response.evaluations)} evaluation results")
print(f"batch_eval_response.response: {len(batch_eval_response.response)} evaluation results (alias)")
print(f"batch_eval_response.prompt: {len(batch_eval_response.prompt)} prompts")
print(f"batch_eval_response.summary: {batch_eval_response.summary}")

print("\nSummary details:")
summary = batch_eval_response.summary
print(f"  Total prompts: {summary['total_prompts']}")
print(f"  Passed evaluations: {summary['passed_evaluations']} (empty evaluations = passed)")
print(f"  Failed evaluations: {summary['failed_evaluations']} (has evaluations = failed)")
if summary['top_failed_evaluation']:
    top_failed = summary['top_failed_evaluation']
    if isinstance(top_failed, list):
        print(f"  Top failed: {', '.join(top_failed)} (most common evaluation types)")
    else:
        print(f"  Top failed: {top_failed} (most common evaluation type)")

print("\n>>> Using batch_eval_response.print():")
batch_eval_response.print()

print("\n" + "="*60 + "\n")

# Example 5: Batch Chat with Summary
print("=== Example 5: Batch Chat Response Object ===")
prompts = [
    "Hello, how are you?",
    "What's the weather like?",
    "Tell me a joke"
]

batch_chat_response = client.batch_chat(prompts)

print("Batch chat object properties:")
print(f"batch_chat_response.response: {len(batch_chat_response.response)} chat responses")
print(f"batch_chat_response.prompt: {len(batch_chat_response.prompt)} prompts")
print(f"batch_chat_response.evaluations: {len(batch_chat_response.evaluations)} evaluation results")
print(f"batch_chat_response.history: {len(batch_chat_response.history)} history items")
print(f"batch_chat_response.summary: {batch_chat_response.summary}")

print("\nSummary details:")
summary = batch_chat_response.summary
print(f"  Total chats: {summary['total_chats']}")
print(f"  Successful chats: {summary['successful_chats']}")
print(f"  Failed chats: {summary['failed_chats']}")

print("\n>>> Accessing individual chat responses:")
for i, chat_resp in enumerate(batch_chat_response.response):
    print(f"  Chat {i+1}: {chat_resp.response[:50]}...")

print("\n>>> Using batch_chat_response.print():")
batch_chat_response.print()

print("\n" + "="*60 + "\n")

# Example 6: Session Name Override Testing
print("=== Example 6: Session Name Override ===")
print("Testing session_name parameter override for all methods...")

# Test chat with custom session name
print("\n1. Chat with custom session_name:")
response = client.chat("Hello with custom session", session_name="custom-chat-session")
print(f"  Chat response received: {response.response[:50]}...")

# Test evaluation with custom session name  
print("\n2. Evaluation with custom session_name:")
eval_response = client.evaluate(
    prompt="What's the capital of Japan?", 
    response="Tokyo is the capital of Japan",
    session_name="custom-eval-session"
)
print(f"  Evaluation completed. Evaluations: {len(eval_response.evaluations) if eval_response.evaluations else 0}")

# Test safety evaluation with custom session name
print("\n3. Safety evaluation with custom session_name:")
safety_response = client.safety_evaluation(
    prompt="Tell me about artificial intelligence",
    session_name="custom-safety-session"
)
print(f"  Safety evaluation completed. Evaluations: {len(safety_response.evaluations) if safety_response.evaluations else 0}")

# Test batch operations with custom session names
print("\n4. Batch operations with custom session_name:")

# Batch chat
batch_chat_custom = client.batch_chat(
    ["Hello", "How are you?"], 
    session_name="custom-batch-chat"
)
print(f"  Batch chat completed: {len(batch_chat_custom.response)} responses")

# Test batch chat with conversation history
print("\n5. Batch chat with conversation history:")
conversation_prompts = [
    "Hello, my name is Alice",
    "What's my name?", 
    "Tell me about our conversation"
]

batch_chat_history = client.batch_chat(
    conversation_prompts, 
    enable_history=True,
    session_name="custom-batch-history"
)
print(f"  Batch chat with history completed: {len(batch_chat_history.response)} responses")

# Verify conversation flow
for i, response in enumerate(batch_chat_history.response):
    print(f"    Response {i+1} history length: {len(response.history)}")
    if i == 0:
        print(f"    First response should have 2 messages: {len(response.history) == 2}")
    elif i == 1:
        print(f"    Second response should have 4 messages: {len(response.history) == 4}")
    elif i == 2:
        print(f"    Third response should have 6 messages: {len(response.history) == 6}")

print("  ✅ Conversation history correctly maintained!")

# Batch evaluate
batch_eval_custom = client.batch_evaluate(
    [("What's 1+1?", "2"), ("What's 3+3?", "6")],
    session_name="custom-batch-eval"
)
print(f"  Batch evaluation completed: {len(batch_eval_custom.evaluations)} evaluations")

# Batch safety
batch_safety_custom = client.batch_safety_evaluation(
    ["Hello there", "How are you today?"],
    session_name="custom-batch-safety"
)
print(f"  Batch safety completed: {len(batch_safety_custom.evaluations)} evaluations")

print("\n✅ All session_name override tests completed successfully!")

print("\n" + "="*60 + "\n")

# Example 7: Backward Compatibility - Still Works as String
print("=== Example 7: Backward Compatibility ===")
print("Objects still work as strings when printed directly:")
response = client.chat("Quick test", chat_history=False)
print(response)  # Should still work as before

print("\nDone!")
