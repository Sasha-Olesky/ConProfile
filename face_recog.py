import cv2
import numpy
import os
import urllib2
from cookielib import CookieJar
import requests
import time
import threading
from bs4 import BeautifulSoup
import MySQLdb
from os import listdir
from os.path import isfile, join
import datetime

cookies = CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookies))
opener.addheaders = [('User-agent', 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 '
                                    '(KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17')]

def searchInfoByURL(url):
    googlePath = 'http://www.google.com/searchbyimage?image_url=' + url
    sourceCode = opener.open(googlePath).read()
    return sourceCode

def searchInfoByImage(filePath):
    searchUrl = 'http://www.google.com/searchbyimage/upload'
    multipart = {'encoded_image': (filePath, open(filePath, 'rb')), 'image_content': ''}
    response = requests.post(searchUrl, files=multipart, allow_redirects=False)
    fetchUrl = response.headers['Location']
    sourceCode = opener.open(fetchUrl).read()  # webbrowser.open(fetchUrl)
    return sourceCode

def searchInfoFromGoogle(filePath, url):
    if url:
        source = searchInfoByURL(filePath)
    else:
        source = searchInfoByImage(filePath)

    soup = BeautifulSoup(source, 'html.parser')

    results = {
        'links': [],
        'descriptions': [],
        'titles': [],
        'similar_images': []
    }
    print("\n\n-------------links---------------\n")
    for div in soup.findAll('div', attrs={'class': 'g'}):
        sLink = div.find('a')
        results['links'].append(sLink['href'])
        print(sLink['href'])

    print("-------------description---------------\n")
    for desc in soup.findAll('span', attrs={'class': 'st'}):
        results['descriptions'].append(desc.get_text())
        print(desc.get_text());

    print("-----------------title-----------------\n")
    for title in soup.findAll('h3', attrs={'class': 'r'}):
        results['titles'].append(title.get_text())
        print(title.get_text())

    print("------------similar_images-------------\n")
    rg_r = soup.find('div', attrs={'rg_r'})
    for similar_image in rg_r.findAll('img', attrs={'_WCg'}):
        img_url = similar_image.get('title')
        results['similar_images'].append(img_url)

    insertDataToMysql(results)

def runQueryMysql(query):
    try:
        db = MySQLdb.connect("localhost", "root", "", "facedb", charset='utf8')
        cursor = db.cursor()
    except MySQLdb.Error as err:
        print("Something went wrong: {}".format(err))
        return None

    try:
        cursor.execute(query)
        db.autocommit(True)
    except (MySQLdb.Error, MySQLdb.Warning) as e:
         print(e)

def insertDataToMysql(results):
    titles = results['titles']
    for title in titles:
        if title != "":
            firstMan = title
            break

    names = firstMan.split()

    firstName = names[0]
    lastName = names[1]

    urls = ['', '', '', '', '', '', '', '', '', '']
    links = results['links']
    count = len(links);

    if count >= 10:
        count = 9

    for i in range(0, count, 1):
        urls[i] = links[i]

    sql = "INSERT INTO people(first_name, last_name, first_date, last_sight, url1, url2, url3, url4, url5, url6, url7, " \
              "url8, url9, url10)  VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % \
          (firstName, lastName, "2017.12.10", "2017.12.10",
           urls[0], urls[1], urls[2], urls[3], urls[4], urls[5], urls[6], urls[7], urls[8], urls[9])
    print(sql)

    runQueryMysql(sql)

def detectFace():
    # Create Camera Object
    cap = cv2.VideoCapture(0)

    # Check if camera opened successfully
    if (cap.isOpened() == False):
        print("Error Connecting Camera")

    # Read until video is completed
    while (cap.isOpened()):
        # Capture frame-by-frame
        ret, frame = cap.read()
        cv2.putText(frame, "If ready, Press 'S' Key...", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, 255)

        if ret == True:
            # Display the resulting frame
            cv2.imshow('Camera', frame)

            # Press Esc on keyboard to  exit
            key = cv2.waitKey(30)
            if key == 27:
                break

            # Press 'S' on keyboard to starting capture
            if key == ord('s'):
                # Load face cascade data
                face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
                if not os.path.exists('faces'):
                    os.makedirs(str('faces'))

                # Detect Faces
                maxFaceCnt = 0
                for counter in range(0, 10):
                    ret, procFrame = cap.read()
                    gray = cv2.cvtColor(procFrame, cv2.COLOR_BGR2GRAY)
                    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
                    faceCnt = 0
                    for (x, y, w, h) in faces:
                        cv2.rectangle(procFrame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                        faceCnt = faceCnt + 1

                    if(maxFaceCnt < faceCnt):
                        maxFaceCnt = faceCnt
                        fileList = os.listdir(str('faces'))
                        for fileName in fileList:
                            os.remove(str('faces/') + fileName)

                        faceIdx = 0
                        for (x, y, w, h) in faces:
                            roi_color = procFrame[y:y + h, x:x + w]
                            name = str('faces/') + str(faceIdx) + '.png'
                            cv2.imwrite(name, roi_color)
                            faceIdx = faceIdx + 1

                    cv2.imshow('Camera', procFrame)
                    cv2.waitKey(30)

                break

        # Break the loop
        else:
            break

    # When everything done, release the video capture object
    cap.release()

    # Closes all the frames
    cv2.destroyAllWindows()

def getCurrentTime():
    now = datetime.datetime.now()
    date = str(now.year) + "." + str(now.month) + "." + str(now.day) + " " + str(now.hour) + ":" + str(now.minute) + ":" + str(now.second)
    return date

def main():

    detectFace()

    mypath = str('faces/')
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    full_path = os.getcwd()
    full_path = full_path.replace("\\", "/")

    date = getCurrentTime()

    for file in onlyfiles:
        filePath = full_path + "/faces/" + file
        sql = "INSERT INTO event(date, image_path, name_id)  VALUES ('%s', '%s', '%s')" % \
              (date, filePath, file)
        print(sql)
        runQueryMysql(sql)

        t = threading.Thread(target=searchInfoFromGoogle, args=(filePath, False,))
        t.start()

    print "Start Time: " + date

    # filePath = "http://images.fanpop.com/images/image_uploads/Stanislav-Ianevski-stanislav-ianevski-217641_288_399.jpg"
    # t1 = threading.Thread(target=searchInfoFromGoogle, args=(filePath, True,))
    # t1.start()
    #
    # filePath = 'C://Users/developer2018/Downloads/2.jpg'  # '/mnt/Images/test.png'
    # t2 = threading.Thread(target=searchInfoFromGoogle, args=(filePath, False,))
    # t2.start()

    time.sleep(60)

    end = time.time()   # Debug runtime
    print "End Time: " + str(end)

    #print "Search Time: " + str(end - start) + ' seconds'

main()
