#Track Zoom attendance with ZAPPy 
(Zoom Attendance Program in Python)


What ZAPPy is:
ZAPPy compares Zoom participant lists with the class roster and creates the attendance sheet. 

Why ZAPPy over Excel:
Students' Zoom IDs are not always the same as their names on the class roster (e.g., janedoe vs. Jane Doe; Johnny Doe vs. John Doe). So, fancy Excel functions may not work well when you try to match Zoom IDs with student names. ZAPPy takes care of the cases shown above as well as keeps tracks of Zoom IDs that are not matched. Moreover, ZAPPy can run multiple Zoom participant lists all at once for the analysis. If you have more files later on, no problem! New analysis will be added to the existing attendance file.

How to run ZAPPy:
1. Download Python 3.0 or above from https://www.python.org/downloads/ for free.
2. Create a folder to save your attendance file later. This folder could be in your class folder, desktop, etc. Name the folder as you want.
3. Save ZAPPy.py in the folder created in Step 2.
a. You can download ZAPPy.py from https://github.com/ykchoi20/ZAPPy.
4. Download the class roster from Canvas and move the file to the folder created in Step 2. 
a. How? Go to your Canvas course site. Go to Grades and click the Actions button. Click Export. Move the file to the folder created in Step 2.
5. IMPORTANT: Change the file name to "Canvas_roster.csv." 
6. Download the Zoom participant list(s) and move the file(s) to the folder created in Step 2. 
7. IMPORTANT: Change the file name to "Zoom_(date of meeting).csv." For example, Zoom_040220 or Zoom_0402section1.csv. The (date of meeting) part of the file name should be one word and will appear in the attendance sheet.
8. Launch a Terminal window from the folder created in Step 2.
a. How? Head into System Preferences and select Keyboard > Shortcuts > Services. Find "New Terminal at Folder" in the settings and click the box. Now, when you're in Finder, just right-click the folder you created in Step 2 and go to Services (at the bottom of the menu) and click "New Terminal at Folder" (source).
9. In the terminal window, type "python 3 ZAPPy.py" and hit enter.
10. If ZAPPy runs successfully, you will see "Attendance.csv" file created in the folder.
11. If you want to run ZAPPy again later with new Zoom participant lists, just repeat Step 6 and 9 only. You do not need to delete the old Zoom participant lists.
