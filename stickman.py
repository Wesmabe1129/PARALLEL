import tkinter as tk
from tkinter import messagebox

# Global variables
player1_pos = [110, 110]  # Starting position for Player 1
player2_pos = [360, 110]  # Starting position for Player 2
stickman1, stickman2 = {}, {}
keys_pressed = set()

def create_main_window():
    global main_window
    main_window = tk.Tk()
    main_window.title("Stickman 1")

    canvas = tk.Canvas(main_window, width=500, height=500, background="black")
    canvas.pack()

    # Draw Stickman 1
    canvas.create_oval(60, 60, 90, 90, fill="white")  # Head
    canvas.create_line(75, 90, 75, 140, fill="white", width=3)  # Body
    canvas.create_line(75, 100, 85, 120, fill="white", width=3)  # Left Arm
    canvas.create_line(75, 100, 95, 120, fill="white", width=3)  # Right Arm
    canvas.create_line(75, 140, 60, 170, fill="white", width=3)  # Left Leg
    canvas.create_line(75, 140, 90, 170, fill="white", width=3)  # Right Leg

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
    can2.create_oval(60, 60, 90, 90, fill="black")  # Head
    can2.create_line(75, 90, 75, 140, fill="black", width=3)  # Body
    can2.create_line(75, 100, 55, 120, fill="black", width=3)  # Left Arm
    can2.create_line(75, 100, 45, 120, fill="black", width=3)  # Right Arm
    can2.create_line(75, 140, 60, 170, fill="black", width=3)  # Left Leg
    can2.create_line(75, 140, 90, 170, fill="black", width=3)  # Right Leg

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

    # Draw Stickman 1 and 2
    stickman1 = draw_stickman(fight_canvas, player1_pos, "white")
    stickman2 = draw_stickman(fight_canvas, player2_pos, "black")

    fight_window.bind("<KeyPress>", key_press)
    fight_window.bind("<KeyRelease>", key_release)

    # Start the game loop
    game_loop()

    fight_window.mainloop()

def draw_stickman(canvas, position, color):
    """Draw a stickman in a boxing stance at the given position."""
    x, y = position
    return {
        # Head
        "head": canvas.create_oval((x, y, x + 30, y + 30), fill=color),
        # Body
        "body": canvas.create_line((x + 15, y + 30, x + 15, y + 80), fill=color, width=3),
        # Left Arm raised to guard head
        "left_arm": canvas.create_line((x + 15, y + 40, x - 10, y + 25), fill=color, width=3),
        # Right Arm raised to guard head
        "right_arm": canvas.create_line((x + 15, y + 40, x + 40, y + 25), fill=color, width=3),
        # Left Leg slightly bent forward
        "left_leg": canvas.create_line((x + 15, y + 80, x, y + 110), fill=color, width=3),
        # Right Leg slightly bent backward
        "right_leg": canvas.create_line((x + 15, y + 80, x + 30, y + 110), fill=color, width=3)
    }


def move_stickman(stickman, dx, dy):
    """Move all parts of the stickman by (dx, dy)."""
    for part in stickman.values():
        fight_canvas.move(part, dx, dy)

# def punch(stickman, arm, punch_out):
#     """Simulate a punch by moving the arm."""
#     arm_line = stickman[arm + "_arm"]
    
#     if punch_out:
#         # Extend the arm
#         if arm == "right":
#             dx, dy = (20, -20)  # Right arm punch extension
#         else:
#             dx, dy = (-20, -20)  # Left arm punch extension
#         fight_canvas.move(arm_line, dx, dy)
#     else:
#         # Retract the arm to its original position
#         original_coords = stickman[f"original_{arm}_arm"]
#         fight_canvas.coords(original_coords)

def punch(stickman, direction, opponent):
    """Perform a punch animation and check for collision."""
    arm_key = "left_arm" if direction == "left" else "right_arm"
    arm = stickman[arm_key]

    # Bend the arm
    fight_canvas.move(arm, -10 if direction == "left" else 10, -10)
    fight_window.after(100, lambda: straighten_punch(stickman, direction, opponent, arm))


def straighten_punch(stickman, direction, opponent, arm):
    """Extend the arm for a punch."""
    fight_canvas.move(arm, -10 if direction == "left" else 10, -10)
    check_collision(stickman, opponent)  # Check for collision during punch
    fight_window.after(200, lambda: retract_punch(stickman, direction, arm))


def retract_punch(stickman, direction, arm):
    """Retract the arm to its original position."""
    fight_canvas.move(arm, 20 if direction == "left" else -20, 20)


def check_collision(punching_stickman, opponent_stickman):
    """Check if the punching arm hits the opponent's head."""
    punching_arm_coords = fight_canvas.bbox(punching_stickman["right_arm"])  # Change to "left_arm" if needed
    opponent_head_coords = fight_canvas.bbox(opponent_stickman["head"])

    if punching_arm_coords and opponent_head_coords:
        overlap = (
            punching_arm_coords[2] > opponent_head_coords[0] and
            punching_arm_coords[0] < opponent_head_coords[2] and
            punching_arm_coords[3] > opponent_head_coords[1] and
            punching_arm_coords[1] < opponent_head_coords[3]
        )
        if overlap:
            # Trigger feedback for collision
            # messagebox.showinfo("Hit!", "A punch landed!")
            print("Punch landed!")  # For debugging



def game_loop():
    """Continuous game loop to process held keys."""
    # Stickman 1 controls
    if "w" in keys_pressed:
        move_stickman(stickman1, 0, -5)
    if "s" in keys_pressed:
        move_stickman(stickman1, 0, 5)
    if "a" in keys_pressed:
        move_stickman(stickman1, -5, 0)
    if "d" in keys_pressed:
        move_stickman(stickman1, 5, 0)
    if "j" in keys_pressed:
        punch(stickman1, "left", stickman2)
    if "k" in keys_pressed:
        punch(stickman1, "right", stickman2)

    # Stickman 2 controls
    if "Up" in keys_pressed:
        move_stickman(stickman2, 0, -5)
    if "Down" in keys_pressed:
        move_stickman(stickman2, 0, 5)
    if "Left" in keys_pressed:
        move_stickman(stickman2, -5, 0)
    if "Right" in keys_pressed:
        move_stickman(stickman2, 5, 0)
    if "4" in keys_pressed:
        punch(stickman2, "left", stickman1)
    if "5" in keys_pressed:
        punch(stickman2, "right", stickman1)

    # Schedule the game loop to run again
    fight_window.after(16, game_loop)  # 16ms for ~60fps

def key_press(event):
    """Add key to pressed set."""
    keys_pressed.add(event.keysym)

def key_release(event):
    """Remove key from pressed set."""
    keys_pressed.discard(event.keysym)

# Create the windows
main_window = create_main_window()
secondary_window = create_secondary_window()

# Run the application
main_window.mainloop()
