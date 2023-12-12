import customtkinter as ctk
import tkinter as tk
from tkinter import *
from tkinter import filedialog
# from labeling_model import classify_sentence, classifier
from toolbag import roundUsing, init_hashmap, print3DHashmap

ctk.set_appearance_mode("light")
ctk.set_default_color_theme('blue')

app = ctk.CTk()
app.title('Ans - Exam AI Engine')
app.geometry('1440x900')
current_selected_button = None 

######################## V=Variables to show in gui ######################

# roundUsing_instance = roundUsing()
# init_hashmap("data\QARtest_1.csv",roundUsing_instance)
# hashmap = roundUsing_instance.getHashmap()
# questions = list(hashmap.keys())
# print3DHashmap(hashmap)

# print(questions)


roundUsing_instance = roundUsing()
questions = [
    "Describe World War Two.", 
    "Translate the following sentence into a formula of epistemic logic, using appropriate translation keys: Alice does not know whether Bob knows that she likes sailing, and Bob knows whether Alice likes sailing",
    "Describe the most important characteristics of a rational agent."
    

]


answers = [
    [
        """World War II, which started on September 1, 1939, was a global conflict primarily involving the Allies, 
        including the United States, the Soviet Union, and the United Kingdom, against the Axis powers, notably Nazi 
        Germany, Italy, and Japan. The war began with Germany's invasion of Poland, prompting Britain and France to 
        declare war on Germany. This conflict was marked by significant events like the Holocaust, the bombing of 
        Pearl Harbor, and the use of atomic bombs on Hiroshima and Nagasaki. The war resulted in immense human 
        suffering and significant changes in the political landscape, leading to the Cold War and the establishment 
        of the United Nations.""",
        """World War 2 was a big war that happened a long time ago. I think it started because some countries were 
        not getting along, and then everyone started fighting. There were a lot of soldiers and tanks, and I remember 
        there was something about a Pearl Harbor movie. It ended because America dropped a big bomb, 
        and then everyone decided to stop fighting. I'm not sure about the details, but it was a really important 
        war."""
    ],
    [
        """The statement 'Alice does not know whether Bob knows that she likes sailing' is interpreted in two parts. 
        The first part, 'Alice does not know,' is 'Not Alice knows.' The second part, 'whether Bob knows that she 
        likes sailing,' is 'Bob knows (P).' So, this part of the sentence is 'Not Alice knows (Bob knows (P)).' 
        The second part of the sentence, 'Bob knows whether Alice likes sailing,' translates to 'Bob knows (Alice 
        knows (P) or Not Alice knows (P)).' Thus, the entire sentence in epistemic logic is 'Not Alice knows (Bob 
        knows (P)) and Bob knows (Alice knows (P) or Not Alice knows (P)).'""",
        """The sentence involves what Alice and Bob know about Alice's interest in sailing. For Alice, the sentence 
        'she does not know if Bob is aware of her liking for sailing' translates to 'Not Alice knows (Bob knows 
        (P)).' However, the student mistakenly translates the second part as just 'Bob knows (P),' missing the detail 
        about Bob knowing whether Alice knows she likes sailing or not. Therefore, their final translation is 'Not 
        Alice knows (Bob knows (P)) and Bob knows (P),' which overlooks Bob's awareness of Alice's knowledge or lack 
        thereof about her liking for sailing."""
    ],
    
    [
        "The primary goal of a rational agent is to achieve the best possible outcome or performance given the available information and resources. This involves making decisions that maximize its success or utility based on its goals and the current state of the environment. A rational agent utilizes information from its environment by perceiving its surroundings, processing the gathered data, and making informed decisions based on that information. This process allows the agent to act in a manner that is most likely to achieve its objectives, considering the current conditions and available data. The ability to evaluate choices is crucial for a rational agent’s effectiveness. It enables the agent to assess different possible actions and select the one that is most likely to lead to the desired outcome. This decision-making process is based on predicting the consequences of each action and choosing the action that aligns best with the agent’s goals. Learning and adaptation are vital for a rational agent, especially in dynamic or complex environments. An agent that can learn from past experiences and adapt to new situations can improve its performance over time. This adaptability ensures that the agent remains effective even as conditions change or new information becomes available."
    ]
    
    
]



rubrics = [
    ["When did the war start?", "Which countries were in the Allies?"],
    ["What is the Logical Translation", "What Epistemic Operators are used?", "Which Complex Knowledge States are present"],
    ["What is the primary goal of a rational agent?", "How does a rational agent utilize information from its environment?", "How important is learning and adaptation for a rational agent?", ],
    
    
    
]


#     ######## simple answer and rubrics test cases
# questions = ["What are the pros and cons of online education?"]
# answers = ["Convenience and flexibility","Interaction challenges"]
# rubrics = ["Clear and concise","Relevance to the question"]

    # add to hashmap
for i in range(len(questions)):
    q = questions[i]
    for a in answers[i]:
        for r in rubrics[i]:
            roundUsing_instance.add(Question=q, Rubric=r, Answer=a)
            
hashmap = roundUsing_instance.getHashmap()
questions = list(hashmap.keys())

print3DHashmap(hashmap)

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

rubric_title = ctk.CTkLabel(side_menu, text="Rubrics", font=("Arial", 20, "bold"), text_color='#1B0166')
rubric_title.pack(padx=10, pady=(10, 5))  # Adjust padding as needed

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

text_widget = Frame(inner_frame, bg='white')
text_widget.pack(side='left', fill='both', expand=True)


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



