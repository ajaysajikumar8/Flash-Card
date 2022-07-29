import random
from tkinter import *
import pandas

BACKGROUND_COLOR = "#B1DDC6"

#------------------------FETCH DATA --------------------------#
data_dict = {}
current_card = {}

try:
    df = pandas.read_csv("data/Words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv")
    data_dict = original_data.to_dict(orient="records") 
else:
    data_dict= df.to_dict(orient="records")


def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(data_dict)
    canvas.itemconfig(card_title, text="French", fill= "black")
    canvas.itemconfig(card_word, text=current_card["French"], fill = "black")
    canvas.itemconfig(card_background, image= french_card_img)
    flip_timer = window.after(3000, func=flip_card)
    
def flip_card():
    canvas.itemconfig(card_title, text= "English", fill= "white")
    canvas.itemconfig(card_word, text = current_card["English"], fill= "white")
    canvas.itemconfig(card_background, image=english_card_img)

def is_known():
    data_dict.remove(current_card)
    data = pandas.DataFrame(data_dict)
    data.to_csv("data/Words_to_learn.csv", index=False)
    next_card()

    

#------------------------UI SETUP --------------------------#
window = Tk()
window.title("Flashy")
window.config(padx=50, pady= 50, bg= BACKGROUND_COLOR)

flip_timer = window.after(3000, func=flip_card)

canvas = Canvas(width=800, height = 526, bg=BACKGROUND_COLOR, highlightthickness=0)
french_card_img = PhotoImage(file="images/card_front.png")
english_card_img = PhotoImage(file= "images/card_back.png")

card_background =canvas.create_image(400, 263, image= french_card_img)
card_title = canvas.create_text(400,150, text="Title", font=("Ariel", 40, "italic"))
card_word = canvas.create_text(400,263, text="Word", font=("Ariel", 60, "bold"))
canvas.grid(row=0, column=0, columnspan=2)

right_img = PhotoImage(file="images/right.png")
left_img = PhotoImage(file="images/wrong.png")

unknown_button = Button(image=left_img, highlightthickness=0, command=next_card)
unknown_button.grid(row=1, column=0)

known_button = Button(image= right_img, highlightthickness=0, command=is_known)
known_button.grid(row=1, column=1)

next_card()


window.mainloop()
