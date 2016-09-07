'''
Created on Jan 17, 2016

@author: Birdy

'''

###CURRENT STATUS: WORKS.
from os import listdir
from os import path
from os import makedirs
from string import replace
from string import find

if __name__ == '__main__':
    lastPic = input("Input the collection and name (e.g. oma/deep-pond.html) of the last page\n  to be added, in quotes: ")
    print("[You entered: "+lastPic+"]")
    collectionString = input("Input the abbreviations of the collections you want to add,\n  all in quotes and separated by a comma and no spaces\n  (e.g. \"OMA,SMA,ROMA,LMEF\")\n  : ")
    print("[You entered: "+collectionString+"]")
    collectionsAll = collectionString.split(',');
    #print collectionsAll; #(debug)
    #Now, we will do the same thing for every project. Whenever we finish the last pic of a collection, we will replace lastPic with it.
    for collectionAbbrev in collectionsAll:
        collectionAbbrev = collectionAbbrev.lower()
        upperCollectionAbbrev = collectionAbbrev.upper()
        
        #we need to make sure that the pages we're going to make have a folder to go in
        if not path.exists("pages/"+collectionAbbrev):
            makedirs("pages/"+collectionAbbrev)
        
        #create the relevant collection page
        collectionPage = open("collections/"+collectionAbbrev+".html","w+")
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
        collectionPage.write('                <!--#include virtual="../../menu1.html" -->\n')
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
        textArchiveListPage.seek(0)
        i = 0;
        while(i < len(textArchiveLines)):
            if(find(textArchiveLines[i],"tr>") >= 0):
                textArchiveLines.pop(i)
            else:
                i += 1
        # this has been a tutorial on how for loops should work.
        
        # this is all we need to do for now - we'll finish this up later.
        
        picList = listdir("images/"+collectionAbbrev+"/")
        picNo = 0
        for pic in picList:
            if(find(pic,".ds") >= 0):
                continue
            
            workName = pic[:-4]
            workDashes = replace(workName," ","-").lower()
            workURL="images/"+collectionAbbrev+"/"+pic
            
            # First, we're going to add a next button to the last thing we did.
            if(picNo == 0):
            #if(pic == picList[0]): [this should not work if the .ds_Store clause above happens.]
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
            picFile.write('                <!--#include file="../../menu.html" -->\n')
            picFile.write('            </div>\n')
            picFile.write('            <div id="content">\n')
            picFile.write('                <div class="post">\n')
            picFile.write('                    <h2><a href="../'+collectionAbbrev+'/index.html">'+upperCollectionAbbrev+'</a> ></h2>\n')
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
            archiveLines.insert(28,'                            <td>\n')
            archiveLines.insert(29,'                                <a href="pages/'+collectionAbbrev+'/'+workDashes+'.html">\n')
            archiveLines.insert(30,'                                    <img src="images/'+collectionAbbrev+'/'+pic+'">\n')
            archiveLines.insert(31,'                                    '+workName+'\n')
            archiveLines.insert(32,'                                </a>\n')
            archiveLines.insert(33,'                            </td>\n')
            
            textArchiveLines.insert(24,'                            <td>\n')
            textArchiveLines.insert(25,'                                <a href="pages/'+collectionAbbrev+'/'+workDashes+'.html">\n')
            textArchiveLines.insert(26,'                                    '+workName+'\n')
            textArchiveLines.insert(27,'                                </a>\n')
            textArchiveLines.insert(28,'                            </td>\n')
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
        collectionListLines.insert(len(collectionListLines)-7,'                        <li><a href="'collectionAbbrev+'/index.html">'+upperCollectionAbbrev+'</a></li>\n')
        for eachLine in collectionListLines:
            collectionListPage.write(eachLine)
        collectionListPage.close()
        
        #And, having done that, we just need to reinsert table rows into the archive.
        #We'll insert starting at 24 and then ending every 25. Then repeat.
        i=23
    while(i < len(archiveLines) - 7):
        if((i - 23) % 26 == 0):
            archiveLines.insert(i,'                        <tr>\n')
        elif((i-23) % 26 == 25):
            archiveLines.insert(i,'                        </tr>\n')
        i += 1
    i=23
    while(i < len(textArchiveLines) - 7):
        if((i - 23) % 22 == 0):
            textArchiveLines.insert(i,'                        <tr>\n')
        elif((i-23) % 22 == 21):
            textArchiveLines.insert(i,'                        </tr>\n')
        i += 1
    
    #And then we add the lines back into the file.
    for eachLine in archiveLines:
        archiveListPage.write(eachLine)
    for eachLine in textArchiveLines:
        textArchiveListPage.write(eachLine)
    archiveListPage.close()
    textArchiveListPage.close()
        #And so we've created one full collection. Now, we just overwrite lastPic and do it again for the next one.
        print("Collection created: "+upperCollectionAbbrev)
        lastPic = collectionAbbrev + "/" + replace((picList[-1])[:-4]," ","-").lower() + ".html"
    #
    #Now we're done, but we should output that we are done.
    print("...All collections created. Last pic: "+lastPic)