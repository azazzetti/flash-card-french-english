from tkinter import *
import random
import pandas as pd

BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
to_learn = {}
# ----------------------------------- READ CSV & SELECT WORDS ----------------------------------- #
try:
    data = pd.read_csv("./data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pd.read_csv("./data/french_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")


def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(card_background, image=front_image)
    canvas.itemconfig(card_word, text=current_card["French"], fill="black")
    canvas.itemconfig(card_title, text="French", fill="black")
    flip_timer = window.after(3000, flip_card)


def flip_card():
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=current_card["English"], fill="white")
    canvas.itemconfig(card_background, image=back_image)


def is_known():
    to_learn.remove(current_card)
    data = pd.DataFrame(to_learn)
    data.to_csv("./data/words_to_learn.csv", index=False)
    next_card()
# ----------------------------------- UI ----------------------------------- #


window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, flip_card)

canvas = Canvas(width=800, height=526, highlightthickness=0, bg=BACKGROUND_COLOR)
front_image = PhotoImage(file="./images/card_front.png")
back_image = PhotoImage(file="./images/card_back.png")
card_background = canvas.create_image(400, 263, image=front_image)
card_title = canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic"))
card_word = canvas.create_text(400, 263, text="", font=("Ariel", 60, "bold"))
canvas.grid(column=0, row=0, columnspan=2)

checkmark_img = PhotoImage(file="./images/right.png")
checkmark_button = Button(image=checkmark_img, highlightthickness=0, command=is_known)
checkmark_button.grid(column=0, row=1)

wrong_img = PhotoImage(file="./images/wrong.png")
unknown_button = Button(image=wrong_img, highlightthickness=0, command=next_card)
unknown_button.grid(column=1, row=1)

next_card()

window.mainloop()