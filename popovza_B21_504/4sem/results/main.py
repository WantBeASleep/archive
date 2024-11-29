import numpy as np
from PIL import Image as pim
from glob import glob
import os
import math

def grac(img):
    inpt = np.array(img, dtype=np.int64)
    h, w = inpt.shape
    gximg = np.zeros((h, w), dtype=np.uint64)
    gyimg = np.zeros((h, w), dtype=np.uint64)
    gimg = np.zeros((h, w), dtype=np.uint64)

    maxgx, maxgy, maxg = 0, 0, 0

    for y in range(1, h-1):
        for x in range(1, w-1):
            gximg[y, x] = np.abs(np.sum(inpt[y-1, x-1:x+2]) - np.sum(inpt[y+1, x-1:x+2]))
            gyimg[y, x] = np.abs(np.sum(inpt[y-1:y+2, x+1]) - np.sum(inpt[y-1:y+2, x-1]))
            gimg[y, x] = gximg[y, x] + gyimg[y, x]

            maxgx = max(maxgx, gximg[y, x])
            maxgy = max(maxgy, gyimg[y, x])
            maxg = max(maxg, gimg[y, x])


    for y in range(1, h-1):
        for x in range(1, w-1):
            gximg[y, x] = math.floor((gximg[y, x] / maxgx) * 255)
            gyimg[y, x] = math.floor((gyimg[y, x] / maxgy) * 255)
            gimg[y, x] = math.floor((gimg[y, x] / maxg) * 255)

    gximg = gximg.astype(np.uint8)
    gyimg = gyimg.astype(np.uint8)
    gimg = gimg.astype(np.uint8)

    T = 25
    res = np.zeros((h, w), dtype=np.uint8)
    for y in range(h):
        for x in range(w):
            if gimg[y, x] >= T:
                res[y, x] = 255
            else:
                res[y, x] = 0

    
    return pim.fromarray(gximg, mode='L'), pim.fromarray(gyimg, mode='L'), pim.fromarray(gimg, mode='L'), pim.fromarray(res, mode='L')


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
    outdir = os.path.join(os.path.dirname(__file__), 'output/')
    for inputname in glob(inptdir):
        name = os.path.splitext(os.path.basename(inputname))[0]
        
        polyTon = toSRGB(inputname)
        polyTon.save(outdir + 'SRGB' + name + '.bmp')

        gx, gy, g, binar = grac(polyTon)
        gx.save(outdir + 'GX' + name + '.bmp')
        gy.save(outdir + 'GY' + name + '.bmp')
        g.save(outdir + 'G' + name + '.bmp')
        binar.save(outdir + 'BIN' + name + '.bmp')

if __name__ == "__main__":
    main()
