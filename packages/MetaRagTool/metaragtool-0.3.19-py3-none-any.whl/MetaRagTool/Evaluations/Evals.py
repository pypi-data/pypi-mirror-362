import gc

from tqdm import tqdm
import wandb

from MetaRagTool import Constants
from MetaRagTool.RAG.Chunkers import ChunkingMethod


def basic_eval(evaluatable_rag, sample_size=200, qa_sample_size=100, top_k=None,multi_hop_hardness_factor=0,run_name=None,
               log_all_retrival_results =False,multi_hop=True,custom_dataset=None,wandb_group=None):
    import MetaRagTool.Evaluations.TestManager as TestManager
    import MetaRagTool.Utils.MRUtils as MRUtils
    import MetaRagTool.Utils.DataLoader as DataLoader
    from MetaRagTool.Utils.MetaRagConfig import MetaRagConfig
    TestManager.verbose_run = log_all_retrival_results

    if run_name is None:
        run_name=evaluatable_rag.__class__.__name__

    Constants.use_wandb = True
    if custom_dataset is not None:
        contexts, qa = custom_dataset
        multi_hop=False
    else:
        contexts, qa = DataLoader.loadWikiFaQa(sample_size=sample_size, qa_sample_size=qa_sample_size, multi_hop_hardness_factor =multi_hop_hardness_factor,multi_hop=multi_hop)
    evaluatable_rag.add_corpus(contexts)
    ragConfig = MetaRagConfig(qas=qa,fine_grain_progressbar = top_k is not None,wandb_group=wandb_group)

    eval_k_base = [1, 5, 10, 15, 20, 30, 40, 50, 70, 100]






    if top_k is not None:
        eval_k_base = [top_k]

    MRUtils.init_wandb(project_name="retrival", run_name=run_name,config=ragConfig.toDict(),group=ragConfig.wandb_group)
    loop = tqdm(eval_k_base, desc='Evaluating', total=len(eval_k_base), disable=ragConfig.fine_grain_progressbar)
    for k in loop:
        ragConfig.top_k=k
        if multi_hop:
            TestManager.full_test_find_in_multiHop(rag=evaluatable_rag,ragConfig=ragConfig,verbose=True)
        else:
            TestManager.full_test_find_in(rag=evaluatable_rag,ragConfig=ragConfig,verbose=True)
        loop.set_postfix({'K': k, 'Run': run_name})






    print("Finished testing")
    wandb.finish(quiet=True)



