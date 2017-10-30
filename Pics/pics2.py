import os, requests, re
from datetime import datetime

def saveImg(imgList, headers = None, imgDir = None):
    x = 0
    imgDir = imgDir.strip("/")
    imgDir = imgDir.strip("\\")
    if not os.path.exists(imgDir):
        os.mkdir(imgDir)
    for imgURL in imgList:
        imgName = imgURL.split(sep = "/")[-1]
        imgFullName = imgDir + os.sep + imgName
        if os.path.exists(imgFullName):
            continue
        r = requests.get(imgURL, headers = headers)
        if r.status_code != requests.codes.ok: # 200
            continue
        with open (imgFullName, "wb") as img:
            img.write(r.content)
            x += 1
    return x

if __name__ == "__main__":
    from datetime import datetime
    from multiprocessing import Pool
    pool = Pool(4)
    imgRoot = "mikako"
    imgDir = ""
    if not os.path.exists(imgRoot):
        os.mkdir(imgRoot)
    pageURL = "http://www.meitulu.com/t/mikako/2.html"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0"}
    rq = requests.get(pageURL, headers = headers)
    htmlRe = re.compile(r"(http://www.meitulu.com/item/\d+).html", re.IGNORECASE)
    hl = htmlRe.findall(rq.text)
    hs = set(hl)
    imgRe = re.compile(r"http\://img\.buxidai\.com\/uploadfile\/[\d\/]+?\.jpg")
    h1 = re.compile(r"\<h1\>(.+)\</h1\>")
    imgDirRe = re.compile(r"[\/\\\:\*\?\<\>\|\n]+?")
    poolResult = list()
    for h in hs:
        for i in range(1, 50):
            if  (i == 1):
                imgURL = h + ".html"
            else:
                imgURL = h + "_{}.html".format(i)
            rq = requests.get(imgURL, headers = headers)
            if rq.status_code != requests.codes.ok: # 200
                 break
            rq.encoding = "utf_8"
            imgList = imgRe.findall(rq.text)
            if (i == 1):
                imgDir = h1.search(rq.text).group(1)
                imgDir = imgDir.strip()
                imgDir = imgDirRe.sub(r".", imgDir)
                imgDir = imgRoot + os.sep + imgDir
                with open(imgDir + ".html", "wt", encoding = "utf_8") as hf:
                    hf.write(rq.text)
            if (len(imgList) != 0):
                poolResult.append(pool.apply_async(saveImg, args = (imgList, headers, imgDir)))
                print(imgURL)
            else:
                break
    pool.close()
    pool.join()
    x = 0
    for res in poolResult:
        x += res.get()
    print("\n\n", x, "张图片")
    with open(imgRoot + os.sep + "pic.txt", "at", encoding = "utf_8") as pic:
        picTime = datetime.now().strftime("%Y%m%d.%H%M%S")
        pic.write(picTime + " --> {} 张图片".format(x))
