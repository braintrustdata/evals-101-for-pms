"""Multi-Turn Customer Support Chat App — PM Webinar

Run this to start an interactive chat session:
    python3 chat_app.py

Every conversation is logged to Braintrust as a single trace with
nested turn spans. Open the production logs in the Braintrust UI
to see the full conversation structure.
"""
import os
from openai import OpenAI
from braintrust import init_logger, traced

logger = init_logger(project="Customer Support Chatbot")
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

SYSTEM_PROMPT = (
    "You are a helpful customer support agent for an e-commerce company. "
    "Be empathetic but efficient. Ask clarifying questions when needed. "
    "If you can resolve the issue, do so. If you need to escalate, "
    "explain why and what the customer should expect next."
)


@traced
def chat(conversation_history):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=conversation_history,
        temperature=1.0,
    )
    return response.choices[0].message.content


def main():
    print("Customer Support Chat (type 'quit' to exit)")
    print("-" * 45)

    conversation_history = [{"role": "system", "content": SYSTEM_PROMPT}]
    turn_number = 0

    with logger.start_span(name="conversation") as conversation_span:
        while True:
            user_input = input("\nYou: ").strip()
            if user_input.lower() == "quit":
                break

            conversation_history.append({"role": "user", "content": user_input})
            turn_number += 1

            with conversation_span.start_span(name=f"turn_{turn_number}") as turn_span:
                response = chat(conversation_history)
                conversation_history.append({"role": "assistant", "content": response})
                turn_span.log(
                    input=user_input,
                    output=response,
                    metadata={"turn_number": turn_number},
                )

            print(f"\nAgent: {response}")

        conversation_span.log(
            input=conversation_history,
            output=conversation_history[-1]["content"] if len(conversation_history) > 1 else None,
            metadata={"total_turns": turn_number},
        )


if __name__ == "__main__":
    main()
