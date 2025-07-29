from MetaRagTool.LLM.GoogleGemini import Gemini
import weave


class JudgeLLM:
    def __init__(self,model_name=Gemini.GEMINI_2_FLASH_LIGHT,RequestPerMinute_limit=30):
        sys_message = """You are an impartial judge evaluating answer quality.
        Your task is to determine if an answer correctly addresses a question based on the ground truth.

        Guidelines for evaluation:
        - Compare the semantic meaning, not exact wording
        - An answer is correct if it contains the key information from ground truth
        - Answers with correct information plus additional details are still correct
        - Consider multilingual content (including Persian/Farsi) equally

        You must respond with ONLY 'yes' or 'no'.
        - 'yes' = the answer contains the key information from ground truth
        - 'no' = the answer is incorrect or missing essential information
        """
        self.llm = Gemini(has_memory=False,custom_system_message=sys_message,model_name=model_name,RequestPerMinute_limit=RequestPerMinute_limit)

    @weave.op()
    def judge(self,question:str,ground_truth:str,answer:str):
        prompt = f"""
        ### Question: {question}
        ### Ground Truth: {ground_truth}
        ### Answer: {answer}
        ### Is the answer correct? Only Answer with 'yes' or 'no'.
        """

        response = self.llm.generate(prompt)
        return response
