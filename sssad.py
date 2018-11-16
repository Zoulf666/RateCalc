# encoding: utf-8
import tkinter
import tkinter.messagebox
from urllib.request import urlopen
from urllib.request import urlretrieve
import urllib
import shutil
from zipfile import *
import json
import threading
import time


def getLocalVersion():
    fileHndl = open("./Updater/version.json", "r")
    lst = json.load(fileHndl)
    fileHndl.close()
    print(lst)
    return lst


def getLocalConfig():
    fileHndl = open("./Updater/config.json", "r")
    lst = json.load(fileHndl)
    fileHndl.close()
    print(lst)
    return lst


def getRemoteVersion():
    url = getLocalConfig()["remote-cfg"]
    cfg = urlopen(url).read().decode("gb2312")
    print(cfg)
    return json.loads(cfg)


def setLocalVersion(lst):
    fileHndl = open("./Updater/version.json", "w")
    s = json.dumps(lst)
    fileHndl.write(s)
    fileHndl.close()


def update(url="hello"):
    print("UPDATING")
    global infoString
    infoString.set("")
    global updateBtn
    updateBtn.destroy()
    # TODO:UPDATE etc
    # 1.download zip(with progressbar)
    # 2.extractAll()
    # 3.change infoString & create updateBtn again
    print(url)
    try:
        def report(count, blockSize, totalSize):
            percent = int(count * blockSize * 100 / totalSize)
            print("已下载%d%%" % (percent))
            infoString.set("已下载%d%%" % (percent))

        for i in range(20):
            time.sleep(3)
            report(i + 1, 5.0, 100)
        # urlretrieve(url, "Client.zip", reporthook=report)
        # thr=threading.Thread(target=urlretrieve,args=(url,"Client.zip"),kwargs={"reporthook":report})
        # thr.start()
    except IOError as e:
        infoString.set("下载失败")
        f = open("./Updater/log.log", "w")
        print("下载失败", file=f)
        print(e, file=f)
    # thr.join()
    infoString.set("下载完成 解压中...")
    try:
        try:
            shutil.rmtree("./.minecraft")
        except:
            pass
        z = ZipFile("Client.zip", "r")
        z.extractall()
    except BadZipFile as e:
        infoString.set("解压失败")
        f = open("./Updater/log.log", "w")
        print("解压失败", file=f)
        print(e, file=f)
    remoteVer = getRemoteVersion()
    del remoteVer["url"]
    setLocalVersion(remoteVer)
    ver = getLocalVersion()["version"]
    desc = getLocalVersion()["desc"]
    infoString.set("\n\n\n更新成功\n版本：%d\n%s" % (ver, desc))
    updateBtn = tkinter.Button(windowHndl, text="检查更新", command=chkUpdate, font=("宋体", 20))
    updateBtn.pack()
    return


def chkUpdate():
    print("UPDATE CHK")
    # remoteVer=getRemoteVersion()
    # localVer=getLocalVersion()
    # print(remoteVer,localVer)
    # if localVer["version"]<remoteVer["version"]:
    #    if (tkinter.messagebox.askyesno("发现新版本","是否更新？")==True):
    threading.Thread(target=update).start()
    #    update("url")
    # else:
    #    tkinter.messagebox.showinfo("无新版本","本地版本是最新的\nGo And Play!")
    return


# init
windowHndl = tkinter.Tk()
windowHndl.geometry("400x300")
windowHndl.wm_title("整合包更新器")

# get ver & desc
ver = 123  # getLocalVersion()["version"]
desc = "hello"  # getLocalVersion()["desc"]
infoString = tkinter.StringVar(value="\n\n\n版本：%d\n%s" % (ver, desc))
info = tkinter.Label(windowHndl, textvariable=infoString, font=("宋体", 20))
info.pack()
updateBtn = tkinter.Button(windowHndl, text="检查更新", command=chkUpdate, font=("宋体", 20))
updateBtn.pack()
windowHndl.mainloop()
# windowT=threading.Thread(target=windowHndl.mainloop())
# windowT.start()