def god_eval(encoder_name, sample_size=200, qa_sample_size=100, multi_hop_hardness_factor=0,
             judged=False, top_k=None, useTool=False, llm=None, reranker_name=None,tests=[],custom_data=None,
             custom_project_name=None,wandb_group=None):
    import MetaRagTool.Evaluations.TestManager as TestManager
    import MetaRagTool.Utils.MRUtils as MRUtils
    from MetaRagTool.Encoders import CrossEncoderReranker

    gc.collect()

    ragConfig = MRUtils.Init(encoder_name=encoder_name, top_k=top_k, sample_size=sample_size,
                             qa_sample_size=qa_sample_size,
                             multi_hop_hardness_factor=multi_hop_hardness_factor, judged=judged, useTool=useTool,
                             multi_hop=True,llm=llm,custom_data=custom_data,custom_project_name=custom_project_name,wandb_group=wandb_group)

    eval_k_base = [1, 5, 10, 15, 20, 30, 40, 50, 70, 100]
    eval_k_half = [1, 3, 5, 8, 12, 18, 25, 33, 42, 50]
    eval_k_low_res = [1,5, 10, 30, 50]
    if top_k is not None:
        eval_k_base = [top_k]
        eval_k_half = [top_k]
        eval_k_low_res = [top_k]

    ragConfig.fine_grain_progressbar = top_k is not None

    encoder_name = f"s{sample_size}_{encoder_name}"
    if multi_hop_hardness_factor != 0:
        encoder_name += f"_hard{multi_hop_hardness_factor}"
    if top_k is not None:
        encoder_name += f"_k{top_k}"

    ragConfig.encoder_name = encoder_name

    def run_test(ks, ragConfig0, rag0):

        loop = tqdm(ks, desc='Evaluating', total=len(ks), disable=ragConfig.fine_grain_progressbar)
        for k0 in loop:
            ragConfig0.top_k = k0
            rag0, results = TestManager.test_retrival(ragConfig=ragConfig0, rag=rag0)
            loop.set_postfix({'K': k0, 'Run': ragConfig0.run_name})
        wandb.finish()
        print("Finished testing")

        return rag0


    rag = None
    ragConfig.reset_rag_attributes()
    ragConfig.run_name = encoder_name
    rag = run_test(eval_k_base, ragConfig, rag)

    if 'r' in tests:
        ragConfig.reset_rag_attributes()
        ragConfig.run_name = f"{encoder_name}_reranked"
        ragConfig.rerank = True
        ragConfig.reranker = CrossEncoderReranker(model_name=reranker_name)
        rag = run_test(eval_k_low_res, ragConfig, rag)


    if 'e' in tests:
        ragConfig.reset_rag_attributes()
        ragConfig.run_name = f"{encoder_name}_enhanced"
        ragConfig.add_neighbor_chunks_smart = True
        ragConfig.replace_retrieved_chunks_with_parent_paragraph = True
        rag = run_test(eval_k_half, ragConfig, rag)



    if 'n' in tests:
        ragConfig.reset_rag_attributes()
        ragConfig.run_name= f"{encoder_name}_add_neighbor_smart"
        ragConfig.add_neighbor_chunks_smart=True
        rag=run_test(eval_k_half,ragConfig,rag)

    if 'rp' in tests:
        ragConfig.reset_rag_attributes()
        ragConfig.run_name= f"{encoder_name}_replace_with_paragraph"
        ragConfig.replace_retrieved_chunks_with_parent_paragraph=True
        rag=run_test(eval_k_half,ragConfig,rag)

    if 'dfs' in tests:
        ragConfig.reset_rag_attributes()
        ragConfig.run_name= f"{encoder_name}_depth_first_retrival"
        ragConfig.depth_first_retrival = True
        rag=run_test(eval_k_half,ragConfig,rag)

    if 'edfs' in tests:
        ragConfig.reset_rag_attributes()
        ragConfig.run_name= f"{encoder_name}_enhanced_depth_first_retrival"
        ragConfig.depth_first_retrival = True
        ragConfig.add_neighbor_chunks_smart=True
        ragConfig.replace_retrieved_chunks_with_parent_paragraph=True
        rag=run_test(eval_k_half,ragConfig,rag)

    if 'bfs' in tests:
        ragConfig.reset_rag_attributes()
        ragConfig.run_name= f"{encoder_name}_breath_first_retrival"
        ragConfig.breath_first_retrival = True
        rag=run_test(eval_k_half,ragConfig,rag)

    if 'ebfs' in tests:
        ragConfig.reset_rag_attributes()
        ragConfig.run_name= f"{encoder_name}_enhanced_breath_first_retrival"
        ragConfig.breath_first_retrival = True
        ragConfig.add_neighbor_chunks_smart=True
        ragConfig.replace_retrieved_chunks_with_parent_paragraph=True
        rag=run_test(eval_k_half,ragConfig,rag)

    if 'wbfs' in tests:
        ragConfig.reset_rag_attributes()
        ragConfig.run_name= f"{encoder_name}_weighted_bfs_retrival"
        ragConfig.weighted_bfs = True
        rag=run_test(eval_k_half,ragConfig,rag)

    if 'ewbfs' in tests:
        ragConfig.reset_rag_attributes()
        ragConfig.run_name= f"{encoder_name}_enhanced_weighted_bfs_retrival"
        ragConfig.weighted_bfs = True
        ragConfig.add_neighbor_chunks_smart=True
        ragConfig.replace_retrieved_chunks_with_parent_paragraph=True
        rag=run_test(eval_k_half,ragConfig,rag)

    if 'refl' in tests:
        ragConfig.reset_rag_attributes()
        ragConfig.run_name= f"{encoder_name}_reflections"
        ragConfig.include_reflections = True
        rag=run_test(eval_k_half,ragConfig,rag)

    if 'refr' in tests:
        ragConfig.reset_rag_attributes()
        ragConfig.run_name= f"{encoder_name}_refractions"
        ragConfig.include_refractions = True
        rag=run_test(eval_k_half,ragConfig,rag)




    if 'sent' in tests:
        rag=None
        ragConfig.reset_rag_attributes()
        ragConfig.run_name= f"{encoder_name}_sentence"
        ragConfig.splitting_method=ChunkingMethod.SENTENCE
        rag=run_test(eval_k_base,ragConfig,rag)


    if 'rec' in tests:
        rag=None
        ragConfig.reset_rag_attributes()
        ragConfig.run_name= f"{encoder_name}_recursive"
        ragConfig.splitting_method=ChunkingMethod.RECURSIVE
        rag=run_test(eval_k_base,ragConfig,rag)


    if 'par' in tests:
        rag=None
        ragConfig.reset_rag_attributes()
        ragConfig.run_name= f"{encoder_name}_PARAGRAPH"
        ragConfig.splitting_method=ChunkingMethod.PARAGRAPH
        rag=run_test(eval_k_base,ragConfig,rag)


    if 'sentmc' in tests:
        rag=None
        ragConfig.reset_rag_attributes()
        ragConfig.run_name= f"{encoder_name}_SENTENCE_MERGER_CROSS_PARAGRAPH"
        ragConfig.splitting_method=ChunkingMethod.SENTENCE_MERGER_CROSS_PARAGRAPH
        rag=run_test(eval_k_base,ragConfig,rag)


    if 'embp' in tests:
        rag=None
        ragConfig.reset_rag_attributes()
        ragConfig.run_name= f"{encoder_name}_use_parentParagraph_embeddings"
        ragConfig.use_parentParagraph_embeddings=True
        rag=run_test(eval_k_base,ragConfig,rag)

        if 'embpe' in tests:
            ragConfig.reset_rag_attributes()
            ragConfig.run_name= f"{encoder_name}_use_parentParagraph_embeddings_enhanced"
            ragConfig.use_parentParagraph_embeddings=True
            ragConfig.add_neighbor_chunks_smart=True
            ragConfig.replace_retrieved_chunks_with_parent_paragraph=True
            rag=run_test(eval_k_half,ragConfig,rag)

    if 'embn' in tests:
        rag=None
        ragConfig.reset_rag_attributes()
        ragConfig.run_name= f"{encoder_name}_use_neighbor_embeddings"
        ragConfig.use_neighbor_embeddings=True
        rag=run_test(eval_k_base,ragConfig,rag)

        if 'embne' in tests:
            ragConfig.reset_rag_attributes()
            ragConfig.run_name= f"{encoder_name}_use_neighbor_embeddings_enhanced"
            ragConfig.use_neighbor_embeddings=True
            ragConfig.add_neighbor_chunks_smart=True
            ragConfig.replace_retrieved_chunks_with_parent_paragraph=True
            rag=run_test(eval_k_half,ragConfig,rag)

    if 'embr' in tests:
        rag=None
        ragConfig.reset_rag_attributes()
        ragConfig.run_name= f"{encoder_name}_enriched_embeddings"
        ragConfig.use_neighbor_embeddings=True
        ragConfig.use_parentParagraph_embeddings=True
        ragConfig.embedding_steering_influence_factor=0.2
        rag=run_test(eval_k_base,ragConfig,rag)

        if 'embre' in tests:
            ragConfig.reset_rag_attributes()
            ragConfig.run_name=f"{encoder_name}_enriched_embeddings_enhanced"
            ragConfig.use_neighbor_embeddings=True
            ragConfig.use_parentParagraph_embeddings=True
            ragConfig.embedding_steering_influence_factor=0.2
            ragConfig.replace_retrieved_chunks_with_parent_paragraph=True
            ragConfig.add_neighbor_chunks_smart=True
            rag=run_test(eval_k_half,ragConfig,rag)


    if 'norm' in tests:
        rag=None
        ragConfig.reset_rag_attributes()
        ragConfig.run_name=f"{encoder_name}_Normalized_text"
        rag.normalizer=None
        ragConfig.normalize_text=True
        rag=run_test(eval_k_base,ragConfig,rag)

    if 'best' in tests:
        rag = None
        ragConfig.reset_rag_attributes()
        ragConfig.run_name = f"{encoder_name}_godmode"
        ragConfig.add_neighbor_chunks_smart = True
        ragConfig.replace_retrieved_chunks_with_parent_paragraph = True
        ragConfig.use_neighbor_embeddings = True
        ragConfig.use_parentParagraph_embeddings = True
        ragConfig.embedding_steering_influence_factor = 0.2
        ragConfig.rerank = True
        ragConfig.reranker = CrossEncoderReranker(model_name=reranker_name)
        rag = run_test(eval_k_low_res, ragConfig, rag)

    if 'bestnr' in tests:
        rag = None
        ragConfig.reset_rag_attributes()
        ragConfig.run_name = f"{encoder_name}_godMode_no_rerank"
        # ragConfig.normalize_text=True
        ragConfig.use_neighbor_embeddings = True
        ragConfig.use_parentParagraph_embeddings = True
        ragConfig.embedding_steering_influence_factor = 0.2
        ragConfig.replace_retrieved_chunks_with_parent_paragraph = True
        ragConfig.add_neighbor_chunks_smart = True
        rag = run_test(eval_k_half, ragConfig, rag)

    gc.collect()




