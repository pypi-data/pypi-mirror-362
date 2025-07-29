# Auto-Py-To-App
 Auto-Py-To-App is a GUI for cx_Freeze, which is a library to change .py excutables into .exe (on windows) or binary files (on Mac OS).

 The famous library to package python script, maybe you heard about it once, named as pyinstaller. cx_Freeze, however, is trying to catch up with it in recent years.

 For pyinstaller, after you run its command, it will give you an excutable .exe file one way or another, regardless of its robustness. And for many starters, they could find it hard to tune the packaged .exe file.

 cx_Freeze, to some extend, performs better in this field. The adjustment after you package your program can be easier and faster.

 If you want to use pyinstaller, it's suggested that you start with another GUI called [auto-py-to-exe](https://pypi.org/project/auto-py-to-exe/). Auto-Py-To-App is based on auto-py-to-exe, the only difference is auto-py-to-app is powered by cx_Freeze, while auto-py-to-exe is powered by pyinstaller.

# Notice
 If you meet bug when loading cx_Freeze as: 

 ```AttributeError: module 'lief._lief.logging' has no attribute 'LOGGING_LEVEL'```

 It is because cx_Freeze does not support the latest version of lief. You can fix this bug by uninstall lief and re-install an older version of lief, such as lief-0.12.1. Please use:

 ```pip install lief==0.12.1```