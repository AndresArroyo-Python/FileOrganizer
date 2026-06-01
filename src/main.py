# Load libraries
from files_function_library import check_folder as check_folder
from files_function_library import check_file as check_file
from files_function_library import check_list_files as check_list_files
from files_function_library import get_date_file as get_date_file
from files_function_library import check_create_folder as check_create_folder
from files_function_library import copy_files_directory_error as copy_files_directory_error
from files_function_library import get_match_files as get_match_files
from files_function_library import erase_file as erase_file

from log_record_functions import write_log_file as write_log_file

from tkinter import messagebox, simpledialog
from tkinter import Tk
from tkinter.filedialog import askdirectory

#---------------------------------Main Logic-----------------------
#hide the main Tkinter window
Tk().withdraw() 

#initialize variables
folder_orig_selected= False
folder_dest_selected= False
file_exist = False
pref_erase_origin = False
endtext = ""

#open the folder selection dialog
folder_selected = askdirectory(title="Select Files Destination Folder")

if folder_selected:
    #destination file path in next variable declaration
    #example path syntaxis "C:\\01 Andres\\google-python-exercises\\2026"
    #user_dest_path = "C:\\01 Andres\\google-python-exercises"
    user_dest_path = folder_selected
    write_log_file("User select destiny folder " + user_dest_path)
    folder_dest_selected = True
else:
    text = "User cancelled Files Destination Folder selection."
    endtext = text
    write_log_file(text)

#open the folder selection dialog
folder_selected = askdirectory(title="Select Files Originals Folder")

if folder_selected:
    #file destination path in next variable declaration
    #user_orig_path = "C:\\01 Andres\\google-python-exercises\\2026"
    user_orig_path = folder_selected
    write_log_file("User select originals folder " + user_orig_path)
    folder_orig_selected = True
else:
    text = "User cancelled File Originals Folder selection."
    #add a line end to the text in case user canceled folder selection
    if (folder_dest_selected):
        endtext = text
    else:
        endtext = endtext + "\n" + text
    write_log_file(text)
    
#next variable declaration is for keep original files 
#please type True if you want to erase original files or keep as False
#show the popup message
response = messagebox.askyesno("Confirm", "Do you want to erase original files?")

if response:
    write_log_file("User confirmed erase originals")
    pref_erase_origin = True
else:
    write_log_file("User cancel erase originals")


#only if user selected the two folders
if (folder_orig_selected) and (folder_dest_selected):
    #check selected folder
    exist = check_folder(user_dest_path)
    text = ("Original Folder: " + str(user_dest_path) + " Exist: " + str(exist))
    write_log_file (text)
    files = check_list_files(user_orig_path)
    text =  ("Files found: " + str(files))
    write_log_file (text)

    for item in files:
        
        file_orig_path = user_orig_path + "/" + item
        write_log_file (file_orig_path)
        year, month = get_date_file (file_orig_path)
        text = ("Creation year: " + str(year) + " month: " + str(month))
        write_log_file (text)

        final_dest_path = user_dest_path + "/" + year + "/" + year + "-" + month
        text = ("Destiny Folder: " + str(final_dest_path))
        write_log_file (text)
        exist, created = check_create_folder(final_dest_path)
        text = ("Folder exist: " + str(exist) + " created:" + str(created))
        write_log_file(text)

        file_exist = check_file(final_dest_path + "/" + item)
        if file_exist:
            text = ("File found user need to copy it manualy: " + final_dest_path + "/" + item)
            write_log_file(text)
            # show an alert
            messagebox.showinfo("File found", "Please copy file manually \n \n" + final_dest_path + "/" + item)
        else:
            error = copy_files_directory_error(file_orig_path , final_dest_path)
            text = ("Copy error: " + str(error))
            write_log_file(text)
            

            copied_file_path = final_dest_path + "/" + item
            copyprocess = True
            match = get_match_files(file_orig_path, copied_file_path, copyprocess)

            # Check copy error and file match conditions and general preference erase origin is true
            if ((match) and (not error) and pref_erase_origin):
                text = ("Deleting file: " + str(file_orig_path))
                write_log_file(text)
                erase_file(file_orig_path)

else:
    # show an alert
    messagebox.showinfo("Error", endtext)
