# Recovered Photos Organizer

## About

The following article: [Recover deleted files from any drive in Linux](https://www.tomshardware.com/how-to/recover-deleted-files-from-any-drive-in-linux)

Presents the PhotoRec software which comes with testdisk, to help recovering deleted files from your hard drive.

As the output of PhotoRec, the files recovered from your hard drive are spread among several recup_dir.x directories and all filetypes are mixed inside of these directories.

This Python script copies only jpg and png files from inside all of these directories to only one directory called "recovered_photos" (sibling to it) and then moves the thumbnail files to a separate thumbs subdirectory.

## Usage

Run it with python and point it to where the result of the extraction done by PhotoRec is located.

For example:

```bash
python3 ./main.py /Users/jon/Desktop/Recovery 
```
