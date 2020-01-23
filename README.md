# MayaWindowSwitcher
![window_switcher](https://user-images.githubusercontent.com/1896961/72981168-7cfbb380-3e1f-11ea-9173-1cfc3f3d5d06.gif)

Switch between open windows on Maya(like Alt+Tab in windows) 

# Installation
## Hotkey
Drag and drop the `install_hotkey.mel` file into the Maya viewport.

Press `Ctrl+Shift+T` to launch the tool.


## Shelf
Drag and drop the install_shelf.mel file into the Maya viewport.

## Option
Change to simple mode.(disable create thumbnail previews)
```python
from window_switcher import settings
settings.enable_simple_mode()
```

Return to normal mode.
```python
from window_switcher import settings
settings.disable_simple_mode()
```

# License
[MIT](https://en.wikipedia.org/wiki/MIT_License)

# Author
tm8r (https://github.com/tm8r)