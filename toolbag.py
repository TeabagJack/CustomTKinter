from bertModel import bertModel
import torch
import csv
import labeling_model as lm
from transformers import pipeline
import pickle, os
import mysql.connector


class roundUsing:
    def __init__(self,password, label_threshhold = 0.6,host = "localhost",user = "root"):
        # self.hashmap = {}
        self.password = password
        self.host = host
        self.user = user
        self.database = "exam1"
        self.label_threshold = label_threshhold
        self.list = read_labelPredictionForm("data\label_prediction_dataset.csv")
        self.bert = bertModel()
        self.conn = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password
        )
        self.cursor = self.conn.cursor()
        
        
    def getAllStudentNames(self):
        self.conn = self.connect_to_db()
        self.changeDatabase("exam1")
        if self.conn is None:
            return []
        self.cursor = self.conn.cursor()

        query = "SELECT DISTINCT name FROM answers"
        self.cursor.execute(query)
        names = self.cursor.fetchall()

        self.cursor.close()
        self.conn.close()
        return [name[0] for name in names]
    
    def initialize_database(self):
        self.createDB(self.database)
        self.changeDatabase(self.database)
        self.create_tables()
        
    def create_tables(self):
        table_schemas = {
            "answers": ["name VARCHAR(50)", "question LONGTEXT", "answer LONGTEXT"],
            "exam": ["question LONGTEXT", "rubric TEXT"],
            "tag": ["question LONGTEXT", "label VARCHAR(50)"],
            "account": ["name VARCHAR(50)", "accountName VARCHAR(50)", "password VARCHAR(50)"],
            "highlights": ["rubric TEXT", "answer LONGTEXT", "startIndex INTEGER", "endIndex INTEGER", "confidence FLOAT"]
        }
        
        for table_name, columns in table_schemas.items():
            self.createTable(table_name, columns)
            
    
    def createTable(self, tableName, columns):
        column_definitions = ", ".join(columns)
        self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {tableName} ({column_definitions});")
        
    def simplified_insert(self, table_name, data):
        self.connect_to_db()
        self.cursor = self.conn.cursor()
        self.cursor.execute("USE exam1;")  # Explicitly select the database

        # Construct and execute the insert query
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['%s'] * len(data))
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        self.cursor.execute(query, list(data.values()))
        self.conn.commit()
        self.cursor.close()
        self.conn.close()
        
    def execute_query(self, query, values=None):
        try:
            self.connect_to_db()
            self.cursor = self.conn.cursor()

            if values:
                self.cursor.execute(query, values)
            else:
                self.cursor.execute(query)

            self.conn.commit()
        except mysql.connector.Error as err:
            print(f"Error occurred: {err}")
        finally:
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()
        
        
    
    def connect_to_db(self):
        if self.conn is None or not self.conn.is_connected():
            try:
                self.conn = mysql.connector.connect(
                    host=self.host,
                    user=self.user,
                    password=self.password
                )
            except mysql.connector.Error as err:
                print(f"Error connecting to MySQL: {err}")
        return self.conn
    
    def close_connection(self):
        if self.conn is not None and self.conn.is_connected():
            self.conn.close()
            self.conn = None
    
    def createDB(self, databaseName):
        # conn = self.connect_to_db()
        if self.conn is None:
            return
        cursor = self.conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {databaseName};")
        # cursor.close()
        # conn.close()

    def dropDB(self,databaseName):
        self.cursor.execute(f"DROP DATABASE IF EXISTS {databaseName};")

    def changeDatabase(self, databaseName):
        # conn = self.connect_to_db()
        # if self.conn is None:
        #     return
        cursor = self.conn.cursor()
        cursor.execute(f"USE {databaseName};")
        # cursor.close()
        # conn.close()

    def convertListToString(self, colDTList):
        cols = colDTList[0]
        dts1 = colDTList[1]
        dts  = []
        for each in dts1:
            each = each.replace("'", "''")
            each = f"'{each}'"
            dts.append(each)
        columns = ",".join(cols)
        datas = ",".join(dts)
        return columns,datas

    # def createTable(self, tableName, colDTList):
    #     # conn = self.connect_to_db()
    #     # if conn is None:
    #     #     return
    #     # cursor = conn.cursor()

    #     colDT = []
    #     for element1, element2 in zip(colDTList[0], colDTList[1]):
    #         newlist = f"{element1} {element2}"
    #         colDT.append(newlist)
    #     colDT = ", ".join(colDT)
    #     self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {tableName} ({colDT});")

    #     # cursor.close()
    #     # conn.close()
    
    def dropTable(self,tableName):
        self.cursor.execute(f"DROP TABLE IF EXISTS {tableName};")

    def insertData(self, tableName, colDTList):
        self.conn = self.connect_to_db()
        self.changeDatabase("exam1")
        if self.conn is None:
            return
        self.cursor = self.conn.cursor()

        columns, datas = self.convertListToString(colDTList)
        self.cursor.execute(f"INSERT INTO {tableName} ({columns}) VALUES ({datas});")
        self.conn.commit()
        self.cursor.close()
        self.conn.close()

    def queryGenerate(self,tableName,columns,distinct = "",condition=""):
        if condition != "":
            condition = f"WHERE {condition}"
        queryString = f"SELECT {distinct} {columns} FROM {tableName} {condition};"
        return queryString

    def unionQuery(self,queryString1,queryString2):
        unionQuery = f"{queryString1} UNION {queryString2}"
        return unionQuery

    def queryExecutor(self, queryString, order_column="", ASC="ASC", limit=""):
        self.conn = self.connect_to_db()
        self.changeDatabase("exam1")
        if self.conn is None:
            return None

        try:
            self.cursor = self.conn.cursor()
            if order_column:
                queryString += f" ORDER BY {order_column} {ASC}"
            if limit:
                queryString += f" LIMIT {limit}"

            self.cursor.execute(queryString)
            tables = self.cursor.fetchall()
            self.cursor.close()
            self.conn.close()
            return tables

        except mysql.connector.Error as err:
            print(f"Error occurred during query execution: {err}")
            return None

    def getStudentAnswer(self, studentName):
        self.conn = self.connect_to_db()
        self.changeDatabase("exam1")
        if self.conn is None:
            return None
        self.cursor = self.conn.cursor()

        query = self.queryGenerate("answers", "question,answer", "DISTINCT", condition=f"name = '{studentName}'")
        self.cursor.execute(query)
        table = self.cursor.fetchall()

        self.cursor.close()
        self.conn.close()
        return table

    def getQuestionLabel(self, question):
        self.conn = self.connect_to_db()
        self.changeDatabase("exam1")
        if self.conn is None:
            return None
        self.cursor = self.conn.cursor()

        query = self.queryGenerate("Tag", "label", condition=f"question = '{question}'")
        self.cursor.execute(query)
        table = self.cursor.fetchall()

        self.cursor.close()
        self.conn.close()
        return table
    
    def updateData(self, tableName, colDTList, condition=""):
        self.conn = self.connect_to_db()
        self.changeDatabase("exam1")
        if self.conn is None:
            return None
        self.cursor = self.conn.cursor()

        if condition != "":
            condition = f"WHERE {condition}"
        columns, datas = self.convertListToString(colDTList)
        self.cursor.execute(f"UPDATE {tableName} SET {columns} = {datas} {condition};")

        self.cursor.close()
        self.conn.close()
        
    def update_labels(db_connection, question, labels):
        cursor = db_connection.cursor()

        try:
            for label in labels:
                query = "UPDATE tag SET label = %s WHERE question = %s AND label IS NULL"
                cursor.execute(query, (label, question))
            db_connection.commit()
            print(f"Labels updated for question: '{question}'")
        except mysql.connector.Error as err:
            print(f"Error occurred: {err}")
        finally:
            cursor.close()

    def deleteData(self, tableName, condition):
        self.conn = self.connect_to_db()
        self.changeDatabase("exam1")
        if self.conn is None:
            return None
        self.cursor = self.conn.cursor()

        self.cursor.execute(f"DELETE FROM {tableName} WHERE {condition};")

        self.cursor.close()
        self.conn.close()
        
    def getRubrics(self, question):
        self.conn = self.connect_to_db()
        self.changeDatabase("exam1")
        if self.conn is None:
            return None
        self.cursor = self.conn.cursor()

        query = self.queryGenerate("exam", "rubric", condition=f"question = '{question}'")
        self.cursor.execute(query)
        table = self.cursor.fetchall()

        self.cursor.close()
        self.conn.close()
        return table
    
    def getquestions(self):
        self.conn = self.connect_to_db()
        self.changeDatabase("exam1")
        if self.conn is None:
            return None
        self.cursor = self.conn.cursor()

        query = self.queryGenerate("exam", "question", distinct="DISTINCT")
        self.cursor.execute(query)
        table = self.cursor.fetchall()

        self.cursor.close()
        self.conn.close()
        return table
    
    def getLabels(self, question):
        self.conn = self.connect_to_db()
        self.changeDatabase("exam1")
        if self.conn is None:
            return None
        self.cursor = self.conn.cursor()

        query = self.queryGenerate("tag", "label", condition=f"question = '{question}'")
        self.cursor.execute(query)
        table = self.cursor.fetchall()

        self.cursor.close()
        self.conn.close()
        return table

    def getAnswers(self, studentName):
        self.conn = self.connect_to_db()
        self.changeDatabase("exam1")
        if self.conn is None:
            return None
        self.cursor = self.conn.cursor()

        col = ["question", "answer"]
        query = self.queryGenerate("answers", col, condition=f"name = '{studentName}'")
        self.cursor.execute(query)
        table = self.cursor.fetchall()

        self.cursor.close()
        self.conn.close()
        return table
    
    
    def getHighlightsForAnswer(self, answer):
        self.conn = self.connect_to_db()
        self.changeDatabase("exam1")
        if self.conn is None:
            return None
        self.cursor = self.conn.cursor()

        try:
            query = """
                SELECT rubric, AVG(confidence) as avg_confidence
                FROM highlights
                WHERE answer = %s
                GROUP BY rubric
            """
            self.cursor.execute(query, (answer,))
            rubrics_with_confidence = self.cursor.fetchall()
            return rubrics_with_confidence
        except mysql.connector.Error as err:
            print(f"Error occurred during query execution: {err}")
            return []
        finally:
            self.cursor.close()
            self.conn.close()

    
    def getHighlights(self, rubric, answer):
        self.conn = self.connect_to_db()
        self.changeDatabase("exam1")
        if self.conn is None:
            return None
        self.cursor = self.conn.cursor()

        query = "SELECT startIndex, endIndex, confidence FROM highlights WHERE rubric = %s AND answer = %s"
        self.cursor.execute(query, (rubric, answer))
        table = self.cursor.fetchall()

        self.cursor.close()
        self.conn.close()
        return table
    
    def insertHighlights(self, rubric, answer, startIndex, endIndex, confidence):
        self.conn = self.connect_to_db()
        self.changeDatabase("exam1")
        if self.conn is None:
            return None
        self.cursor = self.conn.cursor()
        
        try:
            query = "INSERT INTO highlights (rubric, answer, startIndex, endIndex, confidence) VALUES (%s, %s, %s, %s, %s)"
            data = (rubric, answer, startIndex, endIndex, confidence)
            self.cursor.execute(query, data)
            self.conn.commit()

        except mysql.connector.Error as err:
            print(f"Error occurred during insert operation: {err}")

        finally:
            self.cursor.close()
            self.conn.close()

    def insertLabels(self, question, labels):
        self.conn = self.connect_to_db()
        self.changeDatabase("exam1")
        if self.conn is None:
            return
        self.cursor = self.conn.cursor()

        for label in labels:
            label = f"'{label}'"
            col = ["question", "label"]
            data = [f"'{question}'", label]
            colDT = [col, data]
            columns, datas = self.convertListToString(colDT)
            self.cursor.execute(f"INSERT INTO tag ({columns}) VALUES ({datas});")
        self.conn.commit()
        self.cursor.close()
        self.conn.close()

        
    def getUniqueStudentsForQuestion(self, question):
        self.conn = self.connect_to_db()
        self.changeDatabase("exam1")
        if self.conn is None:
            return None
        self.cursor = self.conn.cursor()

        try:
            query = self.queryGenerate("answers", "name", distinct="DISTINCT", condition=f"question = '{question}'")
            self.cursor.execute(query)
            students = self.cursor.fetchall()
            return students
        except mysql.connector.Error as err:
            print(f"Error occurred during query execution: {err}")
            return None
        finally:
            self.cursor.close()
            self.conn.close()
            
    def checkHighlightsExist(self, rubric, answer):
        self.conn = self.connect_to_db()
        self.changeDatabase("exam1")
        if self.conn is None:
            return None
        self.cursor = self.conn.cursor()

        try:
            query = "SELECT * FROM highlights WHERE rubric = %s AND answer = %s"
            self.cursor.execute(query, (rubric, answer))
            result = self.cursor.fetchall()
            return result
        except mysql.connector.Error as err:
            print(f"Error occurred during query execution: {err}")
            return None
        finally:
            self.cursor.close()
            self.conn.close()

    def checkLabelsExist(self, question):
        self.conn = self.connect_to_db()
        self.changeDatabase("exam1")
        if self.conn is None:
            return None
        self.cursor = self.conn.cursor()

        try:
            query = "SELECT * FROM Tag WHERE question = %s"
            self.cursor.execute(query, (question,))
            result = self.cursor.fetchall()
            return len(result) > 0
        except mysql.connector.Error as err:
            print(f"Error occurred during query execution: {err}")
            return False
        finally:
            self.cursor.close()
            self.conn.close()
            
    #######################################################################################
        

    def save_hashmap_to_cache(self, cache_file):
        with open(cache_file, 'wb') as f:
            pickle.dump(self.hashmap, f)

    def load_hashmap_from_cache(self, cache_file):
        with open(cache_file, 'rb') as f:
            self.hashmap = pickle.load(f)
    
    def add(self,Question,Answer="",Rubric=""):
        if Question in self.hashmap:
            if  Answer in self.hashmap[Question]:
                extract, start, end = self.bert.get_model_output(
                    student_answer=Answer, requirement=Rubric
                    )
                ##check the index is tensor format or not, in case some result is empty or No answer
                if torch.is_tensor(start):
                    start,end = self.bert.get_highlight_indices(Answer,start.item(),end.item())
                    end = end - 4
                    print(f"startChar: {start}")
                    print(f"endChar: {end}")
                else:
                    start = '' 
                    start = '' 
                    end = ''

                # if torch.is_tensor(end):
                #     end = end.item()
                # else:
                #     end = ''

                # if torch.is_tensor(end):
                #     end = end.item()
                # else:
                #     end = ''

                self.hashmap[Question][Answer][Rubric] = [Question,Answer,Rubric,start,end]
            else:
                self.hashmap[Question][Answer] = {}
                self.add(Question,Answer,Rubric)
        else:
            self.hashmap[Question] = {}
            self.hashmap[Question]['Lable'] = generateLabels(Question,self.list,self.threshHold)
            self.add(Question,Answer,Rubric)
    
    def remove(self,Question,Answer="",Rubric=""):
        if Answer == "":
            del self.hashmap[Question]
        else:
            if Rubric == "":
                del self.hashmap[Question][Answer]
            else:
                del self.hashmap[Question][Answer][Rubric]    

    ##################################never be used#########################################
    # def addStartAndEnd(self, Question, Answer, Rubric):                                  #
    #     extract, start, end = self.bert.get_model_output(                                #
    #         student_answer=Rubric, requirement=Answer                                    #
    #     )                                                                                #
    #     self.hashmap[Question][Answer][Rubric] = [Question, Answer, Rubric, start, end]  #
    ########################################################################################
    def getHashmap(self):
        return self.hashmap


