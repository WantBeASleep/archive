import numpy as np
from PIL import Image as pim
from glob import glob
import os

def toSRGB(origPath: str, outPath):
    input_image = pim.open(origPath).convert('RGB')
    origPicArr = np.array(input_image)
    newPicArr = np.zeros((origPicArr.shape[0], origPicArr.shape[1]), dtype=origPicArr.dtype)
    
    for y in range(origPicArr.shape[0]):
        for x in range(origPicArr.shape[1]):
            newPicArr[y][x] = np.mean(origPicArr[y][x]) / 3

    newPic = pim.fromarray(newPicArr, 'L')
    newPic.save(outPath)

def main():
    rootDir = os.path.dirname(__file__)
    for file in glob(os.path.join(rootDir, 'input/*')):
        toSRGB(file, os.path.join(rootDir, 'output', os.path.splitext(os.path.basename(file))[0] + '.bmp'))
    
if __name__ == "__main__":
    main()