import tkinter as tk


window = tk.Tk()

window.minsize(500,500)

window.grid_rowconfigure(1, weight=2)
#window.grid_columnconfigure(0, weight=1)

# add views
content = tk.Frame(master=window)
top_frame = tk.Frame(master=content, background="red")
bot_frame = tk.Frame(master=content, background="blue")

#top frame
lbl_name = tk.Label(master=top_frame, text="Fall Detection Monitor")
lbl_b1 = tk.Label(master=top_frame, text=" ")
lbl_status = tk.Label(master=top_frame, text="Status : ")
lbl_status_bar = tk.Label(master=top_frame, text=" good ")
#bot frame
lbl_bot_panel = tk.Label(master=bot_frame, text="bottom frame")
lbl_b2 = tk.Label(master=bot_frame, text=" ")

btn_monitor = tk.Button(master=bot_frame, text="monitor")

content.pack()
top_frame.grid(row=0,column=0)
bot_frame.grid(row=1,column=0)
lbl_name.grid(row=0,column=0)
lbl_b1.grid(row=1,column=0)
lbl_status.grid(row=2, column=1)
lbl_status_bar.grid(row=2, column=2)

lbl_bot_panel.grid(row=0, column=0)
btn_monitor.grid(row=2, column=0)

window.mainloop()

def set_layout(window):
    print("nothing")






