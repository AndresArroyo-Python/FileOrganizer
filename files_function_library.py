# Import standard modules
import shutil
import os
import filecmp

# Load libraries
from pathlib import Path
from datetime import datetime
from tkinter import messagebox, simpledialog
from tkinter import Tk
from tkinter.filedialog import askdirectory

def check_folder (user_dest_path):
    # user_dest_path is the destination path selected by the user
    folder_path = Path(user_dest_path)                     
    # Set returning control variables to default value
    exist = False
    # Check if the user selected folder path exists
    if folder_path.is_dir():
        exist = True
    # Return control variable
    return exist


def check_file (file_dest_path):
    #check if file exist to avoid overwrite and give the user the option to do it manualy
    file_path = Path(file_dest_path)
    exist = False
    if file_path.is_file():
        exist = True
    return exist


def check_create_folder (user_dest_path):
    # user_dest_path is the destination path selected by the user
    folder_path = Path(user_dest_path)                     
    # Set returning control variables to default value
    exist = False
    created = False
    # Check if the user selected folder path exists
    if folder_path.is_dir():
        exist = True
    # Else then create the folder
    else:                                                  
        Path(user_dest_path).mkdir(parents=True, exist_ok=True)
        created = True
    # Return control variables
    return exist, created                                   


def check_list_files (user_orig_path):
    # user_orig_path is the origin path selected by the user
    files = [f.name for f in Path(user_orig_path).iterdir() if f.is_file()]
    # Return file list
    return files


def get_date_file (file_path):
    # Get stats object
    file = Path(file_path)
    stats = file.stat()
    # Convert timestamp to readable
    mod_time = datetime.fromtimestamp(stats.st_mtime)
    # Get year and month from the information if the file creation date
    year = mod_time.year
    month = mod_time.month
    # Give format to the information to return
    formatedyear = f"{year:04d}"
    formatedmonth = f"{month:02d}"
    return  formatedyear, formatedmonth


def get_year_month ():
    curr_date = datetime.now() 
    # get the year
    year = curr_date.year
    # get the month (as an integer 1-12)
    month = curr_date.month
    # get the day (as an integer 1-12)
    day = curr_date.day
    # format the time as a string "HH:MM:SS" (24-hour format)
    current_time_string = curr_date.strftime("%H:%M:%S")
    # format year and month
    formated_year = f"{year:04d}"
    formated_month = f"{month:02d}"
    formated_day = f"{day:02d}"    
    return current_time_string, formated_year, formated_month, formated_day 


def write_log_file (new_text_line):
    # get current time
    current_time, year, month, day = get_year_month()
    # get current directory
    current_directory = os.getcwd()
    # creates the path
    file_path =  current_directory + "/" + year + "_" + month + "_" + day + "_" + 'file_organizer.txt'
    # creates the content to write
    content = (year + "-" + month + "-" + day +" " + current_time + "> " + new_text_line)

    # open the file in append mode ('a')
    with open(file_path, 'a') as f:     
        # write the new line of content
        # the '\n' ensures the text is on its own line
        f.write(content + '\n')
    return


def copy_files_directory_error (source, destination):
    try:
        # shutil.copy2 copies the file and its metadata
        error = False
        shutil.copy2(source, destination)
        text = ("File copied successfully source: " + str(source) + " to: " + str(destination))
        write_log_file(text)
    except FileNotFoundError:
        error = True
        write_log_file("Error: The source file was not found.")
    except PermissionError:
        error = True
        write_log_file("Error: Permission denied at the source or destination.")
    except shutil.SameFileError:
        error = True
        write_log_file("Error: Source and destination are the same file.")
    except Exception as e:
        error = True
        write_log_file(f"An unexpected error occurred: {e}")
    return error


def get_match_files(source_file, destination_file):
    match = filecmp.cmp(source_file, destination_file, shallow=False)
    write_log_file("Files match" if match else "Files differ")
    return match


def erase_file (file_orig_path):
    file_path = Path(file_orig_path)
    deleted = False
    # Attempt to delete the file
    try:
        file_path.unlink()
        write_log_file(f"File '{file_path}' has been deleted.")
        deleted = True
    except FileNotFoundError:
        write_log_file(f"Error: The file '{file_path}' does not exist.")
    return deleted











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

        final_dest_path = user_dest_path + "/" + year + "/" + month
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
            match = get_match_files(file_orig_path, copied_file_path)

            # Check copy error and file match conditions and general preference erase origin is true
            if ((match) and (not error) and pref_erase_origin):
                text = ("Deleting file: " + str(file_orig_path))
                write_log_file(text)
                erase_file(file_orig_path)

else:
    # show an alert
    messagebox.showinfo("Error", endtext)
