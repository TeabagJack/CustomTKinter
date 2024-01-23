from google.oauth2 import service_account
import google.ai.generativelanguage as glm
from IPython.display import Markdown, display

"""
This class is the main class used for the Attributed Question and Answering task.
You can find detailed documentation written by Google Developers on how to implement the AQA model with
their Generative Language API at https://ai.google.dev/docs/semantic_retriever 

I highly recommend reading the link above as it works great.

To run the model, you need to acquire an API key by creating a Google service account and generating a service account
key. You can see a detailed description on how to do that in the above link.

Once you have the JSON file with your service account key, you create the bot by passing it the path to the JSON file in
the constructor.
"""


def print_response_as_markdown(response: glm.GenerateAnswerResponse):
    display(Markdown(response.answer.content.parts[-1].text))


def get_start_and_end_indices(student_answer: str, subtexts: list[str]):
    indices = []
    for subtext in subtexts:
        start_index = student_answer.find(subtext)
        indices.append([
            start_index+1,
            start_index + len(subtext)+1
        ])
    return indices


class Bot:
    model = "models/aqa"
    answer_style = "VERBOSE"
    temperature = 0.2

    generative_service_client = None
    retriever_service_client = None
    permission_service_client = None

    chat_history = []

    def __init__(self, credentials_file_path):
        credentials = service_account.Credentials.from_service_account_file(
            credentials_file_path
        )

        scoped_credentials = credentials.with_scopes([
            'https://www.googleapis.com/auth/cloud-platform',
            'https://www.googleapis.com/auth/generative-language.retriever'
        ])

        self.generative_service_client = glm.GenerativeServiceClient(credentials=scoped_credentials)
        self.retriever_service_client = glm.RetrieverServiceClient(credentials=scoped_credentials)
        self.permission_service_client = glm.PermissionServiceClient(credentials=scoped_credentials)

    # ----------------------------------------------------------------------------------------------------------------------

    def print_corpora_tree(self, with_chunks: bool = False):
        """
        Print all corpora, all documents for each corpus and all chunks for each document in a tree structure for
        quick viewing.
        :param with_chunks: If True, will print the chunks as well, otherwise will only print Corpora and Documents.
        :return: prints tree
        """

        corpora = self.retriever_service_client.list_corpora()

        for corpus in corpora:
            print(corpus.display_name)
            documents = self.retriever_service_client.list_documents(parent=corpus.name)

            for document in documents:
                print(f"    {document.display_name}")
                chunks = self.retriever_service_client.list_chunks(parent=document.name)

                if with_chunks:
                    for chunk in chunks:
                        print(f"        * {chunk.data.string_value[:100]}\n")

    # ---------------------------------------------------------------------------------------------------------------------

    def get_corpus(self, index: int):
        return self.retriever_service_client.list_corpora().corpora[index]

    def add_corpus(self, display_name: str):
        self.retriever_service_client.create_corpus(
            request=glm.CreateCorpusRequest(
                corpus=glm.Corpus(display_name=display_name)
            )
        )
        print(f"Corpus {display_name} created")
        return

    def delete_corpus(self, index: int):
        corpus_name = self.get_corpus(index=index).name
        request = glm.DeleteCorpusRequest(name=corpus_name)
        self.retriever_service_client.delete_corpus(request)
        print(f"Corpus {corpus_name} has been deleted")

    # ----------------------------------------------------------------------------------------------------------------------

    def get_document(self, corpus_index: int or glm.Corpus, document_index: int):
        if type(corpus_index) is int:
            corpus = self.get_corpus(corpus_index)
        else:
            corpus = corpus_index
        return self.retriever_service_client.list_documents(
            parent=corpus.name
        ).documents[document_index]

    def add_document(self, parent: glm.Corpus, display_name: str):
        self.retriever_service_client.create_document(
            request=glm.CreateDocumentRequest(
                parent=parent.name,
                document=glm.Document(display_name=display_name)
            )
        )
        print(f"Document {display_name} added to Corpus {parent.display_name}")
        return

    def delete_document(self, corpus_index, document_index: int):
        document_name = self.get_document(corpus_index, document_index).name
        request = glm.DeleteDocumentRequest(name=document_name)
        self.retriever_service_client.delete_document(request)
        print(f"Document {document_name} has been deleted")
        return

    # ----------------------------------------------------------------------------------------------------------------------

    def get_chunk(self, corpus_index: int, document_index: int, chunk_index: int):
        document = self.get_document(
            corpus_index=corpus_index,
            document_index=document_index
        )
        return self.retriever_service_client.list_chunks(
            parent=document.name
        ).chunks[chunk_index]

    def add_chunks(self, parent: glm.Document, chunks_passages: list[str]):
        create_chunks_requests = []

        print(f'chunks_passages = {chunks_passages}')

        for chunk_passage in chunks_passages:
            # noinspection PyTypeChecker
            create_chunks_requests.append(
                glm.CreateChunkRequest(
                    parent=parent.name,
                    chunk=glm.Chunk(
                        data={"string_value": chunk_passage}
                    )
                )
            )

        print(f'length of create request list = {len(create_chunks_requests)}')
        print(create_chunks_requests)

        self.retriever_service_client.batch_create_chunks(
            request=glm.BatchCreateChunksRequest(
                parent=parent.name,
                requests=create_chunks_requests
            )
        )

        print(f"Chunks added to document {parent.name}")
        return

    def delete_chunks(self, corpus_index: int, document_index: int, chunk_indices: list[int]):
        chunk_delete_requests = []
        for i in chunk_indices:
            chunk_delete_requests.append(
                glm.DeleteChunkRequest(
                    self.get_chunk(corpus_index, document_index, i).name
                )
            )
        request = glm.BatchDeleteChunksRequest(
            parent=self.get_document(corpus_index, document_index).name,
            requests=chunk_delete_requests
        )
        self.retriever_service_client.batch_delete_chunks(request=request)
        print("Chunk deleted")
        return

    def delete_all_chunks_in_document(self, document: glm.Document):
        chunk_delete_requests = []
        for chunk in self.retriever_service_client.list_chunks(parent=document.name):
            chunk_delete_requests.append(
                glm.DeleteChunkRequest(name=chunk.name)
            )
        request = glm.BatchDeleteChunksRequest(
            parent=document.name,
            requests=chunk_delete_requests
        )
        self.retriever_service_client.batch_delete_chunks(request=request)
        print(f"Chunks in {document.name} deleted")
        return

    # ----------------------------------------------------------------------------------------------------------------------

    def generate_answer(self, query: str, source):

        query_content = glm.Content(parts=[glm.Part(text=query)], role='user')
        self.chat_history.append(query_content)

        retriever_config = glm.SemanticRetrieverConfig(
            source=source.name,
            query=query_content
        )

        request = glm.GenerateAnswerRequest(
            model=self.model,
            contents=[query_content],
            semantic_retriever=retriever_config,
            answer_style=self.answer_style,
            temperature=self.temperature
        )

        response = self.generative_service_client.generate_answer(request=request)

        response_content = glm.Content(parts=response.answer.content.parts, role='model')

        self.chat_history.append(response_content)

        return response

    # ----------------------------------------------------------------------------------------------------------------------

    def clear_chat_history(self):
        self.chat_history.clear()
        return

    def add_student_answer(self, corpus: glm.Corpus, display_name: str, student_answer: str):
        self.add_document(corpus, display_name)
        self.add_chunks(
            parent=self.get_document(
                corpus_index=corpus,
                document_index=-1
            ),
            chunks_passages=[x for x in student_answer.split(sep='.') if x != '']
        )

    def run_model(self, student_answer: str, rubric: str):
        # add student answer as a document
        self.add_student_answer(
            corpus=self.get_corpus(1),
            student_answer=student_answer,
            display_name='display_name'
        )

        # get response
        response = self.generate_answer(
            query=rubric,
            source=self.get_document(1, -1)
        )

        # return indices
        parts = []
        for g_a in response.answer.grounding_attributions:
            parts.append(g_a.content.parts[0].text.strip())

        return get_start_and_end_indices(
            student_answer=student_answer,
            subtexts=parts
        ), response.answerable_probability
