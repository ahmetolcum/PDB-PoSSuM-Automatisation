##import libraries 
#from concurrent.futures import thread
import os
from selenium import webdriver
import time

##import files
from txtconverter import txttoexcel
from concat import folderconcat
from  ppsm import post_possum
from grouping import grouping
def chromesetter(chromeDriver ,dest, headless):
    WINDOW_SIZE = "1920,1080"
    chromeOptions = webdriver.ChromeOptions()
    prefs = {"download.default_directory" : dest}
    if(headless):
        chromeOptions.add_argument("--headless")
        chromeOptions.add_argument("--window-size=%s" % WINDOW_SIZE)
    chromeOptions.add_experimental_option("prefs",prefs)
    browser = webdriver.Chrome(executable_path=chromeDriver, chrome_options=chromeOptions)
    return browser
def inputtaker():
    inpligands = []
    max_RMSD = float(0.0)
    dest1 = input("Enter a path to save required files (Leave empty for current directory): ")
    print("Your input may be a list of ligands or a single one! For multiple inputs put \", \" as a separator!")
    inpligands = input("Enter your ligands' letter code: ")
    while(inpligands == "" ):
        print("Wrong input format!")
        inpligands = input("Enter your ligand's three letter code: ")
    if(inpligands.find(",")):
        inpligands = inpligands.split(",")
        for element in inpligands:
            if element.find(" "):
                element = element.strip()
    for element in inpligands: 
        try:
            os.mkdir(dest1 + element)
        except:
            print(element+ " folder already existed and will be overwriten!")
    if dest1 != "":
        if dest1[len(dest1) - 1 != "/"]:
            dest1 = dest1 + "/"
    else:
        dest1 = os.getcwd()
    max_RMSD = input("Please enter maximum RMSD value (Leaving empty means no any limit): ")
    correctinp = 1
    while(correctinp <= 1):
        cleaninp = input("Do you want to have other ligands in your result? (Whether you want to see other items than yours)(Yes : \"y\", No : \"N\"): ")
        if cleaninp == "y":
            clean = False
            correctinp += 1
        elif(cleaninp == "N"):
            clean = True
            correctinp += 1
        else:
            print("Wrong Input!!!")
            correctinp = 0
    return inpligands,  dest1, clean, max_RMSD
def download_wait(path_to_downloads):
    seconds = 0
    dl_wait = True
    while dl_wait and seconds < 20:
        time.sleep(1)
        dl_wait = False
        for fname in os.listdir(path_to_downloads):
            if fname.endswith('.crdownload'):
                dl_wait = True
        seconds += 1
    return seconds
def PDBconnecter(lenslists, dest, ligand, chromedriver, headless):
    liste = []
    liste2 = []
    coma = ","
    #print("pdbconnecter")
    #print(ligand)
    for element in ligand:
        #print(element)
        browser1 = chromesetter(chromedriver, dest, headless)
        browser1.get("https://www.rcsb.org")
        time.sleep(2)
        search = browser1.find_element_by_xpath("/html/body/div/div[2]/div/div/div[1]/div[2]/div/div[2]/table/tbody/tr[1]/td[2]/div/input")
        search.send_keys(element)
        time.sleep(1)
        find = browser1.find_element_by_xpath("/html/body/div/div[2]/div/div/div[1]/div[2]/div/div[2]/table/tbody/tr[1]/td[2]/div/div/div[2]")
        find.click()
        time.sleep(1)
        but = browser1.find_element_by_xpath("/html/body/div/div[3]/div[1]/div[3]/div[2]/input")
        but.click()
        time.sleep(1)
        down = browser1.find_element_by_xpath("/html/body/div/div[3]/div/div/div[3]/div[2]/div[3]/table/tbody/tr/td[2]/div/div[1]/div[3]/div/div[2]/span")
        down.click()
        time.sleep(1)
        listprot = browser1.find_element_by_tag_name("textarea")
        if len(liste) == 0:
            #print("liste==\"\"")
            listetext = listprot.text
            #print(listetext)
            if(listetext.find(coma) == -1):
                #print("not else")
                liste.append(listetext)
            else:
                #print("else")
                liste = listetext.split(",")
            #print(liste)
            lenslists.append(len(liste))
            #print(lenslists)
        else:
            #print("liste not empty")
            liste2text = listprot.text
            if(liste2text.find(coma)== -1):
                #print("not in coma")
                if liste2text not in liste:
                    #print("in if")
                    liste2.append(liste2text)
                    liste = liste + liste2 
                    lenslists.append(len(liste2))
            else:
                #print("we are in else")
                liste2 = liste2text.split(",")
                not_commons = [item for item in liste2 if item not in liste]
                #print(not_commons)
                commons = [item for item in liste2 if item not in not_commons]
                #print(commons)
                lenslists.append(len(not_commons))
                #print(lenslists)
                liste = liste + not_commons
                #print(len(liste))
    browser1.close()
    return liste
def eliminator(destination, element, list, max_RMSD):
    fileObject = open("{}/{}.txt".format(destination, element), "r")
    lines = fileObject.readlines()
    newlines = []
    somethingtodelete = False
    High_RMSDs = []
    eliminates = []
    for line in lines:
        if (line[0] == "#"):
            row = line.split("|")
            if(len(row[8]) <= 4):
                rmsd_value = float(row[8])
                if(float(rmsd_value) > float(max_RMSD)):
                    High_RMSDs.append(line)
                    somethingtodelete = True
                else:
                    newlines.append(line)
            else:
                newlines.append(line)
        else:
            newlines.append(line)
    fileObject.close()
    if(somethingtodelete):
        fileObject2 = open("{}/{}.txt".format(destination, element), "w")
        for line in newlines:
            fileObject2.write(line)
    return High_RMSDs
