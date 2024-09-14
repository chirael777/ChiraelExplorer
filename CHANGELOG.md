# Changelog

## [Version 1.1.1] 2024-9-14
Typed for five days
### Added:
+ Improved context menu for files
+ Customize the add-ons of the context menu
+ Modified instructions for config.json

## [Version 1.1.0] 2024-9-9
START 1.1
### Added:
+ Icons for buttons of Execute, Rename, Delete, and Info
+ Right-click menus (only "open in new tab" option for directories and "launch" for functions) for fastLines
+ Right-click menus (only "execute" "delete" "rename")
+ Copy files (Ctrl+C)
### Fixed:
* The layout of the title and separator of the quick access bar are unpleasant
* The widths of fastLines are updated deferred when the maximize button of the quick access bar is clicked
* Can't hide the Quick Access bar when pressing F1.Now you can only hide the foreground if you keep pressing F1
* The interval of the timer of the fastBox is too long

## [Version 1.0.9] 2024-9-8
Wow, this is the tenth update
### Added:
+ The args parameter of the executeFile method of the main window class is equivalent to the key pressed when executing the file
+ Add a list named fastDirs to the config.json to represent the folders that you can access quickly. These are added to the Quick Access bar
+ Executing a folder in the Quick Access bar opens that directory in a new tab
+ Use the dictionary method to sort the absolute path of the fastLines
### Fixed:
* The scroll wheel issue in the previous version was not fully fixed
* The button uses .released to detect clicks is not so effectively as .clicked
* The fastLines in  the Quick Access bar is displayed on top of the fileLines in the file bar. It looks uncomfortable
* The pop-up windows with parent are not pretty, so this version makes them without a parent
### Deleted:
- The configuration display and annotation in the original README.md

## [Version 1.0.8] 2024-9-8
### Added:
+ Triggering of fastLine's double-click and enter execution (but no logic after write execution)
+ toolTips of fastLine
+ A cBar is used to split the title of the Quick Access Bar from the fastLine
### Fixed:
* $ doesn't work well as a special type identifier.$ can be used for file names.So now change it to *
* The buttons that maximize the quick access bar and the buttons that minimize the quick access bar are not the same color
* When the mouse is placed in the Quick Access bar, the mouse wheel is scrolled, and the file bar still scrolls up and down
### Removed:
- White background for the Quick Access bar

## [Version 1.0.7] 2024-9-7
### Added:
+ Change the format of the config that originally listed all the keys tiled to a hierarchical one
### Fixed:
* In previous versions, it was said that the Quick Access bar would be started by default when starting the program, but this was not implemented in the code
### Removed:
- The configuration display and annotation in the original README.md

## [Version 1.0.6] 2024-9-7
### Added:
+ Changed the + 〇 icon from text to image icon
+ Added a getMaster method to the Chirael_Explorer class as well
+ Added a fastLine class.
+ Added a settings bar to the Quick Access bar (although it doesn't respond after double-clicking)
### Fixed:
* The order of the shortcuts in the Hotkeys column is confusing in README.MD
* Change the trigger condition of the button from being clicked to being released
### Deleted:
- "icon" keyword in configuration.You must have all the icons

## [Version 1.0.5] 2024-9-6
### Added:
+ When pressing F2 before restarting, ask if open the directory that was opened before the restart after the restart
+ A Quick Access bar on the right of the File bar
+ A button at the top left of the file bar toggles whether to display the Quick Access bar
+ When you start the program, the quick access page will open automatically
+ A button at the top right of the Quick Access bar toggles whether to maximize the Quick Access bar
### Fixed:
* Originally, the text in TabBars was not really visually balanced centered
### Deleted:
- Removed HIM.

## [Version 1.0.4] 2024-9-5
### Added:
+ Add the 〇 button to the right of the middle column to flush the files
+ Added Ctrl-E as a shortcut to press 〇
+ Use F2 to force restart the program
+ Use Ctrl-S to save the background image
+ When selecting file(s), if the number of selected file(s) accounts for more than half of the number of files in the current folder, the text of the Select All button will be ··, and vice versa·
### Fixed:
* When the class Button of stds.py is initializing, the RGB initialization value overflows
### Deleted:
- Removed HIM.

## [Version 1.0.3] 2024-9-4
### Added:
+ A new container is set for all the components in the current version
+ Added F1 as a shortcut
+ Add the ↑ button to the right of the middle column to return to the parent directory   
### Fixed:
* Pressing F1 in previous versions does not hide or show the UI interface
* The buttons for creating a new file and returning to the parent directory are colored differently than others
### Deleted:
- Removed HIM.

## [Version 1.0.2] 2024-9-3
### Added:
+ Warning parts in readme
+ When the rename is initiated, a pop-up window appears, and you enter a new name to rename
### Fixed:
* keypressEvent of fileLine is missing arguments
* The renamed shortcut key is actually Ctrl-A in the code, and it is changed to Ctrl-M
### Deleted:
- Removed HIM.

## [Version 1.0.1] 2024-9-2
Second.
### Added:
- The parent class of Logger is Thread
- When selecting file(s), press Ctrl+M to rename the last selected file
### Fixed:
- The process does not stop after closing the window
- When the background is set to True in the configuration, the file column cannot be displayed
- When previewing an inaccessible file or folder, wait for a Python error to deny access
### Deleted:
- File renamer

## [Version 1.0.0] 2024-9-1
The first public version
### Added:
- Support to preview folder contents, text file contents, and picture sizes
- Support to use hotkeys
- Support for using custom background images and custom fonts
### Fixed:
- It gets stuck when deleting a file
- Pressing Backspace while editing the current path will also return to the parent directory
- The scrollbar does not update when toggling directories
### Removed:
- Removed HIM.