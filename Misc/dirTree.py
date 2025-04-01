import os

def listdir(leval,path):
    for i in os.listdir(path):
        print('| '*(leval + 1) + i)
        if os.path.isdir(path+i):
            listdir(leval+1, path+i)

path = 'F:'+os.sep+'视频'
print(path+os.sep)
listdir(0, path+os.sep)
