import tkinter as tk
from tkinter import messagebox

import threading

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


def create_window_player_1():
    global window_player_1, window_player2, fight_canvas1, fight_canvas2, stickman1, stickman2
    window_player_1 = tk.Tk()
    window_player_1.title("Player 1 - Boxing Ring")

    fight_canvas1 = tk.Canvas(window_player_1, width=500, height=500, background="gray")
    fight_canvas1.pack()

    # Draw the boxing ring
    fight_canvas1.create_rectangle(50, 50, 450, 450, outline="white", width=5)
    fight_canvas1.create_rectangle(100, 100, 400, 400, outline="red", width=2)

    # Draw Stickman 1 and 2
    stickman1 = draw_stickman(fight_canvas1, player1_pos, "yellow", mirror=False)
    stickman2 = draw_stickman(fight_canvas1, player2_pos, "blue", mirror=True)

    window_player_1.bind("<KeyPress>", key_press)
    window_player_1.bind("<KeyRelease>", key_release)

    # Start the game loop
    game_loop()

    window_player_1.mainloop()


def create_window_player_2():
    global window_player_1, window_player2, fight_canvas1, fight_canvas2, stickman1, stickman2

    window_player_2 = tk.Tk()
    window_player_2.title("Player 2 - Boxing Ring")

    fight_canvas2 = tk.Canvas(window_player_2, width=500, height=500, background="gray")
    fight_canvas2.pack()

    # Draw the boxing ring
    fight_canvas2.create_rectangle(50, 50, 450, 450, outline="white", width=5)
    fight_canvas2.create_rectangle(100, 100, 400, 400, outline="red", width=2)

    # Draw Stickman 1 and 2
    stickman1 = draw_stickman(fight_canvas2, player1_pos, "yellow", mirror=False)
    stickman2 = draw_stickman(fight_canvas2, player2_pos, "blue", mirror=True)

    window_player_2.bind("<KeyPress>", key_press)
    window_player_2.bind("<KeyRelease>", key_release)

    # Start the game loop
    game_loop()

    window_player_2.mainloop()




def start_fight_mode():
    thread1 = threading.Thread(target=create_window_player_1)
    thread2 = threading.Thread(target=create_window_player_2)

    thread1.start()
    thread2.start()
    


    

def draw_stickman(canvas, position, color, mirror):
    """Draw a stickman with a bendable arm forming a 'V' shape for punching. 
    If 'mirror' is True, draw a mirrored stickman for Player 2."""
    x, y = position

    stickman = {
        "head": canvas.create_oval((x, y, x + 30, y + 30), fill=color),
        "body": canvas.create_line((x + 15, y + 30, x + 15, y + 80), fill=color, width=3),
        # Left Arm with bend (mirrored if needed)
        "left_upper_arm": canvas.create_line((x + 15, y + 40, x + 35, y + 50), fill=color, width=3) if not mirror else canvas.create_line((x + 15, y + 40, x - 5, y + 50), fill=color, width=3),
        "left_forearm": canvas.create_line((x + 35, y + 50, x + 35, y + 20), fill=color, width=3) if not mirror else canvas.create_line((x - 5, y + 50, x - 5, y + 20), fill=color, width=3),
        # Right Arm with bend (mirrored if needed)
        "right_upper_arm": canvas.create_line((x + 15, y + 40, x + 35, y + 60), fill=color, width=3) if not mirror else canvas.create_line((x + 15, y + 40, x - 5, y + 60), fill=color, width=3),
        "right_forearm": canvas.create_line((x + 35, y + 60, x + 40, y + 20), fill=color, width=3) if not mirror else canvas.create_line((x - 5, y + 60, x - 10, y + 20), fill=color, width=3),
        "left_leg": canvas.create_line((x + 15, y + 80, x, y + 110), fill=color, width=3),
        "right_leg": canvas.create_line((x + 15, y + 80, x + 30, y + 110), fill=color, width=3),
    }

    # Save original arm coordinates
    stickman["original_coords"] = {
        "left_upper_arm": canvas.coords(stickman["left_upper_arm"]),
        "left_forearm": canvas.coords(stickman["left_forearm"]),
        "right_upper_arm": canvas.coords(stickman["right_upper_arm"]),
        "right_forearm": canvas.coords(stickman["right_forearm"]),
    }
    return stickman







def move_stickman(stickman, dx, dy):
    """Move all parts of the stickman by (dx, dy)."""
    for part in stickman.values():
        fight_canvas1.move(part, dx, dy)
        fight_canvas2.move(part, dx, dy)

