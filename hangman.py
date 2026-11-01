import random

# ASCII Art for the 6 stages of the gallows (0 to 6 mistakes)
GALLOWS_STAGES = [
    """
       +---+

       |   |
           |
           |
           |
           |
     =========
    """,
    """
       +---+

       |   |
       O   |
           |
           |
           |
     =========
    """,
    """
       +---+

       |   |
       O   |

       |   |
           |
           |
     =========
    """,
    """
       +---+

       |   |
       O   |
      /|   |
           |
           |
     =========
    """,
    """
       +---+

       |   |
       O   |
      /|\\  |
           |
           |
     =========
    """,
    """
       +---+

       |   |
       O   |
      /|\\  |
      /    |
           |
     =========
    """,
    """
       +---+

       |   |
       O   |
      /|\\  |
      / \\  |
           |
     =========
    """
]

# A fallback word bank if no text file is provided
DEFAULT_WORDS = ["DATHEON", "PYTHON", "DEVELOPER", "INTERFACE", "TERMINAL", "VARIABLE", "FUNCTION"]

def load_words():
    """Attempts to load words from an external file, falling back to a default list."""
    try:
        with open("english_words.txt", "r") as file:
            # Read words, strip whitespace, filter out empty lines, and convert to uppercase
            words = [line.strip().upper() for line in file if line.strip()]
            if words:
                return words
    except FileNotFoundError:
        pass
    return DEFAULT_WORDS

def get_masked_word(word, guessed_letters):
    """Returns the masked version of the secret word separated by spaces."""
    return " ".join([letter if letter in guessed_letters else "_" for letter in word])

def play_hangman():
    # Setup game state
    words = load_words()
    secret_word = random.choice(words).upper()
    
    guessed_letters = set()
    wrong_attempts = 0
    max_attempts = 6

    print("=======================================")
    print("      WELCOME TO HANGMAN GAME         ")
    print("=======================================")

    while wrong_attempts < max_attempts:
        # 1. Display current board status
        print(GALLOWS_STAGES[wrong_attempts])
        masked = get_masked_word(secret_word, guessed_letters)
        print(f"Word to guess: {masked}")
        print(f"Guessed letters: {', '.join(sorted(guessed_letters)) if guessed_letters else 'None'}")
        print(f"Remaining mistakes allowed: {max_attempts - wrong_attempts}")
        print("-" * 40)

        # Check for victory
        if "_" not in masked:
            print("\n🎉 VICTORY! 🎉")
            print(f"Congratulations! You successfully guessed the word: {secret_word}\n")
            return

        # 2. Get user input
        guess = input("Guess a letter: ").strip().upper()

        # Input validation
        if len(guess) != 1 or not guess.isalpha():
            print("⚠️ Invalid input! Please enter a single alphabetical character.")
            continue

        # Check for duplicate guesses
        if guess in guessed_letters:
            print(f"⚠️ You already guessed '{guess}'. No penalty applied.")
            continue

        # 3. Process the guess
        guessed_letters.add(guess)

        if guess in secret_word:
            print(f"✨ Good job! '{guess}' is in the word.")
        else:
            print(f"❌ Incorrect! '{guess}' is not in the word.")
            wrong_attempts += 1

    # 4. Defeat screen if loop completes without winning
    print(GALLOWS_STAGES[wrong_attempts])
    print("\n💀 DEFEAT! 💀")
    print("Game Over. The gallows are complete.")
    print(f"The secret word was: {secret_word}\n")

if __name__ == "__main__":
    while True:
        play_hangman()
        play_again = input("Would you like to play again? (y/n): ").strip().lower()
        if play_again != 'y':
            print("Thanks for playing! Goodbye.")
            break
