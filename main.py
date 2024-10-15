import os
import random
from dotenv import load_dotenv
from swarm import Swarm, Agent

# Load environment variables
load_dotenv()

# Initialize the Swarm client
client = Swarm()

# Define our agents
game_master = Agent(
    name="Game Master",
    instructions="You are the game master for a language learning idiom game. Introduce the game, explain rules, and coordinate between players and language experts."
)

english_expert = Agent(
    name="English Expert",
    instructions="You are an English language expert. Provide idioms, explain their meanings, and evaluate player responses."
)

spanish_expert = Agent(
    name="Spanish Expert",
    instructions="You are a Spanish language expert. Provide idioms, explain their meanings, and evaluate player responses."
)

# Define handoff functions
def consult_english_expert():
    return english_expert

def consult_spanish_expert():
    return spanish_expert

# Add handoff functions to the Game Master
game_master.functions.extend([consult_english_expert, consult_spanish_expert])

def get_idiom_explanation(idiom: str, language: str) -> str:
    """Get an explanation for the given idiom in the specified language."""
    # In a real application, you might use a translation API or database
    return f"[Explanation of '{idiom}' in {language}]"

# Add the idiom explanation function to both language experts
english_expert.functions.append(get_idiom_explanation)
spanish_expert.functions.append(get_idiom_explanation)

def run_idiom_game():
    messages = [{"role": "user", "content": "Let's play a language learning game with idioms!"}]
    current_language = "English"
    score = 0
    rounds = 0

    print("Welcome to the Idiom Challenge!")
    print("Try to guess the meaning of idioms in English and Spanish.")
    print("Type 'switch' to change languages, or 'exit' to end the game.")

    while True:
        response = client.run(agent=game_master, messages=messages)
        print(f"\n{response.agent.name}: {response.messages[-1]['content']}")

        if "What's your guess?" in response.messages[-1]['content']:
            user_input = input("Your guess: ")
            if user_input.lower() == 'exit':
                print(f"\nGame over! Your final score is {score} out of {rounds} rounds.")
                break
            elif user_input.lower() == 'switch':
                current_language = "Spanish" if current_language == "English" else "English"
                print(f"\nSwitching to {current_language} idioms!")
                messages.append({"role": "user", "content": f"Let's switch to {current_language} idioms."})
            else:
                rounds += 1
                if "correct" in response.messages[-1]['content'].lower():
                    score += 1
                print(f"Current score: {score}/{rounds}")
                messages.append({"role": "user", "content": user_input})
        else:
            user_input = input("Press Enter to continue...")
            messages.append({"role": "user", "content": "Continue"})

if __name__ == "__main__":
    # Check if OPENAI_API_KEY is set
    if not os.getenv("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY environment variable is not set.")
        print("Please set your OpenAI API key as an environment variable.")
        exit(1)
    
    run_idiom_game()
