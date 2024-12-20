import tkinter as tk

def create_main_window():
    global canvas, rect
    # Create the main window
    window = tk.Tk()
    window.title("Main Window")
    
    canvas = tk.Canvas(window, width=500, height=500, background="black")
    canvas.pack()

    # Create rectangle in the main window
    rect = canvas.create_rectangle((10, 20, 200, 100), fill="white")

    return window

def create_secondary_window():
    global can2, rect2
    # Create the secondary window
    win2 = tk.Toplevel()
    win2.title("Secondary Window")

    can2 = tk.Canvas(win2, width=500, height=500, background="white")
    can2.pack()

    # Create rectangle in the secondary window
    rect2 = can2.create_rectangle((10, 20, 200, 100), fill="black")

    return win2

def move_rectangles(event):
    # Determine the movement based on the key pressed
    dx, dy = 0, 0
    x, y = 0, 0
    if event.keysym == "w":  # Move up
        dx, dy = 0, -20
    elif event.keysym == "s":  # Move down
        dx, dy = 0, 20
    elif event.keysym == "a":  # Move left
        dx, dy = -20, 0
    elif event.keysym == "d":  # Move right
        dx, dy = 20, 0
    elif event.keysym == "Up":  # Move up
        x, y = 0, -20
    elif event.keysym == "Down":  # Move down
        x, y = 0, 20
    elif event.keysym == "Left":  # Move left
        x, y = -20, 0
    elif event.keysym == "Right":  # Move right
        x, y = 20, 0

    # Move both rectangles
    canvas.move(rect, dx, dy)



    can2.move(rect2, x, y)
    

# Create the windows
main_window = create_main_window()
secondary_window = create_secondary_window()

# Bind key events to both windows
main_window.bind("<Key>", move_rectangles)
secondary_window.bind("<Key>", move_rectangles)

# Run the application
main_window.mainloop()
