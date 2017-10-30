import os, requests

def findImgList(url, params = None, headers = None):
    L = list()
    r = requests.get(url, params = params, headers = headers)
    print("网址", r.url)
    print("Status Code:", r.status_code)
    if r.status_code != requests.codes.ok: #200        
        return L
    s = r.text
    # with open("page.html", "wt", encoding = "utf_8") as p:
        # p.write(s)
    a = 0
    b = 0
    while (a != -1):
        a = s.find("\"http", a)
        if (a != -1):
            b = s.find(".JPG\"", a+5, a+260)
            if (b != -1): # 找到图片链接
                L.append(s[a+1:b+4])
                a = b+5
            else:
                a += 260
    return L

def saveImg(imgList, headers = None, imgDir = None):
    x = 0
    imgDir = imgDir.strip(r"/")
    imgDir = imgDir.strip(r"\\")
    if not os.path.exists(imgDir):
        os.mkdir(imgDir)
    for imgURL in imgList:
        r = requests.get(imgURL, headers = headers)
        if r.status_code != requests.codes.ok: # 200
            continue
        imgName = imgURL.split(sep = "/")[-1]
        with open (imgDir + os.sep + imgName, "wb") as img:
            img.write(r.content)
            x += 1
    return x

if __name__ == "__main__":
    pageURL = "http://t.30edu.com.cn/03962167/Article.do?ID=dabf8849-07d4-48da-b581-583dde385cca"
    params = None
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0"}
    imgL = findImgList(pageURL, params = params)
    x = saveImg(imgL, imgDir = "img")
    print ("{} 张图片".format(x))
