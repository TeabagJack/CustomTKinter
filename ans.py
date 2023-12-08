import customtkinter as ctk
import tkinter as tk
from tkinter import *
from tkinter import filedialog
from labeling_model import classify_sentence, classifier
from toolbag import roundUsing

ctk.set_appearance_mode("light")
ctk.set_default_color_theme('blue')

app = ctk.CTk()
app.title('Ans - Exam AI Engine')
app.geometry('1440x900')
current_selected_button = None 



######################## V=Variables to show in gui ######################

roundUsing_instance = roundUsing()
init_hashmap("data\QARtest_1.csv",roundUsing_instance)
hashmap = roundUsing_instance.getHashmap()
questions = list(hashmap.keys())

print(questions)


# ======================== Top Frame ========================

top_frame = ctk.CTkFrame(app, corner_radius=10, fg_color='white')
top_frame.pack(fill='x', expand=False, padx=0, pady=0)

image = tk.PhotoImage(file='data/ans_logo.png') 
image_label = ctk.CTkLabel(top_frame, image=image, text='')
image_label.pack(side='left', padx=20, pady=10)

user_icon = tk.PhotoImage(file='') 
user_icon_label = ctk.CTkLabel(top_frame, image=user_icon,text='')
user_icon_label.pack(side='right', padx=10, pady=10)

user_details = ctk.CTkLabel(top_frame, text="Teacher Name\nProofs Teacher", font=("Arial", 10), anchor='e')
user_details.pack(side='right', padx=10, pady=10)
# -------------------------------------------------------------


## ======================== Main Frame ========================
main_frame = ctk.CTkFrame(app, corner_radius=10, fg_color='#C6BFD9')
main_frame.pack(fill='both', expand=True, padx=0, pady=0)
# -------------------------------------------------------------


# ======================== Side Menu - Rubrics ========================
side_menu = ctk.CTkFrame(main_frame, corner_radius=10, fg_color='white', border_color='grey', border_width=2, width=200)
side_menu.pack(side='left', fill='y',padx=10, pady=10)

search_var = tk.StringVar()
search_entry = ctk.CTkEntry(side_menu, textvariable=search_var, placeholder_text="Search")
search_entry.pack(padx=10, pady=10, fill='x')

rubric_frame = ctk.CTkFrame(side_menu, corner_radius=10, fg_color='white', border_color='grey', border_width=1, width=200)
rubric_frame.pack(fill='x', padx=10, pady=10)

# --------------------------------------------------------------------


# ======================== Side Menu - Labels ========================
label_menu_width = 200  

label_menu = ctk.CTkFrame(main_frame, corner_radius=10, fg_color='white', border_color='grey', border_width=2, width=label_menu_width)
label_menu.pack(side='right', fill='both', padx=10, pady=10)


def hide_labels_task():
    label_menu.pack_forget()
    show_labels_button.configure(text="Show Labels", command=show_labels_task)
    
def show_labels_task():
    label_menu.pack(side='right', fill='y', padx=10, pady=10)
    show_labels_button.configure(text="Hide Labels", command=hide_labels_task)
    
def classify_labels_per_question():
    labels = ["math", "history", "Arithmetic"]
    sentence = "The square root of four is two"
    answer = classify_sentence(sentence, labels, classifier, 0.7, True)
    print(answer)
    

label_description = ctk.CTkLabel(label_menu, text="Labels", font=("Arial", 20, "bold"), text_color='#1B0166')
label_description.pack(padx=60, pady=10, anchor='n')

list_labels = ['Label 1', 'Label 2', 'Label 3', 'Label 4', 'Label 5', 'Label 6']

for label in list_labels:
    lbl = ctk.CTkLabel(label_menu, text=label, cursor="hand2", text_color='#1B0166')
    lbl.pack(pady=10, padx=30)



# --------------------------------------------------------------------
def button_task():
    print("Button clicked")

task_button = ctk.CTkButton(side_menu, text="Generate Rubrics", command=button_task, fg_color='#1B0166')
task_button.pack(side='bottom', padx=10, pady=10)


# ======================== Content - Right Side ========================

content_frame = ctk.CTkFrame(main_frame, width=600, corner_radius=10, fg_color='white', border_color='grey', border_width=1)
content_frame.pack(side='left', fill='both', expand=True, padx=10, pady=10)

box_frame = ctk.CTkFrame(content_frame, corner_radius=10, bg_color='transparent', fg_color='white')
box_frame.pack(padx=10, pady=10, fill='both', expand=True)

box_frame_left = ctk.CTkFrame(box_frame, corner_radius=10, bg_color='transparent', fg_color='white')
box_frame_left.pack(side='left', padx=10, pady=10, fill='both', expand=True)

box_frame_right = ctk.CTkFrame(box_frame, corner_radius=10, bg_color='transparent', fg_color='white')
box_frame_right.pack(side='right', padx=0, pady=0, fill='both', expand=True)


bold_text = ctk.CTkLabel(box_frame_left, text="Question 1", font=("Arial", 12, "bold"), anchor='w')
bold_text.pack(padx=10, pady=10, anchor='nw')

large_color_text = ctk.CTkLabel(box_frame_left, text="Prove P = NP ", text_color="black", font=("Arial", 20))
large_color_text.pack(pady=10, anchor='nw', padx=20)

show_labels_button = ctk.CTkButton(box_frame_right, text="Show Labels", command=hide_labels_task, fg_color='#1B0166')
show_labels_button.pack(side='right', padx=0, pady=10, anchor='ne')



text_box_frame = ctk.CTkFrame(content_frame, corner_radius=10, bg_color='transparent')
text_box_frame.pack(padx=10, pady=10, fill='both', expand=True)

