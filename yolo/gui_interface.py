import tkinter as tk


class MonitorGUI:

    def __init__(self, controller):
        self.window = tk.Tk()
        self.control = controller
        self.monitor = False

    def on_click_monitor(self):
        self.control.monitor_on()
        self.toggle_monitor_btn()


    def on_click_monitor_off(self):
        self.control.monitor_off()
        self.toggle_monitor_btn()

    def toggle_monitor_btn(self):
        if self.monitor:
            self.monitor = False
            self.btn_monitor['text'] = "monitor"
        else:
            self.monitor = True
            self.btn_monitor['text'] = "close"

    def set_layout(self):
        self.window.minsize(200, 200)
        self.window.grid_rowconfigure(1, weight=1)
        # window.grid_columnconfigure(0, weight=1)

        # add views
        self.content = tk.Frame(master=self.window)
        self.top_frame = tk.Frame(master=self.content)
        self.bot_frame = tk.Frame(master=self.content)

        # top frame
        self.lbl_name = tk.Label(master=self.top_frame, text="Fall Detection Monitor")
        self.lbl_b1 = tk.Label(master=self.top_frame, text=" ")
        self.lbl_status = tk.Label(master=self.top_frame, text="Status : ")
        self.lbl_status_bar = tk.Label(master=self.top_frame, text=" good ", background="green")
        self.lbl_status_bar_good = tk.Label(master=self.top_frame, text=" good ", background="green")
        self.lbl_status_bar_warn = tk.Label(master=self.top_frame, text=" warning ", background="yellow")
        self.lbl_status_bar_bad = tk.Label(master=self.top_frame, text=" bad ", background="red")

        # bot frame
        self.lbl_bot_panel = tk.Label(master=self.bot_frame, text=" ")
        self.lbl_b2 = tk.Label(master=self.bot_frame, text=" ")

        self.btn_monitor = tk.Button(master=self.bot_frame, text="monitor", command=self.on_click_monitor)

        self.content.pack()
        self.top_frame.grid(row=0, column=0)
        self.bot_frame.grid(row=1, column=0)
        self.lbl_name.grid(row=0, column=0)
        self.lbl_b1.grid(row=1, column=0)

        self.lbl_status.grid(row=2, column=0)
        self.lbl_status_bar.grid(row=2, column=1)

        self.lbl_bot_panel.grid(row=0, column=0)
        self.lbl_b2.grid(row=1, column=0)
        self.btn_monitor.grid(row=2, column=1)




    def update_status(self):
        print("updating status")

    def start_mainloop(self):
        self.window.mainloop()


