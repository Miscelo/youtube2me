#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Import Moduls
from __future__ import unicode_literals

import tkinter as tk
try:
    from tkinter import ttk
    from tkinter import messagebox as tkMessageBox
    from tkinter import filedialog
    from tkinter.ttk import *

except ImportError:
    print("""ERROR import tkinter modul. Shit happens!""")

import os

try:
    import youtube_dl
except ImportError:
    print("Please install 'youtube_dl' Modul with -sudo pip install youtube_dl-!")





class Myapp:
    def __init__(self, master):
        self.colors = {"green": "#22cf00", "grey": "#bdbdbd", "red": "#bf0202", "bgcolor": "#1a1a1a", "bgwidget":"#3c3c3c"}
        fm = tk.Frame(master, background=self.colors["bgcolor"])
        fm.pack(padx=20, pady=10, fill=tk.BOTH, expand=tk.YES)

        #introlabel
        self.label1 = tk.Label(fm, text="***  YouTube-Downloader  ***", fg=self.colors["green"],
                               font="Verdana 12 bold", bg=self.colors["bgcolor"])
        self.label1.pack(pady=30)

        #radiobutton to choose file in audio or video format
        self.label2 = tk.Label(fm, text="Choose your file type:",
                               fg=self.colors["grey"], bg=self.colors["bgcolor"])
        self.label2.pack()
        self.v = tk.StringVar(master=master)
        self.v.set("audio")
        self.radiobtn1 = tk.Radiobutton(fm, text="Audio", padx=20, variable=self.v, value="audio",
                                        bg=self.colors["bgcolor"], fg=self.colors["green"], selectcolor="black",
                                        activebackground=self.colors["bgcolor"], activeforeground=self.colors["grey"],
                                        borderwidth=5, highlightthickness=0)
        self.radiobtn1.pack()
        self.radiobtn2 = tk.Radiobutton(fm, text="Video", padx=20, variable=self.v, value="video",
                                        bg=self.colors["bgcolor"], fg=self.colors["green"], selectcolor="black",
                                        activebackground=self.colors["bgcolor"], activeforeground=self.colors["grey"],
                                        borderwidth=5, highlightthickness=0)
        self.radiobtn2.pack()

        #Downloadpath
        self.separator1 = tk.Label(fm, text="-", fg=self.colors["bgcolor"], bg=self.colors["bgcolor"])
        self.separator1.pack(pady=8)
        self.label3 = tk.Label(fm, justify=tk.LEFT, text="Path to Download Folder:",
                               fg=self.colors["grey"], bg=self.colors["bgcolor"])
        self.label3.pack(padx=20, anchor='w')
        self.entry1 = tk.Entry(fm, fg=self.colors["green"], bg=self.colors["bgwidget"], width=200)
        self.entry1.pack(padx=20)
        self.path = str("/home/" + os.getlogin() + "/")
        self.entry1.insert(0, self.path)

        self.btn00 = tk.Button(fm, text="Search", command=self.search_path, fg=self.colors["grey"],
                               bg=self.colors["bgwidget"])
        self.btn00.pack(padx=20, pady=5, anchor='w')


        # widget to copy and paste youtube path
        self.separator2 = tk.Label(fm, text="-", fg=self.colors["bgcolor"], bg=self.colors["bgcolor"])
        self.separator2.pack(pady=8)
        self.label4 = tk.Label(fm, text="Copy & Paste download path from Youtube:",
                               fg=self.colors["grey"], bg=self.colors["bgcolor"])
        self.label4.pack(padx=20, anchor='w')
        self.entry2 = tk.Entry(fm, fg=self.colors["green"], bg=self.colors["bgwidget"], width=200)
        self.entry2.pack(padx=20)




        # Show process of download
        self.label5 = tk.Label(fm, text="Waiting for start!", fg=self.colors["red"], bg=self.colors["bgcolor"])
        self.label5.pack(pady=30)

        #Action buttons. QUIT, Reset Values to standard y Download file
        self.btn01 = tk.Button(fm, text="QUIT", command=self.quit, fg=self.colors["red"],
                               bg=self.colors["bgwidget"])
        self.btn01.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        self.btn02 = tk.Button(fm, text="Reset", command=self.resetvalues, fg=self.colors["grey"],
                               bg=self.colors["bgwidget"])
        self.btn02.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        self.btn03 = tk.Button(fm, text="Download", command=self.download, fg=self.colors["green"],
                               bg=self.colors["bgwidget"])
        self.btn03.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        self.flash()


        #simple function that colors-Dictionary can be approuch outside class. To set background-color of theme.
    def __str__(self):
        return self.colors


    def getdownloadpath(self):
        mydownloadpath = self.entry1.get()
        if mydownloadpath[-1] != "/":
            mydownloadpath = mydownloadpath+"/"
        if os.path.exists(mydownloadpath) == False:
            try:
                os.makedirs(mydownloadpath)
            except PermissionError:
                tkMessageBox.showerror("Permissionproblem", "Permission denied to create path!")
                self.entry1.delete(0, "end")
                self.path = str("/home/" + os.getlogin() + "/")
                self.entry1.insert(0, self.path)
                mydownloadpath = "/home/"+os.getlogin()+"/"
                return mydownloadpath
            else:
                return mydownloadpath
        else:
            if os.access(mydownloadpath, os.W_OK) == True:
                return mydownloadpath
            else:
                tkMessageBox.showerror("Permissionproblem", "Permission denied to create path!")
                self.entry1.delete(0, "end")
                self.path = str("/home/" + os.getlogin() + "/")
                self.entry1.insert(0, self.path)
                mydownloadpath = "/home/" + os.getlogin() + "/"
                return mydownloadpath


    def search_path(self):
        self.path = str(filedialog.askdirectory(initialdir="/home/"+os.getlogin()+"/"))
        self.entry1.delete(0, "end")
        self.entry1.insert(0, self.path)


    def download(self):
        if self.v.get() == "audio":
            self.download_audio()
        elif self.v.get() == "video":
            self.download_video()

    #Flashing
    def flash(self):
        self.label5.config(text="Download")
        bg = self.label5.cget("background")
        fg = self.label5.cget("foreground")
        self.label5.configure(background=fg, foreground=bg)
        root.after(1000, self.flash)


    def download_audio(self):
        mydownloadpath = self.getdownloadpath()
        ydl_opts_audio = {'format': 'bestaudio/best', 'outtmpl': mydownloadpath + '%(title)s.%(ext)s',
                          'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '192',}]}
        youtubeID = [str(self.entry2.get())]
        try:
            with youtube_dl.YoutubeDL(ydl_opts_audio) as ydl:
                ydl.download(youtubeID)
        except Exception:
            tkMessageBox.showerror('DownloadError', 'HTTP-Error 403, audio download forbidden.')
        else:
            pass
        finally:
            pass


    def download_video(self):
        mydownloadpath = self.getdownloadpath()
        ydl_opts_video = {'outtmpl': mydownloadpath + '%(title)s.%(ext)s'}
        youtubeID = [str(self.entry2.get()).strip()]
        try:
            with youtube_dl.YoutubeDL(ydl_opts_video) as ydl:
                ydl.download(youtubeID)
        except Exception:
            tkMessageBox.showerror('DownloadError', 'Error 403, video download forbidden.')
        else:
            pass
        finally:
            pass


    def resetvalues(self):
        self.entry1.delete(0, "end")
        self.entry1.insert(0,"/home/"+os.getlogin()+"/")
        self.entry2.delete(0,"end")


    def quit(self):
        if tkMessageBox.askyesno('Verify', 'Really quit?'):
            root.destroy()



if __name__ == "__main__":
    root = tk.Tk()
    app = Myapp(root)
    root.title("Cleptomaniac 1.0")
    root.geometry("400x512")
    root.minsize(400,512)
    root.configure(background=app.__str__()["bgcolor"])
    root.mainloop()
    print("Good bye!")
    # Program started when finished