def print3DHashmap(hashmap):
    for outer_key, middle_dict in hashmap.items():
        print(f"Outer Key: {outer_key}")
        for middle_key, inner_dict in middle_dict.items():
            print(f"Middle Key: {middle_key}")
            if isinstance(inner_dict,dict):
                for inner_key, value in inner_dict.items():
                    print(f"Inner Key: {inner_key}, Value: {value}")
            elif isinstance(inner_dict,list):
                for element in inner_dict:
                    print(f"inner_element: {element}")
            else:
                print(inner_dict)
                


def init_hashmap(file_path, round_instance, cache_file='hashmap_cache.pkl'):
    if os.path.exists(cache_file):
        round_instance.load_hashmap_from_cache(cache_file)
    else:
        with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
            csvreader = csv.reader(csvfile)
            headers = next(csvreader)
            for row in csvreader:
                round_instance.add(row[0], row[1], row[2])
        round_instance.save_hashmap_to_cache(cache_file)


def read_labelPredictionForm(file_path):
    with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
        csvreader = csv.reader(csvfile)
        list = next(csvreader)
    return list

def generateLabels(question,list,threshHold):
    classifier = pipeline("zero-shot-classification", model="MoritzLaurer/DeBERTa-v3-base-mnli-fever-anli")
    labels = lm.classify_sentence(question, list, classifier, threshHold, True)[0][:3]
    return labels

        


