from tkinter import *
import pandas as pd
from random import choice
from pprint import pprint

BACKGROUND_COLOR = "#B1DDC6"
LANGUAGE = "French"
WORDS_DATA = "data/french_words.csv"

data = pd.DataFrame()
try:
    data = pd.read_csv(r"data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pd.read_csv(r"data/french_words.csv")
    to_learn = original_data.to_dict("records")
else:
    to_learn = data.to_dict("records")

current_card = {}


# ---------------------------------- Next Card ----------------------------#
def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)

    current_card = choice(to_learn)
    canvas.itemconfig(card_background, image=card_front_img)
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_word, text=current_card.get("French"), fill="black")
    flip_timer = window.after(3000, func=flip_card)


def flip_card():
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=current_card.get("English"), fill="white")
    canvas.itemconfig(card_background, image=card_back_img)


def recall_correct():
    to_learn.remove(current_card)
    to_learn_df = pd.DataFrame(to_learn)
    to_learn_df.to_csv(r"data/words_to_learn.csv", index=False)
    next_card()


if __name__ == "__main__":
    # ------------------------------ UI SETUP ------------------------------#
    window = Tk()
    window.title("Flash Card")
    window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

    # Calling flip_card first time
    # call the flip card function after 3s ; time for the user to look at the french word and guess if he/she knows it.
    flip_timer = window.after(3000, func=flip_card)

    canvas = Canvas(width=800, height=526)
    # # Flash Card
    card_front_img = PhotoImage(file="images/card_front.png")
    # Important to create it outside any of the functions since the reference will be lost if created inside any of the
    # functions  after the function call.
    card_back_img = PhotoImage(file="images/card_back.png")

    card_background = canvas.create_image(400, 263, image=card_front_img)
    card_title = canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic"))
    card_word = canvas.create_text(400, 263, text="", font=("Ariel", 60, "bold"))
    canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
    canvas.grid(row=0, column=0, columnspan=2)

    # unknown button
    cross_image = PhotoImage(file="images/wrong.png")
    unknown_button = Button(image=cross_image, highlightthickness=0, command=next_card)
    unknown_button.grid(row=1, column=0)
    # # right button
    check_image = PhotoImage(file="images/right.png")
    known_button = Button(image=check_image, highlightthickness=0, command=recall_correct)
    known_button.grid(row=1, column=1)

    # Call the function next_card() after creating all the UI but before the main loop
    # so that you don't get a blank card, the first time the program is run.
    next_card()
    window.mainloop()
