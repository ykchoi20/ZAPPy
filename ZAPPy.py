import csv
import re
import os.path
import os

# Convert a csv file to a list.
def read_csv(filename):
    with open (filename, 'r') as handle:
        csv_handle = csv.reader(handle)
        list_csv = list(csv_handle)
    return list_csv


# Open the Canvas roster and extract student name (colomn 0) and Canvas ID (column 2).
def create_new_roster(canvas_file, no_matching_message):

    new_roster = [["Student name","SIS User ID", "Zoom ID"]]
    csv_canvas = read_csv(canvas_file)
    student_name_col = 0
    user_ID_col = 2
    included_cols = (student_name_col, user_ID_col)

    for row in csv_canvas[3:]:      # Student name starts from the row 3 on the Canvas roster.
        stu_data = list(row[i] for i in included_cols)
        stu_data.append("No match")
        new_roster.append(stu_data)

    new_roster.append(no_matching_message)

    return new_roster

# Split into two lists: enrolled roster and unmatched Zoom IDs.
def split_roster(student_roster):

    unmatched_Zoom_IDs = []
    enrollment_roster = []
    for row in student_roster:
        if row[0] == "":
            unmatched_Zoom_IDs.append(row)
        else:
            enrollment_roster.append(row)

    return enrollment_roster, unmatched_Zoom_IDs

# Returning User: find the dates that were already checked
# and remove the corresponding Zoom files from further analysis
# New User: create a new roster from Canvas
def zoom_files_to_run(output_filename):

    files_in_folder = os.listdir()
    all_zoom_files =[]
    for filename in files_in_folder:
        if "Zoom" in filename:
            all_zoom_files.append(filename)

    zoom_files = []
    if os.path.exists(output_filename):
        attendance_file = read_csv(output_filename)
        past_dates = attendance_file[0][3:]     # Dates that have been checked for attendance
        for filename2 in all_zoom_files:
            count= 0
            for date in past_dates:
                if date in filename2:
                    count = count +1
            if count==0:
                zoom_files.append(filename2)

    else:
        zoom_files = all_zoom_files

    return zoom_files

# Convert a Zoom participant file into a list. Leave out the header.
def read_zoom(filename):
    list_zoom = read_csv(filename)
    return list_zoom[1:]

# Find the Zoom IDs that have not matched. Mark them as "No match."
def update_zoom_list(zoom_list, c_roster):
    for i in range(len(zoom_list)):
        k=0
        for row in c_roster:
            if zoom_list[i][0] == row[2]:
                zoom_list[i].append("Match")
                k=1
                break
        if k==0:
            zoom_list[i].append("No match")
    
    return zoom_list


# Find the Zoom ID for the students in the Canvas roster.
def update_matches(c_roster, list_zoom):

    # Perfect match!
    for i in range(len(c_roster)):
        j = 0
        if c_roster[i][2] == "No match" or c_roster[i][2] == "Common Last Name":
            for z_row in list_zoom:
                '''
                Canvas roster name = Zoom ID or
                John Doe = johndoe or
                jd123 = jd123@schoolname.edu
                '''

                if c_roster[i][0] == z_row[0] or \
                c_roster[i][0].lower().replace(" ","") == z_row[0] or\
                c_roster[i][1] in z_row[1]:
                    c_roster[i][2] = z_row[0]              # Add the corresponding Zoom ID to the Attendance.csv.
                    list_zoom[j][3] = "Match"
                    break
                j=j+1

    # Leave out students whose last names are common from the best guess algorithm
    no_match_list = []
    c_roster_match_status = c_roster[i][2]

    for i in range(len(c_roster)):
        if c_roster[i][2] == "No match" or c_roster[i][2] == "Common Last Name":
            no_match_list.append(c_roster[i])

    for i in range(len(c_roster)):
        uniq = 0
        c_roster_last_name = c_roster[i][0].split()[1]
        if c_roster[i][2] == "No match" or c_roster[i][2] == "Common Last Name":
            for row in no_match_list:
                if c_roster_last_name == row[0].split()[1]:
                    uniq =uniq + 1

        if uniq >1:
            c_roster[i][2] = "Common Last Name"


    # Best guess: Last name matching
    for i in range(len(c_roster)):
        matched = 0
        for z_row in list_zoom:
            if c_roster[i][2]=="No match" and z_row[3] == "No match":
                z_row_lowercase = "".join(re.split("[^a-zA-Z]*", z_row[0])).lower()  # characters only and make them lowercase
                lastname_lowercase = c_roster[i][0].split()[1].lower()
                length_lastname = len(lastname_lowercase)

                if lastname_lowercase == z_row_lowercase[-length_lastname:]:    # Last name matching
                    c_roster[i][2] = z_row[0]
                    z_row[3] = "Match"

    return c_roster, list_zoom


