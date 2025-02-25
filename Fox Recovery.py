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

if os.name == 'nt': 
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

def MakeBackup():
    BackName = datetime.now().strftime("Backup_%d%m%Y_%H%M%S")
    BackDir = os.path.join(os.getcwd(), BackName)
    os.makedirs(BackDir, exist_ok=True)
    return BackDir

def Logger(message, level="info"):
    Consolelogs.config(state=tk.NORMAL) 
    if level == "info":
        Consolelogs.insert(tk.END, message + '\n', 'info')
    elif level == "error":
        Consolelogs.insert(tk.END, message + '\n', 'error')
    elif level == "warning":
        Consolelogs.insert(tk.END, message + '\n', 'warning')
    Consolelogs.see(tk.END) 
    Consolelogs.config(state=tk.DISABLED) 

def CopyBackup(TheFile, DestFile, BackDir):
    try:
        shutil.copy2(TheFile, DestFile)
        BackupFile = os.path.join(BackDir, os.path.basename(TheFile))
        shutil.copy2(TheFile, BackupFile)
        Logger(f"Copied and backed up: {TheFile} -> {DestFile} and {BackupFile}", "info")
    except FileNotFoundError:
        Logger(f"File not found: {TheFile}", "error")
    except Exception as e:
        Logger(f"Error while copying {TheFile}: {e}", "error")

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
        Logger(f"Copied extensions from '{ExtensionsSource}' to '{ExtensionsDest}'", "info")
    else:
        Logger(f"No extensions found at '{ExtensionsSource}'", "warning")

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
    
    Logger("Starting backup...", "info")
    
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
root.iconbitmap("Fox.ico")

root.configure(bg=Backgroundcolor)

Consolelogs = tk.Text(root, width=80, height=20, bg=Backgroundcolor, fg=Foregroundcolor)
Consolelogs.grid(row=3, columnspan=3, padx=10, pady=5)
Consolelogs.tag_config('info', foreground='green')
Consolelogs.tag_config('error', foreground='red')
Consolelogs.tag_config('warning', foreground='orange')
Consolelogs.config(state=tk.DISABLED)

tk.Label(root, text="Source Profile Directory:", bg=Backgroundcolor, fg=Foregroundcolor).grid(row=0, column=0, padx=10, pady=5, sticky="w")
SourceEntry = tk.Entry(root, width=50, bg=Entrybackground, fg=Entryforeground)
SourceEntry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")
Sourcebutton = tk.Button(root, text="Browse", command=SelectSourceDirectory, bg=Buttoncolor, fg=textcolor)
Sourcebutton.grid(row=0, column=2, padx=5, pady=5)

tk.Label(root, text="Destination Profile Directory:", bg=Backgroundcolor, fg=Foregroundcolor).grid(row=1, column=0, padx=10, pady=5, sticky="w")
DestEntry = tk.Entry(root, width=50, bg=Entrybackground, fg=Entryforeground)
DestEntry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
DestButton = tk.Button(root, text="Browse", command=SelectDestDirectory, bg=Buttoncolor, fg=textcolor)
DestButton.grid(row=1, column=2, padx=5, pady=5)

Backupbutton = tk.Button(root, text="Start Backup & Transfer", command=Start, bg=Buttoncolor, fg=textcolor)
Backupbutton.grid(row=2, columnspan=3, padx=10, pady=10)

InstructionsText = (
    "Instructions:\n"
    "1. **Select the source profile directory**: Choose the profile directory of your browser that you want to backup.\n"
    "   This is usually located in the 'Roaming' folder (e.g., `C:\\Users\\YourUsername\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles`).\n"
    "   Make sure to select the correct profile folder (it should contain files like `places.sqlite`, `logins.json`, etc.).\n"
    "2. **Select the destination profile directory**: Choose where you want to transfer the files.\n"
    "   This can be a new profile directory or an existing one where you want to restore or merge data.\n"
    "3. **Click on 'Start Backup & Transfer'**: Begin the backup and transfer process.\n"
    "   The selected files will be copied to the destination directory and a backup will be created in a separate folder.\n"
    "\n"
    "Important: Ensure that the browser is closed before starting the process to avoid data corruption."
)

def FoxBold(text):
    import re
    BoldTexts = re.findall(r'\*\*(.*?)\*\*', text)
    return BoldTexts

BoldTexts = FoxBold(InstructionsText)

InstructionsFrame = tk.Frame(root, bg=Backgroundcolor)
InstructionsFrame.grid(row=0, column=3, rowspan=4, padx=10, pady=5, sticky='nw')

def Foxlabel(text, bold=False):
    if bold:
        label = tk.Label(InstructionsFrame, text=text, bg=Backgroundcolor, fg=textcolor, font=('Helvetica', 10, 'bold'))
    else:
        label = tk.Label(InstructionsFrame, text=text, bg=Backgroundcolor, fg=textcolor, wraplength=250)
    return label

lines = InstructionsText.split('\n')
for line in lines:
    if '**' in line:
        BoldText = FoxBold(line)[0]
        NotABoldText = line.replace(f'**{BoldText}**', '')
        
        tk.Label(InstructionsFrame, text=NotABoldText, bg=Backgroundcolor, fg=textcolor, wraplength=250).pack(fill='x')
        
        Foxlabel(BoldText, bold=True).pack(fill='x')
    else:
        tk.Label(InstructionsFrame, text=line, bg=Backgroundcolor, fg=textcolor, wraplength=250).pack(fill='x')


root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(3, weight=1)

root.mainloop()
