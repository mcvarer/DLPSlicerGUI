from distutils.command.build_ext import show_compilers
from gettext import npgettext
from hashlib import new
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
from contextlib import contextmanager
import shutil

import os
from threading import Thread, Lock
import time


import pygame

from slicing.slice import getSlices
from slicing.convertobmp import BMP


from tkinter.filedialog import FileDialog

class GUI:

    def __init__(self):
        
        self.firstTime = True
        self.firstTime2 = True
        #Default Variables
        self.width = 1024
        self.height = 768
        
        
        #Initialize main window
        self.root = Tk()
        self.root.title('DLP Slicer')
        self.root.geometry("1920x1080")
        self.wWidth = 1920
        self.wHeight = 1080
        self.sliceState = False

        self.myLabel = Label(text= "DLP Slicer", font='roboto 20 bold', foreground='Dark blue')
        self.myLabel.place(relx=0.5, rely= 15/self.wHeight, anchor=CENTER)

        #File Upload button
        self.file = ''
        self.mymesh = None
        self.dlbtn = Button(self.root,text ='Choose File ',command = lambda:self.open_file_async())


        self.dlbtn.place(x=20, y=20)

        #Slice button
        self.Slice = Button(self.root, text="Slice",padx = 15, pady = 5, command=self.myClick)
        self.Slice.place(relx=0.5, rely =  700/self.wHeight, anchor=CENTER)

        self.my_menu = Menu(self.root)
        self.root.config(menu=self.my_menu)
        self.child = None

        # Lock for file opening 
        self.file_open_lock = Lock()



        self.file_menu = Menu(self.my_menu)

        self.my_menu.add_cascade(label="File", menu=self.file_menu) #File option
        self.file_menu.add_command(label="Save", command=self.save)
        self.file_menu.add_separator()#Creates bar
        self.file_menu.add_command(label="Load", command=self.load)
        self.file_menu.add_separator()#Creates bar
        self.file_menu.add_command(label="New", command=new)
        self.file_menu.add_separator()#Creates bar
        self.file_menu.add_command(label="Exit", command=self.exitnow)

        #Submenu
        self.setting_menu = Menu(self.file_menu,tearoff=0)
        self.my_menu.add_cascade(label='Settings', menu=self.setting_menu)
        self.setting_menu.add_command(label="Resolution", command= self.Resolutions)
        self.setting_menu.add_command(label="Advanced Settings",command= self.Settings)
        #
        #Disable slice button
        self.Slice["state"] = 'disabled'




        

        #photo
        self.photo = PhotoImage(file="Gui\ImageSTL\defaultimage.png")
        self.PhotoImage = self.photo.subsample(2,2)
        self.desired_image = Button(self.root, image = self.PhotoImage).place(relx= 0.5, rely= 200/self. wHeight, anchor=CENTER)


        #Scale
        
        voxelSizeLabel = Label(self.root,text="Unit per Stl Unit :")
        voxelSizeLabel.place(relx = .45, rely=.45)
        self.voxelSize = StringVar()
        self.voxelSize.set(1)
        voxelSizeEntry= Entry(self.root,width=20,text= self.voxelSize)
        voxelSizeEntry.place(relx = .52 , rely = .45)







        #main loop
        self.root.mainloop()


    def open_file_async(self):
        thread = Thread(target=self.open_file, daemon=True)
        thread.start()



    def open_file(self):
        self.clickSound()

        acquired = self.file_open_lock.acquire(blocking=False)
        
        if not acquired:
            return
        
        try:
            file_path = askopenfile(mode='r', filetypes=[('3D Object File', '*jpeg *stl *png')])
            if file_path is not None:
                self.file = r"{}".format(file_path.name)
                print(self.file)

            print('load trimesh')
            self.mymesh =trimesh.load_mesh('{}'.format(self.file))
            print('finish loading')
            print(self.mymesh.extents)

            print('Changing default image')

            self.stlImage(self.file)
        finally:
            self.file_open_lock.release()
            self.Slice["state"] = 'normal'





    def stlImage(self,name):
        title = name.split("/")[-1]
        vertices = self.mymesh.vertices
        array = np.array(vertices)
        minZ = np.min(array[:,2])
        maxZ = np.max(array[:,2])
        print(title)





        slices = []

        for z in np.linspace(minZ, maxZ, 150):
            l = self.mymesh.section(plane_normal=[0,0,-1],plane_origin=[0, 0, z]
                                )

            slices.append(l)
            
        

        
        slices = [slice for slice in slices if slice is not None]


        fig = plt.figure()
        ax = fig.add_subplot(projection='3d')
        print('figure')



        for idx, slice in enumerate(slices):
            x = [slice.vertices[:,0]]
            y = [slice.vertices[:,1]]
            z = [slice.vertices[:,2]]




            ax.scatter(x, y, z,alpha=.5,linewidths=.5, s=1,marker='D',facecolors= 'dimgray') #Alpha is transparency


        ax.grid(False)
        ax.set_title(title)
        ax.set_zlabel('Z')
        fig.tight_layout()
        #Saves this into ImageSTL
        plt.savefig('Gui\\ImageSTL\\file.png')
        print('saved')
        self.photo = PhotoImage(file="Gui\\ImageSTL\\file.png")
        self.PhotoImage = self.photo.subsample(2,2)
        self.desired_image = Button(self.root, image = self.PhotoImage,command=self.show).place(relx= 0.5, rely= 200/self. wHeight, anchor=CENTER)
        


        
        print('done')


    def myClick(self):
        self.clickSound()
        print('Clicked')
        print(self.Slice)

        self.Slice["state"] = 'disabled'

        self.zip_window = Toplevel(self.root)
        self.zip_window.geometry("780x200")
        self.options = ["mm", "in", "ft", "m"]
        self.variable = StringVar(self.zip_window)
        self.variable.set(self.options[0]) # default value

        self.w = OptionMenu(self.zip_window, self.variable, *self.options)
        self.w.place(relx=0.5, rely=0.35, anchor=CENTER)


        self.zip_label = Label(self.zip_window, text="Enter file name: ")
        self.zip_label.place(relx= 0.165, rely = 0.5, anchor=CENTER)
        self.zip_input = Entry(self.zip_window)
        
        self.zip_input.place(relx= 0.3, rely = 0.5, anchor=CENTER)

        self.numSlice_label = Label(self.zip_window, text="Enter Number Of Slices: ")
        self.numSlice_label.place(relx= 0.65, rely = 0.5, anchor=CENTER)
        self.numSlice = IntVar()
        self.numSlice.set(100)
        self.numSlice_input = Entry(self.zip_window,text =self.numSlice)
        self.numSlice_input.place(relx= 0.81, rely = 0.5, anchor=CENTER)

        self.slice_button2 = Button(self.zip_window, text="Slice", padx=20, pady=0, command=self.progress_async)
        self.slice_button2.place(relx=0.5, rely=0.6, anchor=CENTER)

        self.zip_window.protocol('WM_DELETE_WINDOW',self.enable_slice)
        print(self.width, self.height)


            
        


        

    def our_command(self):
        pass

    def file_menu(self):
        pass

    def save():
        pass
    def enable_slice (self):
        self.Slice["state"] = "normal"
        self.zip_window.destroy()
        
    def exitnow(self):
        self.clickSound()

        child = Toplevel(self.root)
        
        child.geometry("250x150")
        exit_label= Label(child, text="Do you want save changes?", font = ('TkDefaultFont', 10))
        exit_label.pack()

        save_button = Button(child, text= "Save", command=self.save) #should save to a file?
        save_button.place(x=42, y=50)
        dont_save_button = Button(child, text= "Don't save", command=self.root.quit)
        dont_save_button.place(x=86, y=50)
        cancel_button = Button(child, text= "Cancel", command=child.destroy)
        cancel_button.place(x=160, y=50)
    
    def load(self):
        pass
    @staticmethod
    def clickSound():
        pygame.init()
        pygame.mixer.init()
        sound = pygame.mixer.Sound("Gui\Music\click.wav")
        sound.set_volume(0.5)
        sound.play() 



    def new(self):
        a = GUI()
        self.root.quit

    def show(self):
        print('Start')
        self.mymesh.show()

   
    def get_res(self,stl_unit_resolution):
        print('getting resolution')
        Resolution = getSlices(self.mymesh, self.numSlice.get(),stl_unit_resolution= stl_unit_resolution, scale=(1,1,1))
        print('done')
        return Resolution
        

    def progress_async(self):
        myThread = Thread(target=self.progressbar,daemon=True)
        myThread.start()
 




    def progressbar(self):
        self.slice_button2['state'] = 'disabled'
        pb1 = Progressbar(self.zip_window, orient=HORIZONTAL, length=300, mode='determinate')
        pb1.place(relx=0.5, rely=0.8, anchor=CENTER)


        stl_unit_resolution = float(self.voxelSize.get())

        
        try:
            dpi = self.dpi.get()
            height = self.height.get()
            width = self.width.get()
        except:
            dpi = 2580
            height = 768
            width = 1024

        print(self.zip_input.get())

        

       
        
        self.zip_window.update_idletasks()
        pb1['value'] += 10
        time.sleep(1)
        print(type(self.numSlice.get()))
        print(stl_unit_resolution)
        Resolution = getSlices(self.mymesh, self.numSlice.get(),stl_unit_resolution= stl_unit_resolution, scale=(1,1,1))
        try:

            folder_name = self.zip_input.get()
            folder_name = 'FinishedWorks\{}'.format(folder_name)
            if not os.path.isdir(folder_name):
                os.makedirs(folder_name)
        except:
            raise Exception("You need to put enter a file name")
            #Put error message box for gui
            

        self.zip_window.update_idletasks()
        pb1['value'] += 10
        time.sleep(1)
       

        BMP(folder_name, Resolution,height,width, dpi=dpi)

            
        

        



        self.zip_window.update_idletasks()
        pb1['value'] += 10
        time.sleep(1)

        

        shutil.make_archive(folder_name, 'zip', '.\FinishedWorks\{}'.format(folder_name))


        


        pb1.destroy()
    
        slice_complete = Label(self.zip_window, text='Slicing has been completed!', foreground='green')
        slice_complete.place(relx=0.5, rely=0.9, anchor=CENTER)
        self.slice_button2['state']= 'normal'

    def e(self):
        pass

    def Settings(self):
        setWindow= Toplevel()
        setWindow.geometry("400x200")
        setWindow.title('Advanced Settings')
    
        



   


        setWindow.protocol('WM_DELETE_WINDOW')




    def Resolutions(self):
        
        
        
        
        resWindow= Toplevel()
        resWindow.geometry("400x200")
        resWindow.title('Select Resolution')

        if self.firstTime == True:

            self.width = IntVar()
            self.width.set(1024)
            
        
            self.height =IntVar()
            self.height.set(768)

            self.dpi = IntVar()
            self.dpi.set(2580)
        
    

        resolution = Label(resWindow, text="Resolution: ")
        resolution.place(relx=0.250, rely=100/200, anchor=CENTER)
        self.reswidth = Entry(resWindow, width=10, text=self.width)
        self.reswidth.place(relx=0.42, rely = 200/400, anchor=CENTER)

        x = Label(resWindow, text='X')
        x.place(relx=0.53, rely=100/200, anchor=CENTER)

      
        self.resheight = Entry(resWindow, width=10, text=self.height)
        self.resheight.place(relx=0.65, rely = 200/400, anchor=CENTER)

        dpiLabel = Label(resWindow, text="DPI: ")
        dpiLabel.place(relx=0.25, rely=150/200, anchor=CENTER)

        self.resdpi = Entry(resWindow,width=10, text=self.dpi)
        self.resdpi.place(relx=.34,rely=140/200)



        self.firstTime = False

        resWindow.protocol('WM_DELETE_WINDOW')


# class runGUI(GUI):
#     def __init__(self):
#         super().__init__()
#         print(self.root)
#         self.clickSound()


if __name__ == "__main__":  
    g= GUI()

 