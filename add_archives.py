'''
Created on Jan 26, 2016

@author: Birdy

'''

import os
import sys
import fileinput
import string
from string import find

if __name__ == '__main__':    
    originalArchiveFile = open("archive/full_archive.html", 'r+')
    filedata = originalArchiveFile.readlines()
        
    currentNumberOfArchivePages = 17 # Including full_archive and final_archive; not including index.html
    archiveStack = []
    e = 0
    lnno = 0
    for eachline in filedata:
        if(e < 22):
            e += 1
            continue
        elif eachline.find("tr>") >= 0:
            continue
        elif eachline.find("</table>") >= 0:
            break
        # now, we can put everything in a queue.
        if(lnno % 6 == 0):
            archiveStack.append([])
            lnno = 1
        else:
            lnno += 1
        archiveStack[-1].insert(0, eachline)
        # Now, after this we should have every single work in the archive.
        e += 1
    # Find how many archive pages we're going to have in total
    numberNewArchivePages = int(len(archiveStack) / 40.0) # this means we won't count the current archive page
    for i in range(numberNewArchivePages):
        # shift all the other ones back
        for j in range(currentNumberOfArchivePages - 2):
            # We need to walk backwards and rename. We don't want to go through full_archive though. 
            arcFileStr = "archive/full_archive_"+str(currentNumberOfArchivePages + i - 1 - j)+".html"
            newFileStr = "archive/full_archive_"+str(currentNumberOfArchivePages + i - j)+".html"
            os.rename(arcFileStr, newFileStr)
    # We have done our shifts. Now we can create some new files.
    # Now we need to create a menu and give it to all existing files. 
    menuStr = '                    [Go to page: <a href="full_archive.html">1</a> '
    totalNumberArchivePages = currentNumberOfArchivePages + numberNewArchivePages
    for i in range(totalNumberArchivePages):
        if(i == 0): continue
        if(i == totalNumberArchivePages - 1):
            menuStr = menuStr + '<a href="full_archive_final.html">' + str(i+1) + '</a> '
        else: 
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
        currentPageString = "archive/full_archive_" + str(numberNewArchivePages - i + 1) + ".html"
        prevString = "full_archive_" + str(numberNewArchivePages - i) + ".html"
        if(i == numberNewArchivePages - 1):
            prevString = "full_archive.html"
        nextString = "full_archive_" + str(numberNewArchivePages - i + 2) + ".html"
        currentPageFile = open(currentPageString, 'w')
        currentPageFile.write('<!--<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">-->\n'\
            '<!DOCTYPE html>\n'\
            '<html "lang=en">\n'\
            '<head>\n'\
            '        <link href="../momaStyleSheet.css" rel="stylesheet" type="text/css">\n'\
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
            thisWork = archiveStack.pop(-40 + j)
            if(j % 4 == 0):
                currentPageFile.write('                        <tr>\n')
            for eachline in reversed(thisWork):
                currentPageFile.write(eachline)
            if(j % 4 == 3):
                currentPageFile.write('                        </tr>\n')
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
    currentPageName = "archive/full_archive.html"
    currentPageFile = open(currentPageName, 'w')
    currentPageFile.write('<!--<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">-->\n'\
                    '<!DOCTYPE html>\n'\
                    '<html "lang=en">\n'\
                    '    <head>\n'\
                    '        <link href="../momaStyleSheet.css" rel="stylesheet" type="text/css">\n'\
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
                    '' + menuStr + ''\
                    '                </div>\n'\
                    '                    <div class="post">'\
                    '                    Warning: these pages get a little bit long, so you might be better served looking through our various <a href="../pages/index.html">collections</a> instead, if you\'re looking to browse. Or if you\'re looking for a specific work whose name you know, you might prefer to search the <a href="index.html">text-based index</a>.'\
                    '                </div>'\
                    '                <div class="post">\n'\
                    '                    <table class="smaller">\n')
    assize = len(archiveStack)
    j = 0
    while len(archiveStack) > 0:
        thisWork = archiveStack.pop()
        if(j % 4 == 0):
            currentPageFile.write('                        <tr>\n')
        for eachline in reversed(thisWork):
            currentPageFile.write(eachline)
        if(j % 4 == 3):
            currentPageFile.write('                        </tr>\n')
        j += 1
    # We're done loading our data.
    if j % 4 != 3:
        currentPageFile.write('                        </tr>\n')
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