inner_frame = Frame(text_box_frame)
inner_frame.pack(fill='both', expand=True)

text_widget = Text(inner_frame, wrap='word', bg='white', fg='black')
text_widget.pack(side='left', fill='both', expand=True)
text_widget.insert('1.0', 'Your large amount of text goes here...')

scrollbar = Scrollbar(inner_frame, command=text_widget.yview)
scrollbar.pack(side='right', fill='y')

text_widget.config(yscrollcommand=scrollbar.set)

# Create a frame for the text box and buttons
bottom_frame = ctk.CTkFrame(content_frame, corner_radius=10, fg_color='white')
bottom_frame.pack(padx=10, pady=10, fill='x')

file_entry = ctk.CTkEntry(bottom_frame, fg_color='white', placeholder_text="enter your question here to add.")
file_entry.pack(side='left', fill='x', expand=True, padx=10)

def upload_file():
    filename = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if filename:
        file_entry.delete(0, END)
        file_entry.insert(0, filename)

def save_file():
    filename = file_entry.get()
    if filename:
        with open(filename, 'r') as file:
            text_content = file.read()
            print(text_content)  

upload_btn = ctk.CTkButton(bottom_frame, text="Upload", command=upload_file, fg_color='#1B0166')
upload_btn.pack(side='left', padx=10)

save_btn = ctk.CTkButton(bottom_frame, text="Save", command=save_file, fg_color='#1B0166')
save_btn.pack(side='left')


# ======================== Dynamically create buttons with this function. ========================

def create_colored_circle(parent, color_value):
    canvas = Canvas(parent, width=20, height=20, bg='white', highlightthickness=0)
    color = 'green' if color_value == 'green' else 'orange' if color_value == 'orange' else 'red'
    canvas.create_oval(5, 5, 15, 15, fill=color, outline=color)
    return canvas

def create_rubric_option(parent, text, color_value):
    frame = ctk.CTkFrame(parent, corner_radius=10, fg_color='white', width=200)
    frame.pack(pady=2, padx=10, fill='x')

    circle = create_colored_circle(frame, color_value)
    circle.pack(side='left', padx=(10, 5))

    label = ctk.CTkLabel(frame, text=text, cursor="hand2", width=200-30)
    label.pack(side='left', padx=5)

    return label


def update_rubrics(question_text, rubric_frame, hashmap):
    question_data = hashmap.get(question_text, {})
    
    for widget in rubric_frame.winfo_children():
        widget.destroy()

    unique_rubrics = set()
    for answer_data in question_data.values():
        if isinstance(answer_data, dict):
            unique_rubrics.update(answer_data.keys())

    for rubric in unique_rubrics:
        if rubric != 'Lable':
            color_value = 'green' 
            rubric_label = create_rubric_option(rubric_frame, rubric, color_value)


def update_question_labels_and_answers(question_number, question_text, bold_label, color_label, text_widget, rubric_frame, hashmap, buttons):
    global current_selected_button
    
    for btn in buttons:
        btn.configure(fg_color="#1B0166")

    # Update the appearance of the selected button
    current_selected_button = buttons[question_number - 1]
    current_selected_button.configure(fg_color="#4C9A2A")
    
    question_data = hashmap.get(question_text, {})

    bold_label.configure(text=f"Question {question_number}")
    color_label.configure(text=question_text)

    formatted_answers = ""
    answer_count = 1 
    for answer, rubrics in question_data.items():
        if answer != 'Lable': 
            formatted_answers += f"Student Answer {answer_count}:\n{answer}\n\n"
            answer_count += 1

    text_widget.delete('1.0', 'end')
    text_widget.insert('1.0', formatted_answers)

    update_rubrics(question_text, rubric_frame, hashmap)




def create_question_buttons(parent_frame, questions, bold_label, color_label, text_widget, rubric_frame, hashmap, fg_color='#1B0166', button_width=100, button_height=30):
    buttons = []
    for i, question_text in enumerate(questions, start=1):
        button_command = lambda i=i, question_text=question_text: update_question_labels_and_answers(i, question_text, bold_label, color_label, text_widget, rubric_frame, hashmap, buttons)
        button = ctk.CTkButton(parent_frame, text=f"Q{i}", command=button_command, fg_color=fg_color, width=button_width, height=button_height)
        button.pack(side='left', padx=10, pady=10)
        buttons.append(button)
        button.pack_forget()

    return buttons


def show_buttons(buttons, start_index, num_buttons=5):
    for button in buttons:
        button.pack_forget()

    for i in range(start_index, min(start_index + num_buttons, len(buttons))):
        buttons[i].pack(side='left', padx=10, pady=10 )


question_frame = ctk.CTkFrame(content_frame, corner_radius=10, fg_color='white', border_color='grey', border_width=1)
question_frame.pack(side='bottom', fill='x', padx=10, pady=10)

buttons = create_question_buttons(question_frame, questions, bold_text, large_color_text, text_widget, rubric_frame, hashmap)

current_index = 0 

def scroll(direction):
    global current_index
    if direction == "left" and current_index > 0:
        current_index -= 5
    elif direction == "right" and current_index < len(buttons) - 5:
        current_index += 5
    show_buttons(buttons, current_index)

button_left = ctk.CTkButton(question_frame, text="<", command=lambda: scroll("left"), fg_color='#1B0166')
button_left.pack(side="left", padx=10, pady=10)

button_right = ctk.CTkButton(question_frame, text=">", command=lambda: scroll("right"), fg_color='#1B0166')
button_right.pack(side="right", padx=10, pady=10)

show_buttons(buttons, current_index)

# =================================================================================================

app.mainloop()
