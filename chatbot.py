import json
import os
import re

# Define a default dataset in case the sample JSON file isn't present
DEFAULT_FAQ_DATA = {
    "greetings": {
        "patterns": [r"\bhello\b", r"\bhi\b", r"\bhey\b", r"\bgreet\b"],
        "responses": [
            "Hello! Welcome to our automated support terminal. How can I assist you today?"
        ],
    },
    "business_hours": {
        "patterns": [
            r"\bhour(s)?\b",
            r"\bopen\b",
            r"\bclose\b",
            r"\bwhen\b.*\bopen\b",
        ],
        "responses": [
            "Our support and business hours are Monday through Friday, 9:00 AM to 5:00 PM EST."
        ],
    },
    "product_faqs": {
        "patterns": [
            r"\bproduct(s)?\b",
            r"\bwarranty\b",
            r"\bprice\b",
            r"\bcost\b",
            r"\bfeatures\b",
        ],
        "responses": [
            "All our hardware products come with a standard 1-year limited warranty. For detailed catalog pricing, please check our main website."
        ],
    },
    "returns": {
        "patterns": [
            r"\breturn(s)?\b",
            r"\brefund(s)?\b",
            r"\bpolicy\b.*\breturn\b",
        ],
        "responses": [
            "We offer a 30-day money-back guarantee. Items must be returned in their original packaging with all included accessories."
        ],
    },
}


def load_dataset(filename="faq_dataset.json"):
    """Loads the intent and response configuration from a JSON file,

    falling back to the default hardcoded rules if the file is missing.
    """
    if os.path.exists(filename):
        try:
            with open(filename, "r") as file:
                return json.load(file)
        except (json.JSONDecodeError, IOError) as e:
            print(
                f"[System Warning] Error loading JSON dataset ({e}). Using default data."
            )
            return DEFAULT_FAQ_DATA
    else:
        # Create the file automatically to demonstrate JSON integration
        try:
            with open(filename, "w") as file:
                json.dump(
                    DEFAULT_FAQ_DATA, file, indent=4
                )  # Format nicely for the user
        except IOError:
            pass
        return DEFAULT_FAQ_DATA


def match_intent(user_input, dataset):
    """Parses user input using regex patterns to find a matching intent."""
    for intent, data in dataset.items():
        for pattern in data.get("patterns", []):
            if re.search(pattern, user_input):
                return data.get("responses", [
                    "I understand your request, but I'm having trouble retrieving the exact details right now."
                ])[0]
    return None


def run_chatbot():
    """Main execution loop for the rule-based terminal chatbot."""
    dataset = load_dataset()

    print("==================================================")
    # Print introductory guidance message
    print("    Rule-Based Interactive Terminal Assistant    ")
    print("==================================================")
    print("Type your questions below. Enter 'bye', 'exit', or 'quit' to close.")
    print("-" * 50)

    # Initial state greeting
    print(
        "Bot: Hello! I am your automated terminal assistant. How can I help you today?"
    )

    while True:
        try:
            user_raw_input = input("You: ")
        except (KeyboardInterrupt, EOFError):
            print("\nBot: Session interrupted. Goodbye!")
            break

        # Step 3: Normalize user input
        clean_input = user_raw_input.strip().lower()

        # Handle clean exit commands
        if clean_input in ["bye", "exit", "quit"]:
            print("Bot: Thank you for reaching out. Goodbye!")
            break

        # Skip empty submissions safely
        if not clean_input:
            continue

        # Step 4 & 5: Match intent and provide graceful fallbacks
        response = match_intent(clean_input, dataset)

        if response:
            print(f"Bot: {response}")
        else:
            print(
                "Bot: I'm sorry, I didn't quite catch that. Could you try rephrasing your question or specify if you're asking about our business hours, product FAQs, or return policies?"
            )

        print("-" * 50)


if __name__ == "__main__":
    run_chatbot()
