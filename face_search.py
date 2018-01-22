import os
import urllib2
from cookielib import CookieJar
import requests
from threading import Thread, Lock
import threading
from bs4 import BeautifulSoup
import MySQLdb
import datetime
import time

cookies = CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookies))
opener.addheaders = [('User-agent', 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 '
                                    '(KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17')]
_db = None
_cursor = None

mutex = Lock()

def connectToMysql():
    global _db
    global _cursor

    try:
        _db = MySQLdb.connect("localhost", "root", "", "facedb", charset='utf8')
        _cursor = _db.cursor()
    except MySQLdb.Error as err:
        print("Something went wrong: {}".format(err))
        return None

def runQueryMysql(query, select = False):
    mutex.acquire()
    try:
        if _cursor == None or _db == None:
            print("Please check mysql service.")
            return

        try:
            _cursor.execute(query)
            _db.autocommit(True)
            if select:
                row = _cursor.rowcount
                return row
        except (MySQLdb.Error, MySQLdb.Warning) as e:
             print(e)
    finally:
        mutex.release()

def insertDataToMysql(results, filePath):
    titles = results['titles']

    names = None
    firstMan = None
    for title in titles:
        if title != "":
            firstMan = title
            break
    if firstMan != None:
        names = firstMan.split()

    firstName = ""
    lastName = ""

    if names == None:
        return
        firstName = "Unknown"
    elif len(names) > 1:
        firstName = names[0]
        lastName = names[1]
    elif len(names) > 0:
        firstName = names[0]

    urls = ['', '', '', '', '', '', '', '', '', '']
    links = results['links']
    count = len(links);

    if count >= 10:
        count = 9

    for i in range(0, count, 1):
        link = links[i]
        if "/search?" in link:
            link = ""
        urls[i] = link

    sql = "SELECT * from people_table WHERE first_name LIKE '%s' and last_name LIKE '%s' AND url1 LIKE '%s'" % \
          (firstName, lastName, urls[0])
    exist = runQueryMysql(sql, True)

    if exist > 0:
        rows = _cursor.fetchall()
        updateId = ""
        for row in rows:
            updateId = row[0]
            break
        nowTime = getCurrentTime()
        sql = "UPDATE people_table SET last_sight = '%s' WHERE id like '%s'" % \
              (nowTime, updateId)
        runQueryMysql(sql)
        return

    sql = "SELECT * from people_table"
    pId = runQueryMysql(sql, True)

    firstDate = getCurrentTime()

    sql = "INSERT INTO people_table(id, first_name, last_name, first_date, last_sight, url1, url2, url3, url4, url5, url6, url7, " \
              "url8, url9, url10)  VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % \
          (pId, firstName, lastName, firstDate, firstDate,
           urls[0], urls[1], urls[2], urls[3], urls[4], urls[5], urls[6], urls[7], urls[8], urls[9])
    print(sql)
    runQueryMysql(sql)

    sql = "SELECT * from event_table"
    eId = runQueryMysql(sql, True)
    date = getCurrentTime()
    sql = "INSERT INTO event_table(id, date, image_path, name_id)  VALUES ('%s', '%s', '%s', '%s')" % \
          (eId, date, filePath, pId)
    print(sql)
    runQueryMysql(sql)

# ------------------ Save complete html ----------------------
    wholeName = firstName + " " + lastName;
    t = threading.Thread(target=saveHttpContent, args=(results['links'], wholeName))
    t.start()

def searchInfoByURL(url):
    googlePath = 'http://www.google.com/searchbyimage?image_url=' + url
    sourceCode = opener.open(googlePath).read()
    return sourceCode

def searchInfoByImage(filePath):
    searchUrl = 'http://www.google.com/searchbyimage/upload'
    multipart = {'encoded_image': (filePath, open(filePath, 'rb')), 'image_content': ''}
    response = requests.post(searchUrl, files=multipart, allow_redirects=False)

    try:
        fetchUrl = response.headers['Location']
        sourceCode = opener.open(fetchUrl).read()  # webbrowser.open(fetchUrl)
    except:
        return None

    return sourceCode

