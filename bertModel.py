# imports
from transformers import AutoModelForQuestionAnswering, AutoTokenizer
import torch


class bertModel:
    def __init__(self):
        # define model
        self.model = AutoModelForQuestionAnswering.from_pretrained(
            "bert-large-uncased-whole-word-masking-finetuned-squad"
        )

        # define tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(
            "bert-large-uncased-whole-word-masking-finetuned-squad"
        )

    def get_highlight_indices(self, student_answer: str, start_logit_index: int, end_logit_index: int):
        tokenized_answer = self.tokenizer(student_answer, return_offsets_mapping=True)
        start_i, start_j = tokenized_answer["offset_mapping"][start_logit_index]
        end_i, end_j = tokenized_answer["offset_mapping"][end_logit_index]

        return start_i, end_j - 2

    def get_model_output(self, student_answer: str, requirement: str):
        # tokenize input texts
        inputs = self.tokenizer.encode_plus(student_answer,
                                            requirement,
                                            return_tensors="pt")

        # generate model answer with metrics
        with torch.no_grad():
            outputs = self.model(**inputs)

        # get model prediction indexes
        answer_start_index = outputs.start_logits.argmax()
        answer_end_index = outputs.end_logits.argmax() + 1

        # set threshold
        if outputs.start_logits[0][answer_start_index] < 0:
            return "", "", "No answer"

        # decode predictions
        model_prediction_tokens = inputs.input_ids[
                                  0, answer_start_index: answer_end_index
                                  ]
        model_prediction = self.tokenizer.decode(model_prediction_tokens)

        return model_prediction, answer_start_index, answer_end_index
