import json

# loads knowledge

def load_knowledge(filename):
    try:
        with open(filename, "r") as l:
            return json.load(l)
    except FileNotFoundError:
        return

# Writing knowledge

def save_knowledge(filename, data):
    with open(filename, "w") as w:
        json.dump(data, w, indent = 4)

# user data 

def User_startup_data():
    try:
        with open("user_data.json", "r") as f:
            user_data = json.load(f)
            user_name = user_data.get("name", None)
    except FileNotFoundError:
        user_name = None

    if not user_name:
        user_name = input("Spec: Hey there, do you mind giving me your name?\nYou: ").strip()
        with open("user_data.json", "w") as f:
            json.dump({"name": user_name}, f)

    try:
        with open("user_data.json", "r") as f:
            user_data = json.load(f)
            user_favColour = user_data.get("colour", None)
    except FileNotFoundError:
        user_favColour = None

    if not user_favColour:
        user_favColour = input("Spec: Whats your faviourite colour??\nYou: ").strip()
        with open("user_data.json", "w") as f:
            json.dump({"colour": user_favColour}, f)
    

    print(f"Hi {user_name}")


# Main loop

def chat():

    User_startup_data()

    preprogrammed = load_knowledge("preprogrammed.json")
    learnt = load_knowledge("learned_memory.json")

    knowledge_total = {**preprogrammed, **learnt}
    print("Spec: Ask me something or exit by typing the letter 'q' \n      For help type 'help' for all the avalible functions. ")

    while True:
        quit_conditions = "quit","q","exit"
        user_input = input('> ').strip().lower()
        if user_input in quit_conditions:
            print("Killing program")
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
    

chat()