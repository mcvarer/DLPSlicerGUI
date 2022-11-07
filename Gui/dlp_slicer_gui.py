from gettext import npgettext
from os import name
from tkinter import *
from tkinter.ttk import Progressbar
import numpy as np
import matplotlib.pyplot as plt
import trimesh as trimesh
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkinter.filedialog import askopenfile 
from PIL import ImageTk, Image
from createImage import *
import time



import pygame
from time import sleep



root = Tk()
root.title("DLP Slicer")
root.geometry("1920x1080")
wWidth = 800
wHeight = 1080
myLabel = Label(text= "DLP Slicer")
myLabel.place(relx=0.5, rely= 15/wHeight, anchor=CENTER)


# Create a photoimage object of the image in the path
photo = PhotoImage(file = "./Gui/ImageSTL/defaultimage.png")

# Resize image to fit on button
photoimage = photo.subsample(2, 2)

# Position image on button
desired_image = Button(root, image = photoimage,).place(relx= 0.5, rely= 100/wHeight, anchor=CENTER)

file = None
zip_window = None

#Contains features for the exit window
def exit():
    print(type(root))
    child = Toplevel(root)
    
    child.geometry("150x150")
    exit_label= Label(child, text="Do you want save changes?", font = ('TkDefaultFont', 10))
    exit_label.pack()

    save_button = Button(child, text= "Save", command=save) #should save to a file?
    save_button.place(x=42, y=50)
    dont_save_button = Button(child, text= "Don't save", command=root.quit)
    dont_save_button.place(x=86, y=50)
    cancel_button = Button(child, text= "Cancel", command=child.destroy)
    cancel_button.place(x=160, y=50)

#Contains the save button's functionality
def save():
	save_window = Toplevel(root)
	save_window.geometry("500x400")
	file_name_label = Label(save_window, text= "Enter file name: ")
	file_name_label.place(x=95, y=100)
	file_name = Entry(save_window, width=20)
	file_name.place(x= 185, y=100)
	file_name_button = Button(save_window, text= "Save", padx = 20, pady=-10)
	file_name_button.place(x = 300, y = 100)#open file
def open_file():
    global file
    file_path = askopenfile(mode='r', filetypes=[('3D Object File', '*jpeg *stl *png')])
    if file_path is not None:
        file = r"{}".format(file_path.name)

    stlImage(file)
    #image frame

    # Create a photoimage object of the image in the path
    photo = PhotoImage(file = "./ImageSTL/file.png")

    # Resize image to fit on button
    photoimage = photo.subsample(2, 2)

    # Position image on button
    global desired_image
    desired_image = Button(root, image = photoimage).place(relx= 0.5, rely= 100/wHeight, anchor=CENTER)


    
#slice functionality
def myClick():
    pygame.init()
    pygame.mixer.init()
    sound = pygame.mixer.Sound("Gui\Music\click.wav")
    sound.set_volume(0.5)
    sound.play() 


    #disable the slice button when the slice button is clicked
    if Slice["state"] == "normal":
        Slice["state"] = "disabled"
    global zip_window
    zip_window = Toplevel(root)
    zip_window.geometry("780x200")

    options = ["mm", "in", "ft", "m"]
    variable = StringVar(zip_window)
    variable.set(options[0]) # default value

    w = OptionMenu(zip_window, variable, *options)
    w.place(relx=0.5, rely=0.35, anchor=CENTER)


    zip_label = Label(zip_window, text="Enter file name: ")
    zip_label.place(relx= 0.165, rely = 0.5, anchor=CENTER)
    zip_input = Entry(zip_window)
    zip_input.place(relx= 0.3, rely = 0.5, anchor=CENTER)

    dpi_label = Label(zip_window, text="Enter DPI: ")
    dpi_label.place(relx= 0.695, rely = 0.5, anchor=CENTER)
    dpi_input = Entry(zip_window)
    dpi_input.place(relx= 0.81, rely = 0.5, anchor=CENTER)

    slice_button2 = Button(zip_window, text="Slice", padx=20, pady=0, command=progressbar)
    slice_button2.place(relx=0.5, rely=0.6, anchor=CENTER)

    zip_window.protocol('WM_DELETE_WINDOW', enable_slice)
    e.get()

