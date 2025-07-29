import gc
import weave
from hazm import word_tokenize as persian_word_tokenize,sent_tokenize as persian_sent_tokenize
from nltk.tokenize import word_tokenize as english_word_tokenize,sent_tokenize as english_sent_tokenize
import numpy as np
import re
import wandb
from collections import OrderedDict

has_logged_in_to_wandb = False




def init_wandb(project_name, run_name, config=None,group=None):
    global has_logged_in_to_wandb
    if not has_logged_in_to_wandb:
        api_key = Constants.WandbToken
        wandb.login(key=api_key)
        has_logged_in_to_wandb = True

    wandb.init(project=project_name, name=run_name, config=config,group=group)


def init_hf():
    from huggingface_hub import login
    hf_token = Constants.HFToken
    login(token=hf_token, add_to_git_credential=False)


def listToString(listOfStrings, separator="\n"):
    output = ""
    for s in listOfStrings:
        output += str(s) + separator
    return output

def get_word_tokenizer():
    if Constants.lang=="multi":
        return english_word_tokenize
    elif Constants.lang=="fa":
        return persian_word_tokenize

    print("Error: lang not set to fa or multi")
    return None

def get_sent_tokenizer():
    if Constants.lang=="multi":
        return english_sent_tokenize
    elif Constants.lang=="fa":
        return persian_sent_tokenize

    print("Error: lang not set to fa or multi")
    return None


def capped_sent_tokenize(text, max_length=500):
    custom_word_tokenizer = get_word_tokenizer()
    sentence_tokenizer = get_sent_tokenizer()
    sentences = sentence_tokenizer(text)
    capped_sentences = []
    for sentence in sentences:
        while token_len(sentence) > max_length:
            tokens = custom_word_tokenizer(sentence)
            capped_sentences.append(" ".join(tokens[:max_length]))
            sentence = " ".join(tokens[max_length:])
        capped_sentences.append(sentence)
    return capped_sentences


def token_len(text):
    custom_word_tokenizer = get_word_tokenizer()
    return len(custom_word_tokenizer(text))




def reflect_vector(q, v):
    proj = np.dot(v, q) / np.dot(q, q) * q
    reflection = 2 * proj - v

    return reflection


def read_pdf(pdf_path, ignore_line_breaks=True):
    import PyPDF2

    text = ""
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        for page in pdf_reader.pages:
            if page.extract_text():
                page_text = page.extract_text()
                if ignore_line_breaks:
                    # Replace single line breaks with space
                    page_text = re.sub(r'(?<!\n)\n(?!\n)', ' ', page_text)
                    text += page_text + '\n'
                else:
                    text += page_text

    return text.strip()


def Init(encoder_name, top_k, sample_size, qa_sample_size,  multi_hop_hardness_factor=0,
         judged=False, useTool=False, llm=None,multi_hop=True,custom_data=None,custom_project_name=None,wandb_group=None):
    from MetaRagTool.Utils.MetaRagConfig import MetaRagConfig
    from MetaRagTool.Encoders.SentenceTransformerEncoder import SentenceTransformerEncoder
    from MetaRagTool.LLM.JudgeLLM import JudgeLLM
    from MetaRagTool.Utils import DataLoader
    from MetaRagTool.LLM.GoogleGemini import Gemini

    gc.collect()

    Constants.use_wandb = True

    if custom_data is not None:
        contexts, qas = custom_data
        multi_hop = False
    else:
        contexts, qas = DataLoader.loadWikiFaQa(sample_size=sample_size, qa_sample_size=qa_sample_size, multi_hop=multi_hop,
                                            multi_hop_hardness_factor=multi_hop_hardness_factor)


    encoder = SentenceTransformerEncoder(encoder_name)
    judge = None

    llm_name= None
    if judged:
        if llm is None:
            llm = Gemini(has_memory=False, RequestPerMinute_limit=15, model_name=Gemini.GEMINI_2_FLASH)
            # llm = OpenaiGpt(has_memory=False, RequestPerMinute_limit=15)

        judge = JudgeLLM(model_name=Gemini.GEMINI_2_FLASH_LIGHT, RequestPerMinute_limit=30)
        llm_name=llm.model_name
        project_name = "fullRag"
        weave.init(project_name)


    else:
        project_name = 'retrival'

    if custom_project_name is not None:
        project_name = custom_project_name

    ragConfig = MetaRagConfig(encoder_name=encoder_name, top_k=top_k, sample_size=sample_size,
                              qa_sample_size=qa_sample_size,
                              multi_hop_hardness_factor=multi_hop_hardness_factor, judged=judged, useTool=useTool,
                              llm_name=llm_name,
                              encoder=encoder, contexts=contexts, qas=qas, llm=llm, judge=judge,
                              project_name=project_name,multi_hop=multi_hop,wandb_group=wandb_group)

    return ragConfig


def remove_duplicates(l):
    return list(OrderedDict.fromkeys(l))



import MetaRagTool.Constants as Constants
