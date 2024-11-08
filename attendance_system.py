import csv
from datetime import datetime
import tkinter as tk
from tkinter import messagebox, PhotoImage
import os

# Password Attendance Function
def password_attendance(root, head_count_label, status_label, entered_password, marked_attendance, attendance_complete, marked_students):
    user_passwords = {
        "Dhrubojyoti": "123456",
        "Student2": "password2",
        "Student3": "password3",
    }

    now = datetime.now()
    current_date = now.strftime("%Y-%m-%d")
    current_time = now.strftime("%H-%M-%S")

    # Specify the new directory path
    directory_path = "C:/Users/Dhrubojyoti/Desktop/Python/projects/Attendance/Records/"
    
    # Ensure the directory exists
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

    # Define the file path with the new directory
    file_name = os.path.join(directory_path, f"{current_date}_Present(By Password).csv")

    # Check if the user has already marked attendance
    entry_exists = False
    if os.path.isfile(file_name):
        with open(file_name, "r") as f:
            lnreader = csv.reader(f)
            for row in lnreader:
                if row[0] == entered_password and row[1] == current_date:
                    entry_exists = True
                    break

    if entry_exists:
        messagebox.showwarning("Warning", "Attendance has already been marked for this time.")
        return False

    user_found = False
    for user, password in user_passwords.items():
        if entered_password == password:
            if user in marked_students:
                messagebox.showwarning("Warning", f"{user} has already marked attendance.")
                return False

            user_found = True
            messagebox.showinfo("Attendance", f"Password accepted for {user}. Marking attendance...")

            marked_students.add(user)
            marked_attendance[0] += 1  # Increment the count

            # Open the file and update or write the new entry
            entries = []
            if os.path.isfile(file_name):
                with open(file_name, "r") as f:
                    lnreader = csv.reader(f)
                    entries = list(lnreader)
                    # Update existing entry if present
                    for i, row in enumerate(entries):
                        if row[0] == user and row[1] == current_date:
                            entries[i] = [user, current_date, "Present"]
                            break
                    else:
                        # Add new entry if not updated
                        entries.append([user, current_date, "Present"])
            else:
                # File does not exist, so create it and add the header
                entries.append(["Name", "Date", "Status"])
                entries.append([user, current_date, "Present"])

            # Write the updated or new entries to the file
            with open(file_name, "w", newline="") as f:
                lnwriter = csv.writer(f)
                lnwriter.writerows(entries)

            # Update head count label
            head_count_label.config(text=f"{marked_attendance[0]} Counts")

            # Check if all students have marked their attendance
            if marked_attendance[0] == len(user_passwords):
                status_label.config(text="Attendance of All the students has been marked")
                attendance_complete[0] = True
                display_final_screen(root)
                return True
            return True

    if not user_found:
        messagebox.showwarning("Error", "Incorrect password. Please try again.")
        return False

def disable_ui(root):
    """Disable all UI elements."""
    for widget in root.winfo_children():
        widget.config(state=tk.DISABLED)

def display_final_screen(root):
    """Display the final screen with the text only."""
    for widget in root.winfo_children():
        widget.destroy()  # Remove all existing widgets

    # Display the text in bold blue color
    final_text_label = tk.Label(root, text="All Attendance Has Been Marked", font=("Arial", 24, "bold"), fg="blue", bg="#f7f2cc")
    final_text_label.pack(expand=True)

    # Run the main loop
    root.mainloop()

