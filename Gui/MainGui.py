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
from createImage import *
import time


import pygame
from time import sleep


class GUI:

    def __init__(self):
        
        #Initialize main window
        self.root = Tk()
        self.root.title('DLP Slicer')
        self.root.geometry("1920x1080")
        self.wWidth = 1920
        self.wHeight = 1080

        self.myLabel = Label(text= "DLP Slicer", font='roboto 20 bold', foreground='Dark blue')
        self.myLabel.place(relx=0.5, rely= 15/self.wHeight, anchor=CENTER)

        #File Upload button
        self.file = ''
        self.mymesh = None
        self.dlbtn = Button(self.root,text ='Choose File ',command = lambda:self.open_file())


        self.dlbtn.place(x=20, y=20)

        #Slice button
        self.Slice = Button(self.root, text="Slice",padx = 15, pady = 5, command=self.myClick)
        self.Slice.place(relx=0.5, rely =  700/self.wHeight, anchor=CENTER)

        self.my_menu = Menu(self.root)
        self.root.config(menu=self.my_menu)
        self.child = None


        self.file_menu = Menu(self.my_menu)

        self.my_menu.add_cascade(label="File", menu=self.file_menu) #File option
        self.file_menu.add_command(label="Save", command=self.save)
        self.file_menu.add_separator()#Creates bar
        self.file_menu.add_command(label="Load", command=self.load)
        self.file_menu.add_separator()#Creates bar
        self.file_menu.add_command(label="New", command=new)
        self.file_menu.add_separator()#Creates bar


        self.file_menu.add_command(label="Exit", command=self.exitnow)
        

        #photo
        self.photo = PhotoImage(file="Gui\ImageSTL\defaultimage.png")
        self.PhotoImage = self.photo.subsample(2,2)
        self.desired_image = Button(self.root, image = self.PhotoImage,).place(relx= 0.5, rely= 200/self. wHeight, anchor=CENTER)
        

        



        






        self.root.mainloop()


    def open_file(self):
        self.clickSound()
        
        file_path = askopenfile(mode='r', filetypes=[('3D Object File', '*jpeg *stl *png')])
        if file_path is not None:
            self.file = r"{}".format(file_path.name)
            print(self.file)

        print('load trimesh')
        self.mymesh =trimesh.load_mesh('{}'.format(self.file))
        print('finish loading')
        print(self.mymesh.extents())



    def stlImage(self,name):
        mymesh = trimesh.load_mesh('{}'.format(name))
        title = name.split("/")[-1]
        vertices = mymesh.vertices
        array = np.array(vertices)
        minZ = np.min(array[:,2])
        maxZ = np.max(array[:,2])
        print(title)





        slices = []

        for z in np.linspace(minZ, maxZ, 100):
            l = mymesh.section(plane_normal=[0,0,-1],plane_origin=[0, 0, z]
                                )

            slices.append(l)
            
        

        
        slices = [slice for slice in slices if slice is not None]


        fig = plt.figure()
        ax = fig.add_subplot(projection='3d')



        for idx, slice in enumerate(slices):
            x = [slice.vertices[:,0]]
            y = [slice.vertices[:,1]]
            z = [slice.vertices[:,2]]




            ax.scatter(x, y, z,alpha=.04,linewidths=.5, s=1,marker='D',facecolors= 'dimgray') #Alpha is transparency


        ax.grid(False)
        ax.set_title(title)
        ax.set_zlabel('Z')
        fig.tight_layout()
        #Saves this into ImageSTL
        plt.savefig('./ImageSTL/file.png')
        print('done')

    def myClick(self):
        self.clickSound()
        print('Clicked')

    def our_command(self):
        pass

    def file_menu(self):
        pass

    def save():
        pass
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


# class runGUI(GUI):
#     def __init__(self):
#         super().__init__()
#         print(self.root)
#         self.clickSound()
        
        

        

    

        
        
  
        

        

        









if __name__ == "__main__":  
    g= GUI()

 