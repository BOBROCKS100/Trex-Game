import tkinter as tk
import random

# Function to get the high score from the file
def get_high_score():
    try:
        with open("high_score.txt", "r") as file:
            return int(file.read())
    except FileNotFoundError:
        return 0

# Function to set the high score in the file
def set_high_score(score):
    with open("high_score.txt", "w") as file:
        file.write(str(score))

# Create the main window
window = tk.Tk()
window.title("T-Rex Game")
window.geometry("400x400")

# Create the canvas
canvas = tk.Canvas(window, width=400, height=400)
canvas.pack()

# Create the sky
sky = canvas.create_rectangle(0, 0, 400, 300, fill="skyblue")

# Create the floor
floor = canvas.create_rectangle(0, 300, 400, 400, fill="saddlebrown")

# Create the T-Rex
trex = canvas.create_rectangle(50, 350, 100, 400, fill="green")

# Create the cacti
cacti = [canvas.create_rectangle(400, 350, 450, 400 - i*30, fill="brown") for i in range(3)]

# Create a variable to keep track of the score
score = tk.IntVar()
score.set(0)

# Create a variable to keep track of the high score
high_score = tk.IntVar()
high_score.set(get_high_score())  # Get the high score from the file

# Function to make the T-Rex jump
def jump(event):
    steps = 15  # Number of steps
    units = 10  # Units moved in each step
    delay = 33  # Delay in ms
    for _ in range(steps):  # Steps up
        if canvas.coords(trex)[1] > 50:  # Prevent the T-Rex from moving above the sky
            canvas.move(trex, 0, -units)
            window.update()
            window.after(delay)
    for _ in range(steps):  # Steps down
        if canvas.coords(trex)[3] < 350:  # Prevent the T-Rex from moving below the floor
            canvas.move(trex, 0, units)
            window.update()
            window.after(delay)

# Function to move the cacti
def move_cacti():
    for cactus in cacti:
        canvas.move(cactus, -10, 0)
        if canvas.coords(cactus)[3] < 350:  # Prevent the cactus from moving below the floor
            canvas.move(cactus, 0, 350 - canvas.coords(cactus)[3])
        if canvas.coords(cactus)[0] < 0:
            canvas.delete(cactus)
            cacti.remove(cactus)
            cacti.append(canvas.create_rectangle(400, 350, 450, 400 - random.randint(0, 2)*30, fill="brown"))
    canvas.after(100, move_cacti)

# Function to check for collision
def check_collision():
    trex_coords = canvas.coords(trex)
    for cactus in cacti:
        cactus_coords = canvas.coords(cactus)
        if trex_coords[2] >= cactus_coords[0] and trex_coords[0] <= cactus_coords[2] and trex_coords[3] >= cactus_coords[1]:
            # Check if the current score is higher than the high score
            if score.get() > high_score.get():
                high_score.set(score.get())
                set_high_score(score.get())  # Set the high score in the file
            canvas.create_text(200, 200, text="Game Over", font=("Arial", 24), fill="red")
            return
        else:
            # Increment the score and update the score label
            score.set(score.get() + 1)
    canvas.after(100, check_collision)

window.bind("<space>", jump)

# Start moving the cacti
move_cacti()

# Check for collision
check_collision()
# Function to restart the game
def restart(event):
    # Reset the T-Rex position
    canvas.coords(trex, 50, 350, 100, 400)
    
    # Reset the cacti positions
    for cactus in cacti:
        canvas.delete(cactus)
    cacti.clear()
    cacti.extend([canvas.create_rectangle(400, 350, 450, 400 - i*30, fill="brown") for i in range(3)])
    
    # Reset the score
    score.set(0)

# Bind the restart function to the left mouse click
window.bind("<Button-1>", restart)

# Start the main loop
window.mainloop()