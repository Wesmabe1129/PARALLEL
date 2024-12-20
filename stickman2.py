import tkinter as tk
from tkinter import messagebox

# Global variables to track positions and punches
player1_pos = [110, 110]  # Starting position for Player 1
player2_pos = [360, 110]  # Starting position for Player 2
stickman1, stickman2 = [], []

def create_main_window():
    global main_window
    main_window = tk.Tk()
    main_window.title("Stickman 1")

    canvas = tk.Canvas(main_window, width=500, height=500, background="black")
    canvas.pack()

    # Draw Stickman 1
    head = canvas.create_oval(60, 60, 90, 90, fill="white")  # Head
    body = canvas.create_line(75, 90, 75, 140, fill="white", width=3)  # Body
    left_arm = canvas.create_line(75, 100, 55, 120, fill="white", width=3)  # Left Arm
    right_arm = canvas.create_line(75, 100, 95, 120, fill="white", width=3)  # Right Arm
    left_leg = canvas.create_line(75, 140, 60, 170, fill="white", width=3)  # Left Leg
    right_leg = canvas.create_line(75, 140, 90, 170, fill="white", width=3)  # Right Leg

    fight_button = tk.Button(main_window, text="Propose Fight", command=propose_fight)
    fight_button.pack()

    return main_window

def create_secondary_window():
    global secondary_window
    secondary_window = tk.Toplevel()
    secondary_window.title("Stickman 2")

    can2 = tk.Canvas(secondary_window, width=500, height=500, background="white")
    can2.pack()

    # Draw Stickman 2
    head = can2.create_oval(60, 60, 90, 90, fill="black")  # Head
    body = can2.create_line(75, 90, 75, 140, fill="black", width=3)  # Body
    left_arm = can2.create_line(75, 100, 55, 120, fill="black", width=3)  # Left Arm
    right_arm = can2.create_line(75, 100, 95, 120, fill="black", width=3)  # Right Arm
    left_leg = can2.create_line(75, 140, 60, 170, fill="black", width=3)  # Left Leg
    right_leg = can2.create_line(75, 140, 90, 170, fill="black", width=3)  # Right Leg

    return secondary_window

def propose_fight():
    response = messagebox.askyesno("Fight Proposal", "Stickman 1 is proposing a fight. Do you accept?")
    if response:
        main_window.destroy()
        start_fight_mode()

def start_fight_mode():
    global fight_window, fight_canvas, stickman1, stickman2
    fight_window = tk.Tk()
    fight_window.title("Stickman Fight - Boxing Ring")

    fight_canvas = tk.Canvas(fight_window, width=500, height=500, background="gray")
    fight_canvas.pack()

    # Draw the boxing ring
    fight_canvas.create_rectangle(50, 50, 450, 450, outline="white", width=5)
    fight_canvas.create_rectangle(100, 100, 400, 400, outline="red", width=2)

    # Draw Stickman 1
    stickman1 = draw_stickman(fight_canvas, player1_pos, "white")
    stickman2 = draw_stickman(fight_canvas, player2_pos, "black")

    fight_window.bind("<KeyPress>", handle_keypress)
    fight_window.mainloop()

def draw_stickman(canvas, position, color):
    """Draw a stickman at the given position."""
    x, y = position
    head = canvas.create_oval(x, y, x + 30, y + 30, fill=color)  # Head
    body = canvas.create_line(x + 15, y + 30, x + 15, y + 80, fill=color, width=3)  # Body
    left_arm = canvas.create_line(x + 15, y + 40, x - 5, y + 60, fill=color, width=3)  # Left Arm
    right_arm = canvas.create_line(x + 15, y + 40, x + 35, y + 60, fill=color, width=3)  # Right Arm
    left_leg = canvas.create_line(x + 15, y + 80, x, y + 110, fill=color, width=3)  # Left Leg
    right_leg = canvas.create_line(x + 15, y + 80, x + 30, y + 110, fill=color, width=3)  # Right Leg
    return [head, body, left_arm, right_arm, left_leg, right_leg]

def move_stickman(stickman, dx, dy):
    """Move all parts of the stickman by (dx, dy)."""
    for part in stickman:
        fight_canvas.move(part, dx, dy)

def punch(stickman, direction):
    """Perform a punching action."""
    arm_index = 2 if direction == "left" else 3  # Left arm: index 2, Right arm: index 3
    arm = stickman[arm_index]
    fight_canvas.move(arm, -10 if direction == "left" else 10, 0)
    fight_window.after(200, lambda: fight_canvas.move(arm, 10 if direction == "left" else -10, 0))

def handle_keypress(event):
    """Handle key presses for player actions."""
    global player1_pos, player2_pos
    key = event.keysym

    # Player 1 controls (WASD + J/K)
    if key == "w":
        move_stickman(stickman1, 0, -10)
        player1_pos[1] -= 10
    elif key == "s":
        move_stickman(stickman1, 0, 10)
        player1_pos[1] += 10
    elif key == "a":
        move_stickman(stickman1, -10, 0)
        player1_pos[0] -= 10
    elif key == "d":
        move_stickman(stickman1, 10, 0)
        player1_pos[0] += 10
    elif key == "j":
        punch(stickman1, "left")
    elif key == "k":
        punch(stickman1, "right")

    # Player 2 controls (Arrow keys + 4/5)
    if key == "Up":
        move_stickman(stickman2, 0, -10)
        player2_pos[1] -= 10
    elif key == "Down":
        move_stickman(stickman2, 0, 10)
        player2_pos[1] += 10
    elif key == "Left":
        move_stickman(stickman2, -10, 0)
        player2_pos[0] -= 10
    elif key == "Right":
        move_stickman(stickman2, 10, 0)
        player2_pos[0] += 10
    elif key == "4":
        punch(stickman2, "left")
    elif key == "5":
        punch(stickman2, "right")

# Create the windows
main_window = create_main_window()
secondary_window = create_secondary_window()

# Run the application
main_window.mainloop()
