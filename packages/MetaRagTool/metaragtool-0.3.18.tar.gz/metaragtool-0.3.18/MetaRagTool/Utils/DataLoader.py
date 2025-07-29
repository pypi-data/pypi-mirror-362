def loadWikiFaQa(sample_size=-1, multi_hop = False,
                 random_seed=50, multi_hop_hardness_factor=0,custom_path=None,qa_sample_size=-1):
    from datasets import load_from_disk, load_dataset
    import pandas as pd
    import MetaRagTool.Constants as Constants

    if Constants.local_mode:
        path = 'D:\Library\MSc Ai\Thesis\Persian RAG\Datasets\synthetic data\\final\WikiFaQA'
        if multi_hop:
            path = f'D:\Library\MSc Ai\Thesis\Persian RAG\Datasets\synthetic data\\final\WikiFaQA_multiHop'

        existing_dataset = load_from_disk(path)
    else:
        path = 'codersan/WikiFaQA'
        if multi_hop:
            path = 'codersan/WikiFaQA_multiHop'
        if custom_path is not None:
            path = custom_path

        dataset_dict = load_dataset(path)
        existing_dataset = dataset_dict["train"]




    if sample_size != -1 and sample_size < len(existing_dataset):
        existing_dataset = existing_dataset.shuffle(seed=random_seed)
        existing_dataset = existing_dataset.select(range(sample_size))

    contexts = existing_dataset['context']
    exactPairs = existing_dataset['exactPairs']

    qa_data = []
    for pair_list in exactPairs:
        for pair in pair_list:
            if multi_hop:
                qa_data.append({
                    'question': pair['question'],
                    'answer1': pair['answer1'],
                    'answer2': pair['answer2'],
                    'distance': pair['distance'],
                })
            else:
                qa_data.append({
                    'question': pair['question'],
                    'answer': pair['answer']
                })

    qa = pd.DataFrame(qa_data)
    if multi_hop_hardness_factor==1:
        # top half of qa
        qa = qa[qa['distance'] >1077]


    elif multi_hop_hardness_factor==2:
        # top quarter of qa
        qa = qa[qa['distance'] > 4963]

    if qa_sample_size != -1 and qa_sample_size < len(qa):
        qa = qa.sample(qa_sample_size, random_state=random_seed)


    return contexts, qa



def load_long_rag(samplesize=-1, qa_sample_size=-1, random_seed=50,is_nq=True):
    from datasets import load_dataset

    path='codersan/LongRAG_nq_filtered'
    if not is_nq:
        path='codersan/LongRAG_hotpot_qa_filtered'
    data = load_dataset(path)
    data=data['full']
    if samplesize != -1 and samplesize < len(data):
        data = data.shuffle(seed=random_seed)
        data = data.select(range(samplesize))
    data=data.to_pandas()
    contexts=data['context'].tolist()
    qa=data.drop(columns=['context'])
    qa = qa.rename(columns={'query': 'question'})

    if qa_sample_size != -1 and qa_sample_size < len(qa):
        qa = qa.sample(qa_sample_size, random_state=random_seed)

    return contexts,qa



def load_scifact(qa_sample_size=-1,random_seed=50):
    from datasets import load_dataset
    data = load_dataset('codersan/scifact_filtered_corpus')
    data=data['train'].to_pandas()
    contexts=data['abstract'].tolist()
    data = load_dataset('codersan/scifact_filtered_claims')
    qa=data['train'].to_pandas()
    qa = qa.rename(columns={'claim': 'question', 'evidence_sentences_str': 'answer'})
    if qa_sample_size != -1 and qa_sample_size < len(qa):
        qa = qa.sample(qa_sample_size, random_state=random_seed)
    return contexts,qa