def updatePeopelTable(imagePath):
    sql = "SELECT people_table.id FROM people_table LEFT JOIN event_table ON(people_table.id = event_table.name_id) WHERE event_table.image_path LIKE '%%%s%%'" % \
          (imagePath);

    exist = runQueryMysql(sql, True)
    if exist > 0:
        rows = _cursor.fetchall()
        updateId = ""
        for row in rows:
            updateId = str(row[0])
            break
        nowTime = getCurrentTime()
        sql = "UPDATE people_table SET last_sight = '%s' WHERE id like '%s'" % \
              (nowTime, updateId)
        runQueryMysql(sql)
        return

def searchInfoFromGoogle(filePath, url=False):
    if url:
        source = searchInfoByURL(filePath)
    else:
        source = searchInfoByImage(filePath)

    if source == None:
        return

    soup = BeautifulSoup(source, 'html.parser')
    results = {
        'links': [],
        'descriptions': [],
        'titles': [],
        'similar_images': []
    }

    print("-----------------title-----------------\n")
    for title in soup.findAll('h3', attrs={'class': 'r'}):
        results['titles'].append(title.get_text())

    print("\n\n-------------links---------------\n")
    for div in soup.findAll('div', attrs={'class': 'g'}):
        sLink = div.find('a')
        link = sLink['href']
        if link != "":
            results['links'].append(link)

    titles = results['titles']

    names = None
    firstMan = None
    for title in titles:
        if title != "":
            firstMan = title
            break

    if firstMan != None:
        names = firstMan.split()

    if names == None:
        return

    print("-------------description---------------\n")
    for desc in soup.findAll('span', attrs={'class': 'st'}):
        results['descriptions'].append(desc.get_text())

    print("------------similar_images-------------\n")
    rg_r = soup.find('div', attrs={'rg_r'})

    try:
        if rg_r != None:
            for similar_image in rg_r.findAll('img', attrs={'_WCg'}):
                img_url = similar_image.get('title')
                results['similar_images'].append(img_url)
    except:
        insertDataToMysql(results, filePath)

    insertDataToMysql(results, filePath)

def getCurrentTime(DateOnly=False):
    now = datetime.datetime.now()
    if DateOnly == True:
        date = str(now.year) + "." + str(now.month) + "." + str(now.day)
    else:
        date = str(now.year) + "." + str(now.month) + "." + str(now.day) + " " + str(now.hour) + ":" + str(now.minute) + ":" + str(now.second)
    return date

def saveHttpContent(links, name):
    rootDir = 'downloads/'

    if not os.path.exists(rootDir):
        os.makedirs(str('downloads'))

    for link in links:
        try:
            page = urllib2.urlopen(link).read()
        except:
            continue

        soup = BeautifulSoup(page, 'html.parser')

        dirName = soup.find('title')

        if dirName == None:
            dirName = name
        else:
            dirName = dirName.get_text()

        if ',' in dirName:
            dirName = dirName.split(',')[0]

        fileName = rootDir + dirName + ".html"
        try:
            with open(fileName, "wb") as f:
                f.write(page)
        except:
            dirName = name
            fileName = rootDir + dirName + ".html"

            try:
                with open(fileName, "wb") as f:
                    f.write(page)
            except:
                fileName = rootDir + "unknown_" + getCurrentTime(True) + ".html"
                with open(fileName, "wb") as f:
                    f.write(page)

        directory = rootDir + dirName + "/"

        try:
            if not os.path.exists(directory):
                os.makedirs(directory)
        except:
            return

        for img in soup('img'):
            try:
                imgUrl = img['src']
            except:
                continue

            if "://" in imgUrl:
                imgFullUrl = imgUrl
            elif "//" in imgUrl:
                imgFullUrl = "http:" + imgUrl
            else :
                imgFullUrl = link + imgUrl


            try:
                img = urllib2.urlopen(imgFullUrl).read()
            except:
                continue

            filename = imgFullUrl[imgFullUrl.rfind("/")+1:]
            imgpath = directory  + filename

            try:
                with open(imgpath, "wb") as f:
                    f.write(img)
            except:
                continue

    print("finish")

# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
#
# def saveCompleteHtml(url):
#
#     browser = webdriver.Firefox()
#
#     browser.get('http://www.yahoo.com')
#     assert 'Yahoo' in browser.title
#
#     elem = browser.find_element_by_name('p')  # Find the search box
#     elem.send_keys('seleniumhq' + Keys.RETURN)
#
#     browser.quit()
