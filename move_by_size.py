#!/usr/bin/python3

from os import path, mkdir, listdir
import shutil

src_dir = "/home/jonathas/Desktop/thumbs"

images = listdir(src_dir)

print(len(images))

for image in images:
    full_path = path.join(src_dir, image)
    if not path.isdir(full_path):
        filesize = path.getsize(full_path)
        if filesize < 2006: # 2kb
            shutil.move(full_path, path.join(src_dir, "small"))

print("After moving small files...")
images = listdir(src_dir)
print(len(images))
