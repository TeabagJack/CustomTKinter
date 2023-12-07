class roundUsing:
    def __init__(self):
        self.hashmap = {}

    
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

    def addStartAndEnd(self,Question,Answer,Rubric,i,j):
        self.hashmap[Question][Answer][Rubric] = [Question,Answer,Rubric,i,j]

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
    round_instance.add("What is your name?","John Doe","Rubric for the question.")
    round_instance.add("What is fish?","animal","Rubric 1 for question 1.")
    round_instance.add("what is fish?","fish is a kind of animal","Rubric 2 for question 1")
    print("Before remove ")
    print3DHashmap(round_instance.getHashmap())
    round_instance.remove("What is your name?",Answer="John Doe")
    print("After remove ")
    print3DHashmap(round_instance.getHashmap())

if __name__ == "__main__":
    main()