def open_password_attendance():
    # Create the root window for the password entry page
    root = tk.Tk()
    root.geometry("800x400")  # Set the size of the window
    root.configure(bg="#f7f2cc")  # Set the background color (matching the image)
    root.title("ASPIRATIONS EDUCATION")  # Set the title (company name)

    # Load the logo image
    logo = PhotoImage(file="C:/Users/Dhrubojyoti/Desktop/Python/projects/Attendance/Aspirations.png")  # Replace with the path to your logo file

    # Frame for the logo and company name
    top_frame = tk.Frame(root, bg="#f7f2cc")
    top_frame.pack(pady=20)

    # Logo Label
    logo_label = tk.Label(top_frame, image=logo, bg="#f7f2cc")
    logo_label.pack(side=tk.LEFT, padx=10)

    # Company Name Label
    company_label = tk.Label(top_frame, text="ASPIRATIONS EDUCATION", font=("Arial", 24, "bold"), fg="green", bg="#f7f2cc")
    company_label.pack(side=tk.LEFT, padx=10)

    # Head Count Label
    head_count_label = tk.Label(root, text="0 Counts", font=("Arial", 24, "bold"), fg="black", bg="#f7f2cc")
    head_count_label.pack(side=tk.RIGHT, padx=30)

    # Status Label for all attendance marked message
    status_label = tk.Label(root, text="", font=("Arial", 12), fg="blue", bg="#f7f2cc")
    status_label.pack(pady=10)

    # Instruction Label
    instruction_label = tk.Label(root, text="Enter the password for attendance:", font=("Arial", 12), fg="green", bg="#f7f2cc")
    instruction_label.pack(pady=10)

    # Password Entry Field
    password_entry = tk.Entry(root, font=("Arial", 12), show='*', width=30)
    password_entry.pack(pady=10)
    password_entry.focus_set()  # Automatically focus on the password entry field

    # List to keep track of marked attendance count and marked students
    marked_attendance = [0]
    attendance_complete = [False]
    marked_students = set()

    def on_submit():
        entered_password = password_entry.get().strip()
        if entered_password.lower() == 'q':
            display_final_screen(root)
            return

        if not attendance_complete[0]:
            if password_attendance(root, head_count_label, status_label, entered_password, marked_attendance, attendance_complete, marked_students):
                password_entry.delete(0, tk.END)

    def on_cancel():
        root.quit()  # Quit the entire program

    # Bind Enter key to the submit action
    root.bind('<Return>', lambda event: on_submit())

    # Frame for the buttons
    button_frame = tk.Frame(root, bg="#f7f2cc")
    button_frame.pack(pady=10)

    # Submit Button
    submit_button = tk.Button(button_frame, text="Submit", font=("Arial", 12, "bold"), command=on_submit, bg="white", fg="green")
    submit_button.pack(side=tk.LEFT, padx=10)

    # Cancel Button (quits the entire program)
    cancel_button = tk.Button(button_frame, text="Cancel", font=("Arial", 12, "bold"), command=on_cancel, bg="white", fg="green")
    cancel_button.pack(side=tk.LEFT, padx=10)

    # Run the main loop
    root.mainloop()

def main():
    # Create the root window for the initial selection page
    root = tk.Tk()
    root.geometry("800x400")  # Set the size of the window
    root.configure(bg="#f7f2cc")  # Set the background color (matching the image)
    root.title("ASPIRATIONS EDUCATION")  # Set the title (company name)
    
    logo = PhotoImage(file="C:/Users/Dhrubojyoti/Desktop/Python/projects/Attendance/Aspirations.png")
    top_frame = tk.Frame(root, bg="#f7f2cc")
    top_frame.pack(pady=20)
    logo_label = tk.Label(top_frame, image=logo, bg="#f7f2cc")
    logo_label.pack(side=tk.LEFT, padx=10)

    # Instruction Label
    instruction_label = tk.Label(root, text="ASPIRATIONS EDUCATION", font=("Arial", 24, "bold"), fg="green", bg="white")
    instruction_label.pack(pady=10)

    # Description Label
    description_label = tk.Label(root, text="Enter '2' for password attendance", font=("Arial", 12), fg="black", bg="#f7f2cc")
    description_label.pack(pady=10)

    # Input Entry Field
    choice_entry = tk.Entry(root, font=("Arial", 12), width=30)
    choice_entry.pack(pady=10)
    choice_entry.focus_set()  # Automatically focus on the choice entry field

    def on_ok():
        choice = choice_entry.get().strip()
        if choice == '2':
            root.destroy()  # Close the initial root window
            open_password_attendance()
        elif choice.lower() == 'q':
            messagebox.showinfo("Exit", "The process was ended by the user.")
        else:
            messagebox.showwarning("Error", "Invalid choice.")

    def on_cancel():
        root.quit()  # Quit the entire program

    # OK and Cancel Buttons
    button_frame = tk.Frame(root, bg="#f7f2cc")
    button_frame.pack(pady=20)

    # Bind Enter key to OK button
    root.bind('<Return>', lambda event: on_ok())

    ok_button = tk.Button(button_frame, text="OK", font=("Arial", 12, "bold"), command=on_ok, bg="white", fg="green")
    ok_button.pack(side=tk.LEFT, padx=20)

    cancel_button = tk.Button(button_frame, text="Cancel", font=("Arial", 12, "bold"), command=on_cancel, bg="white", fg="green")
    cancel_button.pack(side=tk.LEFT, padx=20)

    # Run the main loop
    root.mainloop()

if __name__ == "__main__":
    main()
