import tkinter as tk
from tkinter import ttk
from tkinter import *
from EventNotifier import Notifier

class Gui2D(tk.Frame):
    """Class managing the display interface"""

    port_list = []
    notifier = Notifier(["Notification", "Request"])

    
    def __init__(self, master=None, scene_size=10, locator_height=2, ratio=100, request_subscriber = "", notif_subscriber = ""):
        super().__init__(master)
        self.master = master
        self.size_ratio = ratio
        self.scene_size_m = scene_size
        self.scene_size_p = self.scene_size_m*self.size_ratio
        self.locator_height_m = locator_height

        self.tag_x = StringVar()
        self.tag_y = StringVar()
        self.tag_theta = StringVar()
        self.tag_phi = StringVar()
        self.tag_x.set("x = 0.0 m")
        self.tag_y.set("y = 0.0 m")
        self.tag_theta.set("\u03B8 = 0 °")
        self.tag_phi.set("\u03C6 = 0 °")
        
        self.notifier.subscribe("Notification", notif_subscriber)
        self.notifier.subscribe("Request", request_subscriber)
        self.create_widgets()
        self.draw_canvas()
        coordinates = self.scene_size_p/2-4, self.scene_size_p/2-4, self.scene_size_p/2+4, self.scene_size_p/2+4
        self.tag = self.canvas.create_oval(coordinates, fill="Red")
    
    def create_widgets(self):
        """Function for creating all the widgets"""
        #Button quit
        self.btn_quit = Button(self.master, text="QUIT", fg="red", command=self.master.destroy)
        self.btn_quit.grid(column=0, row=0, padx=(10, 10), pady=(10, 10), columnspan=2)
        #Combobox port list
        self.combo_port = ttk.Combobox(self.master, width=15, values=self.port_list)
        self.combo_port.set("Select a port")
        self.combo_port.bind("<Button-1>", self.combo_port_selected)
        self.combo_port.grid(column=0, row=1, padx=(10, 10), pady=(10, 10))
        #Button open/close port
        self.btn_open = Button(self.master, text="Open", fg="black", width=10, command=self.btn_port_click)
        self.btn_open.grid(column=1, row=1)
        #Frame locator setup
        self.frame_setup = Frame(master=self.master, relief=GROOVE, borderwidth=5)
        self.label_setup = Label(self.frame_setup, text="Setup")
        self.label_setup.grid(column=0, row=0, padx=(10, 10), pady=(10, 5), columnspan=2)
        self.label_height = Label(self.frame_setup, text="Height (m):")
        self.label_height.grid(column=0, row=1, padx=(10, 10), pady=(5, 2), sticky=W)
        self.entry_height = Entry(self.frame_setup, width=7)
        self.entry_height.insert(10, self.locator_height_m)
        self.entry_height.grid(column=0, row=2, padx=(10, 2), pady=(2, 10), sticky=W)
        self.btn_height_set = Button(self.frame_setup, text="Set", fg="black", width=10, command=self.btn_height_set_click)
        self.btn_height_set.grid(column=1, row=2, padx=(2, 10), pady=(10, 10), sticky=W)
        self.frame_setup.grid(column=0, row=2, padx=(10, 10), pady=(10, 10), columnspan=2)
        #Frame tag
        self.frame_label_pos = Frame(master=self.master, relief=GROOVE, borderwidth=5)
        self.label_title = Label(self.frame_label_pos, text="Tag:")
        self.label_title.grid(column=0, row=0, padx=(10, 10), pady=(10, 10), columnspan=2)
        self.label_theta = Label(self.frame_label_pos, textvariable = self.tag_theta)
        self.label_theta.grid(column=0, row=1, padx=(10, 10), pady=(10, 10), sticky=W)
        self.label_phi = Label(self.frame_label_pos, textvariable = self.tag_phi)  
        self.label_phi.grid(column=1, row=1, padx=(10, 10), pady=(10, 10), sticky=W)    
        self.label_x = Label(self.frame_label_pos, textvariable = self.tag_x)
        self.label_x.grid(column=0, row=2, padx=(10, 10), pady=(10, 10), sticky=W)
        self.label_y = Label(self.frame_label_pos, textvariable = self.tag_y)  
        self.label_y.grid(column=1, row=2, padx=(10, 10), pady=(10, 10), sticky=W)
        self.frame_label_pos.grid(column=0, row=3, padx=(10, 10), pady=(10, 10), columnspan=2)
        #Canvas 2D map
        self.canvas = Canvas(self.master, bg='white', width = self.scene_size_p, height = self.scene_size_p)
        self.canvas.grid(column=2, row=0, padx=(10, 10), pady=(10, 10), columnspan=100, rowspan=100)
        
    def draw_canvas(self):
        """Function for drawing all items on the canvas"""
        # draw vertical lines, every 1m
        for i in range(self.size_ratio, self.scene_size_p, self.size_ratio):
            coordinates = i, 0, i, self.scene_size_p
            self.canvas.create_line(coordinates, fill="grey")
            self.canvas.create_text(self.scene_size_p/2, i, anchor="nw", text="{:d}m".format(int(-(i-self.scene_size_p/2)/self.size_ratio)))
        # draw horizontal lines, every 1m
        for i in range(self.size_ratio, self.scene_size_p, self.size_ratio):
            coordinates = 0, i, self.scene_size_p, i
            self.canvas.create_line(coordinates, fill="grey")
            self.canvas.create_text(i, self.scene_size_p/2, anchor="nw", text="{:d}m".format(int((i-self.scene_size_p/2)/self.size_ratio)))
        #draw dot indicating center
        coordinates = self.scene_size_p/2-4, self.scene_size_p/2-4, self.scene_size_p/2+4, self.scene_size_p/2+4
        self.canvas.create_oval(coordinates, fill="black")
    
    def set_list_port(self, port_list):
        """Function for populating the port_list combobox"""
        self.port_list = port_list
        self.combo_port["values"] = self.port_list

    def set_tag_coords(self, x , y, theta, phi):
        """Function for setting the x,y positions on label and on the canvas"""
        #update label corrdinates
        self.tag_x.set("x = {:.1f} m".format(x))
        self.tag_y.set("y = {:.1f} m".format(y))
        self.tag_theta.set("\u03B8 = {:d} °".format(theta))
        self.tag_phi.set("\u03C6 = {:d} °".format(phi))
        #update canvas
        x_p = int(x*self.size_ratio)
        y_p = int(y*self.size_ratio)
        coordinates = self.scene_size_p/2+x_p-4, self.scene_size_p/2+y_p-4, self.scene_size_p/2+x_p+4, self.scene_size_p/2+y_p+4
        self.canvas.coords(self.tag, coordinates)

    def combo_port_selected(self, event=None):
        """Callback triggered by user clicking on the port_list combobox"""
        self.notifier.raise_event("Request", "ListPortRequest", "")	
            
    def btn_port_click(self):
        """Callback triggered by user clicking on the btn_open Button"""
        if self.btn_open["text"] == "Open":
            self.notifier.raise_event("Notification", "OpenPort", self.combo_port.get())
            self.btn_open["text"] = "Close"
        else:
            self.notifier.raise_event("Notification", "ClosePort", "")
            self.btn_open["text"] = "Open"

    def btn_height_set_click(self):
        """Callback triggered by user clicking on the btn_height_set Button"""
        self.notifier.raise_event("Notification", "LocatorHeightChanged", self.entry_height.get())
    
