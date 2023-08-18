![Static Badge](https://img.shields.io/badge/Version-v1.5-8ebff1?style=for-the-badge&logo=v)
![Static Badge](https://img.shields.io/badge/Language-python-3776ab?style=for-the-badge&logo=python)
![Static Badge](https://img.shields.io/badge/Made%20by-Ricardo%20Martins-851ebc?style=for-the-badge)
# BeelProxy  

![Image](https://i.imgur.com/I9FYAFQ.png)  

## Key Features:  

- **Proxy Verification:** Checks the validity of proxy servers using HTTP and SOCKS4/5 protocols.  
- **Multithreading:** Utilizes multithreading with configurable worker count for faster processing.  
- **User-Friendly UI:** Presents a clean and informative terminal interface for user interaction.  
- **Theme Customization:** Supports various themes for enhancing the visual experience.  
- **Configuration Handling:** Utilizes a JSON configuration handler to manage user preferences.  
- **Results Logging:** Saves results to separate files for working and failed proxies.  
- **Capable of removing duplicates:** If the user wants to the script will remove duplicate lines from any file.  
- **Auto-Updater**: Will check for updates on file startup and auto update them if prompt to-do so.
- **Proxy Scrapper**: Gets proxies from many diferrent sources.


## Usage:

#### 1. Put proxies into proxy_list.txt  
#### 2. Select Protocol  
#### 3. Select number of workers  
#### 4. Wait fot it to finish  
#### 5. Output in file named after the proxy protocol

## Notes
- **Worker quantity**: On a **6 core** Intel Core i7-8750H 2.20GHz i was able to use 1000. However 5000 was to much for it. I recommend you to try different numbers and see whats the best option.  
- **Keyboard interrupt**: In the check all function keyboard interrupt does not work



<h3 align="left">Support:</h3>
<p><a href="https://ko-fi.com/beelzebub_uwu"> <img align="left" src="https://cdn.ko-fi.com/cdn/kofi3.png?v=3" height="50" width="210" alt="https://ko-fi.com/account/login" /></a></p><br><br>

# Changelog

```diff

v1.5 18/08/23

+   Fixed autoupdater bug
+   Fixed progress bar width by reading console total width
+   Improved number representations
+   Fixed not detecting proxy file changes after startup
+   Made remove duplicates run automatically after proxy scrape/check


v1.4 17/08/23

+   Improved check all performance
+   Fixed internet error after socks proxy check
+   Added option to remove duplicate lines from default ouput files and default proxy list
+   Added progress bar to remove duplicates function
+   Added current theme display
+   Added change workers default, to settings
+   Added new theme


v1.3 17/08/23

+   Optimized some functions
+   Organized imports
+   Added timestamps
+   Changed show progress functionality
+   Added proxy scrapper
+   Modified remove duplicate function
+   Moved scrapper, themes and updater to a folder


v1.2 16/08/23

+   Added auto-updater
+   Fixed Script not starting automatically after update
+   Fixed Version discrepancy on menus


v1.1 16/08/23

+   Tweaked some UI elements
+   Added Notification control menus
+   Fixed minor bugs
+   Added check all protocols
+   Added remove duplicates option
+   Added change console title

v1.0 15/08/23

+   Made themes
+   Multi-threaded implementation
+   Made Ascii-art menus
+   Added Json config handler
+   Corrected some spelling mistakes 
+   Added Sound notifications
+   Fixed bugs with socks checkers
!   Working on proxy scrapper

```
