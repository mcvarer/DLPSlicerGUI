from trimesh.util import zero_pad
from PIL import Image
import numpy as np



def BMP(folder_name, Resolution,height,width,dpi,Reverse =False):
    #Takes the spacing and generate that amount of slices
    count = 0
    print(len(Resolution))

    gWidth = width/2
    gHeight = height/2

    

    

    if Reverse==True:
        for z in reversed(range(0,len(Resolution)+1)):
            count+=1
            Size = np.zeros(height,width,1)
            for rows in range(0,Resolution):
                for column in range(0,Resolution):
                    if Resolution[rows][column] == 0:
                        Size[rows][height]= 255
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
        try:
            for z in range(0,len(Resolution)):
                count+=1
                Size = np.zeros((width,height)).tolist()
                img = Image.new('1', (width, height))
                pixels = img.load()
                dpi = int(dpi)


                currentRes = Resolution[z].tolist()
                print(len(Resolution[z]),len(Resolution[0][z]))

            
                pointList = []
                print(len(Size))
                for y in range(0,len(currentRes)):
                    for x in range(0,len(currentRes[0])):
                        if currentRes[y][x]==True:
                            pointList.append((y+int(gWidth-10),x+int(gHeight-10))) 
                            #IF object is too big, it might mess with the centering.
                
                for i in pointList:
                    Size[i[0]][i[1]]= 255
                

                            
            

                data = Size
                for i in range(img.size[0]): # each list
                    for j in range(img.size[1]): # each element of 
                        pixels[i, j] = int(data[i][j])
            
                img.save('./{}/example{}.bmp'.format(folder_name,count), dpi = (dpi,dpi)) 
                #img.save('./{}/example{}.bmp'.format(folder_name,z),dpi = (dpi,dpi))
        except:
            pass

            




if __name__ == "__main__":  
    print(np.zeros((1200,100,1)))
    