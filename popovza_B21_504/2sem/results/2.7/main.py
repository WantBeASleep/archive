import numpy as np
from PIL import Image as pim
from glob import glob
import os

def getIntegralsSums(picArr: np.array):
    sSum = np.zeros(picArr.shape, dtype=np.uint64) # - кумулятивная сумма
    qSum = np.zeros(picArr.shape, dtype=np.uint64)
    
    for y in range(picArr.shape[0]):
        for x in range(picArr.shape[1]):
            curI = picArr[y][x]

            spL = sSum[y][x-1] if x > 0 else 0
            qpL = qSum[y][x-1] if x > 0 else 0

            spU = sSum[y-1][x] if y > 0 else 0
            qpU = qSum[y-1][x] if y > 0 else 0

            spF = sSum[y-1][x-1] if (x > 0 and y > 0) else 0 # чего, && нельзя? Куда я попал
            qpF = qSum[y-1][x-1] if (x > 0 and y > 0) else 0
            
            sSum[y][x] = curI + spL + spU - spF
            qSum[y][x] = curI**2 + qpL + qpU - qpF

    return sSum, qSum

def getWinSum(matrix: np.array, y, x, w: int):
    d = w // 2

    left = matrix[y + d][x - d - 1] if (x - d - 1 >= 0) else 0
    up = matrix[y - d - 1][x + d] if (y - d - 1 >= 0) else 0
    prevfull = matrix[y - d - 1][x - d - 1] if (x - d - 1 >= 0 and y - d - 1 >= 0) else 0
    full = matrix[y + d][x + d]

    return full + prevfull - left - up

def getBinPicArr(origPicArr: np.array, w: int) -> np.array:
    sSum, qSum = getIntegralsSums(origPicArr)
    k = 0.2
    R = 128
    d = w // 2

    newPicArr = np.zeros(origPicArr.shape, dtype=np.uint8)
    for y in range(origPicArr.shape[0]):
        for x in range(origPicArr.shape[1]):
            if not (d <= y < origPicArr.shape[0] - d) or not (d <= x < origPicArr.shape[1] - d): # и ! нет, о боже
                continue
        
            m = getWinSum(sSum, y, x, w) / w**2
            lqs = getWinSum(qSum, y, x, w) / w**2
            lmq = np.square(m)
            diff = lqs - lmq

            s = np.sqrt(diff)

            T = m * (1 - k * (1 - s / R))

            newPicArr[y][x] = 255 if origPicArr[y][x] >= T else 0

    return newPicArr

def main():
    rootDir = os.path.dirname(__file__)
    for file in glob(os.path.join(rootDir, 'input/*')):
        picArr = np.array(pim.open(os.path.join(rootDir, file)).convert('L'))
        binPicArr = getBinPicArr(picArr, 9)
        newPic = pim.fromarray(binPicArr).convert('1')
        newPic.save(os.path.join(rootDir, 'output', os.path.basename(file)))
    
if __name__ == "__main__":
    main()



    

