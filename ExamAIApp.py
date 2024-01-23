import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog
from tkinter import *
from toolbag import roundUsing
import mysql.connector
from Bot import *
from label_generation import generate_tags_with_chat_model
from GrammarChecker2 import GrammarChecker2

APPEARANCE_MODE = "light"
COLOR_THEME = 'blue'
WINDOW_TITLE = 'Ans - Exam AI Engine'
WINDOW_GEOMETRY = '1440x900'

# Define  paths
LOGO_IMAGE_PATH = 'data/ans_logo.png'
USER_ICON_PATH = ''
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
        self.corrector = GrammarChecker2()
        self.highlighted_label = None

        
        #################### Start Database ####################
        
        self.round_instance = roundUsing(password="password")
        self.round_instance.initialize_database()
        
        # datas = []

        # datas.append(["How is climate change impacting global weather patterns?","student1","Climate change is significantly impacting global weather patterns, leading to a surge in extreme weather events. We observe more frequent and intense hurricanes, such as Hurricane Harvey in 2017, which caused widespread flooding and devastating impacts. Additionally, heatwaves are becoming more common, as seen in the European heatwave of 2019. These events are clear indicators of the changing climate. Agriculture is heavily affected, with altered precipitation patterns, shifting growing seasons, and increased pest pressure. These changes threaten food security globally, impacting crop yields and quality. To address this, individuals can contribute by adopting sustainable practices, such as reducing meat consumption, using energy-efficient appliances, and supporting renewable energy sources. These efforts collectively help reduce the overall carbon footprint and contribute to mitigating climate change.","What are some specific examples of extreme weather events linked to climate change?"])
        # datas.append(["How is climate change impacting global weather patterns?","student1","Climate change is significantly impacting global weather patterns, leading to a surge in extreme weather events. We observe more frequent and intense hurricanes, such as Hurricane Harvey in 2017, which caused widespread flooding and devastating impacts. Additionally, heatwaves are becoming more common, as seen in the European heatwave of 2019. These events are clear indicators of the changing climate. Agriculture is heavily affected, with altered precipitation patterns, shifting growing seasons, and increased pest pressure. These changes threaten food security globally, impacting crop yields and quality. To address this, individuals can contribute by adopting sustainable practices, such as reducing meat consumption, using energy-efficient appliances, and supporting renewable energy sources. These efforts collectively help reduce the overall carbon footprint and contribute to mitigating climate change.","How do these changes affect agriculture and food security?"])
        # datas.append(["How is climate change impacting global weather patterns?","student1","Climate change is significantly impacting global weather patterns, leading to a surge in extreme weather events. We observe more frequent and intense hurricanes, such as Hurricane Harvey in 2017, which caused widespread flooding and devastating impacts. Additionally, heatwaves are becoming more common, as seen in the European heatwave of 2019. These events are clear indicators of the changing climate. Agriculture is heavily affected, with altered precipitation patterns, shifting growing seasons, and increased pest pressure. These changes threaten food security globally, impacting crop yields and quality. To address this, individuals can contribute by adopting sustainable practices, such as reducing meat consumption, using energy-efficient appliances, and supporting renewable energy sources. These efforts collectively help reduce the overall carbon footprint and contribute to mitigating climate change.","What can individuals do to reduce their carbon footprint?"])
        # datas.append(["How is climate change impacting global weather patterns?","student2","Climate change is impacting global weather patterns, causing extreme weather events like hurricanes and heatwaves. These events have adverse effects on agriculture, affecting crop yields and food security. Individuals can help by reducing their carbon footprint through sustainable practices.","What are some specific examples of extreme weather events linked to climate change?"])
        # datas.append(["How is climate change impacting global weather patterns?","student2","Climate change is impacting global weather patterns, causing extreme weather events like hurricanes and heatwaves. These events have adverse effects on agriculture, affecting crop yields and food security. Individuals can help by reducing their carbon footprint through sustainable practices.","How do these changes affect agriculture and food security?"])
        # datas.append(["How is climate change impacting global weather patterns?","student2","Climate change is impacting global weather patterns, causing extreme weather events like hurricanes and heatwaves. These events have adverse effects on agriculture, affecting crop yields and food security. Individuals can help by reducing their carbon footprint through sustainable practices.","What can individuals do to reduce their carbon footprint?"])
        # datas.append(["How is climate change impacting global weather patterns?","student3","Climate change affects global weather patterns. Extreme weather events, like hurricanes and heatwaves, are becoming more common. This impacts agriculture and food security by affecting crop yields. Individuals can help by reducing their carbon footprint.","What are some specific examples of extreme weather events linked to climate change?"])
        # datas.append(["How is climate change impacting global weather patterns?","student3","Climate change affects global weather patterns. Extreme weather events, like hurricanes and heatwaves, are becoming more common. This impacts agriculture and food security by affecting crop yields. Individuals can help by reducing their carbon footprint.","How do these changes affect agriculture and food security?"])
        # datas.append(["How is climate change impacting global weather patterns?","student3","Climate change affects global weather patterns. Extreme weather events, like hurricanes and heatwaves, are becoming more common. This impacts agriculture and food security by affecting crop yields. Individuals can help by reducing their carbon footprint.","What can individuals do to reduce their carbon footprint?"])

        # datas.append(["What were the key factors that led to the fall of the Roman Empire?","student1","The fall of the Roman Empire can be attributed to a combination of factors. Economic struggles played a crucial role as the empire faced issues such as overreliance on slave labor, high taxation, and economic inequality. These challenges contributed to a decline in productivity and a weakened economic foundation. Simultaneously, military defeats, such as the sack of Rome by the Visigoths in 410 AD and the fall of the Western Roman Empire in 476 AD, further exacerbated Rome's vulnerabilities. The military setbacks not only drained resources but also exposed the empire to external threats. Drawing parallels with modern societies, one can observe echoes of economic mismanagement and military overextension in historical contexts, emphasizing the importance of addressing economic and military challenges for the stability of any society.","How did economic struggles contribute to the empire's decline?"])
        # datas.append(["What were the key factors that led to the fall of the Roman Empire?","student1","The fall of the Roman Empire can be attributed to a combination of factors. Economic struggles played a crucial role as the empire faced issues such as overreliance on slave labor, high taxation, and economic inequality. These challenges contributed to a decline in productivity and a weakened economic foundation. Simultaneously, military defeats, such as the sack of Rome by the Visigoths in 410 AD and the fall of the Western Roman Empire in 476 AD, further exacerbated Rome's vulnerabilities. The military setbacks not only drained resources but also exposed the empire to external threats. Drawing parallels with modern societies, one can observe echoes of economic mismanagement and military overextension in historical contexts, emphasizing the importance of addressing economic and military challenges for the stability of any society.","What role did military defeats play in weakening Rome?"])
        # datas.append(["What were the key factors that led to the fall of the Roman Empire?","student1","The fall of the Roman Empire can be attributed to a combination of factors. Economic struggles played a crucial role as the empire faced issues such as overreliance on slave labor, high taxation, and economic inequality. These challenges contributed to a decline in productivity and a weakened economic foundation. Simultaneously, military defeats, such as the sack of Rome by the Visigoths in 410 AD and the fall of the Western Roman Empire in 476 AD, further exacerbated Rome's vulnerabilities. The military setbacks not only drained resources but also exposed the empire to external threats. Drawing parallels with modern societies, one can observe echoes of economic mismanagement and military overextension in historical contexts, emphasizing the importance of addressing economic and military challenges for the stability of any society.","Can parallels be drawn between the fall of Rome and any modern societies?"])
        # datas.append(["What were the key factors that led to the fall of the Roman Empire?","student2","The fall of the Roman Empire was due to economic struggles and military defeats. Economic issues included reliance on slave labor and high taxes, which weakened the economy. Military defeats, like the sack of Rome, played a role in Rome's decline. Parallels can be drawn with modern societies facing economic challenges and military conflicts.","How did economic struggles contribute to the empire's decline?"])
        # datas.append(["What were the key factors that led to the fall of the Roman Empire?","student2","The fall of the Roman Empire was due to economic struggles and military defeats. Economic issues included reliance on slave labor and high taxes, which weakened the economy. Military defeats, like the sack of Rome, played a role in Rome's decline. Parallels can be drawn with modern societies facing economic challenges and military conflicts.","What role did military defeats play in weakening Rome?"])
        # datas.append(["What were the key factors that led to the fall of the Roman Empire?","student2","The fall of the Roman Empire was due to economic struggles and military defeats. Economic issues included reliance on slave labor and high taxes, which weakened the economy. Military defeats, like the sack of Rome, played a role in Rome's decline. Parallels can be drawn with modern societies facing economic challenges and military conflicts.","Can parallels be drawn between the fall of Rome and any modern societies?"])
        # datas.append(["What were the key factors that led to the fall of the Roman Empire?","student3","The Roman Empire fell because of economic struggles and military defeats. The economy faced problems like high taxes and dependence on slave labor. Military defeats weakened Rome. Modern societies can learn from Rome's mistakes in managing their economies and military engagements.","How did economic struggles contribute to the empire's decline?"])
        # datas.append(["What were the key factors that led to the fall of the Roman Empire?","student3","The Roman Empire fell because of economic struggles and military defeats. The economy faced problems like high taxes and dependence on slave labor. Military defeats weakened Rome. Modern societies can learn from Rome's mistakes in managing their economies and military engagements.","What role did military defeats play in weakening Rome?"])
        # datas.append(["What were the key factors that led to the fall of the Roman Empire?","student3","The Roman Empire fell because of economic struggles and military defeats. The economy faced problems like high taxes and dependence on slave labor. Military defeats weakened Rome. Modern societies can learn from Rome's mistakes in managing their economies and military engagements.","Can parallels be drawn between the fall of Rome and any modern societies?"])

        # datas.append(["How do Shakespeare's plays reflect the society of his time?","student1","Shakespeare's plays serve as a mirror to the society of his time, subtly addressing prevalent social norms and political issues. In 'Hamlet', the themes of power, betrayal, and political corruption are evident, reflecting the political climate of the Elizabethan era. 'Macbeth', on the other hand, delves into the consequences of unchecked ambition and the fragile nature of political stability. Shakespeare's language, characterized by its richness and versatility, amplifies these themes, adding depth and nuance to the exploration of societal issues. The universal human experiences and moral dilemmas depicted in his plays make them timeless, ensuring their continued relevance in contemporary society. The intricate interplay of language and societal reflections in Shakespeare's works cements their enduring impact on audiences across different eras.","Which social norms or political issues are evident in plays like 'Hamlet' or 'Macbeth'?"])
        # datas.append(["How do Shakespeare's plays reflect the society of his time?","student1","Shakespeare's plays serve as a mirror to the society of his time, subtly addressing prevalent social norms and political issues. In 'Hamlet', the themes of power, betrayal, and political corruption are evident, reflecting the political climate of the Elizabethan era. 'Macbeth', on the other hand, delves into the consequences of unchecked ambition and the fragile nature of political stability. Shakespeare's language, characterized by its richness and versatility, amplifies these themes, adding depth and nuance to the exploration of societal issues. The universal human experiences and moral dilemmas depicted in his plays make them timeless, ensuring their continued relevance in contemporary society. The intricate interplay of language and societal reflections in Shakespeare's works cements their enduring impact on audiences across different eras.","How does Shakespeare's use of language contribute to the themes in his plays?"])
        # datas.append(["How do Shakespeare's plays reflect the society of his time?","student1","Shakespeare's plays serve as a mirror to the society of his time, subtly addressing prevalent social norms and political issues. In 'Hamlet', the themes of power, betrayal, and political corruption are evident, reflecting the political climate of the Elizabethan era. 'Macbeth', on the other hand, delves into the consequences of unchecked ambition and the fragile nature of political stability. Shakespeare's language, characterized by its richness and versatility, amplifies these themes, adding depth and nuance to the exploration of societal issues. The universal human experiences and moral dilemmas depicted in his plays make them timeless, ensuring their continued relevance in contemporary society. The intricate interplay of language and societal reflections in Shakespeare's works cements their enduring impact on audiences across different eras.","Are there any ways in which these plays are still relevant today?"])
        # datas.append(["How do Shakespeare's plays reflect the society of his time?","student2","Shakespeare's plays like 'Hamlet' and 'Macbeth' reflect the social norms and political issues of his time. In 'Hamlet', there are themes of power and betrayal, and in 'Macbeth', there's a focus on ambition and political instability. Shakespeare's language is complex and contributes to the themes in his plays. These plays are still relevant today because they explore universal human experiences.","Which social norms or political issues are evident in plays like 'Hamlet' or 'Macbeth'?"])
        # datas.append(["How do Shakespeare's plays reflect the society of his time?","student2","Shakespeare's plays like 'Hamlet' and 'Macbeth' reflect the social norms and political issues of his time. In 'Hamlet', there are themes of power and betrayal, and in 'Macbeth', there's a focus on ambition and political instability. Shakespeare's language is complex and contributes to the themes in his plays. These plays are still relevant today because they explore universal human experiences.","How does Shakespeare's use of language contribute to the themes in his plays?"])
        # datas.append(["How do Shakespeare's plays reflect the society of his time?","student2","Shakespeare's plays like 'Hamlet' and 'Macbeth' reflect the social norms and political issues of his time. In 'Hamlet', there are themes of power and betrayal, and in 'Macbeth', there's a focus on ambition and political instability. Shakespeare's language is complex and contributes to the themes in his plays. These plays are still relevant today because they explore universal human experiences.","Are there any ways in which these plays are still relevant today?"])
        # datas.append(["How do Shakespeare's plays reflect the society of his time?","student3","Shakespeare's plays show things about the society back then. In 'Hamlet' and 'Macbeth', you can see social norms and political stuff. The language he uses is old-fashioned, and it talks about power and betrayal. Some things in the plays are kind of like what we have today.","Which social norms or political issues are evident in plays like 'Hamlet' or 'Macbeth'?"])
        # datas.append(["How do Shakespeare's plays reflect the society of his time?","student3","Shakespeare's plays show things about the society back then. In 'Hamlet' and 'Macbeth', you can see social norms and political stuff. The language he uses is old-fashioned, and it talks about power and betrayal. Some things in the plays are kind of like what we have today.","How does Shakespeare's use of language contribute to the themes in his plays?"])
        # datas.append(["How do Shakespeare's plays reflect the society of his time?","student3","Shakespeare's plays show things about the society back then. In 'Hamlet' and 'Macbeth', you can see social norms and political stuff. The language he uses is old-fashioned, and it talks about power and betrayal. Some things in the plays are kind of like what we have today.","Are there any ways in which these plays are still relevant today?"])

        # datas.append(["What is the potential impact of artificial intelligence on the future of work?","student1","The potential impact of artificial intelligence on the future of work is profound and varied across industries. AI is poised to transform the nature of jobs by automating routine tasks, allowing for increased efficiency and productivity. However, this could lead to job displacement in certain sectors, necessitating a shift in skill requirements towards tasks that are less susceptible to automation, such as those involving creativity, critical thinking, and emotional intelligence. The ethical considerations of deploying AI in the workplace are crucial, including issues related to privacy, bias, and accountability. Preparing for a workforce integrated with AI involves investing in education and training programs to develop the skills needed for collaboration with AI systems, fostering a balance between human and machine capabilities.","How might AI change the nature of jobs in different industries?"])
        # datas.append(["What is the potential impact of artificial intelligence on the future of work?","student1","The potential impact of artificial intelligence on the future of work is profound and varied across industries. AI is poised to transform the nature of jobs by automating routine tasks, allowing for increased efficiency and productivity. However, this could lead to job displacement in certain sectors, necessitating a shift in skill requirements towards tasks that are less susceptible to automation, such as those involving creativity, critical thinking, and emotional intelligence. The ethical considerations of deploying AI in the workplace are crucial, including issues related to privacy, bias, and accountability. Preparing for a workforce integrated with AI involves investing in education and training programs to develop the skills needed for collaboration with AI systems, fostering a balance between human and machine capabilities.","What are the ethical considerations in deploying AI in the workplace?"])
        # datas.append(["What is the potential impact of artificial intelligence on the future of work?","student1","The potential impact of artificial intelligence on the future of work is profound and varied across industries. AI is poised to transform the nature of jobs by automating routine tasks, allowing for increased efficiency and productivity. However, this could lead to job displacement in certain sectors, necessitating a shift in skill requirements towards tasks that are less susceptible to automation, such as those involving creativity, critical thinking, and emotional intelligence. The ethical considerations of deploying AI in the workplace are crucial, including issues related to privacy, bias, and accountability. Preparing for a workforce integrated with AI involves investing in education and training programs to develop the skills needed for collaboration with AI systems, fostering a balance between human and machine capabilities.","How can we prepare for a workforce increasingly integrated with AI?"])
        # datas.append(["What is the potential impact of artificial intelligence on the future of work?","student2","Artificial intelligence will impact the future of work by changing the nature of jobs in various industries. It may automate some tasks, leading to increased efficiency. However, this could result in job displacement. Ethical considerations in using AI at work include privacy and bias issues. To prepare for an AI-integrated workforce, there needs to be investment in education and training.","How might AI change the nature of jobs in different industries?"])
        # datas.append(["What is the potential impact of artificial intelligence on the future of work?","student2","Artificial intelligence will impact the future of work by changing the nature of jobs in various industries. It may automate some tasks, leading to increased efficiency. However, this could result in job displacement. Ethical considerations in using AI at work include privacy and bias issues. To prepare for an AI-integrated workforce, there needs to be investment in education and training.","What are the ethical considerations in deploying AI in the workplace?"])
        # datas.append(["What is the potential impact of artificial intelligence on the future of work?","student2","Artificial intelligence will impact the future of work by changing the nature of jobs in various industries. It may automate some tasks, leading to increased efficiency. However, this could result in job displacement. Ethical considerations in using AI at work include privacy and bias issues. To prepare for an AI-integrated workforce, there needs to be investment in education and training.","How can we prepare for a workforce increasingly integrated with AI?"])
        # datas.append(["What is the potential impact of artificial intelligence on the future of work?","student3","AI will impact jobs in the future. It might change things in different industries. There are some ethical considerations with using AI at work. We need to prepare for AI in the workforce.","How might AI change the nature of jobs in different industries?"])
        # datas.append(["What is the potential impact of artificial intelligence on the future of work?","student3","AI will impact jobs in the future. It might change things in different industries. There are some ethical considerations with using AI at work. We need to prepare for AI in the workforce.","What are the ethical considerations in deploying AI in the workplace?"])
        # datas.append(["What is the potential impact of artificial intelligence on the future of work?","student3","AI will impact jobs in the future. It might change things in different industries. There are some ethical considerations with using AI at work. We need to prepare for AI in the workforce.","How can we prepare for a workforce increasingly integrated with AI?"])

        # datas.append(["How has modern technology influenced the evolution of visual arts?","student1","Modern technology has significantly shaped the evolution of visual arts, with artists creatively incorporating various technologies into their work. For instance, augmented reality (AR) and virtual reality (VR) have been employed to create immersive art experiences, pushing the boundaries of traditional artistic expression. Digital platforms have transformed the distribution and consumption of art, enabling artists to showcase their work globally and fostering new forms of collaboration. This shift has democratized access to art, allowing a wider audience to engage with diverse artistic perspectives. For future artists, this presents both opportunities and challenges as they navigate the digital landscape. Art enthusiasts benefit from increased accessibility but may also face information overload, emphasizing the importance of curation and critical engagement in the digital art realm.","What are some examples of technology being used creatively in recent art?"])
        # datas.append(["How has modern technology influenced the evolution of visual arts?","student1","Modern technology has significantly shaped the evolution of visual arts, with artists creatively incorporating various technologies into their work. For instance, augmented reality (AR) and virtual reality (VR) have been employed to create immersive art experiences, pushing the boundaries of traditional artistic expression. Digital platforms have transformed the distribution and consumption of art, enabling artists to showcase their work globally and fostering new forms of collaboration. This shift has democratized access to art, allowing a wider audience to engage with diverse artistic perspectives. For future artists, this presents both opportunities and challenges as they navigate the digital landscape. Art enthusiasts benefit from increased accessibility but may also face information overload, emphasizing the importance of curation and critical engagement in the digital art realm.","How do digital platforms affect the way art is distributed and consumed?"])
        # datas.append(["How has modern technology influenced the evolution of visual arts?","student1","Modern technology has significantly shaped the evolution of visual arts, with artists creatively incorporating various technologies into their work. For instance, augmented reality (AR) and virtual reality (VR) have been employed to create immersive art experiences, pushing the boundaries of traditional artistic expression. Digital platforms have transformed the distribution and consumption of art, enabling artists to showcase their work globally and fostering new forms of collaboration. This shift has democratized access to art, allowing a wider audience to engage with diverse artistic perspectives. For future artists, this presents both opportunities and challenges as they navigate the digital landscape. Art enthusiasts benefit from increased accessibility but may also face information overload, emphasizing the importance of curation and critical engagement in the digital art realm.","What implications does this have for future artists and art enthusiasts?"])
        # datas.append(["How has modern technology influenced the evolution of visual arts?","student2","Modern technology has influenced the evolution of visual arts. Artists use technology creatively in recent art, like augmented reality and virtual reality. Digital platforms change how art is distributed and consumed. This has implications for future artists and art enthusiasts.","What are some examples of technology being used creatively in recent art?"])
        # datas.append(["How has modern technology influenced the evolution of visual arts?","student2","Modern technology has influenced the evolution of visual arts. Artists use technology creatively in recent art, like augmented reality and virtual reality. Digital platforms change how art is distributed and consumed. This has implications for future artists and art enthusiasts.","How do digital platforms affect the way art is distributed and consumed?"])
        # datas.append(["How has modern technology influenced the evolution of visual arts?","student2","Modern technology has influenced the evolution of visual arts. Artists use technology creatively in recent art, like augmented reality and virtual reality. Digital platforms change how art is distributed and consumed. This has implications for future artists and art enthusiasts.","What implications does this have for future artists and art enthusiasts?"])
        # datas.append(["How has modern technology influenced the evolution of visual arts?","student3","Technology has impacted visual arts. Artists use things like augmented reality and virtual reality in recent art. Digital platforms change how art is distributed and consumed. Future artists and art enthusiasts will be affected.","What are some examples of technology being used creatively in recent art?"])
        # datas.append(["How has modern technology influenced the evolution of visual arts?","student3","Technology has impacted visual arts. Artists use things like augmented reality and virtual reality in recent art. Digital platforms change how art is distributed and consumed. Future artists and art enthusiasts will be affected.","How do digital platforms affect the way art is distributed and consumed?"])
        # datas.append(["How has modern technology influenced the evolution of visual arts?","student3","Technology has impacted visual arts. Artists use things like augmented reality and virtual reality in recent art. Digital platforms change how art is distributed and consumed. Future artists and art enthusiasts will be affected.","What implications does this have for future artists and art enthusiasts?"])

        # datas.append(["What factors contribute to the formation of cultural identity?","student1","The formation of cultural identity is influenced by various factors, and language and tradition are integral components in this process. Language serves as a vessel for cultural expression, shaping collective identity and fostering a sense of belonging. Tradition, encompassing customs, rituals, and artistic expressions, further solidifies cultural identity, providing a link to the past and a framework for social cohesion. Globalization has a dual impact on local cultures – while it introduces external influences and facilitates cultural exchange, it can also lead to the erosion of distinct local practices. Immigrant communities often navigate a delicate balance between integrating into their adopted societies and preserving their original culture. This involves adapting to new environments while maintaining language, traditions, and values, contributing to the rich tapestry of multicultural societies.","How do language and tradition play a role in shaping cultural identity?"])
        # datas.append(["What factors contribute to the formation of cultural identity?","student1","The formation of cultural identity is influenced by various factors, and language and tradition are integral components in this process. Language serves as a vessel for cultural expression, shaping collective identity and fostering a sense of belonging. Tradition, encompassing customs, rituals, and artistic expressions, further solidifies cultural identity, providing a link to the past and a framework for social cohesion. Globalization has a dual impact on local cultures – while it introduces external influences and facilitates cultural exchange, it can also lead to the erosion of distinct local practices. Immigrant communities often navigate a delicate balance between integrating into their adopted societies and preserving their original culture. This involves adapting to new environments while maintaining language, traditions, and values, contributing to the rich tapestry of multicultural societies.","What is the impact of globalization on local cultures?"])
        # datas.append(["What factors contribute to the formation of cultural identity?","student1","The formation of cultural identity is influenced by various factors, and language and tradition are integral components in this process. Language serves as a vessel for cultural expression, shaping collective identity and fostering a sense of belonging. Tradition, encompassing customs, rituals, and artistic expressions, further solidifies cultural identity, providing a link to the past and a framework for social cohesion. Globalization has a dual impact on local cultures – while it introduces external influences and facilitates cultural exchange, it can also lead to the erosion of distinct local practices. Immigrant communities often navigate a delicate balance between integrating into their adopted societies and preserving their original culture. This involves adapting to new environments while maintaining language, traditions, and values, contributing to the rich tapestry of multicultural societies.","How do immigrant communities balance integration and preservation of their original culture?"])
        # datas.append(["What factors contribute to the formation of cultural identity?","student2","Factors contributing to cultural identity include language, tradition, and the impact of globalization. Language and tradition play a role in shaping cultural identity, while globalization affects local cultures. Immigrant communities balance integration and preservation of their original culture.","How do language and tradition play a role in shaping cultural identity?"])
        # datas.append(["What factors contribute to the formation of cultural identity?","student2","Factors contributing to cultural identity include language, tradition, and the impact of globalization. Language and tradition play a role in shaping cultural identity, while globalization affects local cultures. Immigrant communities balance integration and preservation of their original culture.","What is the impact of globalization on local cultures?"])
        # datas.append(["What factors contribute to the formation of cultural identity?","student2","Factors contributing to cultural identity include language, tradition, and the impact of globalization. Language and tradition play a role in shaping cultural identity, while globalization affects local cultures. Immigrant communities balance integration and preservation of their original culture.","How do immigrant communities balance integration and preservation of their original culture?"])
        # datas.append(["What factors contribute to the formation of cultural identity?","student3","Cultural identity is formed by factors like language, tradition, and globalization. Language and tradition shape cultural identity. Globalization impacts local cultures. Immigrant communities balance integration and preservation of their original culture.","How do language and tradition play a role in shaping cultural identity?"])
        # datas.append(["What factors contribute to the formation of cultural identity?","student3","Cultural identity is formed by factors like language, tradition, and globalization. Language and tradition shape cultural identity. Globalization impacts local cultures. Immigrant communities balance integration and preservation of their original culture.","What is the impact of globalization on local cultures?"])
        # datas.append(["What factors contribute to the formation of cultural identity?","student3","Cultural identity is formed by factors like language, tradition, and globalization. Language and tradition shape cultural identity. Globalization impacts local cultures. Immigrant communities balance integration and preservation of their original culture.","How do immigrant communities balance integration and preservation of their original culture?"])
        
        # for each in datas:
        #     q = each[0]
        #     n = each[1]
        #     a = each[2]
        #     r = each[3]
        #     self.insert_values_into_database(q,n,a,r)
        
        self.round_instance.cursor.close()
        self.round_instance.conn.close()
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
        
    def insert_values_into_database(self, question, name, answer,rubric):
        self.round_instance.simplified_insert("answers", {
            "name": name,
            "question": question,
            "answer": answer,
            "rubric": rubric
        })
        self.round_instance.simplified_insert("exam", {
            "question": question,
            "rubric": rubric
        })

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

        user_details = ctk.CTkLabel(self.top_frame, text="Teacher Name\nProofs Teacher", font=self.default_font, text_color=self.text_color, anchor='e')
        user_details.pack(side='right', padx=10, pady=10)
        
    def create_main_frame(self):
        self.main_frame = ctk.CTkFrame(self.base_frame, corner_radius=10, fg_color='#C6BFD9')
        self.main_frame.pack(fill='both', expand=True, padx=0, pady=0)

    def create_rubrics_menu(self):
        self.side_menu = ctk.CTkFrame(self.main_frame, corner_radius=10, fg_color='white', border_color='grey', border_width=2, width=200)
        self.side_menu.pack(side='left', fill='y',padx=10, pady=10)
        self.rubric_title = ctk.CTkLabel(self.side_menu, text="Rubrics", font=("Segoe UI", 20, "bold"), text_color=self.primary_color)
        self.rubric_title.pack(padx=10, pady=(10, 5))
        self.rubric_frame = ctk.CTkFrame(self.side_menu, corner_radius=10, fg_color='white', border_color='grey', border_width=1, width=200)
        self.rubric_frame.pack(fill='x', padx=10, pady=10)

    def create_label_menu(self):
        label_menu_width = 200  
        
        self.label_menu = ctk.CTkFrame(self.main_frame, corner_radius=10, fg_color='white', border_color='grey', border_width=2, width=label_menu_width)
        self.label_menu.pack(side='right', fill='both', padx=10, pady=10)
        
        self.label_title = ctk.CTkLabel(self.label_menu, text="Labels", font=("Segoe UI", 20, "bold"), text_color=self.primary_color)
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

        self.bold_text = ctk.CTkLabel(self.box_frame_left, font=("Segoe UI", 12, "bold"), text_color=self.text_color, anchor='w')
        self.bold_text.pack(padx=10, pady=10, anchor='nw')

        self.large_color_text = ctk.CTkLabel(self.box_frame_left, text_color=self.text_color, font=("Segoe UI", 20, "bold"))
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
            button = ctk.CTkButton(self.question_frame, text=f"Q{i}", fg_color=fg_color, width=button_width, height=button_height, command=lambda i=i: self.question_button_action(i-1))
            self.question_buttons.append(button)

    def question_button_action(self, question_index):
        self.current_question_index = question_index
        selected_question = self.questions[question_index]

        self.bold_text.configure(text=f"Question {question_index + 1}")
        self.large_color_text.configure(text=selected_question)

        existing_labels = self.round_instance.getLabels(selected_question)
        print(existing_labels)
        if not existing_labels:
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
        student_answer = self.get_student_answer(student_index, self.questions[self.current_question_index])
        self.highlight_insertion()
        corrected_answer = self.corrector.handle_student_asnwer(student_answer)
        self.display_student_answer(student_answer, corrected_answer)
        self.display_rubrics_with_confidence(student_answer)

            
