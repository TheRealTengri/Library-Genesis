from requests import get, ConnectionError
from sys import argv, exit
import os
import subprocess
import json
from cursor import hide, show
import getpass
import wget
import urllib
global isbn
hide()
apppath = subprocess.getoutput("echo %appdata%")
apppath += r"\LibGen"
username = getpass.getuser()
downloads = "C:\\Users\\{0}\\Downloads".format(username)
def fiction():
    global isbn
    try:
        os.chdir(apppath)
    except FileNotFoundError:
        os.mkdir(apppath)
    fileexists = os.path.exists('apikey')
    if fileexists == False:
        key = input("Enter your Google Books API key (you can get one at https://developers.google.com/books/docs/v1/using#APIKey): ")
        print("Verifying API key...", end="\r")
        verify = get("https://www.googleapis.com/books/v1/volumes?q=isbn\%3D9780590353427&key={0}".format(key))
        if verify.status_code == 200:
            print("Verifying API key...done")
            with open('apikey', "w+") as keyfile:
                keyfile.write(key)
        elif verify.status_code != 200:
            print("Verifying API key...failed")
            os.system("del /f apikey")
            print("Error: Invalid API key")
            show()
            exit()
    else:
        keyfile = open('apikey', "r+")
        key = keyfile.read()
        verify = get("https://www.googleapis.com/books/v1/volumes?q=isbn\%3D9780590353427&key={0}".format(key))
        if verify.status_code == 200:
            print("Verifying API key...done")
            keyfile.close()
        elif verify.status_code != 200:
            keyfile.close()
            os.system("del /f apikey")
            print("Verifying API key...failed")
            print("Error: Invalid API key")
            show()
            exit()
    try:
        int(isbn)
    except ValueError:
        print("Error: Invalid ISBN")
        show()
        exit()
    isbn = isbn.replace("-", "")
    isbn = isbn.replace(" ", "")
    print("Verifying ISBN...", end="\r")
    try:
        titlesource = str(get("https://www.googleapis.com/books/v1/volumes?q=isbn%3D{0}&key={1}".format(isbn, key)).text)
        titlesource = json.loads(titlesource)
    except ConnectionError:
        print("Error: No connection available")
        show()
        exit()
    try:
        title = titlesource["items"][0]["volumeInfo"]["title"]
        try:
            by = title.index("by")
            title = title[0:by]
            title = title.split()
            title = '+'.join(title)
            author = by + 1
            author = title[author:]
            author = " ".join(author)
        except:
            author = titlesource["items"][0]["volumeInfo"]["authors"][0]
        print("Verifying ISBN...done")
    except KeyError:
        print("Verifying ISBN...failed")
        print("Error: ISBN not supported or invalid (maybe check the ISBN on the google books website)")
        show()
        exit()
    print("Getting download link...", end="\r")
    author = author.split()
    author = "+".join(author)
    search = "{0}+{1}".format(title, author)
    search = search.replace(" ", "+")
    searchurl = "http://libgen.is/fiction/?q={0}".format(search)
    downloadpage = get(searchurl).text
    downloadpage = downloadpage.split("\n")
    downloadlocation = downloadpage.index('\t<td style="width:15%">Author(s)</td>')
    downloadlocation += 19
    downloadpage = downloadpage[downloadlocation]
    downloadpage = downloadpage.split('"')
    downloadpage = downloadpage[3]
    downloadverify = downloadpage.split("/")
    if downloadverify[2] != "93.174.95.29":
        print("Getting download link...failed")
        print("Error: The book is not in Library Genesis")
        show()
        exit()
    else:
        downloadurl = get(downloadpage).text
        downloadurl = downloadurl.split("\n")
        downloadurl = downloadurl[41]
        downloadurl = downloadurl.split('"')
        downloadurl = downloadurl[5]
        print("Getting download link...done")
        print(downloadurl)
        show()
