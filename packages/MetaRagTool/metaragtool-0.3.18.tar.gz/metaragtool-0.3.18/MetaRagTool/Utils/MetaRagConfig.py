from MetaRagTool.RAG.Chunkers import ChunkingMethod

class MetaRagConfig:
    def __init__(self, encoder=None, contexts=None, qas=None, llm=None, splitting_method=ChunkingMethod.SENTENCE_MERGER,
                 chunk_size=90, chunk_overlap=3, top_k=20, use_neighbor_embeddings=False
                 , add_neighbor_chunks=False, add_neighbor_chunks_smart=False,
                 breath_first_retrival=False
                 , depth_first_retrival=False, replace_retrieved_chunks_with_parent_paragraph=False
                 , normalize_text=False, use_parentParagraph_embeddings=False, max_sentence_len=-1,reranker=None,rerank=False,
                 additional_top_k=5, include_reflections=False,
                 include_reflections_k=1, include_refractions=False, sent_merge_merged_chunks=True, multi_hop=False,
                 log_chunking_report=False, weighted_bfs=False,
                 embedding_steering_influence_factor=0.35,
                 add_neighbor_chunks_k=2, judge=None, useTool=False, project_name=None, run_name=None,
                 encoder_name=None, sample_size=None, qa_sample_size=None,
                 multi_hop_hardness_factor=None, judged=None, llm_name=None,fine_grain_progressbar=True

                 ):
        self.fine_grain_progressbar = fine_grain_progressbar
        self.encoder = encoder
        self.contexts = contexts
        self.qas = qas
        self.llm = llm
        self.splitting_method = splitting_method
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.top_k = top_k
        self.use_neighbor_embeddings = use_neighbor_embeddings
        self.add_neighbor_chunks = add_neighbor_chunks
        self.add_neighbor_chunks_smart = add_neighbor_chunks_smart
        self.breath_first_retrival = breath_first_retrival
        self.depth_first_retrival = depth_first_retrival
        self.replace_retrieved_chunks_with_parent_paragraph = replace_retrieved_chunks_with_parent_paragraph
        self.normalize_text = normalize_text
        self.use_parentParagraph_embeddings = use_parentParagraph_embeddings
        if max_sentence_len == -1:
            max_sentence_len = chunk_size
        self.max_sentence_len = max_sentence_len
        self.additional_top_k = additional_top_k
        self.include_reflections = include_reflections
        self.include_reflections_k = include_reflections_k
        self.include_refractions = include_refractions
        self.sent_merge_merged_chunks = sent_merge_merged_chunks
        self.multi_hop = multi_hop
        self.log_chunking_report = log_chunking_report
        self.weighted_bfs = weighted_bfs
        self.embedding_steering_influence_factor = embedding_steering_influence_factor
        self.add_neighbor_chunks_k = add_neighbor_chunks_k
        self.judge = judge
        self.useTool = useTool
        self.project_name = project_name
        self.run_name = run_name

        self.encoder_name = encoder_name
        self.sample_size = sample_size
        self.qa_sample_size = qa_sample_size
        self.multi_hop_hardness_factor = multi_hop_hardness_factor
        self.judged = judged
        self.llm_name = llm_name
        self.reranker = reranker
        self.rerank = rerank

    def toDict(self):
        return {
            "splitting_method": self.splitting_method,
            "chunk_size": self.chunk_size,
            "chunk_overlap": self.chunk_overlap,
            "top_k": self.top_k,
            "use_neighbor_embeddings": self.use_neighbor_embeddings,
            "add_neighbor_chunks": self.add_neighbor_chunks,
            "add_neighbor_chunks_smart": self.add_neighbor_chunks_smart,
            "breath_first_retrival": self.breath_first_retrival,
            "depth_first_retrival": self.depth_first_retrival,
            "replace_retrieved_chunks_with_parent_paragraph": self.replace_retrieved_chunks_with_parent_paragraph,
            "normalize_text": self.normalize_text,
            "use_parentParagraph_embeddings": self.use_parentParagraph_embeddings,
            "max_sentence_len": self.max_sentence_len,
            "additional_top_k": self.additional_top_k,
            "include_reflections": self.include_reflections,
            "include_reflections_k": self.include_reflections_k,
            "include_refractions": self.include_refractions,
            "sent_merge_merged_chunks": self.sent_merge_merged_chunks,
            "multi_hop": self.multi_hop,
            "weighted_bfs": self.weighted_bfs,
            "embedding_steering_influence_factor": self.embedding_steering_influence_factor,
            "add_neighbor_chunks_k": self.add_neighbor_chunks_k,
            "rerank": self.rerank,
            "reranker_name": self.reranker.model_name if self.rerank else None,
            "useTool": self.useTool,
            "encoder_name": self.encoder_name,
            "sample_size": self.sample_size,
            "qa_sample_size": self.qa_sample_size,
            "multi_hop_hardness_factor": self.multi_hop_hardness_factor,
            "judged": self.judged,
            "llm_name": self.llm_name,

        }


    def reset_rag_attributes(self):
        defaultConfig = MetaRagConfig()
        self.log_chunking_report = defaultConfig.log_chunking_report
        self.sent_merge_merged_chunks = defaultConfig.sent_merge_merged_chunks
        self.add_neighbor_chunks_k = defaultConfig.add_neighbor_chunks_k
        self.embedding_steering_influence_factor = defaultConfig.embedding_steering_influence_factor
        self.splitting_method = defaultConfig.splitting_method
        self.chunk_size = defaultConfig.chunk_size
        self.chunk_overlap = defaultConfig.chunk_overlap
        self.use_neighbor_embeddings = defaultConfig.use_neighbor_embeddings
        self.use_parentParagraph_embeddings = defaultConfig.use_parentParagraph_embeddings
        self.add_neighbor_chunks = defaultConfig.add_neighbor_chunks
        self.add_neighbor_chunks_smart = defaultConfig.add_neighbor_chunks_smart
        self.breath_first_retrival = defaultConfig.breath_first_retrival
        self.weighted_bfs = defaultConfig.weighted_bfs
        self.depth_first_retrival = defaultConfig.depth_first_retrival
        self.additional_top_k = defaultConfig.additional_top_k
        self.replace_retrieved_chunks_with_parent_paragraph = defaultConfig.replace_retrieved_chunks_with_parent_paragraph
        self.normalize_text = defaultConfig.normalize_text
        self.include_reflections = defaultConfig.include_reflections
        self.include_reflections_k = defaultConfig.include_reflections_k
        self.include_refractions = defaultConfig.include_refractions
        self.rerank = defaultConfig.rerank


def get_baseline_config():
    return MetaRagConfig(splitting_method=ChunkingMethod.RECURSIVE)


def get_best_config():
    from MetaRagTool.Encoders import CrossEncoderReranker
    return MetaRagConfig(splitting_method=ChunkingMethod.SENTENCE_MERGER,
                         use_neighbor_embeddings=True, use_parentParagraph_embeddings=True,
                         replace_retrieved_chunks_with_parent_paragraph=True,
                         add_neighbor_chunks_smart=True,
                         embedding_steering_influence_factor=0.2,rerank=True,reranker=CrossEncoderReranker(model_name='cross-encoder/mmarco-mMiniLMv2-L12-H384-v1'))



