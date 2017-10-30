import os, requests, re
from time import sleep
import random

def saveImg(imgList, imgDir="", headers=None):
    x = 0
    if (imgDir != ""):
        imgDir = imgDir.strip("/")
        imgDir = imgDir.strip("\\")
        if (imgDir != "") and (imgDir != "'./") and (not os.path.exists(imgDir)):
            os.mkdir(imgDir)
    if headers is None:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0"}
    for imgURL in imgList:
        if (not imgURL.startswith("http://")) and (not imgURL.startswith("https://")) and (not imgURL.startswith("ftp://")):
            imgURL = "http://" + imgURL
        imgName = imgURL.split(sep = "/")[-1]
        imgFullName = imgDir + os.sep + imgName
        if os.path.exists(imgFullName):
            continue
        r = requests.get(imgURL, headers=headers)
        sleep(random.random())
        if r.status_code != requests.codes.ok: # 200
            continue
        with open (imgFullName, "wb") as img:
            img.write(r.content)
            x += 1
    return x

if __name__ == "__main__":
    from datetime import datetime
    from multiprocessing import Pool
    pageURL = r"http://store.glennz.com/collections/all"
    imgRe = re.compile(r"cdn\.shopify\.com/s/files/1/0323/4857/products/.+\.(?:jpg|jpeg)")
    imgDir = "Glennz"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0"}
    pool = Pool(4) # 多线程
    poolResult = list()
    x = 0
    for i in range(1,7):
        params = {"page": i}
        rq = requests.get(pageURL, headers=headers, params=params)
        if rq.status_code != requests.codes.ok: # 200
                 break
        # rq.encoding = "utf_8" # 根据需要更改
        imgList = re.findall(imgRe, rq.text)
        if (len(imgList) == 0):
            print(rq.url)
            continue
        poolResult.append(pool.apply_async(saveImg, args=(imgList, imgDir, headers)))
        sleep(random.randint(0,5))
    print("i =", i)
    pool.close()
    pool.join()
    for res in poolResult:
      x += res.get()
    picTime = datetime.now().strftime("%Y-%m-%d.%H:%M:%S")
    print("\n" + pageURL)
    print(picTime + " ==> {} 张图片".format(x))
