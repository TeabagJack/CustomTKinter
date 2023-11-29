# imports
from transformers import AutoModelForQuestionAnswering, AutoTokenizer
import torch
from sklearn.metrics.pairwise import cosine_similarity

dummy_q = [
    ['Describe the moon landing', 'What is the date of the first moon landing?', 'Who went to the moon?'],
]
dummy_a = [
    """The Moon landing, a pivotal event in human history, occurred on July 20, 1969, when Apollo 11, a mission conducted by NASA, the United States space agency, successfully landed the first humans on the Moon. The spacecraft carried three astronauts: Neil Armstrong, Edwin "Buzz" Aldrin, and Michael Collins. Armstrong and Aldrin descended to the Moon's surface in the Lunar Module, named Eagle, while Collins orbited above in the Command Module, Columbia.

Upon touching down on the Moon, Armstrong famously declared, "That's one small step for [a] man, one giant leap for mankind." This phrase encapsulated the monumental achievement of the mission, highlighting the small, individual act of stepping onto the Moon and its significant implications for humanity. The astronauts spent about two and a half hours outside the spacecraft, collecting lunar material to bring back to Earth, deploying scientific instruments, and taking photographs.

The success of the Moon landing was a result of years of scientific and technological innovation. It marked the culmination of the Space Race, a period of intense competition between the United States and the Soviet Union during the Cold War. The mission not only demonstrated technological and exploratory prowess but also symbolized a significant moment of unity, inspiring millions around the world.

Apollo 11's return to Earth was another feat of engineering. The astronauts re-entered Earth's atmosphere and safely splashed down in the Pacific Ocean. The mission's success opened the door to further space exploration, setting the stage for subsequent lunar missions and the future exploration of other celestial bodies.

""" ,

"""The Moon landing was when America sent a rocket to the Moon a long time ago. I think it was in the 1960s or 1970s. Some guys named Neil Armstrong, Buzz Aldrin, and another one went to the Moon. They went in a big rocket and landed there. Neil Armstrong was the first to walk on the Moon, and he said something famous, but I don't remember exactly what it was. They walked around for a bit and then came back.

I'm not sure why they went to the Moon, but I think it was important. They brought back some rocks and stuff. The whole thing was on TV, and a lot of people watched it. It was a big deal back then because it was the first time anyone had gone to the Moon. I guess it was important for science and space stuff. They used a big rocket to get back to Earth and landed in the ocean. It was a big step for exploring space, but I don’t know much about what happened after that."""
    
]


# define model
model = AutoModelForQuestionAnswering.from_pretrained(
    "bert-large-uncased-whole-word-masking-finetuned-squad"
    )

# define tokenizer
tokenizer = AutoTokenizer.from_pretrained(
    "bert-large-uncased-whole-word-masking-finetuned-squad"
    )

def get_highlight_indices(student_answer:str, start_logit_index:int, end_logit_index:int):

  tokenized_answer = tokenizer(student_answer, return_offsets_mapping=True)
  start_i, start_j = tokenized_answer["offset_mapping"][start_logit_index]
  end_i, end_j = tokenized_answer["offset_mapping"][end_logit_index]

  return (start_i, end_j-2)

def get_model_output(student_answer:str, requirement:str):

  # tokenize input texts
  inputs = tokenizer.encode_plus(student_answer,
                                 requirement,
                                 return_tensors="pt")

  # generate model answer with metrics
  with torch.no_grad():
    outputs = model(**inputs)

  # get model prediction indexes
  answer_start_index = outputs.start_logits.argmax()
  answer_end_index = outputs.end_logits.argmax() + 1

  # set threshold
  if outputs.start_logits[0][answer_start_index] < 0:
    return "",0,0

  # decode predictions
  model_prediction_tokens = inputs.input_ids[
      0, answer_start_index : answer_end_index
  ]
  model_prediction = tokenizer.decode(model_prediction_tokens)

  return model_prediction, answer_start_index, answer_end_index

out_1, start_1, end_1 = get_model_output(dummy_a[0], dummy_q[0][1])
print(out_1)
print(get_highlight_indices(dummy_a[0], start_1, end_1))

out_2, start_2, end_2 = get_model_output(dummy_a[1], dummy_q[0][1])
print(out_2)
print(get_highlight_indices(dummy_a[1], start_2, end_2))