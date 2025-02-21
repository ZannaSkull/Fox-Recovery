import os
import shutil
import glob
import ctypes
from datetime import datetime
import tkinter as tk
from tkinter import messagebox, filedialog

# --- Fox Colors
Backgroundcolor = "#2e2e2e" 
Foregroundcolor = "#ffffff"
Buttoncolor = "#4a4a4a" 
textcolor = "#ffffff" 
Entrybackground = "#3f3f3f" 
Entryforeground = "#ffffff" 

def GamingName(title):
    name = title.encode('cp1252')
    ctypes.windll.kernel32.SetConsoleTitleA(name)

if os.name == 'nt': 
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

def MakeBackup():
    BackName = datetime.now().strftime("Backup_%d%m%Y_%H%M%S")
    BackDir = os.path.join(os.getcwd(), BackName)
    os.makedirs(BackDir, exist_ok=True)
    return BackDir

def Logger(message):
    Consolelogs.config(state=tk.NORMAL) 
    Consolelogs.insert(tk.END, message + '\n')
    Consolelogs.see(tk.END) 
    Consolelogs.config(state=tk.DISABLED) 

def CopyBackup(TheFile, DestFile, BackDir):
    try:
        shutil.copy2(TheFile, DestFile)
        BackupFile = os.path.join(BackDir, os.path.basename(TheFile))
        shutil.copy2(TheFile, BackupFile)
        Logger(f"Copied and backed up: {TheFile} -> {DestFile} and {BackupFile}")
    except FileNotFoundError:
        Logger(f"File not found: {TheFile}")
    except Exception as e:
        Logger(f"Error while copying {TheFile}: {e}")

def CopyFiles(SourceDir, DestDir, FileToCopy, BackDir):
    if not os.path.exists(SourceDir):
        messagebox.showerror("Error", f"The source directory '{SourceDir}' does not exist.")
        return

    os.makedirs(DestDir, exist_ok=True)

    for FileName in FileToCopy:
        TheFile = os.path.join(SourceDir, FileName)
        DestFile = os.path.join(DestDir, FileName)
        CopyBackup(TheFile, DestFile, BackDir)

    ExtensionsSource = os.path.join(SourceDir, 'extensions')
    ExtensionsDest = os.path.join(DestDir, 'extensions')

    if os.path.exists(ExtensionsSource):
        shutil.copytree(ExtensionsSource, ExtensionsDest, dirs_exist_ok=True)
        Logger(f"Copied extensions from '{ExtensionsSource}' to '{ExtensionsDest}'")
    else:
        Logger(f"No extensions found at '{ExtensionsSource}'")

def SessionBackp(SourceDir, DestDir, BackDir):
    SourceBackDir = os.path.join(SourceDir, 'sessionstore-backups')
    DestinBackDir = os.path.join(DestDir, 'sessionstore-backups')

    if not os.path.exists(SourceBackDir):
        messagebox.showinfo("Notice", f"The backup directory '{SourceBackDir}' does not exist.") 
        return

    os.makedirs(DestinBackDir, exist_ok=True)

    BackupFiles = ['recovery.jsonlz4', 'recovery.baklz4', 'previous.jsonlz4']

    UpgradeFiles = glob.glob(os.path.join(SourceBackDir, 'upgrade.jsonlz4-*'))

    for FileName in BackupFiles:
        TheFile = os.path.join(SourceBackDir, FileName)
        DestFile = os.path.join(DestinBackDir, FileName)
        CopyBackup(TheFile, DestFile, BackDir)

def Start():
    SourceDir = SourceEntry.get().strip()
    DestDir = DestEntry.get().strip()

    FileToCopy = [
        'logins.json',
        'cookies.sqlite',
        'extensions.json',
        'places.sqlite',
        'prefs.js',
        'bookmarks.json',
        'sessionstore.jsonlz4',
    ]

    BackDir = MakeBackup()
    
    Logger("Starting backup...")
    
    CopyFiles(SourceDir, DestDir, FileToCopy, BackDir)
    SessionBackp(SourceDir, DestDir, BackDir)

    messagebox.showinfo("Backup Completed", f"The files were copied to '{DestDir}' and the backup directory is '{BackDir}'")

def SelectSourceDirectory():
    directory = filedialog.askdirectory(title="Select Source Profile Directory")
    if directory: 
        SourceEntry.delete(0, tk.END)
        SourceEntry.insert(0, directory)

def SelectDestDirectory():
    directory = filedialog.askdirectory(title="Select Destination Profile Directory")
    if directory:
        DestEntry.delete(0, tk.END) 
        DestEntry.insert(0, directory) 

root = tk.Tk()
root.title("Fox Recovery")

root.configure(bg=Backgroundcolor)

tk.Label(root, text="Source Profile Directory:", bg=Backgroundcolor, fg=Foregroundcolor).grid(row=0, column=0, padx=10, pady=5, sticky="w")
SourceEntry = tk.Entry(root, width=50, bg=Entrybackground, fg=Entryforeground)
SourceEntry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")
Sourcebutton = tk.Button(root, text="Browse", command=SelectSourceDirectory, bg=Buttoncolor, fg=textcolor)
Sourcebutton.grid(row=0,column=2,padx=5,pady=5)

tk.Label(root, text="Destination Profile Directory:", bg=Backgroundcolor, fg=Foregroundcolor).grid(row=1,column=0,padx=10,pady=5,sticky="w")
DestEntry = tk.Entry(root,width=50,bg=Entrybackground ,fg=Entryforeground)
DestEntry.grid(row=1,column=1,padx=10,pady=5 ,sticky="ew")
DestButton = tk.Button(root,text="Browse",command=SelectDestDirectory,bg=Buttoncolor ,fg=textcolor)
DestButton.grid(row=1,column=2,padx=5,pady=5)

Backupbutton = tk.Button(root,text="Start Backup & Transfer",command=Start,bg=Buttoncolor ,fg=textcolor)
Backupbutton.grid(row=2,columnspan=3,padx=10,pady=10)

Consolelogs = tk.Text(root,width=80,height=20,bg=Backgroundcolor ,fg=Foregroundcolor)
Consolelogs.grid(row=3,columnspan=3,padx=10,pady=5)
Consolelogs.config(state=tk.DISABLED)

InstructionsText = (
    "Instructions:\n"
    "1. Select the source profile directory of your browser.\n"
    "   (Usually located in the Roaming folder)\n"
    "2. Select the destination profile directory where you want to transfer files.\n"
    "3. Click on 'Start Backup & Transfer' to begin the process.\n"
)

ReadThat = tk.Label(
    root,
    text=InstructionsText,
    bg=Backgroundcolor,
    fg=textcolor,
    justify=tk.LEFT,
    anchor='nw',
    padx=10,
    pady=10
)
ReadThat.grid(row=0, column=3, rowspan=4, padx=10, pady=5, sticky='nw')

root.grid_columnconfigure(1 ,weight=1)
root.grid_rowconfigure(3 ,weight=1)

root.mainloop()
