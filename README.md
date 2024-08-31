# Bulk-EXIF-Editor
Small Python utility to edit EXIF "date created" metadata on large bulks of photos.

## Usage

Make sure you have `piexif`, `tkinter` and `tkcalendar` installed on your Python environment of choice.

If you haven't already, just download them using `pip`:
```shell
pip install tkcalendar piexif tkinter
```

Then you can just run the utility with:
```
python -m bulk_exif_editor
```
or
```
python bulk_exif_editor.py
```

## Building an executable file

It's really straightforward to transform this small python utility in a full-fat `.exe` portable file.  
Firsly you need to install `Pyinstaller`:
```
pip install pyinstaller
```
Then you can just run the following line of code:
```
pyinstaller --onefile --windowed --collect-all=babel bulk_exif_editor.py
```
Some files and folders will be created, you can find the resulting executable file in `dist`.

Enjoy!