def nonfiction():
    global isbn
    try:
        os.chdir(apppath)
    except FileNotFoundError:
        os.mkdir(apppath)
    fileexists = os.path.exists('apikey')
    if fileexists == False:
        key = input("Enter your Google Books API key (you can get one at https://developers.google.com/books/docs/v1/using#APIKey): ")
        print("Verifying API key...", end="\r")
        verify = get("https://www.googleapis.com/books/v1/volumes?q=isbn\%3D9780590353427&key={0}".format(key))
        if verify.status_code == 200:
            print("Verifying API key...done")
            with open('apikey', "w+") as keyfile:
                keyfile.write(key)
        elif verify.status_code != 200:
            print("Verifying API key...failed")
            os.system("del /f apikey")
            print("Error: Invalid API key")
            show()
            exit()
    else:
        keyfile = open('apikey', "r+")
        key = keyfile.read()
        verify = get("https://www.googleapis.com/books/v1/volumes?q=isbn\%3D9780590353427&key={0}".format(key))
        if verify.status_code == 200:
            print("Verifying API key...done")
            keyfile.close()
        elif verify.status_code != 200:
            keyfile.close()
            os.system("del /f apikey")
            print("Verifying API key...failed")
            print("Error: Invalid API key")
            show()
            exit()
    try:
        int(isbn)
    except ValueError:
        print("Error: Invalid ISBN")
        show()
        exit()
    isbn = isbn.replace("-", "")
    isbn = isbn.replace(" ", "")
    print("Verifying ISBN...", end="\r")
    try:
        titlesource = str(get("https://www.googleapis.com/books/v1/volumes?q=isbn%3D{0}&key={1}".format(isbn, key)).text)
        titlesource = json.loads(titlesource)
    except ConnectionError:
        print("Error: No connection available")
        show()
        exit()
    try:
        title = titlesource["items"][0]["volumeInfo"]["title"]
        try:
            by = title.index("by")
            title = title[0:by]
            title = title.split()
            title = '+'.join(title)
            author = by + 1
            author = title[author:]
            author = " ".join(author)
        except:
            author = titlesource["items"][0]["volumeInfo"]["authors"][0]
        print("Verifying ISBN...done")
    except KeyError:
        print("Verifying ISBN...failed")
        print("Error: ISBN not supported or invalid (maybe check the ISBN on the google books website)")
        show()
        exit()
    print("Getting download link...", end="\r")
    author = author.split()
    author = "+".join(author)
    search = "{0}+{1}".format(title, author)
    search = search.replace(" ", "+")
    searchurl = "http://libgen.is/search.php?req={0}".format(search)
    downloadpage = get(searchurl).text
    downloadpage = downloadpage.split("\n")
    try:
        downloadpage = downloadpage[805]
    except IndexError:
        print("Getting download link...failed")
        print("Error: The book is not in Library Genesis")
        show()
        exit()
    downloadpage = downloadpage.replace("\t", "")
    downloadpage = downloadpage.split("'")
    downloadpage = downloadpage[1]
    downloadverify = downloadpage.split("/")
    if downloadverify[2] != "93.174.95.29":
        print("Getting download link...failed")
        print("Error: The book is not in Library Genesis")
        print(downloadverify)
        show()
        exit()
    else:
        downloadurl = get(downloadpage).text
        downloadurl = downloadurl.split("\n")
        downloadurl = downloadurl[41]
        downloadurl = downloadurl.split('"')
        downloadurl = downloadurl[5]
        print("Getting download link...done")
        print(downloadurl)
        show()
print(len(argv))
if len(argv) < 3:
    print("Format: libgen [fiction or nonfiction] isbn")
    show()
    exit()
else:
    isbn = argv[2:]
    isbn = "".join(isbn)
    genre = argv[1]
    try:
        int(isbn)
    except:
        isbn = isbn.replace("-", "")
if genre == "fiction":
    try:
        fiction()
    except KeyboardInterrupt:
        print("\nExiting...")
        show()
        exit()
    except ConnectionError:
        print("Error: No connection available")
        show()
        exit()
    except ValueError:
        print("Error: The book is not in Library Genesis")
        show()
        exit()
elif genre == "nonfiction":
    try:
        nonfiction()
    except KeyboardInterrupt:
        print("\nExiting...")
        show()
        exit()
    except ConnectionError:
        print("Error: No connection available")
        show()
        exit()
    except ValueError:
        print("Error: The book is not in Library Genesis")
        show()
        exit()
else:
    print("Format: libgen [fiction or nonfiction] isbn")
    show()
    exit()
