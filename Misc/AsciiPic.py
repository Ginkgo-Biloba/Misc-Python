from PIL import Image
import argparse

# 70 个字符
ascChar = list(""" .\'`^",:;Il!i><~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$""")

# 将256灰度映射到 70 个字符上
def rgb2char(r, g, b, alpha=255, ascChar=ascChar):
    if (alpha == 0):
        return ' '
    grey = (0.2126 * r + 0.7152 * g + 0.0722 * b) * alpha / 255
    unit = (256.0 + 1) / len(ascChar)
    return ascChar[int(grey/unit)]

def img2asc(imgIn, txtOut=None, wOut=80, hOut=80, ascChar=ascChar):
    im = Image.open(imgIn)
    im = im.convert(mode="RGBA")
    im = im.resize((wOut, hOut), Image.BILINEAR)
    txt = str()

    for i in range(hOut):
        for j in range(wOut):
            (r, g, b, a) = im.getpixel((j, i))
            txt += rgb2char(r, g, b, a, ascChar)
        txt += '\n'

    print(txt)

    # 输出到文本文件
    if txtOut is not None:
        with open(txtOut, "w", encoding="utf-8") as f:
            f.write(txt)
    
if __name__ == "__main__":
    
    # 获取参数
    parser = argparse.ArgumentParser()
    parser.add_argument("file") # 输入文件
    parser.add_argument("-o", "--output") # 输出文件
    parser.add_argument("--wo", type=int, default=80) # 输出字符画宽
    parser.add_argument("--ho", type=int, default=80) # 输出字符画高

    # 解析参数
    args = parser.parse_args()
    imgIn = args.file
    txtOut = args.output
    wOut = args.wo
    hOut = args.ho

    img2asc(imgIn, txtOut, wOut, hOut)
