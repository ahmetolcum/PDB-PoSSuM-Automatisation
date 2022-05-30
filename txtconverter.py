from genericpath import exists
import xlsxwriter
import os
def txttoexcel(destination):
    arr = os.listdir(destination) #current directory (directory that txt files found)
    strtxt = ".txt"
    finaldest = destination + "/ExcelFiles"
    os.mkdir(finaldest)
    for txtfile in arr:
        if txtfile.__contains__(strtxt): # to take only txt files 
            name = txtfile[:4]
            fileObject = open(destination + "/" +txtfile, "r")
            if not exists (finaldest + "/"+ name + ".xlsx" ): #if it exist don't edit
                with open(finaldest + "/"+ name + ".xlsx", "a+") as c:
                    print("{}.txt file converted to xlsx file!".format(name))
                #print(name, ": ", txtfile) #debug purposes 
                workbook = xlsxwriter.Workbook(finaldest + "/"+ name + ".xlsx") #create a workbook
                worksheet = workbook.add_worksheet("structure") #create a worksheet named ‘structure’
                header ="structure1"
                worksheet.set_header(header)
                #data = open("/Users/ahmetolcum/Documents/Sabanci/ENS491/9/Report_PoSSuM (2).txt","r") #load data
                linelist = fileObject.readlines() #read each line in the txt
                count = len(linelist) #count the number of lines
                #print (count) #print the number of lines
                a=0
                for num in range(0, count): #create each line 
                    line = linelist[num] #load each line in variable line
                    if(line[0] == "#"):
                        splitline = line.split("|") #split lines
                        splitline = splitline[1:]
                        #print(splitline)
                        worksheet.write_row(a, 0, splitline) #write each line in excel “{PDBid}.xlsx”
                        a+=1
                    else:
                        if (line.find(":") != -1):
                            infoline = line.split(":")
                            worksheet.write_row(a, 0, infoline)
                        elif(line.find("=") != -1):
                            infoline = line.split(">=")

                            worksheet.write_row(a, 0, infoline)
                        else:
                            infoline = []
                            infoline.append(line)
                            worksheet.write_row(a, 0, infoline)
                        a += 1 
                workbook.close() #<<<close workbook, important to complete the task
    print("Directory is completed") # feedback about last completed directory that have multiple txt files in it (named in grouplist)
    return finaldest
if __name__ == "__main__":
    destination = "/Users/ahmetolcum/Downloads/PDBSUM/COA"
    txttoexcel(destination)

