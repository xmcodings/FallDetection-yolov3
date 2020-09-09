import live_yolo_opencv as yolocv
import cv2
import tkinter as tk


def update_status(input):
    print("updating status")
    if input == 1:
        lbl_status_bar_good["text"] = "bad"
    else:
        lbl_status_bar_good["text"] = "good"

def on_click_monitor():
    print("clicked!")


def toggle_monitor_btn():
    global monitor
    if monitor:
        btn_monitor['text'] = "monitor"
        monitor = False
    else:
        btn_monitor['text'] = "close"
        monitor = True


if __name__ == "__main__":
    window = tk.Tk()
    monitor = False
    cap = cv2.VideoCapture()

    window.minsize(200, 200)
    window.grid_rowconfigure(1, weight=1)
    # window.grid_columnconfigure(0, weight=1)

    # add views
    content = tk.Frame(master=window)
    top_frame = tk.Frame(master=content)
    bot_frame = tk.Frame(master=content)

    # top frame
    lbl_name = tk.Label(master=top_frame, text="Fall Detection Monitor")
    lbl_b1 = tk.Label(master=top_frame, text=" ")
    lbl_status = tk.Label(master=top_frame, text="Status : ")
    lbl_status_bar = tk.Label(master=top_frame, text=" good ", background="green")
    lbl_status_bar_good = tk.Label(master=top_frame, text=" good ", background="green")
    lbl_status_bar_warn = tk.Label(master=top_frame, text=" warning ", background="yellow")
    lbl_status_bar_bad = tk.Label(master=top_frame, text=" bad ", background="red")

    # bot frame
    lbl_bot_panel = tk.Label(master=bot_frame, text=" ")
    lbl_b2 = tk.Label(master=bot_frame, text=" ")

    btn_monitor = tk.Button(master=bot_frame, text="monitor", command=on_click_monitor)

    content.pack()
    top_frame.grid(row=0, column=0)
    bot_frame.grid(row=1, column=0)
    lbl_name.grid(row=0, column=0)
    lbl_b1.grid(row=1, column=0)

    lbl_status.grid(row=2, column=0)
    lbl_status_bar.grid(row=2, column=1)

    lbl_bot_panel.grid(row=0, column=0)
    lbl_b2.grid(row=1, column=0)
    btn_monitor.grid(row=2, column=1)
    window.after(0, update_status())

