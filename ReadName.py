import os
path=r"D:\2021 s2\8715\Video\Video"
files=os.listdir(path)

lenN=len(files)
for i in range (0,lenN):
    head, sep, tail = files[i].partition('.myreel')
    files[i]=head


for i in range (0,lenN):
    print(files[i])