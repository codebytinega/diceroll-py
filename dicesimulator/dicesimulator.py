import random 
import tkinter as tk
import time


dice_faces = {
    1: (
        "┌───────┐",
        "│       │",
        "│   ●   │",
        "│       │",
        "└───────┘"
    ),
     2: (
        "┌───────┐",
        "│ ●     │",
        "│       │",
        "│     ● │",
        "└───────┘"
    ),
    3: (
        "┌───────┐",
        "│ ●     │",
        "│   ●   │",
        "│     ● │",
        "└───────┘"
    ),
    4: (
        "┌───────┐",
        "│ ●   ● │",
        "│       │",
        "│ ●   ● │",
        "└───────┘"
    ),
    5: (
        "┌───────┐",
        "│ ●   ● │",
        "│   ●   │",
        "│ ●   ● │",
        "└───────┘"
    ),
    6: (
        "┌───────┐",
        "│ ●   ● │",
        "│ ●   ● │",
        "│ ●   ● │",
        "└───────┘"
    ),
     
}


def roll_dice():
    time.sleep(1)
    result = random.randint(1, 6)
    dice_label.config(text="\n".join(dice_faces[result]))
    result_label.config(text=f"you rolled a{result} 🎲")
    
# create main window
root = tk.Tk()
root.title("Dice Rolling Simulator🎲")
root.geometry("300x300")
    
# displaying the dices face
dice_label = tk.Label(root,text="", font=("courier",20), justify="left")
dice_label.pack(pady=10)
    
# Result text
result_label = tk.Label(root, text="", font=("Helvetica", 16))
result_label.pack()
    
# Roll button
roll_button = tk.Button(root, text="Roll Dice", font=("Helvetica", 14), command=roll_dice)
roll_button.pack(pady=10)
    
# Quit button
quit_button =tk.Button(root, text="Quit", font=("Helvetica", 12), command=root.destroy)
quit_button.pack()
    
# Start GUI
root.mainloop()


    