def main():
    # Create an instance of the RoundUsing class
    round_instance = roundUsing(password="password")

    # three_d_nested_hashmap = {
    #     'outer_key1': {
    #         'middle_key1': {
    #             'inner_key1': 'value111',
    #             'inner_key2': 'value112'
    #         },
    #         'middle_key2': {
    #             'inner_key3': 'value113',
    #             'inner_key4': 'value114'
    #         }
    #     },
    #     'outer_key2': {
    #         'middle_key3': {
    #             'inner_key5': 'value125',
    #             'inner_key6': 'value126'
    #         },
    #         'middle_key4': {
    #             'inner_key7': 'value127',
    #             'inner_key8': 'value128'-
    #         }
    #     }
    #     }    
    # print3DHashmap(three_d_nested_hashmap)

    # Add new questions, rubrics, and answers

    ###################################### highlight part test################################
    ############### workable test cases
    questions = ["Describe World War Two."]
    answers = [
        """World War II, which started November 1 1939, was a global conflict primarily involving the Allies, 
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
    ]
    rubrics = ["When did the war start?", "Which countries were in the Allies?"]

    
    ######## simple answer and rubrics test cases
    # questions = ["What are the pros and cons of online education?"]
    # answers = ["Convenience and flexibility","Interaction challenges"]
    # rubrics = ["Clear and concise","Relevance to the question"]
    # questions = ["What are the pros and cons of online education?"]
    # answers = ["Convenience and flexibility","Interaction challenges"]
    # rubrics = ["Clear and concise","Relevance to the question"]

    # add to hashmap
    # for q in questions:
    #     for a in answers:
    #         for r in rubrics:
    #             round_instance.add(Question=q, Rubric=r, Answer=a)
    # for q in questions:
    #     for a in answers:
    #         for r in rubrics:
    #             round_instance.add(Question=q, Rubric=r, Answer=a)

    #######################################init hashmap test##################################
    # init_hashmap("data\QARtest.csv",round_instance)
    # init_hashmap("data\QARtest.csv",round_instance)

    # print3DHashmap(round_instance.getHashmap())

    #######################################Database###########################################
    round_instance.createDB("exam1")
    round_instance.changeDatabase("exam1")

    # cols = ["name","question","answer"]
    # datatype = ["VARCHAR(50)","LONGTEXT","LONGTEXT"]
    # colDT = [cols,datatype]
    # round_instance.createTable("answers",colDT)

    # cols = ["question","rubric"]
    # datatype = ["LONGTEXT","TEXT"]
    # colDT = [cols,datatype]
    # round_instance.createTable("exam",colDT)

    # cols = ["question","label"]
    # datatype = ["LONGTEXT","VARCHAR(50)"]
    # colDT = [cols,datatype]
    # round_instance.createTable("Tag",colDT)

    # cols = ["name","accountName","password"]
    # datatype = ["VARCHAR(50)","VARCHAR(50)","VARCHAR(50)"]
    # colDT = [cols,datatype]
    # round_instance.createTable("account",colDT)

    # cols = ["rubric","answer","startIndex","endIndex"]
    # datatype = ["TEXT","LONGTEXT","INTEGER","INTEGER"]
    # colDT = [cols,datatype]
    # round_instance.createTable("highlights",colDT)
    
    # cols = ["name","question","answer"]
    # data = ["'student1'","'Describe World War Two.'","""'World War II, which started November 1 1939, was a global conflict primarily involving the Allies, 
    #     including the United States, the Soviet Union, and the United Kingdom, against the Axis powers, notably Nazi 
    #     Germany, Italy, and Japan. The war began with Germany''s invasion of Poland, prompting Britain and France to 
    #     declare war on Germany. This conflict was marked by significant events like the Holocaust, the bombing of 
    #     Pearl Harbor, and the use of atomic bombs on Hiroshima and Nagasaki. The war resulted in immense human 
    #     suffering and significant changes in the political landscape, leading to the Cold War and the establishment 
    #     of the United Nations.'"""]
    # col_data = [cols,data]
    # round_instance.insertData("answers",colDTList=col_data)
    
    # cols = ["question","rubric"]
    # data = ["'Describe World War Two.'","'When did the war start?'"]
    # col_data = [cols,data]
    # round_instance.insertData("exam",colDTList=col_data)

    # round_instance.insertLabels("'Describe World War Two.'")
    

    tables = round_instance.queryExecutor(queryString=round_instance.unionQuery(queryString1=round_instance.queryGenerate("answers","*",distinct="DISTINCT",condition="question = 'Describe World War Two.'"),queryString2=round_instance.queryGenerate("exam","*",condition="question = 'Describe World War Two.")))
    for each in tables:
        for each1 in each:
            print(each1)

    # round_instance.conn.commit()
    # round_instance.cursor.close()
    # round_instance.conn.close()
 
if __name__ == "__main__":
    main()
    