# Add Zoom ID that were not matched to the unmatched_Zoom_IDs list.
def update_unmatched_Zooms(list_zoom, unmatched_Zoom_IDs, enrollment_roster):

    past_dates = enrollment_roster[0][3:]

    # Collect unmathed Zoom IDs from the Zoom list
    no_match_Zoom = []
    for row in list_zoom:
        if row[3] == "No match":
            no_match_Zoom.append(row[0])
    #print(no_match_Zoom)
    # If there is no unmatched Zoom in the starting roster, just add all
    # unmatched Zoom IDs to the roster.
    if len(unmatched_Zoom_IDs) ==1:
        for id in no_match_Zoom:
            add_row = ["","", id]
            for i in range(len(past_dates)):    # Add a blank for dates already checked
                add_row.append("0")
            unmatched_Zoom_IDs.append(add_row)

    else:
        for id in no_match_Zoom:
            k=0
            for row in unmatched_Zoom_IDs[1:]:
                if id == row[2]:
                    k=1
                    break
            if k==0:
                add_row = ["","", id]
                for i in range(len(past_dates)):
                    add_row.append("0")
                unmatched_Zoom_IDs.append(add_row)

    return unmatched_Zoom_IDs


def check_attendance(roster, zoom_list):
    for row in roster[1:]:
        atten = 0
        for z_row in zoom_list:
            if row[2] == z_row[0]:
                row.append("1")
                atten = 1
                break
        if atten == 0:
            row.append("0")
    return roster

# Put two files (enrollment roster and unmatched Zoom IDs) together and
# create/overwrite Attendance.csv file.
def create_attendance_file(output_filename, enrollment_roster, unmatched_Zoom_IDs):
    with open (output_filename, 'w') as final:
        writer = csv.writer(final)
        writer.writerows(enrollment_roster)
        writer.writerows(unmatched_Zoom_IDs)


def main():
    # Input_files: For a new user, the Canvas roster and the Zoom participant list(s)
    #              For a returning user, the Attendance.csv and the Zoom participant list(s)
    # Output_file: Attendance.csv

    output_filename = 'Attendance.csv'
    canvas_file = 'Canvas_roster.csv'
    no_matching_message = ["","","Zoom IDs below have no matching names in the Canvas Roster"]


    # Input file #1: Attendance.csv or Canvas roster
    # Read Attendance.csv if it exists. If Attendance.csv does not exit (i.e. a new user),
    # open the Canvas roster and extract student name and Canvas ID.

    if os.path.exists(output_filename):
        student_roster = read_csv(output_filename)
    else:
        student_roster = create_new_roster(canvas_file, no_matching_message)

    # Split into two lists: enrolled roster and unmatched Zoom IDs.
    enrollment_roster, unmatched_Zoom_IDs = split_roster(student_roster)

    # Input file #2: Zoom participant list(s)
    # Returning User: find the dates that were already checked
    # and remove the corresponding Zoom files from further analysis
    # New User: create a new roster from Canvas
    zoom_files = zoom_files_to_run(output_filename)

    zoom_file_number = len(zoom_files)

    for j in range(zoom_file_number):
        list_zoom = read_zoom(zoom_files[j])
        zoom_updated = update_zoom_list(list_zoom, enrollment_roster)
        # Match the roster from Canvas with the Zoom list

        enrollment_roster_updated, zoom_updated = update_matches(enrollment_roster, zoom_updated)

        # Add unmatched Zoom IDs if any
        unmatched_Zoom_IDs_updated = update_unmatched_Zooms(zoom_updated, unmatched_Zoom_IDs, enrollment_roster)

        # Check the attendance. 1 for attendance, 0 for absence.
        date = zoom_files[j].split("_")[1].split(".")[0]
        enrollment_roster_updated[0].append(date)
        enrollment_roster = check_attendance(enrollment_roster_updated, zoom_updated)
        unmatched_Zoom_IDs = check_attendance(unmatched_Zoom_IDs_updated, zoom_updated)

    # Create or overwrite Attendance.csv file
    create_attendance_file(output_filename, enrollment_roster, unmatched_Zoom_IDs)

    print("Success! Attendance.csv file has been created/updated.")

if __name__ == "__main__":
    main()
