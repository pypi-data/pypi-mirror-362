import weave
from MetaRagTool.LLM.LLMIdentity import LLMIdentity
from openai import OpenAI
import time


class OpenaiGpt(LLMIdentity):


    endpoint_azure = "https://models.inference.ai.azure.com"
    endpoint_openrouter = "https://openrouter.ai/api/v1"
    MODEL_deepseek_v3 = "deepseek/deepseek-chat-v3-0324:free"
    MODEL_llama_4_maverick = "meta-llama/llama-4-maverick:free"
    MODEL_llama_3="meta-llama/llama-3.3-70b-instruct:free"
    MODEL_gpt_4o = "gpt-4o"

    def __init__(self, model_name=MODEL_deepseek_v3, has_memory=True, custom_system_message=None,
                 RequestPerMinute_limit=15, endpoint=endpoint_openrouter, api_key=None):
        from MetaRagTool import Constants

        if api_key is None:
            api_key = Constants.API_KEY_OPENROUTER
        super().__init__(model_name=model_name, has_memory=has_memory, custom_system_message=custom_system_message,
                         RequestPerMinute_limit=RequestPerMinute_limit)
        self.client = OpenAI(
            base_url=endpoint,
            api_key=api_key,
        )

        self.reset_history()

    def reset_history(self):
        system_instruction = self.GetCorrectSystemMessage(None)
        self.messages_history = [
            {"role": "system", "content": system_instruction},
            # {"role": "system","content": [{"type": "text","text": system_instruction}]}

        ]

    @weave.op()
    def generate(self, prompt: str, query_to_be_saved: str = None, tool_function=None) -> str:
        if tool_function is not None:
            print("OpenaiGpt does not support tool use")

        if self.RequestPerMinute_limit > 0 and tool_function is not None:
            self.manage_rpm()

        self.messages_history.append({"role": "user", "content": prompt})
        # self.messages_history.append( {"role": "user", "content": [{"type": "text", "text": prompt}]})



        while True:
            try:
                response = self.client.chat.completions.create(
                    messages=self.messages_history,
                    model=self.model_name,
                    # tools=
                )
                text_output=response.choices[0].message.content
                break
            except Exception as e:
                print(f"Error sending message, waiting 10 seconds to retry")
                time.sleep(10)




        if not self.has_memory:
            self.reset_history()

        self.messages_history.append(response.choices[0].message)

        return text_output