def test_rerankers(reranker_names=None,encoder_name='sentence-transformers/LaBSE', sample_size=200, qa_sample_size=100, multi_hop_hardness_factor=0,top_k=None,custom_project_name=None,wandb_group=None):
    import MetaRagTool.Evaluations.TestManager as TestManager
    import MetaRagTool.Utils.MRUtils as MRUtils
    from MetaRagTool.Encoders import CrossEncoderReranker

    if reranker_names is None:
        reranker_names = [

            # r=CrossEncoderReranker('bartowski/lb-reranker-0.5B-v1.0-GGUF') #error when loadding
            # r=CrossEncoderReranker('mixedbread-ai/mxbai-rerank-large-v2') #error when infer
            # r=CrossEncoderReranker('mixedbread-ai/mxbai-rerank-base-v2') #error when infer
            'Alibaba-NLP/gte-multilingual-reranker-base',
            "cross-encoder/ms-marco-MiniLM-L-6-v2",
            'cross-encoder/ms-marco-electra-base',
            'cross-encoder/ms-marco-MiniLM-L12-v2',
            'cross-encoder/mmarco-mMiniLMv2-L12-H384-v1',
            'cross-encoder/ms-marco-TinyBERT-L2-v2',
             'cross-encoder/stsb-roberta-large',
            'cross-encoder/monoelectra-base',
            'cross-encoder/stsb-distilroberta-base'
            'BAAI/bge-reranker-v2-m3',
            'BAAI/bge-reranker-large',
            'Omartificial-Intelligence-Space/ARA-Reranker-V1',
            'NAMAA-Space/GATE-Reranker-V1',
            'NAMAA-Space/Namaa-Reranker-v1',
            'jinaai/jina-reranker-v2-base-multilingual'
        ]



        good_reranker_names =[
            'Alibaba-NLP/gte-multilingual-reranker-base',
            'cross-encoder/mmarco-mMiniLMv2-L12-H384-v1',
            'BAAI/bge-reranker-v2-m3',
            'BAAI/bge-reranker-large',
            'Omartificial-Intelligence-Space/ARA-Reranker-V1',
            'jinaai/jina-reranker-v2-base-multilingual'

        ]


    ragConfig = MRUtils.Init(encoder_name=encoder_name, top_k=top_k, sample_size=sample_size,
                             qa_sample_size=qa_sample_size,
                             multi_hop_hardness_factor=multi_hop_hardness_factor, judged=False, useTool=False,
                             multi_hop=True,custom_project_name=custom_project_name,wandb_group=wandb_group)

    eval_k_base = [1,5, 10, 30, 50,80]


    if top_k is not None:
        eval_k_base = [top_k]

    ragConfig.fine_grain_progressbar = top_k is not None

    encoder_name = f"s{sample_size}_{encoder_name}"
    if multi_hop_hardness_factor != 0:
        encoder_name += f"_hard{multi_hop_hardness_factor}"
    if top_k is not None:
        encoder_name += f"_k{top_k}"

    ragConfig.encoder_name = encoder_name

    def run_test(ks, ragConfig0, rag0):
        loop = tqdm(ks, desc='Evaluating', total=len(ks), disable=ragConfig.fine_grain_progressbar)
        for k0 in loop:
            ragConfig0.top_k = k0
            rag0, results = TestManager.test_retrival(ragConfig=ragConfig0, rag=rag0)
            loop.set_postfix({'K': k0, 'Run': ragConfig0.run_name})
        wandb.finish()
        return rag0

    rag = None
    ragConfig.reset_rag_attributes()
    ragConfig.run_name = encoder_name
    rag = run_test(eval_k_base, ragConfig, rag)

    for reranker_name in reranker_names:
        gc.collect()
        ragConfig.reset_rag_attributes()
        ragConfig.run_name = f"{encoder_name}_reranked_{reranker_name}"
        ragConfig.rerank = True
        ragConfig.reranker = CrossEncoderReranker(model_name=reranker_name)
        rag = run_test(eval_k_base, ragConfig, rag)







