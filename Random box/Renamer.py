#Just a small program to change the names of video files I download.

import os

#os.rename(old_name, new_name)
#root, dirs, files = os.walk(path, topdown = True)

files = list(os.scandir(path='.'))
quality_id = ('2160p', '1080p', '720p', '540p', '480p', 'XviD', 'HDTV', 'WEB')

for i in range(len(files)):
    file = files[i]
    files[i] = file.name

count = 0
for file in files:
    if file[-3:] != '.py':
        old_name, extension = os.path.splitext(file)
        for q in quality_id:
            idx = old_name.find(q)
            if idx != -1:
                break
        if idx != -1:
            count += 1
            new_name = old_name[:idx-1]
            new_name = new_name.replace('.',' ')
            new_name = new_name.title()
            os.rename(old_name + extension, new_name + extension)

print(str(count) + ' files renamed.')
os.system('pause')