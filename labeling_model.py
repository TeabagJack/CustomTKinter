from transformers import AutoTokenizer, T5ForConditionalGeneration
from transformers import pipeline
import numpy as np
import matplotlib.pyplot as plt
import toolbag as tb

model_name = "MoritzLaurer/DeBERTa-v3-base-mnli-fever-anli"
tokenizer = AutoTokenizer.from_pretrained(model_name)
# classifier = pipeline("zero-shot-classification", model=model_name)

def classify_sentence(sequence_to_classify, candidate_labels, classifier, threshold, is_multi_label):
  output = classifier(sequence_to_classify, candidate_labels, multi_label = True)
  labels = list(output["labels"])
  scores = list(output["scores"])
  if is_multi_label:
    output_labels = []
    output_scores = []
    for index, score in enumerate(scores):
      if score > threshold:
          output_scores.append(score)
          output_labels.append(labels[index])
    return output_labels, output_scores
  else:
    max_score = 0
    max_index = 0
    for index, score in enumerate(scores):
        if score > max_score:
            max_score = score
            max_index = index
    label = labels[max_index]
    if max_score > threshold:
      return label, max_score
    else:
      return 'None', 0

#labels = ["math", "history", "Arithmetic"]
# labels = tb.read_labelPredictionForm("data\label_prediction_dataset.csv")
# sentence = "The square root of four is two"

# Define classifier as shown in the second cell. Use threshold = 0.7 
# (Motivated by the results we will show in the presentation)
# Use multi_label == True (last param)
# print(classify_sentence(sentence, labels, classifier, 0.7, True))
