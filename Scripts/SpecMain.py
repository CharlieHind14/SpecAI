import json
import sys, os

# getting path

def get_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


# loads knowledge

def load_knowledge(filename):
    try:
        file = get_path(filename)
        with open(file, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return

# Writing knowledge

def save_knowledge(filename, data):
    file = get_path(filename)
    with open(file, "w") as w:
        json.dump(data, w, indent = 4)


# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


# user data 

def User_startup_data():
    try:
        file = get_path("user_data.json")
        with open(file, "r") as f:
            user_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        user_data = {}  # start fresh if file doesn't exist or is empty

    # Ask for name if not already saved
    if "name" not in user_data:
        user_data["name"] = input("Spec: Hi! What's your name?\nYou: ").strip()

    # Ask for favorite color if not already saved
    if "favorite_color" not in user_data:
        user_data["favorite_color"] = input(f"Spec: Nice to meet you {user_data['name']}! What's your favorite color?\nYou: ").strip()

    # Save updated data back to the file
    with open(file, "w") as f:
        json.dump(user_data, f, indent=4)
    
    print(f"Spec: Hi, {user_data['name']}!")

def User_data_reset():
    try:
        file = get_path("user_data.json")
        with open(file, "w") as f:
            json.dump({}, f)
    except (FileNotFoundError, json.JSONDecodeError):
        print("User Data reset failed - FILE ERROR")

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def Help():
    print('Spec: You asked me for help :) Here are all the functions currently avalible:\n-Reset User Data - removes all known user-data ( once ran restart me )')

    finish = input("press entire to continue... ")
    

# Main loop

def chat():

    User_startup_data()

    preprogrammed = load_knowledge("preprogrammed.json")
    learnt = load_knowledge("learned_memory.json")

    knowledge_total = {**preprogrammed, **learnt}
    print("Spec: Ask me something or exit by typing the letter 'q' \n      For help type 'help' for all the avalible functions. ")

    def Main_Run():
        while True:
            quit_conditions = "quit","q","exit"
            user_input = input('> ').strip().lower()
            if user_input in quit_conditions:
                print("Killing program")
                return
            if user_input == "help":
                Help()
                Main_Run()
            if user_input == "reset":
                User_data_reset()
                break
            if user_input in knowledge_total:
                print("Spec >", knowledge_total[user_input])
            else:
                # If unknown, ask the user
                answer = input("Spec: I don't know, can you tell me?\nYou: ")
                knowledge_total[user_input] = answer  # update in-memory
                learnt[user_input] = answer         # update learned dictionary
                save_knowledge("learned_memory.json", learnt)  # save to file
                print("Spec: Got it! I will remember that.")
        
    Main_Run()

chat()