def punch(stickman, direction, opponent, canvas):
    """Perform a punch animation and check for collision."""
    upper_arm_key = "left_upper_arm" if direction == "left" else "right_upper_arm"
    forearm_key = "left_forearm" if direction == "left" else "right_forearm"
    
    upper_arm = stickman[upper_arm_key]
    forearm = stickman[forearm_key]
    
    dx = -20 if direction == "left" else 20  # Move horizontally
    dy = 0  # Keep it at the same vertical level
    
    # Straighten the upper arm
    canvas.coords(upper_arm, 
        canvas.coords(upper_arm)[0], canvas.coords(upper_arm)[1], 
        canvas.coords(upper_arm)[0] + dx, canvas.coords(upper_arm)[1] + dy
    )
    
    # Straighten the forearm to align with the upper arm
    canvas.coords(forearm, 
        canvas.coords(upper_arm)[2], canvas.coords(upper_arm)[3], 
        canvas.coords(upper_arm)[2] + dx, canvas.coords(upper_arm)[3] + dy
    )
    
    # Check collision
    canvas.after(100, lambda: check_collision(stickman, opponent, canvas))
    canvas.after(200, lambda: retract_punch(stickman, direction, canvas))

def retract_punch(stickman, direction, canvas):
    """Retract the arm back to its original V-shaped guarding position."""
    upper_arm_key = "left_upper_arm" if direction == "left" else "right_upper_arm"
    forearm_key = "left_forearm" if direction == "left" else "right_forearm"
    
    # Get the current body position
    body_coords = canvas.coords(stickman["body"])
    body_x, body_y = body_coords[0], body_coords[1]  # Top of the body
    
    # Define offsets for the guarding position relative to the body
    if direction == "left":
        upper_arm_offset = (0, 10, -20, 30)
        forearm_offset = (-20, 30, -20, -10)
    else:  # right
        upper_arm_offset = (0, 10, 20, 30)
        forearm_offset = (20, 30, 25, -10)

    # Calculate new positions for the upper arm and forearm
    upper_arm_coords = [
        body_x + upper_arm_offset[0], body_y + upper_arm_offset[1],
        body_x + upper_arm_offset[2], body_y + upper_arm_offset[3]
    ]
    forearm_coords = [
        body_x + forearm_offset[0], body_y + forearm_offset[1],
        body_x + forearm_offset[2], body_y + forearm_offset[3]
    ]
    
    # Reset the arm positions
    canvas.coords(stickman[upper_arm_key], *upper_arm_coords)
    canvas.coords(stickman[forearm_key], *forearm_coords)






def check_collision(punching_stickman, opponent_stickman, canvas):
    """Check if the punching arm hits the opponent's head."""
    punching_arm_coords = canvas.bbox(punching_stickman["left_forearm"])  # Change to "left_arm" if needed
    opponent_head_coords = canvas.bbox(opponent_stickman["head"])

    if punching_arm_coords and opponent_head_coords:
        overlap = (
            punching_arm_coords[2] > opponent_head_coords[0] and
            punching_arm_coords[0] < opponent_head_coords[2] and
            punching_arm_coords[3] > opponent_head_coords[1] and
            punching_arm_coords[1] < opponent_head_coords[3]
        )
        if overlap:
            print("Punch landed!")  # For debugging or triggering events


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
        punch(stickman1, "left", stickman2, canvas=fight_canvas1)
        punch(stickman1, "left", stickman2, canvas=fight_canvas2)
    if "k" in keys_pressed:
        punch(stickman1, "right", stickman2, canvas=fight_canvas1)
        punch(stickman1, "right", stickman2, canvas=fight_canvas2)

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
        punch(stickman2, "left", stickman1, canvas=fight_canvas1)
        punch(stickman2, "left", stickman1, canvas=fight_canvas2)
    if "5" in keys_pressed:
        punch(stickman2, "right", stickman1, canvas=fight_canvas1)
        punch(stickman2, "right", stickman1, canvas=fight_canvas2)

    # Schedule the game loop to run again
    fight_canvas1.after(16, game_loop)  # 16ms for ~60fps
    # fight_canvas2.after(16, game_loop)  # 16ms for ~60fps



def key_press(event):
    """Add key to pressed set."""
    keys_pressed.add(event.keysym)

def key_release(event):
    """Remove key from pressed set."""
    keys_pressed.discard(event.keysym)




# Create the windows
main_window = create_main_window()
# secondary_window = create_secondary_window()

# Run the application
main_window.mainloop()
