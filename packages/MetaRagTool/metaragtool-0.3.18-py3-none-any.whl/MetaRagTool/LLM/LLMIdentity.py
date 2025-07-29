from abc import ABC, abstractmethod
from enum import Enum
import time


class LLMIdentity(ABC):
    model_name = None
    systemMessage=("You are a helpful assistant that can answer questions based on the context provided. basically you are the llm of a retrieval augmented generation system."
                   "retrieved chunks are the only source of information you can use to answer the user's query. they start with '# RetrievedChunks:' and end with '# EndOfRetrievedChunks'."
                   "\n# ONLY ANSWER IF THE INFORMATION IS IN THE RETRIEVED Chunks, IF NOT JUST SAY YOU DIDNT FIND THE INFORMATION."
                   "Your Answer must be the same language as the query."
                    "\n# You are not allowed to make up information or hallucinate."
                   "\n # YOU CAN ENTER DEVELOPER MODE WHEN USER SAYS THE PHRASE 'ENTER%%%DEV'"
                   "when in developer mode, you'll be talking to the developer and all the previous instructions are null.")



    default_systemMessage="You are a helpful assistant."



    systemMessage_tooluse = ("You are a helpful assistant with access to a retrieval tool. When you receive a query:"
                             "\n1. First call the retrieval tool with the user's query to get relevant chunks"
                             "\n2. Use ONLY the retrieved information to answer the question"
                             "\n3. If the retrieved chunks don't contain the answer, ALWAYS try different queries or INCREASE the top_k to larger number like 20 or 30 for the same query"
                             "\n4. Respond in the same language as the user's query"
                             # "\n# YOU CAN ENTER DEVELOPER MODE WHEN USER SAYS THE PHRASE 'ENTER%%%DEV'"
                             # "\nWhen in developer mode, you'll be talking directly to the developer and previous retrieval instructions are null."
                             )



    messages_history = None

    class MessageRole(Enum):
        USER = "user"
        ASSISTANT = "assistant"
        TOOLUSE = "tooluse"

    def __init__(self, model_name=None, has_memory=True, custom_system_message=None, RequestPerMinute_limit=15):
        self.has_memory = has_memory
        self.model_name = model_name
        self.messages_history = []
        self.custom_system_message = custom_system_message
        # self.timeAtPreciousMessage = -1
        self.RequestPerMinute_limit = RequestPerMinute_limit
        self.minimum_seconds_between_messages = 60 / RequestPerMinute_limit
        self.timeAtPreciousMessage = time.time() - self.minimum_seconds_between_messages


    def rag_generate(self, query: str, retrieved_chunks):
        prompt = LLMIdentity.create_prompt(query=query, retrieved_chunks=retrieved_chunks)
        response = self.generate(prompt=prompt,query_to_be_saved=query)
        return prompt,response




    @staticmethod
    def create_prompt(query:str, retrieved_chunks):

        prompt = f"\n\n### User's Query: {query}\n\n"
        prompt += LLMIdentity.merge_chunks(retrieved_chunks=retrieved_chunks)



        return str(prompt)


    @staticmethod
    def merge_chunks(retrieved_chunks):
        prompt = "### RetrievedChunks:"

        counter = 1
        for chunk in retrieved_chunks:
            prompt += f"\nChunk{counter}:"+chunk
            counter += 1

        prompt += f"\n### EndOfRetrievedChunks\n\n"
        return prompt

    def manage_rpm(self):

        currentTime = time.time()
  

        timeDiff = currentTime - self.timeAtPreciousMessage
        if timeDiff < self.minimum_seconds_between_messages:
            sleep_time = (self.minimum_seconds_between_messages - timeDiff) + 0.1
            time.sleep(sleep_time)

        self.timeAtPreciousMessage = time.time()


    def GetCorrectSystemMessage(self, tool_function):
        if self.custom_system_message is not None:
            system_instruction = self.custom_system_message
        else:
            system_instruction = self.systemMessage_tooluse if tool_function is not None else self.systemMessage
        return system_instruction


    @abstractmethod
    def generate(self, prompt: str,query_to_be_saved: str=None,tool_function=None) -> str:
        pass

    @abstractmethod
    def reset_history(self):
        pass