def embedding_steering_influence_factor(encoder_name, sample_size=200, qa_sample_size=100, multi_hop_hardness_factor=0,
             judged=False, top_k=None, useTool=False, llm=None,custom_data=None,custom_project_name=None,wandb_group=None):
    import MetaRagTool.Evaluations.TestManager as TestManager
    import MetaRagTool.Utils.MRUtils as MRUtils

    gc.collect()

    ragConfig = MRUtils.Init(encoder_name=encoder_name, top_k=top_k, sample_size=sample_size,
                             qa_sample_size=qa_sample_size,
                             multi_hop_hardness_factor=multi_hop_hardness_factor, judged=judged, useTool=useTool,
                             multi_hop=True,llm=llm,custom_data=custom_data,custom_project_name=custom_project_name,wandb_group=wandb_group)

    eval_k_base = [1, 5, 10, 15, 20, 30, 40, 50, 70, 100]


    if top_k is not None:
        eval_k_base = [top_k]

    ragConfig.fine_grain_progressbar = top_k is not None

    encoder_name = f"s{sample_size}_{encoder_name}"
    if multi_hop_hardness_factor != 0:
        encoder_name += f"_hard{multi_hop_hardness_factor}"
    if top_k is not None:
        encoder_name += f"_k{top_k}"

    ragConfig.encoder_name = encoder_name

    def run_test(ks, ragConfig0, rag0):

        loop = tqdm(ks, desc='Evaluating', total=len(ks), disable=ragConfig.fine_grain_progressbar)
        for k0 in loop:
            ragConfig0.top_k = k0
            rag0, results = TestManager.test_retrival(ragConfig=ragConfig0, rag=rag0)
            loop.set_postfix({'K': k0, 'Run': ragConfig0.run_name})
        wandb.finish()
        print("Finished testing")

        return rag0


    for embedding_steering_influence_factor_value in [0.05,0.1, 0.2, 0.3, 0.4,0.6,0.8]:

        rag = None
        ragConfig.reset_rag_attributes()
        ragConfig.run_name = f"{encoder_name}_enriched_embeddings_alpha={embedding_steering_influence_factor_value}"
        ragConfig.use_neighbor_embeddings = True
        ragConfig.use_parentParagraph_embeddings = True
        ragConfig.embedding_steering_influence_factor = embedding_steering_influence_factor_value
        rag = run_test(eval_k_base, ragConfig, rag)






