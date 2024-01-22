import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog
from tkinter import *
from toolbag import roundUsing
import mysql.connector
from Bot import *
from label_generation import generate_tags_with_chat_model

# Define constants for appearance and color theme
APPEARANCE_MODE = "light"
COLOR_THEME = 'blue'
WINDOW_TITLE = 'Ans - Exam AI Engine'
WINDOW_GEOMETRY = '1440x900'

# Define file paths
LOGO_IMAGE_PATH = 'data/ans_logo.png'
USER_ICON_PATH = ''  # Update with actual path
creds_path = 'learningsemanticsearch.json'


class ExamAIApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title(WINDOW_TITLE)
        self.geometry(WINDOW_GEOMETRY)
        ctk.set_appearance_mode(APPEARANCE_MODE)
        ctk.set_default_color_theme(COLOR_THEME)
        
        self.default_font = ('Segoe UI', 10)
        self.primary_color = '#1B0166'
        self.secondary_color = '#C6BFD9'
        self.text_color = 'black'
        self.highlight_color = '#FFD700'
        
        #################### Start Database ####################
        self.round_instance = roundUsing(password="password")
        # print("step 1")
        self.round_instance.connect_to_db()
        # print("step 2")
        # self.round_instance.createDB("exam1")
        # print("step 3")
        self.round_instance.changeDatabase("exam1")
        # print("step 4")
        
        # cols = ["name","question","answer"]
        # datatype = ["VARCHAR(50)","LONGTEXT","LONGTEXT"]
        # colDT = [cols,datatype]
        # self.round_instance.createTable("answers",colDT)

        # cols = ["question","rubric"]
        # datatype = ["LONGTEXT","TEXT"]
        # colDT = [cols,datatype]
        # self.round_instance.createTable("exam",colDT)

        # cols = ["question","label"]
        # datatype = ["LONGTEXT","VARCHAR(50)"]
        # colDT = [cols,datatype]
        # self.round_instance.createTable("tag",colDT)

        # cols = ["name","accountName","password"]
        # datatype = ["VARCHAR(50)","VARCHAR(50)","VARCHAR(50)"]
        # colDT = [cols,datatype]
        # self.round_instance.createTable("account",colDT)

        # cols = ["rubric","answer","startIndex","endIndex", "confidence"]
        # datatype = ["TEXT","LONGTEXT","INTEGER","INTEGER", "DOUBLE"]
        # colDT = [cols,datatype]
        # self.round_instance.createTable("highlights",colDT)
        
        # cols = ["name","question","answer"]
        # data = ["'student1'","'Describe World War Two.'","""'World War II, which started November 1 1939, was a global conflict primarily involving the Allies, including the United States, the Soviet Union, and the United Kingdom, against the Axis powers, notably Nazi Germany, Italy, and Japan. The war began with Germany''s invasion of Poland, prompting Britain and France to declare war on Germany. This conflict was marked by significant events like the Holocaust, the bombing of Pearl Harbor, and the use of atomic bombs on Hiroshima and Nagasaki. The war resulted in immense human suffering and significant changes in the political landscape, leading to the Cold War and the establishment of the United Nations.'"""]
        # col_data = [cols,data]
        # self.round_instance.insertData("answers",colDTList=col_data)
        
        # cols = ["question","rubric"]
        # data = ["'Describe World War Two.'","'When did the war start?'"]
        # col_data = [cols,data]
        # self.round_instance.insertData("exam",colDTList=col_data)

        # self.round_instance.insertLabels("Describe World War Two.")
        

        

        # tables = self.round_instance.queryExecutor(queryString=self.round_instance.unionQuery(queryString1=self.round_instance.queryGenerate("answers","*",distinct="DISTINCT",condition="question = 'Describe World War Two.'"),queryString2=self.round_instance.queryGenerate("exam","*",condition="question = 'Describe World War Two.")))
        # for each in tables:
        #     for each1 in each:
        #         print(each1)

        
        # self.round_instance.cursor.close()
        # self.round_instance.conn.close()
        self.round_instance.close_connection() 

    ####################################### END Database###########################################
    
    #################### HIGHLIGHTING PART ####################
        self.bot = Bot(creds_path)
    
    ###########################################################
    
        # self.db_connection()
        
        self.questions = self.fetch_questions()

        self.question_buttons = []
        self.current_index = 0
        self.create_base_frame()
        self.create_top_frame()
        self.create_main_frame()
        self.create_rubrics_menu()
        self.create_label_menu()
        self.create_content_area()
        self.create_top_content_frame()
        self.create_content()
        self.create_questions_frame()

    def create_base_frame(self):
        self.base_frame = ctk.CTkFrame(self, corner_radius=10, fg_color='white')
        self.base_frame.pack(fill='both', expand=True, padx=0, pady=0)
        
    def create_top_frame(self):
        self.top_frame = ctk.CTkFrame(self.base_frame, corner_radius=10, fg_color='white')
        self.top_frame.pack(fill='x', expand=False, padx=0, pady=0)

        image = tk.PhotoImage(file='data/ans_logo.png') 
        image_label = ctk.CTkLabel(self.top_frame, image=image, text='')
        image_label.pack(side='left', padx=20, pady=10)

        user_icon = tk.PhotoImage(file='') 
        user_icon_label = ctk.CTkLabel(self.top_frame, image=user_icon,text='')
        user_icon_label.pack(side='right', padx=10, pady=10)

        user_details = ctk.CTkLabel(self.top_frame, text="Teacher Name\nProofs Teacher",
                                    font=self.default_font, text_color=self.text_color, anchor='e')
        user_details.pack(side='right', padx=10, pady=10)
        
    def create_main_frame(self):
        self.main_frame = ctk.CTkFrame(self.base_frame, corner_radius=10, fg_color='#C6BFD9')
        self.main_frame.pack(fill='both', expand=True, padx=0, pady=0)

    def create_rubrics_menu(self):
        self.side_menu = ctk.CTkFrame(self.main_frame, corner_radius=10, fg_color='white', border_color='grey', border_width=2, width=200)
        self.side_menu.pack(side='left', fill='y',padx=10, pady=10)

        self.rubric_title = ctk.CTkLabel(self.side_menu, text="Rubrics", font=("Arial", 20, "bold"),
                                         text_color=self.primary_color)
        self.rubric_title.pack(padx=10, pady=(10, 5)) 

        search_var = tk.StringVar()
        search_entry = ctk.CTkEntry(self.side_menu, textvariable=search_var, placeholder_text="Search")
        search_entry.pack(padx=10, pady=10, fill='x')

        self.rubric_frame = ctk.CTkFrame(self.side_menu, corner_radius=10, fg_color='white', border_color='grey', border_width=1, width=200)
        self.rubric_frame.pack(fill='x', padx=10, pady=10)
        
        self.task_button = ctk.CTkButton(self.side_menu, text="Generate Rubrics", fg_color='#1B0166')
        self.task_button.pack(side='bottom', padx=10, pady=10)

    def create_label_menu(self):
        label_menu_width = 200  
        
        self.label_menu = ctk.CTkFrame(self.main_frame, corner_radius=10, fg_color='white', border_color='grey', border_width=2, width=label_menu_width)
        self.label_menu.pack(side='right', fill='both', padx=10, pady=10)
        
        self.label_title = ctk.CTkLabel(self.label_menu, text="Labels", font=("Arial", 20, "bold"),
                                        text_color=self.primary_color)
        self.label_title.pack(padx=10, pady=(10, 5))
        
        self.label_frame = ctk.CTkFrame(self.label_menu, corner_radius=10, fg_color='white', border_color='grey', border_width=1, width=200)
        self.label_frame.pack(fill='x', padx=10, pady=10)

    def create_content_area(self):
        self.content_frame = ctk.CTkFrame(self.main_frame, width=600, corner_radius=10, fg_color='white', border_color='grey', border_width=1)
        self.content_frame.pack(side='left', fill='both', expand=True, padx=10, pady=10)
        
    def create_top_content_frame(self):
        self.top_content_frame = ctk.CTkFrame(self.content_frame, corner_radius=10, fg_color='white', border_color='grey', border_width=1)
        self.top_content_frame.pack(side='top', fill='both', padx=10, pady=10, expand = True)

    def create_content(self):
        self.box_frame = ctk.CTkFrame(self.top_content_frame, corner_radius=10, bg_color='transparent', fg_color='white')
        self.box_frame.pack(padx=10, pady=10, fill='both', expand=False)

        self.box_frame_left = ctk.CTkFrame(self.box_frame, corner_radius=10, bg_color='transparent', fg_color='white')
        self.box_frame_left.pack(side='left', padx=10, pady=10, anchor='nw')

        self.box_frame_right = ctk.CTkFrame(self.box_frame, corner_radius=10, bg_color='transparent', fg_color='white')
        self.box_frame_right.pack(side='right', padx=0, pady=0, anchor='ne')

        self.bold_text = ctk.CTkLabel(self.box_frame_left, font=("Arial", 12, "bold"),
                                      text_color=self.text_color, anchor='w')
        self.bold_text.pack(padx=10, pady=10, anchor='nw')

        self.large_color_text = ctk.CTkLabel(self.box_frame_left, text_color=self.text_color,
                                             font=("Arial", 20))
        self.large_color_text.pack(pady=10, anchor='nw', padx=20)

        self.show_labels_button = ctk.CTkButton(self.box_frame_right, text="Hide Labels", command=self.hide_labels_task, fg_color='#1B0166')
        self.show_labels_button.pack(side='right', padx=0, pady=10, anchor='ne')

    def create_student_list_frame(self, num_students, unique_students):
        self.student_list_frame = ctk.CTkFrame(self.top_content_frame, corner_radius=10, fg_color='white', border_color='grey', border_width=2, width=200)
        self.student_list_frame.pack(side='right', fill='both', padx=10, pady=10, expand=True)

        self.canvas = Canvas(self.student_list_frame)
        self.canvas.pack(side='left', fill='both', expand=True)

        self.scrollbar = Scrollbar(self.student_list_frame, orient='vertical', command=self.canvas.yview)
        self.scrollbar.pack(side='right', fill='y')

        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox('all')))

        self.inner_frame = ctk.CTkFrame(self.canvas, corner_radius=10, fg_color='white', border_color='grey', border_width=1)
        self.canvas.create_window((0, 0), window=self.inner_frame, anchor='nw')
        rows = 5
        for i, student_name in enumerate(unique_students):
            btn = ctk.CTkButton(self.inner_frame, text=student_name, command=lambda i=i: self.student_button_action(i))
            btn.grid(row=i % rows, column=i // rows, padx=10, pady=5, sticky="nsew")


    
    def create_questions_frame(self):
        self.question_frame = ctk.CTkFrame(self.content_frame, corner_radius=10, fg_color='white', border_color='grey', border_width=1)
        self.question_frame.pack(side='bottom', fill='x', padx=10, pady=10, anchor='s')
        
        self.button_left = ctk.CTkButton(self.question_frame, text="<", command=lambda: self.scroll("left"), fg_color='#1B0166')
        self.button_left.pack(side="left", padx=10, pady=10)

        self.button_right = ctk.CTkButton(self.question_frame, text=">", command=lambda: self.scroll("right"), fg_color='#1B0166')
        self.button_right.pack(side="right", padx=10, pady=10)
        
        self.create_question_buttons()

        self.show_buttons(self.current_index)
        
        

####################  Hide labels Functions ####################

    def hide_labels_task(self):
        self.label_menu.pack_forget()
        self.show_labels_button.configure(text="Show Labels", command=self.show_labels_task)
        
    def show_labels_task(self):
        self.label_menu.pack(side='right', fill='y', padx=10, pady=10)
        self.show_labels_button.configure(text="Hide Labels", command=self.hide_labels_task)
        
        
######################## Question Buttons ####################
        
    def create_question_buttons(self, fg_color='#1B0166', button_width=100, button_height=30):
        for i, question_text in enumerate(self.questions, start=1):
            button = ctk.CTkButton(self.question_frame, text=f"Q{i}: {question_text}", fg_color=fg_color, width=button_width, height=button_height, command=lambda i=i: self.question_button_action(i-1))
            self.question_buttons.append(button)

    def question_button_action(self, question_index):
        self.current_question_index = question_index
        selected_question = self.questions[question_index]

        self.bold_text.configure(text=f"Q{question_index + 1}")
        self.large_color_text.configure(text=selected_question)

        existing_labels = self.round_instance.getLabels(selected_question)
        print(existing_labels)
        if all(label[0] is None for label in existing_labels):
            print(f"No labels found for '{selected_question}'. Generating labels.")
            tags = generate_tags_with_chat_model(selected_question) 
            self.round_instance.insertLabels(selected_question, tags)
            print(f"Labels added for '{selected_question}': {tags}")
        else:
            print(f"Labels already exist for '{selected_question}'.")
        self.load_and_display_rubrics(question_index)
        self.load_and_display_labels(question_index)
        self.show_student_list_frame()
        
    def student_button_action(self, student_index):
        self.current_student_index = student_index
        student_answer = self.get_student_answer(student_index)
        self.highlight_insertion()  # Insert highlights for this student's answer
        self.display_student_answer(student_answer)
        self.display_rubrics_with_confidence(student_answer)

            
#################### End Question Buttons ####################        
#################### Rubrics and Labels ####################

    def confidence_to_color(self, confidence):
        confidence = max(0.0, min(1.0, confidence)) 
        yellow_red = 255
        yellow_green = 255
        if confidence < 0.5:
            red = 255
            green = int((confidence / 0.5) * yellow_green)
            blue = 0
        else:
            red = int(((1.0 - confidence) / 0.5) * yellow_red)
            green = 255
            blue = 0
        return f'#{red:02x}{green:02x}{blue:02x}'

    def display_rubrics_with_confidence(self, student_answer):
        for widget in self.rubric_frame.winfo_children():
            widget.destroy()

        rubrics_with_confidence = self.round_instance.getHighlightsForAnswer(student_answer)
        for index, (rubric, confidence) in enumerate(rubrics_with_confidence):
            color = self.confidence_to_color(confidence)
            canvas = tk.Canvas(self.rubric_frame, width=20, height=20, bg=color, highlightthickness=0)
            canvas.create_oval(5, 5, 15, 15, fill=color, outline=color)
            canvas.grid(row=index, column=0, padx=(5, 5), pady=5, sticky="w")
            rubric_label = ctk.CTkLabel(self.rubric_frame, text=rubric, width=200)
            rubric_label.grid(row=index, column=1, sticky="w")
            rubric_label.bind("<Button-1>", lambda event, r=rubric: self.on_rubric_label_click(r, student_answer))
            
    def on_rubric_label_click(self, rubric, student_answer):
        highlights = self.round_instance.getHighlights(rubric, student_answer)
        if highlights:
            for highlight in highlights:
                start_index, end_index = highlight[0], highlight[1]
                print(f"Highlighting from {start_index} to {end_index}")
                self.highlight_text(start_index, end_index)
                print(student_answer[start_index:end_index])
                print(len(student_answer))
        else:
            print(f"No highlights found for rubric '{rubric}'")


    def highlight_text(self, start_index, end_index):
        self.answer_text.tag_remove("highlight", "1.0", "end")
        self.answer_text.tag_config("highlight", background=self.highlight_color, foreground="black")
        self.answer_text.tag_add("highlight", f"1.{start_index}", f"1.{end_index}")

    
    def highlight_insertion(self):
        rubrics = self.round_instance.getRubrics(self.questions[self.current_question_index])
        for rubric in rubrics:
            rubric_text = rubric[0]
            student_answer = self.get_student_answer(self.current_student_index)

            existing_highlights = self.round_instance.checkHighlightsExist(rubric_text, student_answer)
            if existing_highlights:
                print(f"Highlights for '{rubric_text}' already exist in the database.")
            else:
                print(f"No highlights found for '{rubric_text}'. Running model.")
                indices = self.bot.run_model(student_answer, rubric_text)
                self.round_instance.insertHighlights(rubric_text, student_answer, indices[0][0], indices[0][1], 0.5)
                print(f"Highlights added for '{rubric_text}': {indices}")
    

    
#################### End Rubrics and Labels ####################

    def show_buttons(self, start_index, num_buttons=5):
        for button in self.question_buttons:
            button.pack_forget()

        for i in range(start_index, min(start_index + num_buttons, len(self.question_buttons))):
            self.question_buttons[i].pack(side='left', padx=10, pady=10 )
    
    def scroll(self, direction):
        if direction == "left" and self.current_index > 0:
            self.current_index -= 5
        elif direction == "right" and self.current_index < len(self.question_buttons) - 5:
            self.current_index += 5
        self.show_buttons(self.current_index)
        
    
        
    #################### End Question Buttons ####################
    
    def switch_to_answer_frame(self):
        self.student_list_frame.pack_forget()
        self.create_answer_frame()
                
    def clear_rubrics_display(self):
            for widget in self.rubric_frame.winfo_children():
                widget.destroy()

    def switch_to_student_list(self):
        self.answer_frame.pack_forget()
        self.clear_rubrics_display() 
        self.student_list_frame.pack(side='right', fill='both', padx=10, pady=10, expand=True)

        
    
    def show_student_list_frame(self):
        # Logic to display the student list frame
        if hasattr(self, 'student_list_frame'):
            self.student_list_frame.pack_forget()
        selected_question = self.questions[self.current_question_index]
        unique_students = self.get_unique_students(selected_question)

        self.create_student_list_frame(len(unique_students), unique_students)
        
    def get_unique_students(self, question):
        student_data = self.round_instance.getUniqueStudentsForQuestion(question)
        unique_students = [data[0] for data in student_data]  # Adjust based on your data structure
        return unique_students
    
    def display_student_answer(self, answer, start_index=None, end_index=None):
        self.switch_to_answer_frame()
        self.answer_text.delete("1.0", "end")  # Clear existing text
        self.answer_text.insert("1.0", answer)  # Insert new text
        if start_index is not None and end_index is not None:
            self.highlight_text(start_index, end_index)


    def create_answer_frame(self):
        if not hasattr(self, 'answer_frame'):
            self.answer_frame = ctk.CTkFrame(self.top_content_frame, corner_radius=10, fg_color='white', border_color='grey', border_width=1)
            self.answer_frame.pack(side='bottom', fill='both', expand=True, padx=10, pady=10)

            self.answer_text = Text(self.answer_frame, font=("Arial", 16), wrap="word", height=10, bg='#FFFFFF')
            self.answer_text.pack(padx=10, pady=(10, 5))

            return_button = ctk.CTkButton(self.answer_frame, text="Back to Students", command=self.switch_to_student_list, fg_color='#1B0166')
            return_button.pack(pady=10)
        else:
            self.answer_frame.pack(side='bottom', fill='both', expand=True, padx=10, pady=10)


    
    
    #################### DATABASE CONNECTIONS ####################
    def db_connection(self):
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="password",
                database="exam1"
            )
            if conn.is_connected():
                print("Successfully connected to the database")
            else:
                print("Failed to connect to the database")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            
            
    #################### DATABASE FETCHES ####################
    def fetch_questions(self):
        print("Fetching questions...")
        question_data = self.round_instance.getquestions()
        print(f"Questions fetched: {question_data}")

        if question_data is None:
            return []

        questions = [q[0] for q in question_data]
        return questions

    def load_and_display_rubrics(self, question_index):
        rubrics = self.round_instance.getRubrics(self.questions[question_index])

        for widget in self.rubric_frame.winfo_children():
            widget.destroy()

        for rubric in rubrics:
            rubric_label = ctk.CTkLabel(self.rubric_frame, text=rubric, width=200)
            rubric_label.pack()

    def load_and_display_labels(self, question_index):
        labels = self.round_instance.getLabels(self.questions[question_index])
        for widget in self.label_frame.winfo_children():
            widget.destroy()
        for label in labels:
            label_label = ctk.CTkLabel(self.label_frame, text=label, width=200)
            label_label.pack()

    def get_student_answer(self, student_index):
        student_name = "Student" + str(student_index + 1)
        answer_data = self.round_instance.getStudentAnswer(student_name)

        if answer_data:
            return answer_data[0][1]
        else:
            return "No answer found"

def main():
    app = ExamAIApp()
    app.mainloop()

if __name__ == "__main__":
    main()