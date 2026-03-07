# QuickViewer
a lightweight image viewer program that aims to be visually similar to old discontinued [Picasa Image Viewer](https://en.wikipedia.org/wiki/Picasa) that is built on pyQt5 and works on Linux.

## Installation

```shell
python -m venv v
v/bin/pip install -r requirements.txt
```
then you can run with
```shell
v/bin/python main.py {path_to_image}
```
however you might want to add it as a desktop entry file if you are to use it as a daily program using
```ini
[Desktop Entry]
Type=Application
Name=QuickViewer
Comment=Custom image viewer
Exec=#desired path
Icon=#optional icon path
Terminal=false
Categories=Graphics;Viewer;
MimeType=image/png;image/jpeg;image/gif;image/bmp;image/tiff;
```
then move it to `~/.local/share/applications/`
