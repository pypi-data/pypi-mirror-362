from abc import ABC, abstractmethod
from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch



class Reranker(ABC):

    def __init__(self, model_name: str, verbose=False):
        self.verbose = verbose
        self.model_name = model_name

    @abstractmethod
    def get_scores(self, query:str, chunks: list):
        pass


    def apply_rerank_raw_texts(self, query: str, chunks: list):
        scores = self.get_scores(query=query, chunks=chunks)
        sorted_chunks = [x for _, x in sorted(zip(scores, chunks), reverse=True)]
        return sorted_chunks

    def apply_rerank_MRChunks(self, query: str, chunks: list):
        chunk_texts = [chunk.Text for chunk in chunks]
        scores = self.get_scores(query=query, chunks=chunk_texts)
        sorted_chunks = [x for _, x in sorted(zip(scores, chunks), key=lambda pair: pair[0], reverse=True)]
        return sorted_chunks

class CrossEncoderReranker(Reranker):
    def __init__(self, model_name: str, verbose=False):
        from sentence_transformers import CrossEncoder
        from MetaRagTool import Constants

        super().__init__(model_name, verbose)
        self.model = CrossEncoder(model_name, trust_remote_code=Constants.trust_remote_code)

    def get_scores(self, query: str, chunks: list):
        sentence_pairs = [[query, doc] for doc in chunks]
        scores = self.model.predict(sentence_pairs)
        return scores


class AutoModelForSequenceClassificationReranker(Reranker):
    def __init__(self, model_name: str, verbose=False):
        super().__init__(model_name, verbose)

        self.model = AutoModelForSequenceClassification.from_pretrained(
            model_name,
            torch_dtype="auto",
            trust_remote_code=True
        )
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)

    def get_scores(self, query: str, chunks: list):
        sentence_pairs = [[query, doc] for doc in chunks]

        inputs = self.tokenizer(sentence_pairs, padding=True, truncation=True, return_tensors="pt", max_length=1024)

        with torch.no_grad():
            scores = self.model(**inputs).logits

        return scores.float().numpy().tolist()

