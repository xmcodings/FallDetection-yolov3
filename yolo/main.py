import gui_interface
import oldController
import threading

class GUIThread(threading.Thread):

    def __init__(self, name, thread_class):
        threading.Thread.__init__(self)
        self.GUI_Class = thread_class
        self.name = name


    def run(self):
        print("running ", self.name)
        self.GUI_Class.set_layout()

class DetectionThread(threading.Thread):

    def __init__(self, name, thread_class):
        threading.Thread.__init__(self)
        self.GUI_Class = thread_class
        self.name = name

    def run(self):
        print("running ", self.name)
        self.GUI_Class.start_monitor()




control = oldController.OldController()
view = gui_interface.MonitorGUI(control)

#mon = threading.Thread(target=control.start_monitor())
#mon.start()

monitor_thread = DetectionThread("monitor", control)
monitor_thread.start()

view.set_layout()


#control.start_monitor()

view.start_mainloop()


#guiThread = GUIThread("gui", view)
#guiThread.start()

