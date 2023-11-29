import customtkinter as ctk
import tkinter as tk
from tkinter import *
from tkinter import filedialog

ctk.set_appearance_mode("light")
ctk.set_default_color_theme('blue')

app = ctk.CTk()
app.title('Ans - Exam AI Engine')
app.geometry('1440x900')

# New top frame for the image and user details
top_frame = ctk.CTkFrame(app, corner_radius=10, fg_color='white')
top_frame.pack(fill='x', expand=False, padx=0, pady=0)

# Place an image on the left side of the top frame
image = tk.PhotoImage(file='data/ans_logo.png')  # Replace with your image path
image_label = ctk.CTkLabel(top_frame, image=image, text='')
image_label.pack(side='left', padx=20, pady=10)

# Place user icon and details on the right side of the top frame
user_icon = tk.PhotoImage(file='')  # Replace with your icon path
user_icon_label = ctk.CTkLabel(top_frame, image=user_icon,text='')
user_icon_label.pack(side='right', padx=10, pady=10)

user_details = ctk.CTkLabel(top_frame, text="Teacher Name\nProofs Teacher", font=("Arial", 10), anchor='e')
user_details.pack(side='right', padx=10, pady=10)

main_frame = ctk.CTkFrame(app, corner_radius=10, fg_color='#C6BFD9')
main_frame.pack(fill='both', expand=True, padx=0, pady=0)

# Create the side menu frame with a contrasting border
side_menu = ctk.CTkFrame(main_frame, corner_radius=10, fg_color='white', border_color='grey', border_width=2)
side_menu.pack(side='left', fill='y',padx=10, pady=10)

# Search entry field in the side menu
search_var = tk.StringVar()
search_entry = ctk.CTkEntry(side_menu, textvariable=search_var, placeholder_text="Search")
search_entry.pack(padx=10, pady=10, fill='x')

# ======================== Side Menu - Labels ========================

label_menu = ctk.CTkFrame(main_frame, corner_radius=10, fg_color='white', border_color='grey', border_width=2)
label_menu.pack(side='right', fill='both', padx=10, pady=10)

def hide_labels_task():
    label_menu.pack_forget()
    show_labels_button.configure(text="Show Labels", command=show_labels_task)
    
def show_labels_task():
    label_menu.pack(side='right', fill='y', padx=10, pady=10)
    show_labels_button.configure(text="Hide Labels", command=hide_labels_task)
    

# label Description
label_description = ctk.CTkLabel(label_menu, text="Labels", font=("Arial", 20, "bold"), text_color='#1B0166')
label_description.pack(padx=60, pady=10, anchor='n')

# Create a list of labels to be displayed in the side menu
labels = ['Label 1', 'Label 2', 'Label 3', 'Label 4', 'Label 5', 'Label 6']

for label in labels:
    lbl = ctk.CTkLabel(label_menu, text=label, cursor="hand2", text_color='#1B0166')
    lbl.pack(pady=10, padx=30)


# Function to update labels based on search
def update_labels():
    search_term = search_var.get().lower()
    for label in label_widgets:
        if search_term in label.cget("text").lower():
            label.pack(pady=2, padx=10, fill='x')
        else:
            label.pack_forget()

# Bind the search entry to update labels on key release
search_var.trace_add("write", lambda name, index, mode: update_labels())


# Placeholder function for the button task
def button_task():
    # You can add your functionality here
    print("Button clicked")

# Add a button at the bottom of the side menu
task_button = ctk.CTkButton(side_menu, text="Generate Rubrics", command=button_task, fg_color='#1B0166')
task_button.pack(side='bottom', padx=10, pady=10)


# ======================== Content - Right Side ========================

# Create the content section on the right
content_frame = ctk.CTkFrame(main_frame, width=600, corner_radius=10, fg_color='white', border_color='grey', border_width=1)
content_frame.pack(side='left', fill='both', expand=True, padx=10, pady=10)

# Create a box frame inside the content_frame
box_frame = ctk.CTkFrame(content_frame, corner_radius=10, bg_color='transparent', fg_color='white')
box_frame.pack(padx=10, pady=10, fill='both', expand=True)

box_frame_left = ctk.CTkFrame(box_frame, corner_radius=10, bg_color='transparent', fg_color='white')
box_frame_left.pack(side='left', padx=10, pady=10, fill='both', expand=True)

box_frame_right = ctk.CTkFrame(box_frame, corner_radius=10, bg_color='transparent', fg_color='white')
box_frame_right.pack(side='right', padx=0, pady=0, fill='both', expand=True)


# Add different styles of text inside the box frame
bold_text = ctk.CTkLabel(box_frame_left, text="Question 1", font=("Arial", 12, "bold"), anchor='w')
bold_text.pack(padx=10, pady=10, anchor='nw')

large_color_text = ctk.CTkLabel(box_frame_left, text="Prove P = NP ", text_color="black", font=("Arial", 20))
large_color_text.pack(pady=10, anchor='nw', padx=20)

show_labels_button = ctk.CTkButton(box_frame_right, text="Show Labels", command=hide_labels_task, fg_color='#1B0166')
show_labels_button.pack(side='right', padx=0, pady=10, anchor='ne')



