from abc import ABC, abstractmethod
import numpy as np
from tqdm.notebook import tqdm


class Encoder(ABC):

    def __init__(self, model_name: str, verbose=False):
        self.verbose = verbose
        self.model_name = model_name

    @abstractmethod
    def encode(self, sentences, isQuery=True):
        pass


class OneByOneEncoder(Encoder, ABC):

    def __init__(self, model_name: str, verbose=False):
        super().__init__(model_name, verbose)

    @abstractmethod
    def _encode_str(self, sentence: str):
        pass

    def __encode_list(self, sentences):
        embeddings = list()
        counter = 0
        for s in tqdm(sentences, total=len(sentences), desc="Encoding corpus"):
            embeddings.append(self._encode_str(s))
            counter += 1

        return np.array([emb[0] for emb in embeddings])

    def encode(self, sentences, isQuery=True):
        if isinstance(sentences, str):
            return self._encode_str(sentences)
        elif len(sentences) == 1:
            return self._encode_str(sentences[0])
        else:
            return self.__encode_list(sentences)


