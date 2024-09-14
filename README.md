# Chirael Explorer
It's a file management tool inspired by Windows Explorer, but with unique improvements and features.  
Changelogs: [CHANGELOG.md](./CHANGELOG.md)
## Installation
1. Download the compressed file of the source code and extract it.
2. Run `pip install -r requirements.txt` to install the library.
## Usages
Run `python main.py` to launch the explorer.
## Requires
    
    1. Windows
    2. Python interpreter with version ≥ 3.6
## Configurations
Just edit config.json.
```json
{
  "bg": {
    "enabled": 0,
    "stretch": 0
  },
  "font": {
    "name": "Microsoft YaHei",
    "italic": 0,
    "bold": 0
  },
  "logger": 1,
  "accentColor": [
    204,
    232,
    255
  ],
  "fastDirs":[
    "C:/"
  ],
  "menus":{
    "file":[
      ["用记事本打开","notepad <s>","assets/ico/txt.png"]
    ]
  }
}
```
#### The way to add an item to the context menu:
##### Add a new list to the "files" of "menus".
+ It should be read`[textOnItem,command,iconForItem]`
+ textOnItem should be a string;
+ command should be a command in console(`<s>` will be replaced to the path of the file)  
+ ionForItem should be the path of the icon
### Warning:
- If there is no config.json, the program will be generated automatically.
- If your config.json is formatted incorrectly, the program will <u>**overwrite**</u> it with the default configuration!
## Acknowledgments
Thanks to everyone who has contributed to this project!
## Author
- Name: `澈七` `Chirael7`
- [Bilibili](https://space.bilibili.com/1268117780): `https://space.bilibili.com/1268117780`
- [Github](https://github.com/chirael777): `https://github.com/chirael777`
## License
This project is open-source and available under the `MIT License`.
### Hotkeys
- `Alt + Add`: Create a new tab.
- `Ctrl + A`: Select all or none of the files in this directory.
- `Ctrl + E`: Refresh the current directory.
- `Ctrl + Enter`: Open the directory in a new tab.
- `Ctrl + M`: Rename the last selected file when selecting files.
- `Ctrl + S`: Save the background image.
- `Delete`: Transfer the selected file(s) to the Trash.
- `End/Home`: Scroll to the end/start of the current directory.
- `F1`: Hide or show the foreground interface.
- `F2`: Restart the program.
- `Shift + Delete`: Permanently delete the selected file(s).
- `Enter`: Execute the selected file(s).