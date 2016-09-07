'''
Created on Aug 19, 2015

@author: Birdy

'''

from os import listdir
from os import path
from os import makedirs
from string import replace
from string import find
from PIL import Image
import sys
import ftplib
import datetime
import images2gif

def createGif(name, imageRefList, prefix="", suffix=""):
    # Create our reference list
    rlist = []
    for eachString in imageRefList:
        if(find(eachString,".ds") >= 0 or find(eachString, ".DS") >= 0):
            continue
        rlist.append(prefix+eachString+suffix)
        pass
    # First: find dimensions of the images.
    avgHeightToWidth = 0.0
    count = 0.0
    imageList = []
    for eachItem in rlist:
        imageList.append(Image.open(eachItem)) # add item to imageList. Useful for later.
        s = imageList[-1].size
        avgHeightToWidth += (float(s[1]) / float(s[0]))
        count += 1.0
        pass
    avgHeightToWidth /= count
    # We will stretch all images to average dimensions
    finalDimensions = (300, int(300 * avgHeightToWidth))
    finalImageList = []
    for eachImage in imageList:
        finalImageList.append(eachImage.resize(finalDimensions, Image.ANTIALIAS))
        pass
    # Now, create our gif.
    # silence the console
    save_stdout = sys.stdout
    sys.stdout = open('trash', 'w')
    images2gif.writeGif(filename=name+".gif", images=finalImageList, duration=2, repeat=True, dither=True)
    sys.stdout = save_stdout
    pass

