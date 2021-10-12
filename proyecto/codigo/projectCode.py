#https://github.com/mauriciotoro/ST0245-Eafit/tree/master/proyecto/datasets/csv/enfermo_csv
#https://raw.githubusercontent.com/mauriciotoro/ST0245-Eafit/master/proyecto/datasets/csv/enfermo_csv/0.csv
#span class="css-truncate css-truncate-target d-block width-fit"><a class="js-navigation-open Link--primary" title=
import urllib.request
from collections import deque
import time
import numpy  as np
from matplotlib import pyplot as plt
import math

class Webscraping:
    def __init__(self, url):
        self.__url__ = url
        self.__cvsName__ = "name"

    def download(self):
        #gets the page code 
        urllib.request.urlretrieve(self.__url__,self.__cvsName__)
        return self.__cvsName__
    

    def read (self):
        #reads the page code
        with open(self.__cvsName__,"r") as firstText:
            text = firstText.read()
            return text



    # very specific web scraping 
    def __textToVector__(self,texto):
        #get scraps most of the page code 
        keytext = 'span class="css-truncate css-truncate-target d-block width-fit"><a class="js-navigation-open Link--primary" title='
        vectorDinamico = [] 
        lineas = texto.split("\n")
        for linea in lineas:
            if keytext in linea :
                x = linea.strip()
                vectorDinamico.insert(0,x)
        return vectorDinamico

    def specialPrint(vector):
        #print arrays 
        for i in vector:
            print(i)
            time.sleep(0.5)

    def __scraping__(self,vector):
        #gets the title of the image of the page
        newVector = []
        for line in vector:
            a = line.find('title=')
            b = line.find('" data-pjax="#repo-content-pjax-container"')
            newVector.insert(0,line[a+7:b].strip().replace(" ","%20"))
        return newVector
    
    def scrappedvector(self):
        #gets the title of the image of the page return an array
        text = self.read()
        text = self.__textToVector__(text)
        vector = self.__scraping__(text)
        return vector

class ImagesCsv:
    
    def __init__(self):
        self.__baseUrl__ = "https://raw.githubusercontent.com/mauriciotoro/ST0245-Eafit/master/proyecto/datasets/csv/"
        self.__listUrl__ = self.__baseUrl__
        self.__url__ = self.__baseUrl__

    def setImageList(self,url):
        self.__listUrl__ = self.__baseUrl__  + url +"/"

    def setImage(self,url):
        self.__url__ = self.__listUrl__ + url

    def geturl(self):
        return self.__url__
    
    def setUrl(self,url,subUrl):
        self.setImageList(url)
        self.setImage(subUrl)

    def getImageCsv(self,subUrl):
        #get the csv file and turns it in to a list compose of lists
        #in other words a matrix returns a matrix of the csv
        self.setImage(subUrl)
        web = Webscraping(self.__url__)
        name = web.download()
        matrix01 = np.genfromtxt(name,delimiter = ",", dtype=int)
        return matrix01

