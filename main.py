import customtkinter
import subprocess
from CTkMessagebox import CTkMessagebox

# Set the appearance mode and color theme
customtkinter.set_appearance_mode("Dark")  # Optional: Set to dark mode
customtkinter.set_default_color_theme("dark-blue")  # Set the theme to dark-blue

# Set the passcode
passcode = "123456789"

# Create the CustomTkinter app
app = customtkinter.CTk()
app.title("BrowserLock App")

# Create a header label
header_label = customtkinter.CTkLabel(app, text="Browser Lock", font=("Arial", 24, "bold"))
header_label.pack(pady=(20, 5))  # Add some padding for spacing

# Create a subheader label
subheader_label = customtkinter.CTkLabel(app, text="To access the browser, please put the Correct code.", font=("Arial", 14))
subheader_label.pack(pady=(0, 20))  # Add some padding for spacing

# Function to check the passcode
def check_passcode():
    # Check if all entries are filled
    if any(entry.get() == "" for entry in entries):
        CTkMessagebox(title="Error", message="Please fill all passcode fields.", icon="cancel")
        return

    user_input = "".join([entry.get() for entry in entries])
    
    if user_input == passcode:
        subprocess.Popen(["/snap/bin/brave"])  # Launch Brave browser
        app.destroy()
    else:
        CTkMessagebox(title="Error", message="Incorrect passcode. Please try again.", icon="cancel")
        for entry in entries:
            entry.delete(0, "end")

# Function to handle input validation and navigation
def on_key_press(event, index):
    if len(event.char) == 1 and event.char.isdigit():  # Allow only one digit
        entries[index].delete(0, "end")  # Clear previous input

        
        # Move to the next entry if not the last one
        if index < len(entries) - 1:
            entries[index + 1].focus_set()
        else:
            # If it's the last entry, check the passcode when filled
            check_passcode()  # Call check_passcode() here after inserting character
    elif event.keysym == "Return":  # Move to next entry on Enter key
        if index < len(entries) - 1:
            entries[index + 1].focus_set()
        else:
            check_passcode()
    else:
        # Prevent non-numeric input
        return "break"

# Create a frame for the passcode entries
passcode_frame = customtkinter.CTkFrame(app)
passcode_frame.pack(pady=20)

# Create the passcode entries with bindings
entries = []
for i in range(9):
    entry = customtkinter.CTkEntry(passcode_frame, width=50, font=("Arial", 24), justify="center", show="*")
    entry.pack(side="left", padx=5)
    entry.bind("<Key>", lambda event, index=i: on_key_press(event, index))  # Bind key press event
    entries.append(entry)

# Create a submit button (optional since we now check on fill)
submit_button = customtkinter.CTkButton(app, text="Submit", command=check_passcode)
submit_button.pack(pady=10)

# Create a footer label with small text
footer_label = customtkinter.CTkLabel(app, text="Made by Ryan Baig", font=("Arial", 10))
footer_label.pack(side="bottom", pady=(10, 20))  # Add some padding for spacing

# Run the app
app.mainloop()