#################### End Question Buttons ####################
#################### Rubrics and Labels ######################

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

            rubric_label = ctk.CTkLabel(self.rubric_frame, text=rubric, width=200, wraplength=200, font=("Segoe UI", 11, "bold"))
            rubric_label.grid(row=index, column=1, sticky="w", padx=(5, 5), pady=5)
            rubric_label.bind("<Button-1>", lambda event, r=rubric, l=rubric_label: self.on_rubric_label_click(r, student_answer, l))

    def highlight_label(self, label):
        if self.highlighted_label is not None:
            self.highlighted_label.configure(fg_color="white")

        # Highlight the new label
        label.configure(fg_color="#FFD700")
        self.highlighted_label = label

    def on_rubric_label_click(self, rubric, student_answer, label):
        self.answer_text.tag_remove("highlight", "1.0", "end")
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

        self.highlight_label(label)



    def highlight_text(self, start_index, end_index):
        self.answer_text.tag_config("highlight", background=self.highlight_color, foreground="black")
        self.answer_text.tag_add("highlight", f"1.{start_index}", f"1.{end_index}")

    
    def highlight_insertion(self):
        rubrics = self.round_instance.getRubrics(self.questions[self.current_question_index])
        for rubric in rubrics:
            rubric_text = rubric[0]
            student_answer = self.get_student_answer(self.current_student_index, self.questions[self.current_question_index])
            print(f"Checking highlights for '{rubric_text}' in '{student_answer}'")

            existing_highlights = self.round_instance.checkHighlightsExist(rubric_text, student_answer)
            if existing_highlights:
                print(f"Highlights for '{rubric_text}' already exist in the database.")
            else:
                print(f"No highlights found for '{rubric_text}'. Running model.")
                print(f"Running model for '{rubric_text}' in '{student_answer}'")
                try:
                    indices, confidence_model = self.bot.run_model(student_answer, rubric_text)
                except:
                    indices, confidence_model = self.bot.run_model(student_answer, rubric_text)
                print(f"Model results for '{rubric_text}': {indices}, {confidence_model}")
                    
                for index_pairs in indices:
                    self.round_instance.insertHighlights(rubric_text, student_answer, index_pairs[0], index_pairs[1], confidence_model)
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
        unique_students = [data[0] for data in student_data]
        return unique_students
    
    def display_student_answer(self, answer, corrected_answer, start_index=None, end_index=None):
        self.switch_to_answer_frame()
        self.answer_text.delete("1.0", "end")
        self.answer_text.insert("1.0", answer)
        self.correction_text.delete("1.0", "end")
        self.correction_text.insert("1.0", corrected_answer)
        if start_index is not None and end_index is not None:
            self.highlight_text(start_index, end_index)
            


    def create_answer_frame(self):
        if not hasattr(self, 'answer_frame'):
            self.answer_frame = ctk.CTkFrame(self.top_content_frame, corner_radius=10, fg_color='white', border_color='grey', border_width=1)
            self.answer_frame.pack(side='top', fill='both', expand=True, padx=10, pady=10)
            
            self.answer_label = ctk.CTkLabel(self.answer_frame, text="Student Answer", font=("Segoe UI", 20, "bold"),
                                                text_color=self.primary_color)
            self.answer_label.pack(padx=10, pady=(10, 5))

            self.answer_text = Text(self.answer_frame, font=("Segoe UI", 11), wrap="word", height=10, bg='#FFFFFF')
            self.answer_text.pack(padx=10, pady=(10, 5))
            
            self.correction_frame = ctk.CTkFrame(self.top_content_frame, corner_radius=10, fg_color='white', border_color='grey', border_width=1)
            self.correction_frame.pack(side='bottom', fill='both', expand=True, padx=10, pady=10)

            self.correction_label = ctk.CTkLabel(self.correction_frame, text="Corrected: Spelling, Grammar", font=("Segoe UI", 20, "bold"), 
                                                text_color=self.primary_color)
            self.correction_label.pack(padx=10, pady=(10, 5))
            
            self.correction_text = Text(self.correction_frame, font=("Segoe UI", 11), wrap="word", height=10, bg='#FFFFFF')
            self.correction_text.pack(padx=10, pady=(10, 5))

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
        print("Fetching questions")
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
            rubric_text = rubric[0]
            rubric_label = ctk.CTkLabel(self.rubric_frame, text=rubric_text, width=200, wraplength=200, font=("Segoe UI", 11, "bold"))
            rubric_label.pack(padx=(5, 5), pady=5)


    def load_and_display_labels(self, question_index):
        labels = self.round_instance.getLabels(self.questions[question_index])
        for widget in self.label_frame.winfo_children():
            widget.destroy()
        for label_tuple in labels:
            label = label_tuple[0]
            label_label = ctk.CTkLabel(self.label_frame, text=label, width=200, font=("Segoe UI", 11, "bold"))
            label_label.pack()

            
    def get_all_student_names(self):
        return self.round_instance.getAllStudentNames()

    def get_student_answer(self, student_index, question):
        all_student_names = self.get_all_student_names()
        if student_index < len(all_student_names):
            student_name = all_student_names[student_index]
            answer = self.round_instance.getStudentAnswer(student_name, question)
            return answer if answer else "No answer found"
        else:
            return "Invalid student index"

        

def main():
    app = ExamAIApp()
    app.mainloop()

if __name__ == "__main__":
    main()