from trimesh.util import zero_pad
from PIL import Image
import numpy as np


def BMP(folder_name, Resolution,height,width,dpi,Reverse =False):
    #Takes the spacing and generate that amount of slices
    count = 0
    


    if Reverse==True:
        for z in reversed(range(0,len(Resolution)+1)):
            count+=1
            img = Image.new('1', (height, width))
            pixels = img.load()
            dpi = int(dpi)

            data = Resolution[z]
            for i in range(img.size[0]): # each list
                for j in range(img.size[1]): # each element of 
                    pixels[i, j] = int(data[i][j])

            trans_image = img.transpose(Image.Transpose.TRANSPOSE)

            flipped_image = trans_image.transpose(Image.FLIP_LEFT_RIGHT) #Flipped it to remove mirror effect
        
            flipped_image.save('./{}/example{}.bmp'.format(folder_name,count), dpi = (dpi,dpi)) 
            #img.save('./{}/example{}.bmp'.format(folder_name,z),dpi = (dpi,dpi))
        
    else:
        for z in range(0,len(Resolution)+1):
            count+=1
            img = Image.new('1', (height, width))
            pixels = img.load()
            dpi = int(dpi)

            data = Resolution[z]
            for i in range(img.size[0]): # each list
                for j in range(img.size[1]): # each element of 
                    pixels[i, j] = int(data[i][j])
        

            trans_image = img.transpose(Image.Transpose.TRANSPOSE)

            flipped_image = trans_image.transpose(Image.FLIP_LEFT_RIGHT) #Flipped it to remove mirror effect
        
            flipped_image.save('./{}/example{}.bmp'.format(folder_name,count), dpi = (dpi,dpi)) 
            #img.save('./{}/example{}.bmp'.format(folder_name,z),dpi = (dpi,dpi))




if __name__ == "__main__":  
    pass