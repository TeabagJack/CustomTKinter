from transformers import AutoTokenizer, T5ForConditionalGeneration, AutoModelForSeq2SeqLM, pipeline
import difflib

tokenizer = AutoTokenizer.from_pretrained("grammarly/coedit-large")
model = T5ForConditionalGeneration.from_pretrained("grammarly/coedit-large")



class GrammarChecker2:
    def __init__(self):
        self.model = model
        self.tokenizer = tokenizer


    def correct_grammar(self, text):
        # # Generate corrected text from the grammar model
        # matches = self.grammar_check.generate_text(text, args=settings)
        # print(f'matches: {matches}, type: {type(matches)}')
        # # Extract original and corrected text
        original_text = text
        corrected_text = self.correct_text(text)
        # corrected_text = matches.text if matches and matches.text else text
        # print(f'corrected: {corrected_text}, type: {type(corrected_text)}')
        # # Calculate the differences between original and corrected text
        differences = list(difflib.ndiff(original_text.split(), corrected_text.split()))

        # differences = list(difflib.ndiff(corrected_text.split(), original_text.split()))

        # Extract corrected words
        corrected_words = [word[2:] for word in differences if word.startswith('+ ')]

        # Calculate the total count of found mistakes
        foundmistakes_count = len(corrected_words)

        # return print(f"Corrected: {corrected_text}\nWords Corrected: {corrected_words}\nCount:{foundmistakes_count}")
        return corrected_text, corrected_words, foundmistakes_count

    def highlight_mistakes(self, txt):
        text, words, count = self.correct_grammar(txt)

        highlighted_text = []
        for word in text.split():
            if word in words:
                new_word = '**' + word + '**'
                highlighted_text.append(new_word)
            else: highlighted_text.append(word)
        return " ".join(highlighted_text)#, text

    def correct_text(self, text):
        input_txt = "Fix grammatical errors in this sentence:" + text
        input_ids = self.tokenizer(input_txt, return_tensors="pt").input_ids
        outputs = self.model.generate(input_ids, max_length=256)
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)

    def handle_student_asnwer(self, text):
        # 1 split in list of str for every sentence
        text_list = text.split('.')
        text_list = [x for x in text_list if x] # remove empty string

        # 2 highlight every sentence
        highlighted = [self.highlight_mistakes(t) for t in text_list]

        return ".".join(highlighted)


      

# #How to use

# # 1 create model
# corrector = GrammarChecker2()
# # 2 get text
# txt = "Climate change is signiifcantly impacting global weather patterns leading to a surge in extreme weather events. We observe more frequents and intense hurricanes, like as Hurricane Harvey in 2017, which caused widespread flooding and devastating impacts. Additionally heatwaves are becoming more common, as seen in the European heatwave of 2019. These events are clear indicators of the changing climate. Agriculture is heavily affected, with altered precipitation patterns, shifting growing seasons, and increased pest pressure. These changes threaten food security globally, impacting crop yields and quality. To address this, individuals can contribute by adopting sustainable practices, such as reducing meat consumption, using energy-efficient appliances, and supporting renewable energy sources. These efforts collectively help reduce the overall carbon footprint and contribute to mitigating climate change."
# # 3 use method `handle_student_asnwer(txt)`
# corrector.handle_student_asnwer(txt)