if __name__ == '__main__':
    lastPic = input("Input the collection and name (e.g. oma/deep-pond.html)\n  of the last page to be added, in quotes:")
    print("You entered: " + lastPic)
    collectionAbbrev = input("Input the abbreviation (e.g. OMA) of the collection\n  you want to add, in quotes:")
    print("You entered: " + collectionAbbrev)
    collectionAbbrev = collectionAbbrev.lower()
    upperCollectionAbbrev = collectionAbbrev.upper()
    input("Make sure that you have written this week's description text in the first line of \"title.txt\".")
    descTextFile = open("title.txt")
    descText = descTextFile.readline()
    descTextFile.close()
    
    print "Creating collection: " + upperCollectionAbbrev + "..."
    
    #we need to make sure that the pages we're going to make have a folder to go in
    if not path.exists("pages/"+collectionAbbrev):
        makedirs("pages/"+collectionAbbrev)
        pass
    
    #create the relevant collection page
    collectionPage = open("pages/"+collectionAbbrev+"/index.html","w+")
    collectionPage.write('<!--<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">-->\n')
    collectionPage.write('<!DOCTYPE html>\n')
    collectionPage.write('<html "lang=en">\n')
    collectionPage.write('    <head>\n')
    collectionPage.write('        <link href="../../momaStyleSheet.css" rel="stylesheet" type="text/css">\n')
    collectionPage.write('        <meta http-equiv="Content-type" content="text/html;charset=utf-8">\n')
    collectionPage.write('        <title>Collection - '+upperCollectionAbbrev+'</title>\n')
    collectionPage.write('\n')
    collectionPage.write('        <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.11.2/jquery.min.js"></script>\n')
    collectionPage.write('        <!--if I ever care about jquery-->\n')
    collectionPage.write('        <script src="../../setHeight.js"></script>\n')
    collectionPage.write('    </head>\n')
    collectionPage.write('    <body>\n')
    collectionPage.write('        <div id="header">Monitors of Modern Art</div>\n')
    collectionPage.write('        <div id="container">\n')
    collectionPage.write('            <div id="menu">\n')
    collectionPage.write('                <!--#include virtual="../../menu2.shtml" -->\n')
    collectionPage.write('            </div>\n')
    collectionPage.write('            <div id="content">\n')
    collectionPage.write('                <div class="post">\n')
    collectionPage.write('                <h2><a href="../index.html">Collections</a> ></h2>\n')
    collectionPage.write('                <h1>'+upperCollectionAbbrev+'</h1><br>\n')
    collectionPage.write('                <h3>This title is only an acronym. <a href="../../contact.html">Be the first to expand it correctly</a>, and get the chance to name a picture from a future gallery!</h3><br>\n')
    collectionPage.write('                <table>\n')
    
    # We also need to open the archive page so that we can do some work on it.
    archiveListPage = open('archive/full_archive.html','r+')
    textArchiveListPage = open('archive/index.html','r+')
    textArchiveLines = textArchiveListPage.readlines()
    archiveLines = archiveListPage.readlines()
    archiveListPage.seek(0)
    i = 0;
    while(i < len(archiveLines)):
        if(find(archiveLines[i],"tr>") >= 0):
            archiveLines.pop(i)
        else:
            i += 1
            pass
    textArchiveListPage.seek(0)
    i = 0;
    while(i < len(textArchiveLines)):
        if(find(textArchiveLines[i],"tr>") >= 0):
            textArchiveLines.pop(i)
        else:
            i += 1
            pass
    # this has been a tutorial on how for loops should work.
    
    # this is all we need to do for now - we'll finish this up later.
    
    picList = listdir("images/"+collectionAbbrev+"/")
    for i in range(len(picList)):
        if(find(picList[i],".ds") >= 0 or find(picList[i], ".DS") >= 0):
            picList.pop(i)
            break
    picNo = 0
    for pic in picList:
        if(find(pic,".ds") >= 0 or find(pic, ".DS") >= 0):
            continue
        
        workName = pic[:-4]
        workDashes = replace(workName," ","-").lower()
        workURL="images/"+collectionAbbrev+"/"+pic
        
        # First, we're going to add a next button to the last thing we did.
        if(pic == picList[0]):
            lastFile = open('pages/'+lastPic,'r+')
            lastFileLines = lastFile.readlines()
            lastFile.seek(0)
            lastFileLines[39] = (lastFileLines[39])[:-11] + '/ <a href="../'+collectionAbbrev+'/'+workDashes+'.html">Next</a> '+(lastFileLines[39])[-11:]
            for eachLine in lastFileLines:
                lastFile.write(eachLine)
            lastFile.close()
        
        # Once that's done, we will create a new page for our new image.
        picFile = open("pages/"+collectionAbbrev+"/"+workDashes+".html","w+")
        picFile.write('<!--<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">-->\n')
        picFile.write('<!DOCTYPE html>\n')
        picFile.write('<html "lang=en">\n')
        picFile.write('    <head>\n')
        picFile.write('        <link href="../../momaStyleSheet.css" rel="stylesheet" type="text/css">\n')
        picFile.write('        <meta http-equiv="Content-type" content="text/html;charset=utf-8">\n')
        picFile.write('        <title>'+workName+'</title>\n')
        picFile.write('\n')
        picFile.write('        <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.11.2/jquery.min.js"></script>\n')
        picFile.write('        <script src="../../setHeight.js"></script>\n')
        picFile.write('        <!--if I ever care about jquery-->\n')
        picFile.write('    </head>\n')
        picFile.write('    <body>\n')
        picFile.write('        <div id="fb-root"></div>\n')
        picFile.write('            <script>\n')
        picFile.write('                window.fbAsyncInit = function() {\n')
        picFile.write('                    FB.init({\n')
        picFile.write("                        appId      : 'MOMA',\n")
        picFile.write('                        xfbml      : true,\n')
        picFile.write("                        version    : 'v2.4'\n")
        picFile.write('                    });\n')
        picFile.write('                };\n')
        picFile.write('                (function(d, s, id) {\n')
        picFile.write('                    var js, fjs = d.getElementsByTagName(s)[0];\n')
        picFile.write('                    if (d.getElementById(id)) return;\n')
        picFile.write('                    js = d.createElement(s); js.id = id;\n')
        picFile.write('                    js.src = "//connect.facebook.net/en_US/sdk.js#xfbml=1&version=v2.4&appId=1017414321642054";\n')
        picFile.write('                    fjs.parentNode.insertBefore(js, fjs);\n')
        picFile.write("                }(document, 'script', 'facebook-jssdk'));\n")
        picFile.write('            </script>\n')
        picFile.write('        <div id="header">Monitors of Modern Art</div>\n')
        picFile.write('        <div id="container">\n')
        picFile.write('            <div id="menu">\n')
        picFile.write('                <!--#include virtual="../../menu2.shtml" -->\n')
        picFile.write('            </div>\n')
        picFile.write('            <div id="content">\n')
        picFile.write('                <div class="post">\n')
        picFile.write('                    <h2><a href="index.html">'+upperCollectionAbbrev+'</a> ></h2>\n')
        picFile.write('                    <h1>'+workName.upper()+'</h1>\n')
        ## setting up previous and next links
        if (picNo == 0): 
            previousWork = "../"+lastPic
        else:
            previousWork = replace((picList[picNo - 1])[:-4]," ","-").lower()+".html"
        prevNextStr = previousWork + '">Previous</a>'
        nextWork = ""
        if (pic != picList[-1]):
            nextWork = replace((picList[picNo+1])[:-4]," ","-").lower()+".html"
            prevNextStr = prevNextStr + ' / <a href="' + nextWork + '">Next</a>'
        picFile.write('                    <h2>[ <a href="'+prevNextStr+' ]</h2><br>\n')
        ## continuing on, now...
        picFile.write('                    <img src="../../images/'+collectionAbbrev+'/'+pic+'" onload="setGoodHeight(this);">\n')
        picFile.write('                    <div class="fb-comments" data-href="'+workDashes+'.html" data-numposts="10"></div>\n')
        picFile.write('                </div>\n')
        picFile.write('            </div>\n')
        picFile.write('            <div id="footer">&copy Louis Jacobowitz 2016</div>\n')
        picFile.write('        </div>\n')
        picFile.write('    </body>\n')
        picFile.write('</html>\n')
        
        #Done writing a new page for this work. Now close the document.
        picFile.close()
        
        #Now we add this picture to the collection page. Remember, three to a row.
        if(picNo % 3 == 0):
            collectionPage.write('                        <tr>\n')
        collectionPage.write('                            <td>\n')
        collectionPage.write('                                <a href="'+workDashes+'.html">\n')
        collectionPage.write('                                    <img src="../../images/'+collectionAbbrev+'/'+pic+'"><br>\n')
        collectionPage.write('                                    <p>'+workName+'</p>\n')
        collectionPage.write('                                </a>\n')
        collectionPage.write('                            </td>\n')
        if((picNo % 3 == 2) or (pic == picList[-1])):
            collectionPage.write('                        </tr>\n')
        
        #Finally, we need to add pages to the archive. We'll write six lines to the array.
        archiveLines.insert(27,'                            <td>\n')
        archiveLines.insert(28,'                                <a href="../pages/'+collectionAbbrev+'/'+workDashes+'.html">\n')
        archiveLines.insert(29,'                                    <img src="../images/'+collectionAbbrev+'/'+pic+'">\n')
        archiveLines.insert(30,'                                    '+workName+'\n')
        archiveLines.insert(31,'                                </a>\n')
        archiveLines.insert(32,'                            </td>\n')
        
        textArchiveLines.insert(23,'                            <td>\n')
        textArchiveLines.insert(24,'                                <a href="../pages/'+collectionAbbrev+'/'+workDashes+'.html">\n')
        textArchiveLines.insert(25,'                                    '+workName+'\n')
        textArchiveLines.insert(26,'                                </a>\n')
        textArchiveLines.insert(27,'                            </td>\n')
        #And we're done! From here on, all the modifications we need to make are for the collection, not for the individual works.
        picNo += 1
        
    # Finishing up the collection page.
    collectionPage.write('                   </table>\n')
    collectionPage.write('                </div>\n')
    collectionPage.write('            </div>\n')
    collectionPage.write('            <div id="footer">&copy Louis Jacobowitz 2016</div>\n')       
    collectionPage.write('        </div>\n')
    collectionPage.write('    </body>\n')
    collectionPage.write('</html>\n')
    #and closing it now that it's done.
    collectionPage.close()
    
    #Now we need to add our collection to the list of collections.
    collectionListPage = open('pages/index.html','r+')
    collectionListLines = collectionListPage.readlines()
    collectionListPage.seek(0)
    collectionListLines.insert(len(collectionListLines)-7,'                        <li><a href="'+collectionAbbrev+'/index.html">'+upperCollectionAbbrev+'</a></li>\n')
    for eachLine in collectionListLines:
        collectionListPage.write(eachLine)
    collectionListPage.close()
    
    #And, having done that, we just need to reinsert table rows into the archive.
    #We'll insert starting at 24 and then ending every 25. Then repeat.
    i=27
    while(i < len(archiveLines) - 7):
        if((i - 27) % 26 == 0):
            archiveLines.insert(i,'                        <tr>\n')
        elif((i-27) % 26 == 25):
            archiveLines.insert(i,'                        </tr>\n')
        i += 1
        pass
    i=23
    while(i < len(textArchiveLines) - 7):
        if((i - 23) % 22 == 0):
            textArchiveLines.insert(i,'                        <tr>\n')
        elif((i-23) % 22 == 21):
            textArchiveLines.insert(i,'                        </tr>\n')
        i += 1
        pass
    
    #And then we add the lines back into the file.
    for eachLine in archiveLines:
        archiveListPage.write(eachLine)
        pass
    for eachLine in textArchiveLines:
        textArchiveListPage.write(eachLine)
        pass
    archiveListPage.close()
    textArchiveListPage.close()
    #and that should be all involved in creating the files themselves.
    
    # Now to create the slideshow image
    print "Creating slideshow GIF..."
    # Image ref list, we already have. It's picList.
    createGif(name=collectionAbbrev, imageRefList=picList, prefix="images/"+collectionAbbrev+"/")
    
    print "Updating front page..."
    indexfile = open("index.html", 'r+')
    indexlines = indexfile.readlines()
    # Get today's date...
    today = datetime.date.today()
    nday = str(today.day)
    nyear = str(today.year)
    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    nmonth = " " + months[today.month - 1] + " "
    # edit relevant lines in index
    indexlines[39] = '                    <td class="image"><a href="pages/'+collectionAbbrev+'/index.html"><img class="title" src="'+collectionAbbrev+'.gif" align="left" onload="newNoteHeight(this);"></a></td><td class="elsewise">\n'
    indexlines[40] = '                    <h1><a href="pages/'+collectionAbbrev+'/index.html">New Collection: '+upperCollectionAbbrev+'</a></h1>\n'
    indexlines[41] = '                    <h2>' + nday + nmonth + nyear + '</h2>\n'
    indexlines[43] = '                    <p>This week\'s new collection is '+upperCollectionAbbrev+' (<a href="contact.html">guess what that acronym stands for</a> and you can name an upcoming work!). ' + descText + '</p><br><br>\n'
    # and now reinsert them.
    indexfile.seek(0)
    for eachLine in indexlines:
        indexfile.write(eachLine)
        pass
    indexfile.close()
    
    # DO THE FTP THING
    print "Attempting to connect to FTP host..."
    ftp = ftplib.FTP(host="ftp.artmonitors.com", user="*******@artmonitors.com", passwd="********", acct="*******@artmonitors.com")
    print "Successfully connected to FTP."
    # Find and transfer all image files
    ifn = ftp.mkd("/images/" + collectionAbbrev)
    print "    Adding image files to new folder:", ifn
    for pic in picList:
        if(find(pic,".ds") >= 0 or find(pic, ".DS") >= 0):
            continue
        picstring = "images/"+collectionAbbrev+"/"+pic
        fileToTransfer = open(picstring, "rb")
        #STOR /images/cnma/picname.jpg
        ftp.storbinary(cmd="STOR "+ifn+"/"+pic, fp=fileToTransfer)
        fileToTransfer.close()
        # this should suffice
        pass
    # Find and transfer all relevant page files
    pfn = ftp.mkd("/pages/" + collectionAbbrev)
    print "    Overwriting outdated pages and adding new pages to new folder:", pfn
    # Replace the former index file
    indexfile = open("pages/index.html")
    ftp.storlines(cmd="STOR /pages/index.html", fp=indexfile)
    indexfile.close()
    # Replace the last collection's last page
    lastFile = open("pages/"+lastPic)
    ftp.storlines(cmd="STOR /pages/"+lastPic, fp=lastFile)
    lastFile.close()
    # Create the new collection's folder, add them all.
    pageList = listdir("pages/"+collectionAbbrev)
    for page in pageList:
        if(find(page, ".ds") >= 0 or find(page, ".DS") >= 0):
            continue
        pagestring = "pages/"+collectionAbbrev+"/"+page
        fileToTransfer = open(pagestring)
        ftp.storlines(cmd="STOR "+pfn+"/"+page, fp=fileToTransfer)
        fileToTransfer.close()
        pass
    print "    Overwriting archive pages..."
    # Archive index
    arcFile = open("archive/index.html")
    ftp.storlines(cmd="STOR /archive/index.html", fp=arcFile)
    arcFile.close()
    # Full archive
    fullArcFile = open("archive/full_archive.html")
    ftp.storlines(cmd="STOR /archive/full_archive.html", fp=fullArcFile)
    fullArcFile.close()
    print "    Overwriting front page..."
    idxFile = open("index.html")
    ftp.storlines(cmd="STOR /index.html", fp=idxFile)
    idxFile.close()
    idxFile = open(collectionAbbrev+".gif", 'rb')
    ftp.storbinary(cmd="STOR /"+collectionAbbrev+".gif", fp=idxFile)
    idxFile.close()
    
    print "Process complete. Collection "+upperCollectionAbbrev+" created and uploaded."
    