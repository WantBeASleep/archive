import numpy as np
from PIL import Image as pim
from glob import glob
import os

m, n = 2, 3

def resample(m, n : int, input_path, output_path : str):
    input_image = pim.open(input_path)
    if input_image.mode != 'RGB':
        input_image = input_image.convert('RGB')

    origPicArr = np.array(input_image)
    origH, origW = origPicArr.shape[:2]
    newH, newW = origH * m // n, origW * m // n

    newPicArr = np.zeros((newH, newW, origPicArr.shape[2]), dtype=origPicArr.dtype)
    for y in range(newH):
        for x in range(newW):
            relH, relW = y * n // m, x * n // m
            newPicArr[y][x] = origPicArr[relH][relW]
    
    newPic = pim.fromarray(newPicArr)
    newPic.save(output_path)

def main():
    curdir = os.getcwd()
    for file in glob('input/*'):
        in_path = os.path.join(curdir, file)
        
        #Растяжение в M раз _1
        out_path = os.path.join(curdir, 'output/', '1_' + os.path.basename(file))
        resample(m, 1, in_path, out_path)

        # Сжатие в N раз _2
        out_path = os.path.join(curdir, 'output/', '2_' + os.path.basename(file))
        resample(1, n, in_path, out_path)

        # Resample в 2 прохода
        out_path_stage1 = os.path.join(curdir, 'output/', 'tech_' + os.path.basename(file))
        resample(m, 1, in_path, out_path_stage1)
        out_path = os.path.join(curdir, 'output/', '3_' + os.path.basename(file))
        resample(1, n, out_path_stage1, out_path)
        os.remove(out_path_stage1)

        #Resample в 1 проход
        out_path = os.path.join(curdir, 'output/', '4_' + os.path.basename(file))
        resample(m, n, in_path, out_path)
    
    
if __name__ == "__main__":
    main()

# go 