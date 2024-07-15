# Simple_Bootloader_on_Python
## Version Alpha_1.0.0.1

In this version, the basic code for the loading screen was written.
<img src="https://github.com/NicknameRoot/Simple_Python_Bootloader/blob/gh-pages/version_aplha_1.0.0.1.gif?raw=true">

One third-party library was used in the form of [Link](https://github.com/Textualize/rich), to create a visually pleasing console interface.

In the internal structure of the code, it is planned to link to the configuration file and improve the functionality of the code.

you can see it on a separate website using this [Link](https://nicknameroot.github.io/Simple_Bootloader_on_Python/)

## Version Alpha_1.0.1.5
The main code and internal functions were written in this version

This project was developed for Windows and with the expectation of its use under Windows, for which a simple script was created [Start.bat](https://github.com/NicknameRoot/Simple_Bootloader_on_Python/blob/gh-pages/Alpha_1.0.1.5/Start.bat) was written to start the bootloader [Bootloader.py
](https://github.com/NicknameRoot/Simple_Bootloader_on_Python/blob/gh-pages/Alpha_1.0.1.5/Bootloader.py).
The main loader console window is launched and subsequent loaded scripts are opened in separate console windows.

Now, when launched, the bootloader script accesses the configuration file [Config.cfg](https://github.com/NicknameRoot/Simple_Bootloader_on_Python/blob/gh-pages/Alpha_1.0.1.5/Config.cfg):

```cfg
[Scripts]
script_1 = "new-bot.py", auto_r:y
script_2 = "old-bot.py", auto_r:n
script_3 = "test.c", auto_r:y
```

This configuration file contains the names of the .py codes (if they are located in the same directory with the loader) or the path to the .py codes (for example, "C:\test.py"), which will be loaded provided that the parameter is specified in the configuration file auto-restart `auto_r: [y/n] ` of the script when it ends, the `y` key means that the script will be restarted upon completion, and the `n` key means that the script will not be restarted until the loader is completely stopped and the loader itself is restarted bootloader.

In this version, the console interface has been improved, becoming pleasing to the eye and easy to read.

In the main console window, the version of the loader will now be displayed and the download status will be shown. As an example of a successful launch, I launched my discord bot `new-bot.py` through this loader, which launched successfully, showing the result in the main console window:

<img src=https://github.com/NicknameRoot/Simple_Bootloader_on_Python/blob/gh-pages/Alpha_1.0.1.5/Demo_Files/Load_Demo.gif>

In case the executable `.py` file is closed, the loader script checks the status of the running `.py` files every 10 seconds, and the configuration file has already been added with a restart parameter that when closed (regardless of what reason) if the `y` key is specified in the parameter then the script will be reloaded after 5 seconds (taking into account that if the executable `.py` files are very demanding, a delay of 5 seconds was introduced). Using the example, I forcibly closed the console of my running discord bot, after which the script completed the task assigned to it to restart.

<img src=https://github.com/NicknameRoot/Simple_Bootloader_on_Python/blob/gh-pages/Alpha_1.0.1.5/Demo_Files/Restart_Demo.gif>

Now let's talk about the fact that this loader was written exclusively to launch `.py` files (since I needed it), if it was in the configuration file [Config.cfg](https://github.com/NicknameRoot/Simple_Bootloader_on_Python/blob/gh-pages/Alpha_1.0.1.5/Config.cfg): if a non-`.py` file is specified, then until the next restart of the bootloader itself, the inappropriate file will be excluded from the launch queue at the time the bootloader itself is running, and the work will be continued if other supported `.py` files are specified in the configuration file, if no other files are specified for loading in the configuration file, then the bootloader will not load the user's system and will shut down after 10 seconds.
To demonstrate how it works, I added a `test.c` file to the configuration file that is not supported for launching and removed other files from the list, after which the loader performed its job correctly.

<img src=https://github.com/NicknameRoot/Simple_Bootloader_on_Python/blob/gh-pages/Alpha_1.0.1.5/Demo_Files/Error_Demo.gif>
