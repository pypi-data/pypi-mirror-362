import gc
import math
import MetaRagTool.Constants as Constants
from tqdm.notebook import tqdm
import wandb
import time as time


import MetaRagTool.Utils.MRUtils as MRUtils
from MetaRagTool.RAG.MetaRAG import MetaRAG
from MetaRagTool.Utils.MetaRagConfig import MetaRagConfig
from MetaRagTool.Utils.MRUtils import token_len

verbose_run = False


from abc import ABC, abstractmethod
class EvaluatableRAG(ABC):
    def __init__(self):
        self.chunk_size= -1
        self.ChunksList=[]
        self.time_to_encode_corpus=-1

    @abstractmethod
    def retrieve(self,query, top_k):
        pass

    @abstractmethod
    def add_corpus(self,contexts:list):
        pass

def check_exact_retrieval(rag, pair, verbose=False, top_k=5):
    query = pair[1]['sentence_A']
    answer = pair[1]['sentence_B']

    retrieved = rag.retrieve(query, top_k=top_k)

    if verbose:
        print0(f'query : {query}\n answer : {answer}\n retrieved : ')
        print0(MRUtils.listToString(retrieved))

    if answer in retrieved:
        if verbose: print0('\n Correct')
        return 1
    else:
        if verbose: print0('\n Incorrect')
        return 0


def full_test_exact_match(rag, testData, top_k=5):
    correct = 0
    counter = 0

    tqdm_loop = tqdm(testData.iterrows(), total=len(testData), desc="Evaluating")
    for row in tqdm_loop:
        counter += 1
        correct += check_exact_retrieval(rag=rag, pair=row, top_k=top_k)
        tqdm_loop.set_postfix({'Accuracy': correct / counter})

    print0(f'{correct} out of {counter} Accuracy = {correct / counter}')


def full_test_find_in(rag,ragConfig:MetaRagConfig, question_key='question', answer_key='answer',verbose=False):
    t1 = time.time()
    correct = 0
    counter = 0
    average_precision = 0

    all_retrieved_length = 0
    correct_retrieved_length = 0

    tqdm_loop = tqdm(ragConfig.qas.iterrows(), total=len(ragConfig.qas), desc="Evaluating",disable=not ragConfig.fine_grain_progressbar)
    for row in tqdm_loop:
        counter += 1
        query = row[1][question_key]
        answer = row[1][answer_key]

        retrieved = rag.retrieve(query, top_k=ragConfig.top_k)
        retrieved = MRUtils.listToString(retrieved)

        retrieved_len = token_len(retrieved)
        all_retrieved_length += retrieved_len

        if answer in retrieved:
            correct += 1
            correct_retrieved_length += retrieved_len
            average_precision += token_len(answer) / retrieved_len

        if verbose:
            print0(f'query : {query}\n answer : {answer}\n retrieved : ')
            print0(retrieved)

        acc = correct / counter
        avg_len = math.floor(all_retrieved_length / counter)
        efficiency = math.floor((acc * 100) ** 3 / avg_len)

        tqdm_loop.set_postfix({'Accuracy': acc, 'Avg retrieved length': str(avg_len), 'Efficiency': str(efficiency)})

    total_time = time.time() - t1
    average_precision /= counter
    print0(f'Correct : {correct} out of {counter} = {acc} ')
    print0(f'Average Precision : {average_precision}')
    print0(f'Length Accuracy Efficiency : {efficiency} ')
    print0(f'Average retrieved length : {avg_len}')
    print0(f'Total time : {total_time}')

    if Constants.use_wandb:
        wandb.log({
            'k': ragConfig.top_k,
            'chunk_size': rag.chunk_size,
            'Accuracy': acc,
            'Avg retrieved length': avg_len,
            'Efficiency': efficiency,
            'Average Precision': average_precision,
            'Total time': total_time,
            'corpus size': len(rag.ChunksList),
            'time to encode corpus': rag.time_to_encode_corpus

        })

    return avg_len, efficiency, acc


