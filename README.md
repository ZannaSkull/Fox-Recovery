# Fox Recovery: Browser Profile Transfer Tool

## Description

`Fox Recovery` is a Python-based utility designed to simplify the process of transferring browser profile data (including logins, cookies, extensions, and settings) from one location to another. This is useful when migrating to a new computer, creating a backup, or moving your profile between different installations of the same browser.

**Important:** This tool copies sensitive data like passwords and cookies. Use it responsibly and only on trusted computers.

## Features

*   **User-friendly GUI:**  Provides a simple graphical interface for selecting source and destination directories.
*   **Automatic Backup:** Creates a timestamped backup of your profile before transferring data to prevent data loss.
*   **Comprehensive Data Transfer:** Copies key files and directories to preserve your logins, cookies, extensions, settings, and browsing sessions.
*   **Logging:** Displays progress messages and any errors in a console log within the GUI.

## Supported Browsers

The script is primarily designed for browsers that store profile data in a similar directory structure. It has been tested with:

*   Mozilla Firefox
*   Waterfox
*   Zen Browser
*   Floorp
*   Midori

## Installation

1.  **Install Python:** Ensure you have Python 3.x installed on your system.  You can download it from [https://www.python.org/downloads/](https://www.python.org/downloads/).
2.  **Install Tkinter:** Tkinter should come pre-installed with most Python installations. If not, you may need to install it separately using your system's package manager (e.g., `apt-get install python3-tk` on Debian/Ubuntu).
3.  **Download the script:** Save Fox Recovery to a directory of your choice.

## Usage

1.  **Run the script:** Execute the Python script by double-clicking it or running `Fox Recovery.py` from the command line.
2.  **Locate your browser profile directory:**  Follow the instructions within the GUI to find your browser's profile directory.  Common locations are:
    *   **Firefox:** `%APPDATA%\Mozilla\Firefox\Profiles` (You can type this directly into the Explorer address bar)
    *   **Waterfox:** `%APPDATA%\Waterfox\Profiles`
    *   **Zen:** `%APPDATA%\Zen\Profiles`
    *   **Floorp:** `%APPDATA%\Floorp\Profiles`
    *   **Midori:** `%APPDATA%\Midori\Profiles`
3.  **Select source and destination directories:**  Use the "Browse" buttons to select the source profile directory (the profile you want to copy) and the destination directory (where you want to copy it to).
4.  **Start the transfer:** Click the "Start Backup & Transfer" button.
5.  **Monitor the progress:**  Observe the console log for progress messages and any errors.
6.  **Close Browsers:** Ensure all instances of the source and destination browsers are closed before running the script.
7.  **Verify:** After the transfer is complete, open the "destination" browser and verify that your logins, cookies, extensions, and settings have been successfully transferred.

## Important Considerations

*   **Close the browser:** Make sure the browser you are transferring *from* is completely closed before running the script. Otherwise, some files might be in use and cannot be copied correctly. It's generally a good idea to close the browser you are transferring *to* as well, until the transfer is complete.
*   **Profile Compatibility:** Transferring profiles between different browser versions or even different browsers may not always work perfectly. There could be compatibility issues.
*   **Security:** Be cautious when transferring profile data, especially if you are moving it to a computer you don't fully trust. The profile contains sensitive information such as passwords and cookies.
*   **Permissions:** Make sure you have the necessary permissions to read from the source directory and write to the destination directory.
*   **Large Profiles:** If your browser profile is very large, the copying process may take a significant amount of time.

## Troubleshooting

*   **Error: "Source directory does not exist"**: Double-check that you have entered the correct path to the source profile directory.
*   **Error: "Permission denied"**: Ensure you have the necessary permissions to read from the source directory and write to the destination directory.  Try running the script as an administrator.
*   **Transfer seems incomplete**: Make sure the browser you are transferring from is completely closed.  Also, check the console log for any error messages.
*   **Browser doesn't load profile correctly:** Compatibility issues can sometimes occur. Try clearing the browser's cache and restarting it. If issues persist, the profile may not be fully compatible.

## Disclaimer

This script is provided as-is, without any warranty. The user assumes all responsibility for any data loss or other issues that may arise from using this tool.  Always back up your data before performing any data transfer operations.

## Author

Hisako🎀