class CosCompression:
    def __init__(self):
        self.quantificationTable =  np.matrix([[16,11,10,16,24,40,51,61],
                                               [12,12,14,19,26,58,60,55],
                                               [14,13,16,24,40,57,69,56],
                                               [14,17,22,29,51,87,80,62],
                                               [18,22,37,56,68,109,103,77],
                                               [24,36,55,64,81,104,113,92],
                                               [49,64,78,87,103,121,120,101],
                                               [72,92,95,98,112,100,103,99]])

    
    def matrixNormalization(self,matrix01,flag = True):
        if flag:
            matrix01 = np.where(matrix01 > 0,matrix01-128, matrix01-128) #change 
        else:
            matrix01 = np.where(matrix01 > 0,matrix01+128, matrix01+128)
        return matrix01

    def matrixResizing(self, matrix01):
        size = matrix01.shape
        if size[0]%8 == 0 and size[1]%8 == 0:
            return matrix01
        if size[0]%8 != 0:
            row = 8-(size[0]-((size[0]//8)*8))
            for i in range(row):
                matrix01 = np.r_[matrix01,np.matrix(matrix01[-1])]

        if size[0]%8 != 0:
            column = 8-(size[1]-((size[1]//8)*8))
            for i in range(column):
                matrix01 = np.c_[matrix01,matrix01[:,-1]]
        
        return matrix01

    def matrixT(self):
        list01 = [[ self.C1() if i == 0 else self.C2(j,i) for j in range(8)]for i in range(8)]
        matrix01 = np.matrix(list01)
        return matrix01
        pass

    def C1(self):
        return round(1/(math.sqrt(8)),4)

    def C2(self,j,i):
        return round(math.sqrt(1/4)*math.cos(((2*j+1)*i*math.pi)/16),4)


    def CDT(self,matrix01):
        matrixN = self.matrixNormalization(matrix01)
        matrixD = np.round(np.matmul(np.matmul(self.matrixT(),matrixN),np.transpose(self.matrixT())),1)
        compressedMatrix = np.round(np.where(matrixD > 0,matrixD/self.quantificationTable, matrixD/self.quantificationTable)).astype(int)
        return compressedMatrix

    def CDT_Compression(self,matrix01):
        matrix02 = self.matrixResizing(matrix01)
        size = matrix02.shape

        for i in range(0,size[0],8):
            for j in range(0,size[1],8):
                matrix02[i:i+8,j:j+8] = self.CDT(matrix02[i:i+8,j:j+8])
        return matrix02



    def inverseCDT(self,compressedMatrix):
        size = list(compressedMatrix.shape)
        matrixN = np.multiply(compressedMatrix,self.quantificationTable)
        matrixD = np.round(np.matmul(np.matmul(np.transpose(self.matrixT()),matrixN),self.matrixT()),1)
        decompressedMatrix = self.matrixNormalization(matrixD,False)
        return decompressedMatrix

    def CDT_Decompression(self,matrix01):
        matrix02 = self.matrixResizing(matrix01)
        size = matrix02.shape

        for i in range(0,size[0],8):
            for j in range(0,size[1],8):
                matrix02[i:i+8,j:j+8] = self.inverseCDT(matrix02[i:i+8,j:j+8])
        return matrix02


class General:
    def __init__(self):
        self.__baseUrl__ = "https://github.com/mauriciotoro/ST0245-Eafit/tree/master/proyecto/datasets/csv/"
        self.__url__ = self.__baseUrl__

    def setUrl(self,file):
        self.__url__ = self.__baseUrl__ + file

    def gg(self,file):

        self.setUrl(file)
        
        print("getting links...",end = "")
        web = Webscraping(self.__url__)
        web.download() 
        vector = web.scrappedvector()
        print(" done")
        
        image = ImagesCsv()
        print("saving "+  file + "...")
        image.setImageList(file)
        cos = CosCompression()
        
        for i in (vector[:-3]):#change
            
            matrixImagenCsv = image.getImageCsv(i)
            compresedMatrix = cos.CDT_Compression(matrixImagenCsv)
            decompresedMatrix = cos.CDT_Decompression(compresedMatrix)

            '''
            print (matrixImagenCsv)

            fig = plt.figure(figsize=(32,32))
            fig.add_subplot(1,2,1)
            plt.imshow(matrixImagenCsv,cmap = "gray")

            print (compresedMatrix)

            fig.add_subplot(1,2,2)
            plt.imshow(compresedMatrix, cmap= "gray")
            '''
            
        #plt.show
            

        print(" done")

        #code
        
        

        print("clearing "+  file + "...", end = "")
        matrixImagenCsv = 0
        print(" done")

def main ():
    test02()

def testMain01():
    gen = General()
    gen.gg("enfermo_csv")
    gen.gg("sano_csv")

def test01(vector1,vector2):
    print(vector1)
    Webscraping.specialPrint(vector = vector1)
    Webscraping.specialPrint(vector = vector2)
    
def test02():
    gen = General()
    gen.gg("enfermo_csv")
    gen.gg("sano_csv")

def test03():
    url = "https://github.com/mauriciotoro/ST0245-Eafit/tree/master/proyecto/datasets/csv/enfermo_csv/"
    web = Webscraping(url)
    web.download() 
    vector = web.scrappedvector()
    image = ImagesCsv()
    image.setImageList("enfermo_csv")


    matrix = image.getImageCsv(vector[0])
    print (matrix[99:105,:5])



main()