def on_rubric_click(question_text, rubric,event=None):
    
    print(f"Rubric clicked: {rubric} for question: {question_text}")
    question_data = hashmap.get(question_text, {})
    answer_widgets = student_answer_widgets.get(question_text, [])


    for answer_text_widget in answer_widgets:
        answer_text_widget.tag_remove("highlight", "1.0", "end")
        answer_text = answer_text_widget.get("1.0", "end-1c").strip()
        for answer_key, rubric_data in question_data.items():
            if answer_key != 'Lable' and rubric in rubric_data:
                rubric_info = rubric_data.get(rubric, [])
                if len(rubric_info) >= 5:
                    stored_answer_text = rubric_info[1]
                    if stored_answer_text.strip() == answer_text:
                        start, end = rubric_info[3], rubric_info[4]
                        print(f"Highlighting text for rubric '{rubric}': start index = {start}, end index = {end}")
                        if start != '' and end != '':
                            highlight_text(answer_text_widget, start, end)
                        break




def create_rubric_option(parent, text, color_value, question_text, rubric):
    frame = ctk.CTkFrame(parent, corner_radius=10, fg_color='white', width=200)
    frame.pack(pady=2, padx=10, fill='x')

    circle = create_colored_circle(frame, color_value)
    circle.pack(side='left', padx=(10, 5))

    label = ctk.CTkLabel(frame, text=text, cursor="hand2", width=200-30)
    label.pack(side='left', padx=5)
    label.bind("<Button-1>", lambda event: on_rubric_click(question_text, rubric, event))

    return label




def get_text_index(char_count, text_widget):
    content = text_widget.get("1.0", "end-1c")
    line, char = 1, 0
    for i, c in enumerate(content):
        if i == char_count:
            break
        if c == "\n":
            line += 1
            char = 0
        else:
            char += 1
    return f"{line}.{char}"

def highlight_text(text_widget, start_char, end_char):
    if start_char != '' and end_char != '':
        start_index = get_text_index(int(start_char), text_widget)
        end_index = get_text_index(int(end_char), text_widget)
        print(f"Attempting to highlight from {start_index} to {end_index}")
        print(f"Text to be highlighted: '{text_widget.get(start_index, end_index)}'")
        text_widget.tag_add("highlight", start_index, end_index)
        text_widget.tag_config("highlight", background="yellow")


def update_rubrics(question_text, rubric_frame, hashmap):
    for widget in rubric_frame.winfo_children():
        widget.destroy()
        
    question_data = hashmap.get(question_text, {})
    unique_rubrics = set()

    for answer, rubrics in question_data.items():
        if answer != 'Lable':
            unique_rubrics.update(rubrics.keys())

    for rubric in unique_rubrics:
        if rubric != 'Lable':
            color_value = 'green'
            rubric_label = create_rubric_option(rubric_frame, rubric, color_value, question_text, rubric)




def update_labels_for_question(question_text, label_menu, hashmap):
    question_data = hashmap.get(question_text, {})
    labels = question_data.get("Lable", [])
    for widget in label_menu.winfo_children():
        widget.destroy()

    for label_text in labels:
        label = ctk.CTkLabel(label_menu, text=label_text, cursor="hand2", text_color='#1B0166')
        label.pack(pady=10, padx=30)
        
        

def create_scrollable_answer_frame(parent):
    answer_container_frame = Frame(parent)
    answer_container_frame.pack(fill='both', expand=True, padx=10, pady=10)

    canvas = Canvas(answer_container_frame, bg='white')
    canvas.pack(side='left', fill='both', expand=True)

    scrollbar = Scrollbar(answer_container_frame, orient='vertical', command=canvas.yview)
    scrollbar.pack(side='right', fill='y')

    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind('<Configure>',lambda e: canvas.configure(scrollregion=canvas.bbox('all')))

    answer_frame = Frame(canvas)
    canvas.create_window((0, 0), window=answer_frame, anchor='nw', width=875, height=600)

    return answer_frame
        
        
student_answer_widgets = {}

def update_question_labels_and_answers(question_number, question_text, bold_label, color_label, container_frame, rubric_frame, label_menu, hashmap, buttons):
    global current_selected_button
    global student_answer_widgets
    
    for widget in container_frame.winfo_children():
        widget.destroy()
    student_answer_widgets[question_text] = []

    for btn in buttons:
        btn.configure(fg_color="#1B0166")
    current_selected_button = buttons[question_number - 1]
    current_selected_button.configure(fg_color="#4C9A2A")

    bold_label.configure(text=f"Question {question_number}")
    color_label.configure(text=question_text)

    scrollable_answer_frame = create_scrollable_answer_frame(container_frame)

    answer_count = 1
    for answer, rubrics in hashmap.get(question_text, {}).items():
        if answer != 'Lable':
            answer_label = Label(scrollable_answer_frame, text=f"Student Answer {answer_count}:", font=("Arial", 12, "bold"),)
            answer_label.pack(anchor='w')

            answer_text_widget = Text(scrollable_answer_frame, wrap='word', bg='white', fg='black', height=5)
            answer_text_widget.pack(fill='both', expand=True)
            answer_text_widget.insert('1.0', answer)

            student_answer_widgets[question_text].append(answer_text_widget)

            answer_count += 1
    
    update_labels_for_question(question_text, label_menu, hashmap)
    update_rubrics(question_text, rubric_frame, hashmap)


def create_question_buttons(parent_frame, questions, bold_label, color_label, text_widget, rubric_frame, hashmap, fg_color='#1B0166', button_width=100, button_height=30):
    buttons = []
    for i, question_text in enumerate(questions, start=1):
        button_command = lambda i=i, question_text=question_text: update_question_labels_and_answers(i, question_text, bold_label, color_label, text_widget, rubric_frame, label_menu, hashmap, buttons)
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
