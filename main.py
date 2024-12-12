import pandas
import random
from tkinter import *

BG_COLOR = "#B1DDC6"
words_to_learn = {}
current_card = {}

# ---------------------------------- COLLECTING DATA ----------------------------------- #
try:
    words_df = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    words_df = pandas.read_csv("data/french_words.csv")
    words_to_learn = words_df.to_dict(orient="records")
else:
    words_to_learn = words_df.to_dict(orient="records")

# --------------------------------REMOVING LEARNT CARDS ------------------------------- #


def remove_learnt_word():
    words_to_learn.remove(current_card)
    data = pandas.DataFrame(words_to_learn)
    data.to_csv(path_or_buf="data/words_to_learn.csv", index=False)
    next_card()


# ----------------------------------- CARD FLIPPING ----------------------------------- #


def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(words_to_learn)
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_word, text=current_card["French"], fill="black")
    canvas.itemconfig(card_image, image=card_front_img)
    flip_timer = window.after(3000, flip_card)


def flip_card():
    global current_card
    canvas.itemconfig(card_image, image=card_back_img)
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=current_card["English"], fill="white")


# -------------------------------------- UI SETUP -------------------------------------- #

window = Tk()
window.title("French Flash Card App")
window.config(padx=50, pady=50, bg=BG_COLOR)

flip_timer = window.after(3000, flip_card)

canvas = Canvas(width=800, height=526, background=BG_COLOR, highlightthickness=0)
card_front_img = PhotoImage(file="images/card_front.png")
card_back_img = PhotoImage(file="images/card_back.png")
card_image = canvas.create_image(400, 263, image=card_front_img)
card_title = canvas.create_text(400, 150, text="", font=("Arial", 40, "italic"), fill="black")
card_word = canvas.create_text(400, 263, text="", font=("Arial", 60, "bold"), fill="black")
canvas.grid(row=0, column=0, columnspan=2)

right_button_img = PhotoImage(file="images/right.png")
right_button = Button(image=right_button_img, borderwidth=0, bg=BG_COLOR, command=remove_learnt_word)
right_button.grid(row=1, column=0)

wrong_button_img = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=wrong_button_img, borderwidth=0, bg=BG_COLOR, command=next_card)
wrong_button.grid(row=1, column=1)

next_card()

window.mainloop()