# Create another box frame for the large text area
text_box_frame = ctk.CTkFrame(content_frame, corner_radius=10, bg_color='transparent')
text_box_frame.pack(padx=10, pady=10, fill='both', expand=True)

# Create an inner frame to hold the text widget and the scrollbar
inner_frame = Frame(text_box_frame)
inner_frame.pack(fill='both', expand=True)

# Create a Text widget for displaying and highlighting text
text_widget = Text(inner_frame, wrap='word', bg='white', fg='black')
text_widget.pack(side='left', fill='both', expand=True)
text_widget.insert('1.0', 'Your large amount of text goes here...')

# Create a Scrollbar and attach it to text_widget
scrollbar = Scrollbar(inner_frame, command=text_widget.yview)
scrollbar.pack(side='right', fill='y')

# Configure the text_widget to use the scrollbar
text_widget.config(yscrollcommand=scrollbar.set)

# Create a frame for the text box and buttons
bottom_frame = ctk.CTkFrame(content_frame, corner_radius=10, fg_color='white')
bottom_frame.pack(padx=10, pady=10, fill='x')

# Create a single-line text entry widget
file_entry = ctk.CTkEntry(bottom_frame, fg_color='white', placeholder_text="enter your question here to add.")
file_entry.pack(side='left', fill='x', expand=True, padx=10)

# Function to handle file upload
def upload_file():
    filename = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if filename:
        file_entry.delete(0, END)
        file_entry.insert(0, filename)

# Function to save the file's content
def save_file():
    filename = file_entry.get()
    if filename:
        with open(filename, 'r') as file:
            text_content = file.read()
            # Here you can implement what you want to do with the text content
            print(text_content)  # Example: print the content

# Add an upload button
upload_btn = ctk.CTkButton(bottom_frame, text="Upload", command=upload_file, fg_color='#1B0166')
upload_btn.pack(side='left', padx=10)

# Add a save confirmation button
save_btn = ctk.CTkButton(bottom_frame, text="Save", command=save_file, fg_color='#1B0166')
save_btn.pack(side='left')

question_frame = ctk.CTkFrame(content_frame, corner_radius=10, fg_color='white', border_color='grey', border_width=1)
question_frame.pack(side='bottom', fill='x', padx=10, pady=10)

button_question = ctk.CTkButton(question_frame, text="Q1", command=button_task, fg_color='#1B0166')
button_question1 = ctk.CTkButton(question_frame, text="Q2", command=button_task, fg_color='#1B0166')
button_question2 = ctk.CTkButton(question_frame, text="Q3", command=button_task, fg_color='#1B0166')
button_question.pack(side='left', padx=10, pady=10)
button_question1.pack(side='left', padx=10, pady=10)
button_question2.pack(side='left', padx=10, pady=10)
button_question3 = ctk.CTkButton(question_frame, text="Q4", command=button_task, fg_color='#1B0166')
button_question3.pack(side='left', padx=10, pady=10)
button_question4 = ctk.CTkButton(question_frame, text="Q5", command=button_task, fg_color='#1B0166')
button_question4.pack(side='left', padx=10, pady=10)
button_question5 = ctk.CTkButton(question_frame, text="Q6", command=button_task, fg_color='#1B0166')
button_question5.pack(side='left', padx=10, pady=10)

# Global variable to keep track of the currently selected label
current_selected_label = None

# Function to handle label clicks
def on_label_click(event, label_widget):
    global current_selected_label

    # Reset the color of the previously selected label
    if current_selected_label is not None:
        current_selected_label.configure(fg_color='white')

    # Update the color of the currently selected label
    label_widget.configure(fg_color='#9953f5')  # Replace with your specific color

    # Update the reference to the currently selected label
    current_selected_label = label_widget

    # Add any additional functionality you need
    print(f"{label_widget.cget('text')} clicked")
    
    
# Function to create a colored circle
def create_colored_circle(parent, color_value):
    canvas = Canvas(parent, width=20, height=20, bg='white', highlightthickness=0)
    color = 'green' if color_value == 'green' else 'orange' if color_value == 'orange' else 'red'
    canvas.create_oval(5, 5, 15, 15, fill=color, outline=color)
    return canvas

# Modify the label/button creation to include a colored circle
def create_menu_option(parent, text, color_value):
    frame = ctk.CTkFrame(parent, corner_radius=10, fg_color='white')
    frame.pack(pady=2, padx=10, fill='x')

    # Create and pack the colored circle
    circle = create_colored_circle(frame, color_value)
    circle.pack(side='left', padx=(10, 5))

    # Create and pack the label/button
    label = ctk.CTkLabel(frame, text=text, cursor="hand2")
    label.pack(side='left')

    return label

# Example usage of create_menu_option
labels = [('Option 1', 'green'), ('Option 2', 'orange'), ('Option 3', 'red'), ('Option 4', 'green'), ('Option 5', 'orange'), ('Option 6', 'red')]
label_widgets = []

# When creating labels, bind them to the new click event handler
for text, color in labels:
    lbl = create_menu_option(side_menu, text, color)
    lbl.bind("<Button-1>", lambda event, lbl=lbl: on_label_click(event, lbl))
    label_widgets.append(lbl)
    
update_labels()

app.mainloop()
