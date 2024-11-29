import numpy as np
from PIL import Image as pim
from glob import glob
import os

def microchel(x, y, arr):
    mat = np.sum(arr[y-1:y+1, x:x+2]) // 4
    disp = (arr[y][x] - mat) ** 2 + (arr[y][x+1] - mat) ** 2 + (arr[y-1][x] - mat) ** 2 + (arr[y-1][x+1] - mat) ** 2
    return mat, disp

def macrochel(x, y, arr):
    mat, disp = microchel(x-1, y+1, arr)

    tmat, tdisp = microchel(x, y+1, arr)
    if tdisp < disp:
        disp = tdisp
        mat = tmat

    tmat, tdisp = microchel(x-1, y, arr)
    if tdisp < disp:
        disp = tdisp
        mat = tmat

    tmat, tdisp = microchel(x, y, arr)
    if tdisp < disp:
        disp = tdisp
        mat = tmat

    return mat
    

def plavycheeWinda(img):
    inptArr = np.array(img)
    h, w = inptArr.shape
    newArr = np.zeros((h, w), dtype=np.uint8)
    for y in range (1, h-2):
        for x in range (1, w-2):
            newArr[y][x] = macrochel(x, y, inptArr)
    
    return pim.fromarray(newArr, mode='L')

def toSRGB(imgname):
    input_image = pim.open(imgname).convert('RGB')
    origPicArr = np.array(input_image)
    newPicArr = np.zeros((origPicArr.shape[0], origPicArr.shape[1]), dtype=origPicArr.dtype)
    
    for y in range(origPicArr.shape[0]):
        for x in range(origPicArr.shape[1]):
            newPicArr[y][x] = np.mean(origPicArr[y][x])

    return pim.fromarray(newPicArr, mode='L')


def main():
    inptdir = os.path.join(os.path.dirname(__file__), 'input/*')
    for filename in glob(inptdir):
        polyTon = toSRGB(filename)
        res = plavycheeWinda(polyTon)
        res.save(os.path.join(os.path.dirname(__file__), 'output', os.path.splitext(os.path.basename(filename))[0] + '.bmp'))

if __name__ == "__main__":
    main()
