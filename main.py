#!/usr/bin/python3

import sys
from os import path, mkdir, listdir
import shutil
from PIL import Image
import csv

class RPO:

    _thumbs_width = 512
    _filetypes = ["jpg", "png"]
    _result_dir_name = "recovered_photos"

    def __init__(self, argv):
        self._validate_input_dir(argv)
        self._src_dir = argv[1]
        self._process()

    def _validate_input_dir(self, argv):
        try:
            srcdir = argv[1]
            if not path.exists(srcdir):
                raise Exception("The path you informed is not accessible or doesn't exist")
            if not path.isdir(srcdir):
                raise Exception("The path you informed is not a directory")
        except IndexError as err:
            print("Please call the script informing the directory where your photos are located")
            sys.exit(1)
        except Exception as err:
            print(err)
            sys.exit(1)

    def _process(self):
        self._create_dirs()

        for dir_path in self._get_src_recovery_dirs():
            print("==> Copying images from: " + dir_path + " to " + self._result_dir)
            self._copy_images(self._get_images_from_path(dir_path), dir_path)

        result_images = self._get_images_from_path(self._result_dir)
        self._move_thumbnails(result_images)

        print("\nImages: " + str(self._images_count) + "\n")
        print("Thumbnails: " + str(self._thumbs_count) + "\n")

    def _create_dirs(self):
        self._result_dir = path.realpath(path.join(self._src_dir, ".." , self._result_dir_name))
        self._thumbs_dir = path.join(self._result_dir, "thumbs")

        if not path.isdir(self._result_dir):
            print("==> Creating result dir: " + self._result_dir)
            mkdir(self._result_dir)

        if not path.isdir(self._thumbs_dir):
            print("==> Creating thumbs dir: " + self._thumbs_dir)
            mkdir(self._thumbs_dir)

    def _get_src_recovery_dirs(self):
        file_list = listdir(self._src_dir)
        src_recovery_dirs = []

        self._already_copied_dirs = self._get_already_copied_dirs()
        file_list = set(file_list).difference(set(self._already_copied_dirs))

        # Finish copying the last directory in the csv file, in case not all its files were copied yet
        if len(self._already_copied_dirs) > 0:
            file_list.add(self._already_copied_dirs.copy().pop())

        for filename in file_list:
            dir_path = path.realpath(path.join(self._src_dir, filename))
            if path.isdir(dir_path):
                src_recovery_dirs.append(dir_path)

        return src_recovery_dirs

    def _get_already_copied_dirs(self):
        try:
            self._csv_file_path = path.join(self._result_dir, "rpo.csv")
            dirs = []

            if path.exists(self._csv_file_path):
                with open(self._csv_file_path) as f:
                    reader = csv.reader(f)
                    dirs = list(reader)[0]

            if len(dirs) > 0:
                print("==> Continuing the process from the previous time")
        except IndexError as err:
            pass
        finally:
            return dirs

    def _get_images_from_path(self, dir_path):
        file_list = listdir(dir_path)
        images = []

        for filename in file_list:
            try:
                file_extension = path.splitext(filename)[1][1:]
                if file_extension in self._filetypes:
                    images.append(path.join(dir_path, filename))
            except Exception as err:
                print(err)

        return images
    
    def _copy_images(self, images, dir_path):
        for image in images:
            shutil.copy(image, self._result_dir)

        dir_name = path.basename(dir_path)
        if not dir_name in self._already_copied_dirs:
            with open(self._csv_file_path, "a") as f:
                if (len(self._already_copied_dirs) > 0):
                    f.write("," + dir_name)
                else:
                    f.write(dir_name)
                    self._already_copied_dirs.append(dir_name)

    def _move_thumbnails(self, result_images):
        self._thumbs_count = 0

        for image in result_images:
            if self._is_image_thumbnail(image):
                try:
                    shutil.move(image, path.join(self._thumbs_dir, path.basename(image)))
                    self._thumbs_count += 1
                except Exception as err:
                    print(err)
        
        self._images_count = len(result_images) - self._thumbs_count

    def _is_image_thumbnail(self, img_path):
        try:
            img = Image.open(img_path)
            w,h = img.size
            return w <= self._thumbs_width
        except Exception as err:
            return False

if __name__ == "__main__":
   RPO(sys.argv)