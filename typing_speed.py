import random
import time
import tkinter as tk
import json  # Import JSON module for saving/loading records

# Read phrases from the file or use a default list if the file is missing
try:
    with open("typing_speed_phrases.txt") as p:
        ps = p.read()
        phrase_list = ps.split("\n")
except FileNotFoundError:
    print("Warning: 'typing_speed_phrases.txt' not found. Using default phrases.")
    phrase_list = [
        "The quick brown fox jumps over the lazy dog",
        "Practice makes perfect",
        "A journey of a thousand miles begins with a single step",
        "To be or not to be, that is the question",
        "All that glitters is not gold"
    ]

# Global variable to track already asked phrases
already_asked = []

# File to store user records
records_file = "typing_speed_records.json"

# Load existing records or initialize an empty dictionary
try:
    with open(records_file, "r") as f:
        user_records = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    user_records = {}

# Function to save user records to a file
def save_user_records():
    try:
        with open(records_file, "w") as f:
            json.dump(user_records, f, indent=4)
    except Exception as e:
        print(f"Error saving user records: {e}")

# Function to save the history of the typing test
def save_history(name: str, wpm, mistakes: int):
    name = name.strip().lower()  # Normalize username
    text = f"{name.capitalize()} had an average typing speed of {wpm} wpm with {mistakes} mistakes committed.\n"
    try:
        with open(r"typing_speed_history.txt", "a") as f:
            f.write(text)
            f.write(f"Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write('-' * 50 + '\n')
    except Exception as e:
        print(f"Error saving history: {e}")

    if name not in user_records:
        user_records[name] = []
    user_records[name].append({"wpm": wpm, "mistakes": mistakes})
    save_user_records()

# Function to read the history from the file
def read_history():
    try:
        with open(r"typing_speed_history.txt", "r") as f:
            fc = f.read()
            if fc:
                print(fc)
            else:
                print("No history yet.")
    except FileNotFoundError:
        print("History file not found. No history available.")
    except Exception as e:
        print(f"Error reading history: {e}")

# Function to display previous WPM records for a user
def view_records():
    name = tname.get("1.0", "end").strip().lower()  # Normalize username
    if not name:
        typ_speed.config(text="Please enter your name to view records.")
        return

    if name in user_records:
        records = user_records[name]
        record_text = f"Previous records for {name.capitalize()}:\n"
        for idx, record in enumerate(records, start=1):
            record_text += f"{idx}. {record['wpm']} WPM, {record['mistakes']} mistakes\n"
        typ_speed.config(text=record_text)
    else:
        typ_speed.config(text=f"No records found for {name.capitalize()}.")

# Function to calculate the typing speed
def calc_typing_speed(name: str):
    name = name.strip().lower()  # Normalize username
    sum_wpm = 0
    mistakes = 0
    mistake_dict = {}

    for i in range(1, 6):
        # Generating a random unused phrase
        while True:
            phrase = random.choice(phrase_list).strip().lower()  # Normalize phrase
            if phrase not in already_asked:
                already_asked.append(phrase)
                print(f"Phrase {i}: {phrase}")
                phrase_ques = phrase.split(" ")
                break
        
        # Start Typing Phase
        init = time.time()
        user_ans = input(f"Type this: {phrase}\n").strip().lower()  # Normalize user input
        finish = time.time()

        user_ans = user_ans.split(" ")

        if len(user_ans) == len(phrase_ques):
            wpm = (len(phrase_ques) * 60) // (finish - init)
            sum_wpm += wpm
            for idx, word in enumerate(user_ans):
                if word != phrase_ques[idx]:
                    mistakes += 1
                    mistake_dict[phrase_ques[idx]] = word
        else:
            print("You didn't type the whole phrase!")

    average_wpm = sum_wpm / 5
    result = f"Hey {name.capitalize()}, your average typing speed is {average_wpm} wpm with {mistakes} mistakes.\n"
    print(result)

    if mistake_dict:
        print("Your typing mistakes are:")
        for correct, typed in mistake_dict.items():
            print(f"{correct} --> {typed}")

    save_history(name, average_wpm, mistakes)


# Tkinter GUI Code
window = tk.Tk()
window.title("Typing Speed Calculator")
window.geometry("800x600")

# Enhanced GUI styling
window.configure(bg="#f0f8ff")  # Set a light blue background

# Frame for name entry
frame_name = tk.Frame(window, bg="#f0f8ff")
frame_name.pack(pady=20)

lname = tk.Label(frame_name, text="Enter your name", font=("Arial", 15), bg="#f0f8ff")
lname.pack(side="left", padx=10)

tname = tk.Text(frame_name, height=1, width=30, font=("Arial", 15), bg="#ffffff", relief="solid", bd=1)
tname.pack(side="left", padx=10)

# Frame for the given phrase
frame_phrase = tk.Frame(window, bg="#f0f8ff")
frame_phrase.pack(pady=20)

l_given_phrase = tk.Label(frame_phrase, text="Phrase", font=("Arial", 15), bg="#f0f8ff")
l_given_phrase.pack(pady=5)

t_given_phrase = tk.Text(frame_phrase, height=2, width=60, font=("Arial", 15), state="disabled", bg="#ffffff", relief="solid", bd=1)
t_given_phrase.pack()

# Disable copy and paste for the given phrase widget
def disable_copy_paste(event):
    return "break"

t_given_phrase.bind("<Control-c>", disable_copy_paste)  # Disable copy
t_given_phrase.bind("<Control-v>", disable_copy_paste)  # Disable paste

# Real-time typing speed label
real_time_speed = tk.Label(window, text="Typing speed: 0 WPM", font=("Arial", 15), bg="#f0f8ff")
real_time_speed.pack(pady=10)

# Start typing button
def start_typing():
    global init
    global start_time
    name = tname.get("1.0", "end").strip()  # Get the name from the text widget

    if not name:
        return  # Don't start the test if name is empty

    start_time = time.time()
    t_typed_phrase.config(state="normal")
    t_typed_phrase.delete("1.0", "end")
    real_time_speed.config(text="Typing speed: 0 WPM")
    change_phrase()  # Call change_phrase when typing starts

# Update real-time typing speed
def update_speed(event):
    global start_time

    typed_text = t_typed_phrase.get("1.0", "end").strip()
    phrase = t_given_phrase.get("1.0", "end").strip()

    if typed_text == "":
        return

    # Calculate the time elapsed
    elapsed_time = time.time() - start_time
    words_typed = len(typed_text.split())

    # Calculate WPM
    wpm = (words_typed * 60) // elapsed_time

    # Update the real-time speed
    real_time_speed.config(text=f"Typing speed: {wpm} WPM")

# Frame for typing area
frame_typing = tk.Frame(window, bg="#f0f8ff")
frame_typing.pack(pady=20)

l_typed_phrase = tk.Label(frame_typing, text="Type the given phrase below:", font=("Arial", 15), bg="#f0f8ff")
l_typed_phrase.pack(pady=5)

t_typed_phrase = tk.Text(frame_typing, height=1, width=60, font=("Arial", 15), state="disabled", bg="#ffffff", relief="solid", bd=1)
t_typed_phrase.pack()

# Function to handle the "Enter" key press
def on_enter(event):
    stop_typing()  # Stop typing when the Enter key is pressed
    change_phrase()  # Change to the next phrase

# Update the phrase to a new random one
def change_phrase():
    global already_asked
    # Reset already_asked if all phrases have been used
    if len(already_asked) == len(phrase_list):
        already_asked = []

    # Generate a new random phrase
    try:
        phrase = random.choice([p for p in phrase_list if p not in already_asked])
        t_given_phrase.config(state="normal")
        t_given_phrase.delete("1.0", "end")
        t_given_phrase.insert("1.0", phrase)
        t_given_phrase.config(state="disabled")
        already_asked.append(phrase)
    except IndexError:
        typ_speed.config(text="No phrases available. Please restart the application.")

# Stop typing function
def stop_typing():
    final = time.time()
    user_ans = t_typed_phrase.get("1.0", "end").strip().lower().split()  # Normalize user input
    phrase = t_given_phrase.get("1.0", "end").strip().lower().split()  # Normalize phrase

    if len(user_ans) == len(phrase):
        difference = final - start_time
        wpm = (len(phrase) * 60) // difference
        typ_speed.config(text=f"Your typing speed is: {wpm} WPM")
        save_history(tname.get("1.0", "end").strip(), wpm, 0)
    else:
        typ_speed.config(text="You didn't type the whole phrase!")

# Typing speed result label
typ_speed = tk.Label(window, font=("Arial", 15), bg="#f0f8ff")
typ_speed.pack(pady=10)

# Add a start button after name entry
start_button = tk.Button(window, text="Start Typing", font=("Arial", 15), bg="#4caf50", fg="white", relief="raised", bd=2, command=start_typing)
start_button.pack(pady=10)

# Add a button to view records
view_button = tk.Button(window, text="View Records", font=("Arial", 15), bg="#2196f3", fg="white", relief="raised", bd=2, command=view_records)
view_button.pack(pady=10)

# Bind the typing event to track real-time speed
t_typed_phrase.bind("<KeyRelease>", update_speed)

# Bind the "Enter" key to move to the next phrase
t_typed_phrase.bind("<Return>", on_enter)

# Run the Tkinter window
window.mainloop()
