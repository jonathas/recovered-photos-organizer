#!/usr/bin/python3

from os import path, mkdir, listdir
import shutil

src_dir = "/run/media/jonathas/Elements/recovered_photos"
filename = "f347199488.jpg"

file_path = path.join(src_dir, filename)

print(file_path)

images = listdir(src_dir)
images.sort()

# print(images)
print(len(images))

target_element = images.index(filename) + 1
new_list = images[target_element:]

print(len(new_list))

for image in new_list:
    full_path = path.join(src_dir, image)
    if not path.isdir(full_path):
        shutil.move(full_path, path.join(src_dir, "continuing"))