#pro5i4u563ywq2f    WDgress bar
def progressbar():#Where function would be used
    sound = pygame.mixer.Sound("Gui\Music\click.wav")
    sound.set_volume(0.5)
    sound.play() 

    pb1 = Progressbar(zip_window, orient=HORIZONTAL, length=300, mode='determinate')
    pb1.place(relx=0.5, rely=0.8, anchor=CENTER)



    zip_window.update_idletasks()
    pb1['value'] += 50
    time.sleep(1)
    scale = v1.get()
    



    zip_window.update_idletasks()
    pb1['value'] += 50
    time.sleep(1)

    pb1.destroy()
 
    slice_complete = Label(zip_window, text='Slicing has been completed!', foreground='green')
    slice_complete.place(relx=0.5, rely=0.9, anchor=CENTER)

#function to re-enable the slice button
def enable_slice():
    Slice["state"] = "normal"
    zip_window.destroy()

# #Input boxes and labels for width, x-scale, height, y-scale, slices, and z-scale
v1 = IntVar()
v1.set(100)
voxel_label = Label(root, text="Voxel size: ")
voxel_label.place(relx=0.387, rely=200/wHeight, anchor=CENTER)
voxel = Entry(root, width=10, text=v1)
voxel.place(relx=0.42, rely = 200/wHeight, anchor=CENTER)

v2 = IntVar()
v2.set(1)
x_scale_label = Label(root, text="X-Scale: ")
x_scale_label.place(relx=0.39, rely=250/wHeight, anchor=CENTER)
x_scale = Entry(root, width=10, text=v2)
x_scale.place(relx=0.42, rely = 250/wHeight, anchor=CENTER)

v3 = IntVar()
v3.set(1)
pitch_label = Label(root, text="Pitch: ")
pitch_label.place(relx=0.474, rely=200/wHeight, anchor=CENTER)
pitch = Entry(root, width=10, text=v3)
pitch.place(relx=0.5, rely = 200/wHeight, anchor=CENTER)

v4 = IntVar()
v4.set(1)
y_scale_label = Label(root, text="Y-Scale: ")
y_scale_label.place(relx=0.47, rely=250/wHeight, anchor=CENTER)
y_scale = Entry(root, width=10, text=v4)
y_scale.place(relx=0.5, rely = 250/wHeight, anchor=CENTER)

v5 = IntVar()
v5.set(100)
slices_label = Label(root, text="Slices: ")
slices_label.place(relx=0.553, rely=200/wHeight, anchor=CENTER)
slices = Entry(root, width=10, text=v5)
slices.place(relx=0.58, rely=200/wHeight, anchor=CENTER)

v6 = IntVar()
v6.set(1)
z_scale_label = Label(root, text="Z-Scale: ")
z_scale_label.place(relx=0.55, rely=250/wHeight, anchor=CENTER)
z_scale = Entry(root, width=10, text=v6)
z_scale.place(relx=0.58, rely=250/wHeight, anchor=CENTER)

# #menu bar
my_menu = Menu(root)

root.config(menu=my_menu)

def our_command():
    pass
file_menu = Menu(my_menu)

my_menu.add_cascade(label="File", menu=file_menu) #File option

file_menu.add_command(label="New...", command=our_command)
file_menu.add_separator()#Creates bar
file_menu.add_command(label="Exit",command=exit)

# #Choose file button
dlbtn = Button(
    root, 
    text ='Choose File ', 
    command = lambda:open_file()
    ) 


dlbtn.place(x=20, y=20)
# #create and edit menu item.
# edit_menu = Menu(my_menu)
# my_menu.add_cascade(label='Settings', menu = edit_menu)
# edit_menu.add_command(label='Settings1', command=our_command)
# edit_menu.add_command(label='Settings2', command=root.quit)

# #Slice button
Slice = Button(root, text="Slice",padx = 15, pady = 5, command=myClick)
Slice.place(relx=0.5, rely = 300/wHeight, anchor=CENTER)

# #upload button
print(zip_window)
root.mainloop()