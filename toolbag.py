from bertModel import bertModel
import csv


class roundUsing:
    def __init__(self):
        self.hashmap = {}
        self.bert = bertModel()

    
    def add(self,Question,Answer="",Rubric=""):
        if Question in self.hashmap:
            if  Answer in self.hashmap[Question]:
                self.hashmap[Question][Answer][Rubric] = [Question,Answer,Rubric]
            else:
                self.hashmap[Question][Answer] = {}
                self.add(Question,Answer,Rubric)
        else:
            self.hashmap[Question] = {}
            self.hashmap[Question]['Lable'] = ["label1","label2","label3"]
            self.add(Question,Answer,Rubric)
    
    def remove(self,Question,Answer="",Rubric=""):
        if Answer == "":
            del self.hashmap[Question]
        else:
            if Rubric == "":
                del self.hashmap[Question][Answer]
            else:
                del self.hashmap[Question][Answer][Rubric]    

    def addStartAndEnd(self, Question, Answer, Rubric):
        extract, start, end = self.bert.get_model_output(
            student_answer=Rubric, requirement=Answer
        )
        self.hashmap[Question][Answer][Rubric] = [Question, Answer, Rubric, start, end]

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

def init_hashmap(file_path,round_instance):
    with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
        csvreader = csv.reader(csvfile)
        headers = next(csvreader)  # Assuming the first row contains headers
        for row in csvreader:
            round_instance.add(row[0],row[1],row[2])



def main():
    # Create an instance of the RoundUsing class
    round_instance = roundUsing()

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
    # questions = ["Describe World War Two."]
    # answers = [
    #     """World War II, which started November 1 1939, was a global conflict primarily involving the Allies, 
    #     including the United States, the Soviet Union, and the United Kingdom, against the Axis powers, notably Nazi 
    #     Germany, Italy, and Japan. The war began with Germany's invasion of Poland, prompting Britain and France to 
    #     declare war on Germany. This conflict was marked by significant events like the Holocaust, the bombing of 
    #     Pearl Harbor, and the use of atomic bombs on Hiroshima and Nagasaki. The war resulted in immense human 
    #     suffering and significant changes in the political landscape, leading to the Cold War and the establishment 
    #     of the United Nations.""",

    #     """World War 2 was a big war that happened a long time ago. I think it started because some countries were 
    #     not getting along, and then everyone started fighting. There were a lot of soldiers and tanks, and I remember 
    #     there was something about a Pearl Harbor movie. It ended because America dropped a big bomb, 
    #     and then everyone decided to stop fighting. I'm not sure about the details, but it was a really important 
    #     war."""
    # ]
    # rubrics = ["When did the war start?", "Which countries were in the Allies?"]
    # # add to hashmap
    # for q in questions:
    #     for a in answers:
    #         for r in rubrics:
    #             round_instance.add(Question=q, Rubric=r, Answer=a)
    #             round_instance.addStartAndEnd(q, a, r)

    #######################################init hashmap test##################################
    init_hashmap("data\QARtest.csv",round_instance)

    print3DHashmap(round_instance.getHashmap())
if __name__ == "__main__":
    main()
