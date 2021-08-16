#https://github.com/mauriciotoro/ST0245-Eafit/tree/master/proyecto/datasets/csv/enfermo_csv
#https://raw.githubusercontent.com/mauriciotoro/ST0245-Eafit/master/proyecto/datasets/csv/enfermo_csv/0.csv
#span class="css-truncate css-truncate-target d-block width-fit"><a class="js-navigation-open Link--primary" title=
import urllib.request
from collections import deque
import time

class Webscraping:
    def __init__(self, url):
        self.__url__ = url
        self.__arrayName__ = "name"

    def download(self):
        #gets the page code 
        urllib.request.urlretrieve(self.__url__,self.__arrayName__)
    

    def read (self):
        #reads the page code
        with open(self.__arrayName__,"r") as firstText:
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

    def __getImageCsv__(self,subUrl):
        #get the csv file and turns it in to a list compose of lists
        #in other words a matrix returns a matrix of the csv
        self.setImage(subUrl)
        web = Webscraping(self.__url__)
        web.download()
        text = web.read()
        lineas = text.split("\n")
        list01 = [[int(i) for i in linea if i != ","]for linea in lineas ]
        return list01


    def getImageCsvList(self,url,vector):
        self.setImageList(url)
        mainList = deque()
        for name in vector[0:len(vector)-3]:
            
            mainList.insert(0,self.__getImageCsv__(name))
            #print(self.geturl())
        return mainList
            

def main ():
    cow = Cow()
    cow.generalCows("enfermo_csv")
    cow.generalCows("sano_csv")


    
class Cow:
    def __init__(self):
        self.__baseUrl__ = "https://github.com/mauriciotoro/ST0245-Eafit/tree/master/proyecto/datasets/csv/"
        self.__url__ = self.__baseUrl__

    def setUrl(self,file):
        self.__url__ = self.__baseUrl__ + file

    def generalCows(self,file):

        self.setUrl(file)

        print("getting links...",end = "")
        web = Webscraping(self.__url__)
        web.download() 
        vector = web.scrappedvector()
        print(" done")
        
        images = ImagesCsv()
        print("saving "+  file + "...", end = "")
        cowsImagesCsv = images.getImageCsvList(file,vector)
        print(" done")

        #code

        print("clearing "+  file + "...", end = "")
        cowsImagesCsv.clear()
        print(" done")



def test01(vector1,vector2):
    print(vector1)
    Webscraping.specialPrint(vector = vector1)
    Webscraping.specialPrint(vector = vector2)
    



main()