def full_test_find_in_multiHop(rag,ragConfig:MetaRagConfig,verbose =False):
    t1 = time.time()
    foundBoth = 0
    foundOne = 0
    counter = 0
    average_precision = 0

    all_retrieved_length = 0
    correct_retrieved_length = 0

    tqdm_loop = tqdm(ragConfig.qas.iterrows(), total=len(ragConfig.qas), desc="Evaluating",disable=not ragConfig.fine_grain_progressbar)
    for row in tqdm_loop:
        counter += 1
        query = row[1]['question']
        answer1 = row[1]['answer1']
        answer2 = row[1]['answer2']

        retrieved = rag.retrieve(query, top_k=ragConfig.top_k)
        retrieved = MRUtils.listToString(retrieved)

        retrieved_len = token_len(retrieved)

        all_retrieved_length += retrieved_len

        if answer1 in retrieved and answer2 in retrieved:
            foundBoth += 1
            foundOne += 1
            correct_retrieved_length += retrieved_len
        elif answer1 in retrieved or answer2 in retrieved:
            foundOne += 1

        if verbose:
            print0(f'query : {query}\n answer1 : {answer1}\n answer2 : {answer2}\n retrieved : ')
            print0(retrieved)

        full_acc = foundBoth / counter
        half_acc = foundOne / counter

        if answer1 in retrieved and answer2 in retrieved:
            average_precision += (token_len(answer1) + token_len(answer2)) / retrieved_len
        elif answer1 in retrieved or answer2 in retrieved:
            if answer1 in retrieved:
                average_precision += token_len(answer1) / retrieved_len
            if answer2 in retrieved:
                average_precision += token_len(answer2) / retrieved_len

        avg_len = math.floor(all_retrieved_length / counter)
        efficiency = math.floor((full_acc * 100) ** 3 / avg_len)

        tqdm_loop.set_postfix({'Accuracy': full_acc, 'Half Accuracy': half_acc, 'Avg retrieved length': str(avg_len),
                               'Efficiency': str(efficiency)})

    total_time = time.time() - t1
    average_precision /= counter

    print0()
    print0(f'Test Results for k = {ragConfig.top_k} :')
    print0(f'Average Precision : {average_precision}')
    print0(f'Full Accuracy (found both) : {foundBoth} out of {counter} = {full_acc} ')
    print0(f'Half Accuracy (found at least one)  : {foundOne} out of {counter} = {half_acc} ')
    print0(f'Length Accuracy Efficiency : {efficiency} ')
    print0(f'Average retrieved length : {avg_len}')

    if foundBoth > 0:
        print0(f'Average correct retrieved length : {math.floor(correct_retrieved_length / foundBoth)}')
    else:
        print0('Average correct retrieved length : N/A (no correct retrievals)')
    print0(f'Total time : {total_time}')

    print0(f'Total time : {total_time}')

    if Constants.use_wandb:
        wandb.log({
            'k': ragConfig.top_k,
            'chunk_size': rag.chunk_size,
            'Full Accuracy': full_acc,
            'Half Accuracy': half_acc,
            'Avg retrieved length': avg_len,
            'Efficiency': efficiency,
            'Average Precision': average_precision,
            'Total time': total_time,
            'corpus size': len(rag.ChunksList),
            'time to encode corpus': rag.time_to_encode_corpus,
        })

    return avg_len, efficiency, full_acc, half_acc


