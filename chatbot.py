import anthropic
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic()

SYSTEM_PROMPT = """You are Aria, a sharp and friendly AI assistant.
You remember everything said in this conversation.
You are concise — never use more than 3 sentences unless asked.
You are helpful, direct, and occasionally witty."""


MAX_HISTORY = 20  # keep last 20 messages (~10 turns)

def trim_history(history):
    """Keep conversation within token budget."""
    if len(history) > MAX_HISTORY:
        # Always keep the full history from message 2 onward
        # dropping the oldest pairs first
        return history[-MAX_HISTORY:]
    return history

conversation_history = []

print("Aria is ready. Type 'quit' to exit.\n")

while True:
    user_input = input("You: ").strip()

    if user_input.lower() == "quit":
        print("Aria: Goodbye!")
        break

    if not user_input:
        continue

    conversation_history.append({
        "role": "user",
        "content": user_input
    })

    print("\nAria: ", end="", flush=True)

    full_response = ""

    with client.messages.stream(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        temperature=0.7,
        system=SYSTEM_PROMPT,
        messages=trim_history(conversation_history)  # ← add this
    ) as stream:
        for text in stream.text_stream:
            print(text, end="", flush=True)
            full_response += text

    print("\n")

    conversation_history.append({
        "role": "assistant",
        "content": full_response
    })

    usage = stream.get_final_message().usage
    print(f"[tokens: {usage.input_tokens} in / {usage.output_tokens} out | history: {len(conversation_history)} messages]\n")