def possumdownloader(ligand, list,lenlist, numelement, destination, chromedriver, headless, max_RMSD):
    one = True
    noresultlist = []
    inputted_pro = 0
    #print("possum downloader")
    destroot = destination
    #print(list)
    if list:
        time.sleep(1)
        done = 0 
        a = 0 
        toc = time.time()
        lenlistcounter = 0
        loopcounter = 0
        print("Estimation is calculating...")
        for element in range(len(list)):  
            if len(list[element]) == 4 :
                if ( loopcounter >= lenlist[lenlistcounter]):
                    lenlistcounter = lenlistcounter + 1
                    loopcounter = 0
                destination = destroot + "/" + ligand[lenlistcounter]
                #print(destination)
                driver = chromesetter(chromedriver, destination, headless)
                driver.get("http://possum.cbrc.jp/PoSSuM/search_k.html")
                time.sleep(1)
                pdbid = driver.find_element_by_name("params[0]")
                ligand_loc = driver.find_element_by_name("params[1]")
                pdbid.send_keys(list[element])
                #print(ligand[lenlistcounter])
                ligand_loc.send_keys(ligand[lenlistcounter])
                loopcounter += 1
                download = driver.find_element_by_xpath("/html/body/div/div[2]/div[2]/form/table/tbody/tr[11]/td[2]/input[2]")
                download.click()
                time.sleep(0.5)
                submit = driver.find_element_by_xpath("/html/body/div/div[2]/div[2]/form/table/tbody/tr[12]/td/input")
                submit.click()
                time.sleep(0.5)
                done += 1
                namenotchanged = True
                #If there is no any result from PoSSuM the algorithm takes so long 
                secs = download_wait(destination)
                if namenotchanged:
                    try:
                        if (destination +"/Report_PoSSuM.txt"):
                            filename = destination + "/" + list[element] + ".txt"
                            os.rename(destination +"/Report_PoSSuM.txt", filename)
                            namenotchanged = False
                    except:
                        noresultlist.append(element)
                        print("No any result for the " + list[element] + "!")
                if not namenotchanged and max_RMSD != None:
                    High_RMSDs = eliminator(destination, list[element], list, max_RMSD)
                #driver.close()
                '''
                if High_RMSDs:
                    for item in High_RMSDs:
                        element = item.split("|")
                        #print(element)
                        destination = destroot + "/" + ligand[lenlistcounter]
                        driver = chromesetter(chromedriver, destination, headless)
                        driver.get("http://possum.cbrc.jp/PoSSuM/search_k.html")
                        time.sleep(1)
                        pdbid = driver.find_element_by_name("params[0]")
                        ligand_loc = driver.find_element_by_name("params[1]")
                        pdbid.send_keys(element[1])
                        #print(ligand[lenlistcounter])
                        ligand_loc.send_keys(ligand[lenlistcounter])
                        download = driver.find_element_by_xpath("/html/body/div/div[2]/div[2]/form/table/tbody/tr[11]/td[2]/input[2]")
                        download.click()
                        time.sleep(0.5)
                        submit = driver.find_element_by_xpath("/html/body/div/div[2]/div[2]/form/table/tbody/tr[12]/td/input")
                        submit.click()
                        time.sleep(0.5)
                        namenotchanged = True
                        if namenotchanged:
                            try:
                                if (destination +"/Report_PoSSuM.txt"):
                                    filename = destination + "/" + element[1] + ".txt"
                                    os.rename(destination +"/Report_PoSSuM.txt", filename)
                                    namenotchanged = False
                            except:
                                noresultlist.append(element)
                                print("No any result for the " + element[1] + "!")
                        if not namenotchanged and max_RMSD != None:
                            High_RMSDs2 = eliminator(destination, element[1], list, max_RMSD)
                High_RMSDs = []
                '''
                numelement = len(list)
                percent = done * 100
                percent = float(percent) / float(numelement)
                print("{:.2f}".format(percent) ,"% completed! Download in progress...", )
                if(percent > a):
                    a = a + 5
                    tic = time.time()
                    remtime = tic - toc
                    estimate = (100-percent) * remtime
                    estimate = estimate / percent
                    estimate = estimate / 60
                    print(f"Estimated time to complete {estimate:0.4f} minutes")
        print("Download completed!")         
    driver.close()
    return noresultlist, High_RMSDs
def main():
    #The desired directory needed to be changed. Destination can be found in inputtaker function 
    ''''
    chromedriver = "/Users/ahmetolcum/Documents/DevSpace/Selenium/chromedriver" #Give the path of the chrome driver for the selenium 
    resultless, lenlist = [], []
    clean = False
    ligand, destination, clean, max_RMSD = inputtaker()
    headless = True
    prolist = PDBconnecter(lenlist, destination, ligand, chromedriver, headless)
    totalenght = len(prolist)
    totalpro = totalenght / 6
    numpro = len(prolist)
    resultless, High_RMSDs = possumdownloader(ligand, prolist,lenlist, numpro, destination, chromedriver, headless, max_RMSD)
    print(High_RMSDs)
    '''
    destination = "/Users/ahmetolcum/Downloads/PDBSUM/COA"
    exceldest = txttoexcel(destination)
    #concatfolder = folderconcat(exceldest)
    #print("now post_possum")
    #resultfiles = post_possum(exceldest)
    print("now grouping")
    #grouping(exceldest)
if __name__ == "__main__":
    main()

############PROBLEMS TO FIX
'''
-
- 
'''