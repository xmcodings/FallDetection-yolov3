import tkinter as tk



window = tk.Tk()
window.title("fall alarm system")
window.minsize(500,600)
window.rowconfigure([0, 1], minsize=10)
window.columnconfigure([0, 1, 2, 3, 4], minsize=10)


def center(win):
    # Call all pending idle tasks - carry out geometry management and redraw widgets.
    win.update_idletasks()
    # Get width and height of the screen
    width = win.winfo_width()
    height = win.winfo_height()
    # Calculate geometry
    x = (win.winfo_screenwidth() // 2) - (width // 2)
    y = (win.winfo_screenheight() // 2) - (height // 2)
    # Set geometry
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))

def create_layout(win):

    top_frame = tk.Frame()

    lbl_title = tk.Label(text = 'Fall Detect System')
    lbl_title.grid(row = 1, column = 0)




center(window)
create_layout(window)




window.mainloop()







