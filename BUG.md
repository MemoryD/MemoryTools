#### 开发日志

- 2020/3/26

    - [ ] 发现bug1：

    ```
    Traceback (most recent call last):
      File "memorytools.py", line 75, in <module>
        MemoryTool().run()
      File "memorytools.py", line 69, in run
        self.ct.start()
      File "C:\Users\memory\OneDrive\code\MemoryTools\memorytools\copytrans.py", line 123, in start
        self.trans(self.translator, source)
      File "C:\Users\memory\OneDrive\code\MemoryTools\memorytools\copytrans.py", line 86, in trans
        la, pro = judgeLanguage(source)
      File "C:\Users\memory\OneDrive\code\MemoryTools\memorytools\utils.py", line 151, in judgeLanguage
        return ('zh-cn', zh_num / total)
    ZeroDivisionError: division by zero
    ```

    原因分析：传入的字符串只有空格或换行，或者过滤掉特殊符号后只有空格或换行。

    解决：加入检测。

    ---

    - [ ] 发现bug2:

    ```
    Traceback (most recent call last):
      File "memorytools.py", line 75, in <module>
        MemoryTool().run()
      File "memorytools.py", line 69, in run
        self.ct.start()
      File "C:\Users\memory\OneDrive\code\MemoryTools\memorytools\copytrans.py", line 122, in start
        source = p.paste()                                          # 获得剪切板内容
      File "C:\Users\memory\AppData\Local\Programs\Python\Python36\lib\site-packages\pyperclip\__init__.py", line 455, in paste_windows
        with clipboard(None):
      File "C:\Users\memory\AppData\Local\Programs\Python\Python36\lib\contextlib.py", line 81, in __enter__
        return next(self.gen)
      File "C:\Users\memory\AppData\Local\Programs\Python\Python36\lib\site-packages\pyperclip\__init__.py", line 417, in clipboard
        raise PyperclipWindowsException("Error calling OpenClipboard")
    pyperclip.PyperclipWindowsException: Error calling OpenClipboard ([WinError 5] 拒绝访问。)
    ```

    