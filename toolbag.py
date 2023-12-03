class roundUsing:
    def __init__(self):
        self.hashmap = {}

    def add(self,Question,Rubric="",Answer=""):
        if Question in self.hashmap:
            if  Rubric in self.hashmap[Question]:
                self.hashmap[Question][Rubric][Answer] = [Question,Rubric,Answer]
            else:
                self.hashmap[Question][Rubric] = {}
                self.add(Question,Rubric,Answer)
        else:
            self.hashmap[Question] = {}
            self.add(Question,Rubric,Answer)
    
    def remove(self,Question,Rubric="",Answer=""):
        if Rubric == "":
            del self.hashmap[Question]
        else:
            if Answer == "":
                del self.hashmap[Question][Rubric]
            else:
                del self.hashmap[Question][Rubric][Answer]    

    def addStartAndEnd(self,Question,Rubric,Answer,i,j):
        self.hashmap[Question][Rubric][Answer] = [Question,Rubric,Answer,i,j]

    def getHashmap(self):
        return self.hashmap

def print3DHashmap(hashmap):
    for outer_key, middle_dict in hashmap.items():
        print(f"Outer Key: {outer_key}")
        for middle_key, inner_dict in middle_dict.items():
            print(f"Middle Key: {middle_key}")
            for inner_key, value in inner_dict.items():
                print(f"Inner Key: {inner_key}, Value: {value}")


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
    #             'inner_key8': 'value128'
    #         }
    #     }
    #     }
    
    # print3DHashmap(three_d_nested_hashmap)

    # Add new questions, rubrics, and answers
    round_instance.add("What is your name?","Rubric for the question.","John Doe")
    print("Before remove ")
    print3DHashmap(round_instance.getHashmap())
    round_instance.remove("What is your name?",Rubric="Rubric for the question.")
    print("After remove ")
    print3DHashmap(round_instance.getHashmap())

if __name__ == "__main__":
    main()

