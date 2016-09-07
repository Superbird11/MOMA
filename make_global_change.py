'''
Created on Jan 26, 2016

@author: Birdy

'''

import os
import sys
import fileinput
import string
from string import find

def find_all(str, rep, retArr = []):
    ino = str.find(rep)
    if(ino >= 0):
        retArr.append(ino)
        retArr = find_all(str[ino+1:], rep, retArr)
    return retArr

def replaceList():
    return ["bma.html",
    "boma.html",
    "cma.html",
    "cmaa.html",
    "coma.html",
    "dma.html",
    "ewma.html",
    "iama.html",
    "lfma.html",
    "lmef.html",
    "loma.html",
    "maat.html",
    "mabw.html",
    "mac.html",
    "mai.html",
    "maj.html",
    "mama.html",
    "maot.html",
    "map.html",
    "maps.html",
    "mawf.html",
    "mawh.html",
    "mbma.html",
    "mima.html",
    "mla.html",
    "mma.html",
    "mmma.html",
    "mots.html",
    "ncma.html",
    "nmma.html",
    "oma.html",
    "pma.html",
    "rbma.html",
    "rma.html",
    "roma.html",
    "ssma.html",
    "stma.html",
    "tma.html",
    "uma.html",
    "vmma.html",
    "vpma.html"]  

if __name__ == '__main__':
    root = "./"
    rootFileList = os.listdir(root)
    extendedFileList = [] # List of files to be changed
    for str in rootFileList:
        if(find(str, ".") == -1):
            #Then this is a directory and we can run this again.
            recursiveFileList1 = os.listdir(root+str+"/")
            for str2 in recursiveFileList1:
                if(find(str2, ".") == -1):
                    #Then this is another directory and we can run this again. I don't need to nest any more than two levels
                    # deep, and it's not worth making the project recursive.
                    recursiveFileList2 = os.listdir(root+str+"/"+str2+"/")
                    for str3 in recursiveFileList2:
                        if(find(str3, ".html") >= 0):
                            #If it's an html file, add it to the list of files to be changed.
                            extendedFileList.append(root+str+"/"+str2+"/"+str3)
                elif(find(str2, ".html") >= 0):
                    #If it's an html file, add it to the list of files to be changed.
                    extendedFileList.append(root+str+"/"+str2)
        elif(find(str, ".html") >= 0):
            #If it's an html file, add it to the list of files to be changed.
            extendedFileList.append(str)
        #If it's not a html file, it's not going to be included in any sort of global change.
    #All inputs complete. Files can now be operated upon.
    for filename in extendedFileList:
        #First: contents of the files. (Precondition: all files have the extension .html)
        filedata = None
        file = open(filename, 'r')
        filedata = file.read()
        file.close()

        #PLACE ALL CHANGES TO THE CONTENTS OF FILES BELOW HERE. [FORMAT: filedata.replace("oldstring","newstring") ]
        #MAKE SURE THEY ARE IN THE CORRECT ORDER
#Current issue:
#The replace function just isn't working. Need to look into why.
        if(filename.find("pages/") >= 0 and filename.find("index.html") < 0):
            filedata = string.replace(filedata, "../../../../.shtml","../../menu2.shtml")
        
    
        #ALL CHANGES GO ABOVE THIS LINE
        file = open(filename, 'w')
        file.write(filedata)
        file.close()
        #All contents of the files should have been changed by now.
        #Second: the names of the files themselves. (Since the files do not interact with each other 
        #   during this process it should not be a problem to do these one after the other for each file)
        #NAME CHANGES GO BELOW THIS LINE

        #NAME CHANGES GO AOVE THIS LINE
        print "Changes made to file:" , filename 
    #And that should be all.    
    print "All changes made. Program complete."
#

#CHANGELOG:
#  