#
#
# def qa_ratio_impact(encoder_name="sentence-transformers/LaBSE", local_mode=False):
#     Constants.local_mode = local_mode
#     Constants.use_wandb = True
#     encoder = SentenceTransformerEncoder(encoder_name)
#     sample_size = -1
#     rag = None
#     contexts, qas = DataLoader.loadWikiFaQa(sample_size=sample_size, multi_hop=True, qa_sample_ratio=1)
#     qa_ratios = [0.01, 0.02, 0.04, 0.06, 0.08, 0.1, 0.2, 0.3, 0.4, 0.5, 0.7, 1]
#
#     MyUtils.init_wandb(project_name="qa_sample_ratio", run_name=encoder_name)
#     for qa_ratio in qa_ratios:
#         _, qas = DataLoader.loadWikiFaQa(sample_size=sample_size, multi_hop=True, qa_sample_ratio=qa_ratio)
#         rag, res = TestManager.test_retrival(encoder, contexts, qas, rag=rag,
#                                              splitting_method=ChunkingMethod.SENTENCE_MERGER,
#                                              log_chunking_report=False, top_k=20, multi_hop=True)
#     wandb.finish()
#
#     MyUtils.init_wandb(project_name="qa_sample_ratio", run_name=f"{encoder_name}_enhanced")
#     for qa_ratio in qa_ratios:
#         _, qas = DataLoader.loadWikiFaQa(sample_size=sample_size, multi_hop=True, qa_sample_ratio=qa_ratio)
#         rag, res = TestManager.test_retrival(encoder, contexts, qas, rag=rag,
#                                              splitting_method=ChunkingMethod.SENTENCE_MERGER,
#                                              log_chunking_report=False, top_k=20, multi_hop=True,
#                                              add_neighbor_chunks_smart=True,
#                                              replace_retrieved_chunks_with_parent_paragraph=True)
#     wandb.finish()
#
#
# def encoder_on_chunk_size(encoder_name, sample_size=500, qa_sample_size=100, local_mode=False):
#     Constants.local_mode = local_mode
#     Constants.use_wandb = True
#     contexts, qas = DataLoader.loadWikiFaQa(sample_size=sample_size, qa_sample_size=qa_sample_size, multi_hop=True)
#     encoder = SentenceTransformerEncoder(encoder_name)
#
#     chunk_size_eval_range = range(3, 15)
#     chunk_size_eval_step = 10
#
#     MyUtils.init_wandb(project_name="testingChunkingSizeFair", run_name=f"not_fair_{encoder_name}")
#     for i in chunk_size_eval_range:
#         size = i * chunk_size_eval_step
#         TestManager.test_retrival(encoder, contexts, qas, llm=None, splitting_method=ChunkingMethod.SENTENCE_MERGER,
#                                   top_k=20, multi_hop=True, log_chunking_report=False, chunk_size=size)
#         gc.collect()
#
#     wandb.finish()
#
#     MyUtils.init_wandb(project_name="testingChunkingSizeFair", run_name=f"not_fair_{encoder_name}_enhanced")
#     for i in chunk_size_eval_range:
#         size = i * chunk_size_eval_step
#         TestManager.test_retrival(encoder, contexts, qas, llm=None, splitting_method=ChunkingMethod.SENTENCE_MERGER,
#                                   top_k=20, multi_hop=True, log_chunking_report=False, chunk_size=size,
#                                   add_neighbor_chunks_smart=True,
#                                   replace_retrieved_chunks_with_parent_paragraph=True)
#         gc.collect()
#
#     wandb.finish()
#
#
# def encoder_on_chunk_size_fair(encoder_name, sample_size=500, qa_sample_size=100, local_mode=False):
#     Constants.local_mode = local_mode
#     Constants.use_wandb = True
#     contexts, qas = DataLoader.loadWikiFaQa(sample_size=sample_size, qa_sample_size=qa_sample_size, multi_hop=True)
#     encoder = SentenceTransformerEncoder(encoder_name)
#
#     constant_k_chunk_size = 900
#     chunk_size_eval_range = range(3, 15)
#     chunk_size_eval_step = 10
#
#     MyUtils.init_wandb(project_name="testingChunkingSizeFair", run_name=encoder_name)
#     for i in chunk_size_eval_range:
#         size = i * chunk_size_eval_step
#         k = constant_k_chunk_size // size
#         TestManager.test_retrival(encoder, contexts, qas, llm=None, splitting_method=ChunkingMethod.SENTENCE_MERGER,
#                                   top_k=k, multi_hop=True, log_chunking_report=False, chunk_size=size)
#         gc.collect()
#
#     wandb.finish()
#
#     MyUtils.init_wandb(project_name="testingChunkingSizeFair", run_name=f"{encoder_name}_enhanced")
#     for i in chunk_size_eval_range:
#         size = i * chunk_size_eval_step
#         k = constant_k_chunk_size // size
#         TestManager.test_retrival(encoder, contexts, qas, llm=None, splitting_method=ChunkingMethod.SENTENCE_MERGER,
#                                   top_k=k, multi_hop=True, log_chunking_report=False, chunk_size=size,
#                                   add_neighbor_chunks_smart=True,
#                                   replace_retrieved_chunks_with_parent_paragraph=True)
#         gc.collect()
#
#     wandb.finish()
#
#
# def corpus_size(encoder_name, local_mode=False):
#     llm = None
#     Constants.local_mode = local_mode
#     Constants.use_wandb = True
#
#     contexts, qas = DataLoader.loadWikiFaQa(sample_size=50, multi_hop=True, qa_sample_size=100)
#     all_contexts, all_qas = DataLoader.loadWikiFaQa(multi_hop=True)
#
#     # remove contexts from all_contexts (contexts is a list of strings)
#     all_contexts = [context for context in all_contexts if context not in contexts]
#     encoder = SentenceTransformerEncoder(encoder_name)
#
#     MyUtils.init_wandb(project_name="CorpusSize", run_name=encoder_name)
#     rag, res = TestManager.test_retrival(encoder, contexts, qas, llm=llm,
#                                          splitting_method=ChunkingMethod.SENTENCE_MERGER,
#                                          log_chunking_report=False, top_k=20, multi_hop=True)
#     batch_size = 100
#     for i in range(0, len(all_contexts), batch_size):
#         batch = all_contexts[i:i + batch_size]
#         rag.add_corpus(batch)
#         TestManager.test_retrival(encoder, contexts, qas, llm=llm, rag=rag,
#                                   splitting_method=ChunkingMethod.SENTENCE_MERGER,
#                                   log_chunking_report=False, top_k=20, multi_hop=True)
#
#     wandb.finish()
#
