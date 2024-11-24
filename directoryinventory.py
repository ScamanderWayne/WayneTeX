import os
import tkinter
import codecs

with codecs.open("tree.txt", "w", "utf8") as f:
    os.chdir("c:\\Users\\alibi\\WayneTeX")
    os.system("tree /f |clip")
    root = tkinter.Tk()   
    tree = root.clipboard_get()
    f.write(tree)