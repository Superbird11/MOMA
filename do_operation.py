'''
Created on Jan 26, 2016

@author: Birdy

'''

import os
import sys
import fileinput
import string
from string import find
from math import floor

if __name__ == '__main__':    
    originalArchiveFile = open("archive/full_archive.html", 'r+')
    filedata = originalArchiveFile.readlines()
        
    currentNumberOfArchivePages = 17 # Including full_archive and final_archive; not including index.html
    archiveStack = []
    e = 0
    lnno = 0
    for eachline in filedata:
        if(e < 26):
            e += 1
            continue
        elif eachline.find("<table>") >= 0 or eachline.find("div>") >= 0:
            continue
        elif eachline.find("</table>") >= 0:
            break
        # now, we can put everything in a queue.
        if(lnno % 6 == 0):
            archiveStack.append([])
            lnno = 1
        else:
            lnno += 1
        archiveStack[-1].append(eachline)
        # Now, after this we should have every single work in the archive.
        e += 1
    # Find how many archive pages we're going to have in total
    numberNewArchivePages = int(floor(len(archiveStack) / 40.0)) # this means we won't count the current archive page
    print len(archiveStack), numberNewArchivePages
    for i in range(numberNewArchivePages):
        # shift all the other ones back
        for j in range(currentNumberOfArchivePages - 2):
            # We need to walk backwards and rename. We don't want to go through full_archive though. 
            arcFileStr = "archive/full_archive_"+str(currentNumberOfArchivePages - 1 - j)+".html"
            newFileStr = "archive/full_archive_"+str(currentNumberOfArchivePages - j)+".html"
            try:
                os.rename(arcFileStr, newFileStr)
            except OSError:
                continue
    # We have done our shifts. Now we can create some new files.
    # Now we need to create a menu and give it to all existing files. 
    menuStr = '                    [Go to page: <a href="full_archive.html">1</a> '
    totalNumberArchivePages = currentNumberOfArchivePages + numberNewArchivePages
    for i in range(totalNumberArchivePages):
        if(i == 0): continue
        menuStr = menuStr + '<a href="full_archive_' + str(i+1) + '.html">' + str(i+1) + '</a> '
    menuStr = menuStr + ']'
    # Now, let's replace that line (and prev/next page lines) for all existing archive pages
    for i in range(currentNumberOfArchivePages - 1): # not counting first
        currentPageNumber = i + numberNewArchivePages + 2
        currentPageString = ''
        if(i == currentNumberOfArchivePages - 2):
            currentPageString = "archive/full_archive_final.html"
        else:
            currentPageString = "archive/full_archive_" + str(currentPageNumber) + ".html"
        currentPageFile = open(currentPageString, 'r')
        currentPageLines = currentPageFile.readlines()
        currentPageFile.close()
        pnline = '                    [ <a href="full_archive_' + str(currentPageNumber - 1) + '.html">Previous Page</a> | <a href="full_archive_'\
            + str(currentPageNumber + 1) + '.html">Next Page</a> ]'
        if(i == currentNumberOfArchivePages - 3):
            pnline = '[ <a href="full_archive_' + str(currentPageNumber - 1) + '.html">Previous Page</a> | <a href="full_archive_final.html">Next Page</a> ]'
        elif(i == currentNumberOfArchivePages - 3):
            pnline = '[ <a href="full_archive_' + str(currentPageNumber - 1) + '.html">Previous Page</a> ]'
        currentPageLines[19] = pnline
        currentPageLines[20] = menuStr
        # Now, reinsert...
        currentPageFile = open(currentPageString, 'w')
        for j in currentPageLines:
            currentPageFile.write(j + "\n")
        currentPageFile.close()
    # We've fixed every existing file now. Except the first one - we'll get to it later.
    # Now to create all our new files.
    for i in range(numberNewArchivePages):
        currentPageString = "full_archive_" + str(numberNewArchivePages - i + 1) + ".html"
        prevString = "full_archive_" + str(numberNewArchivePages - i) + ".html"
        if(i == numberNewArchivePages - 1):
            prevString = "full_archive.html"
        nextString = "full_archive_" + str(numberNewArchivePages - i + 2) + ".html"
        currentPageFile = open(currentPageString, 'w')
        currentPageFile.write('<!--<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">-->\n'\
            '<!DOCTYPE html>\n'\
            '<html "lang=en">\n'\
            '<head>\n'\
            '        <link href="momaStyleSheet.css" rel="stylesheet" type="text/css">\n'\
            '        <meta http-equiv="Content-type" content="text/html;charset=utf-8">\n'\
            '        <title>MOMA - Archive</title>\n'\
            '        \n'\
            '        <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.11.2/jquery.min.js"></script>\n'\
            '        <!--if I ever care about jquery-->\n'\
            '    </head>\n'\
            '    <body>\n'\
            '        <div id="header">Monitors of Modern Art</div>\n'\
            '        <div id="container">\n'\
            '            <div id="menu">\n'\
            '                <!--#include virtual="../menu1.shtml" -->\n'\
            '            </div>\n'\
            '            <div id="content">\n'
            '                <div class="post">\n'\
            '                    [ <a href="'+prevString+'">Previous Page</a> / <a href="'+nextString+'">Next Page</a> ]\n'\
            '' + menuStr + ''\
            '                </div>\n'\
            '                <div class="post">\n'\
            '                    <table class="smaller">\n')
        for j in range(40):
            thisWork = archiveStack.pop()
            if(j % 4 == 0):
                currentPageFile.write('                        <tr>')
            for eachline in thisWork:
                currentPageFile.write(eachline)
            if(j % 4 == 3):
                currentPageFile.write('                        </tr>')
        # We're done loading our data.
        currentPageFile.write('                    </table>\n'\
                    '                </div>\n'\
                    '            </div>\n'\
                    '            <div id="footer">&copy Louis Jacobowitz 2016</div>\n'\
                    '        </div>\n'\
                    '    </body>\n'\
                    '</html>')
        currentPageFile.close()
    # Finally, rewrite the first page.
    currentPageName = "full_archive.html"
    currentPageFile = read(currentPageName, 'w')
    currentPageFile.write('<!--<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">-->\n'\
                    '<!DOCTYPE html>\n'\
                    '<html "lang=en">\n'\
                    '<head>\n'\
                    '        <link href="momaStyleSheet.css" rel="stylesheet" type="text/css">\n'\
                    '        <meta http-equiv="Content-type" content="text/html;charset=utf-8">\n'\
                    '        <title>MOMA - Archive</title>\n'\
                    '        \n'\
                    '        <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.11.2/jquery.min.js"></script>\n'\
                    '        <!--if I ever care about jquery-->\n'\
                    '    </head>\n'\
                    '    <body>\n'\
                    '        <div id="header">Monitors of Modern Art</div>\n'\
                    '        <div id="container">\n'\
                    '            <div id="menu">\n'\
                    '                <!--#include virtual="../menu1.shtml" -->\n'\
                    '            </div>\n'\
                    '            <div id="content">\n'
                    '                <div class="post">\n'\
                    '                    [ <a href="full_archive_2.html">Next Page</a> ]\n'\
                    '' + menustr + ''\
                    '                </div>\n'
                    '                <div class="post">\n'\
                    '                    <table class="smaller">\n')
    assize = len(archiveStack)
    while len(archiveStack) > 0:
        thisWork = archiveStack.pop()
        if(j % 4 == 0):
            currentPageFile.write('                        <tr>')
        for eachline in thisWork:
            currentPageFile.write(eachline)
        if(j % 4 == 3):
            currentPageFile.write('                        </tr>')
    # We're done loading our data.
    if assize % 4 != 3:
        currentPageFile.write('                        </tr>')
    currentPageFile.write('                    </table>\n'\
                    '                </div>\n'\
                    '            </div>\n'\
                    '            <div id="footer">&copy Louis Jacobowitz 2016</div>\n'\
                    '        </div>\n'\
                    '    </body>\n'\
                    '</html>')
    currentPageFile.close()
    #
    #
    print "...Complete."