def judged(rag:MetaRAG,ragConfig:MetaRagConfig,verbose=False):
    t1 = time.time()

    correct = 0
    incorrect = 0
    invalidJudgment = 0

    counter = 0

    all_llm_answer_len = 0
    # correct_retrieved_length = 0

    tqdm_loop = tqdm(ragConfig.qas.iterrows(), total=len(ragConfig.qas), desc="Evaluating",disable=not ragConfig.fine_grain_progressbar)
    for row in tqdm_loop:
        counter += 1
        query = row[1]['question']

        if ragConfig.multi_hop:
            answer1 = row[1]['answer1']
            answer2 = row[1]['answer2']
            ground_truth = f"{answer1}\n\n{answer2}"
        else:
            ground_truth = row[1]['answer']

        llm_answer = rag.ask(query, include_prompt=False, top_k=ragConfig.top_k, useTool=ragConfig.useTool)

        judgement = ragConfig.judge.judge(question=query, ground_truth=ground_truth, answer=llm_answer)

        llm_answer_len = token_len(llm_answer)

        all_llm_answer_len += llm_answer_len

        if "yes" in judgement.lower():
            correct += 1
        elif "no" in judgement.lower() and "Error" not in llm_answer:
            incorrect += 1
        else:
            invalidJudgment += 1

        if verbose:
            print0(f'query : {query}\n ground_truth : {ground_truth}\n answer : {llm_answer}\n judgement : {judgement}')

        correct_perc = correct / counter
        incorrect_perc = incorrect / counter
        invalidJudgment_perc = invalidJudgment / counter

        avg_len = math.floor(all_llm_answer_len / counter)
        efficiency = math.floor((correct_perc * 100) ** 3 / avg_len)

        tqdm_loop.set_postfix(
            {'Correct': correct_perc, 'Incorrect': incorrect_perc, 'Invalid Judgment': invalidJudgment_perc,
             'Avg retrieved length': str(avg_len),
             'Efficiency': str(efficiency)})

    total_time = time.time() - t1
    print0()
    print0(f'Test Results for k = {ragConfig.top_k} :')
    print0(f'Correct : {correct} out of {counter} = {correct_perc} ')
    print0(f'Incorrect : {incorrect} out of {counter} = {incorrect_perc} ')
    print0(f'Invalid Judgment : {invalidJudgment} out of {counter} = {invalidJudgment_perc} ')
    print0(f'Length Accuracy Efficiency : {efficiency} ')
    print0(f'Average retrieved length : {avg_len}')
    print0(f'Total time : {total_time}')

    if Constants.use_wandb:
        wandb.log({
            'k': ragConfig.top_k,
            'chunk_size': rag.chunk_size,
            'Correct': correct_perc,
            'Incorrect': incorrect_perc,
            'Invalid Judgment': invalidJudgment_perc,
            'Avg retrieved length': avg_len,
            'Efficiency': efficiency,
            'Total time': total_time,
            'corpus size': len(rag.ChunksList),
            'time to encode corpus': rag.time_to_encode_corpus,
            'Correct to Valid ratio': correct / (correct + incorrect),
        })

    return avg_len, efficiency, correct_perc, incorrect_perc, invalidJudgment_perc


def test_retrival(ragConfig: MetaRagConfig, rag:MetaRAG=None, manage_wandb=True):
    print0("-----------------------------")
    if ragConfig.fine_grain_progressbar:print(f"\nNEW TEST multi_hop:{ragConfig.multi_hop} for encoder : {ragConfig.encoder.model_name}")
    print0("-----------------------------")

    if Constants.use_wandb and manage_wandb:
        if ragConfig.project_name is None or ragConfig.run_name is None:
            print("You need to provide wandb_project_name and wandb_config_name or set Constants.use_wandb to False")

        MRUtils.init_wandb(project_name=ragConfig.project_name, run_name=ragConfig.run_name,
                           config=ragConfig.toDict())

    if rag is None:
        rag = MetaRAG(encoder_model=ragConfig.encoder, llm=ragConfig.llm)
        reset_All = True
    else:
        reset_All = False

    rag.apply_config(ragConfig)

    if reset_All:
        rag.add_corpus(ragConfig.contexts)

    if verbose_run: rag.report()

    if (ragConfig.judge is not None and ragConfig.llm is None) or (
            ragConfig.judge is None and ragConfig.llm is not None):
        print("You need to provide both judge and llm or none of them")
        return


    if ragConfig.llm is not None and ragConfig.judge is not None:
        res = judged(rag,ragConfig)
    else:
        if ragConfig.multi_hop:
            res = full_test_find_in_multiHop(rag,ragConfig)
        else:
            res = full_test_find_in(rag,ragConfig)



    gc.collect()

    return rag, res


def print0(s="\n"):
    if verbose_run: print(s)
