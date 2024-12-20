import tkinter as tk

window = tk.Tk()

canvas = tk.Canvas(window, width=500, height=500, background="black")
canvas.pack()

win2 = tk.Tk()

can2 = tk.Canvas(win2, width=500, height=500, background="white")
can2.pack()

rect2 = can2.create_rectangle((10, 20, 200, 100), fill="black")

# canvas.create_rectangle((left, top, right, bottom))
rect = canvas.create_rectangle((10, 20, 200, 100), fill="white")


def move_rectangle(event):
    if event.keysym == "w":  # Move up
        canvas.move(rect, 0, -20)
    elif event.keysym == "s":  # Move down
        canvas.move(rect, 0, 20)
    elif event.keysym == "a":  # Move left
        canvas.move(rect, -20, 0)
    elif event.keysym == "d":  # Move right
        canvas.move(rect, 20, 0)

    elif event.keysym == "Up":  # Move up
        can2.move(rect2, 0, -20)
    elif event.keysym == "Down":  # Move down
        can2.move(rect2, 0, 20)
    elif event.keysym == "Left":  # Move left
        can2.move(rect2, -20, 0)
    elif event.keysym == "Right":  # Move right
        can2.move(rect2, 20, 0)

def move_rectangle2(event):
    if event.keysym == "Up":  # Move up
        can2.move(rect2, 0, -20)
    elif event.keysym == "Down":  # Move down
        can2.move(rect2, 0, 20)
    elif event.keysym == "Left":  # Move left
        can2.move(rect2, -20, 0)
    elif event.keysym == "Right":  # Move right
        can2.move(rect2, 20, 0)


def click(event):
    print("Button Click!")


# canvas.tag_bind(rect, "<Button-1>", click)

canvas.bind("<Key>", move_rectangle)
can2.bind("<Key>", move_rectangle)



window.mainloop()