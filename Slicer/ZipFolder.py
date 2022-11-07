#Zipping file
import shutil


def Zip(dir_name, output_filename):
    shutil.make_archive(output_filename, 'zip', dir_name)



#Zip('D:\PyVox\HQCUBE','')