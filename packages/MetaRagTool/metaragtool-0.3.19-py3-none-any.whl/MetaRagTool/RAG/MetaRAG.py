import time
import faiss
import numpy as np
from hazm import Normalizer

from MetaRagTool.RAG.Chunkers import ChunkerFactory
from MetaRagTool.RAG.DocumentStructs import MRSentence, MRDocument, MRParagraph, generate_document_structure
from MetaRagTool.RAG.Chunkers import ChunkingMethod

from MetaRagTool.Utils.MRUtils import capped_sent_tokenize, token_len, reflect_vector, remove_duplicates

from MetaRagTool.LLM.LLMIdentity import LLMIdentity
from MetaRagTool.Encoders.Encoder import Encoder
from MetaRagTool.Encoders.Reranker import Reranker



class MetaRAG:


    def __init__(self, encoder_model: Encoder, llm: LLMIdentity=None, reranker_model: Reranker = None,
                 splitting_method=ChunkingMethod.SENTENCE_MERGER, chunk_size=90, chunk_overlap=3, max_sentence_len=-1,
                 use_neighbor_embeddings=False
                 , use_parentParagraph_embeddings=False, add_neighbor_chunks=False, add_neighbor_chunks_smart=False,
                 breath_first_retrival=False
                 , depth_first_retrival=False,
                 replace_retrieved_chunks_with_parent_paragraph=False, normalize_text=False, normalizer=Normalizer(),
                 rerank=False,
                 additional_top_k=5, include_reflections=False,
                 include_refractions=False, sent_merge_merged_chunks=True, log_chunking_report=True, weighted_bfs=False,
                 embedding_steering_influence_factor=0.35, add_neighbor_chunks_k=2):



        self.add_neighbor_chunks_k = add_neighbor_chunks_k
        self.log_chunking_report = log_chunking_report
        self.additional_top_k = additional_top_k
        if max_sentence_len == -1:
            max_sentence_len = chunk_size
        self.max_sentence_len = max_sentence_len
        self.llm = llm
        self.splitting_method = splitting_method
        self.chunk_size = chunk_size
        self.encoder_model = encoder_model
        self.chunk_overlap = chunk_overlap
        self.index = None
        self.DocumentsList = []
        self.ChunksList = []
        self.use_neighbor_embeddings = use_neighbor_embeddings
        self.use_parentParagraph_embeddings = use_parentParagraph_embeddings
        self.add_neighbor_chunks = add_neighbor_chunks
        self.add_neighbor_chunks_smart = add_neighbor_chunks_smart
        self.breath_first_retrival = breath_first_retrival
        self.depth_first_retrival = depth_first_retrival
        self.replace_retrieved_chunks_with_parent_paragraph = replace_retrieved_chunks_with_parent_paragraph
        self.normalize_text = normalize_text
        self.normalizer = normalizer
        self.rerank = rerank
        self.reranker_model = reranker_model
        self.include_reflections = include_reflections
        self.include_refractions = include_refractions
        self.weighted_bfs = weighted_bfs
        self.embedding_steering_influence_factor=embedding_steering_influence_factor

        # merge small chunks into normal ones
        self.sent_merge_merged_chunks = sent_merge_merged_chunks
        self.time_to_encode_corpus = 0
        self.answer_mode='none'

        self.chunker = None

    def apply_best_config(self):
        from MetaRagTool.Utils import get_best_config
        bestConfig = get_best_config()
        self.apply_config(bestConfig)



    def report(self):
        default_values = {
            'splitting_method': None,
            'chunk_size': None,
            'chunk_overlap': 3,
            'max_sentence_len': 90,
            'use_neighbor_embeddings': False,
            'use_parentParagraph_embeddings': False,
            'add_neighbor_chunks': False,
            'add_neighbor_chunks_smart': False,
            'breath_first_retrival': False,
            'depth_first_retrival': False,
            'replace_retrieved_chunks_with_parent_paragraph': False,
            'normalize_text': False,
            'rerank': False,
            'additional_top_k': 5,
            'include_reflections': False,
            'include_refractions': False,
            'sent_merge_merged_chunks': True,
        }

        for param, default_value in default_values.items():
            current_value = getattr(self, param)
            if current_value != default_value:
                print(f"{param}: {current_value}")

    def apply_config(self, ragConfig):

        self.splitting_method = ragConfig.splitting_method
        self.chunk_size = ragConfig.chunk_size
        self.chunk_overlap = ragConfig.chunk_overlap
        self.max_sentence_len = ragConfig.max_sentence_len
        if self.max_sentence_len == -1:
            self.max_sentence_len = self.chunk_size
        self.use_neighbor_embeddings = ragConfig.use_neighbor_embeddings
        self.use_parentParagraph_embeddings = ragConfig.use_parentParagraph_embeddings
        self.add_neighbor_chunks = ragConfig.add_neighbor_chunks
        self.add_neighbor_chunks_smart = ragConfig.add_neighbor_chunks_smart
        self.breath_first_retrival = ragConfig.breath_first_retrival
        self.depth_first_retrival = ragConfig.depth_first_retrival
        self.replace_retrieved_chunks_with_parent_paragraph = ragConfig.replace_retrieved_chunks_with_parent_paragraph
        self.normalize_text = ragConfig.normalize_text
        self.include_reflections = ragConfig.include_reflections
        self.include_refractions = ragConfig.include_refractions
        self.sent_merge_merged_chunks = ragConfig.sent_merge_merged_chunks
        self.log_chunking_report = ragConfig.log_chunking_report
        self.add_neighbor_chunks_k = ragConfig.add_neighbor_chunks_k
        self.embedding_steering_influence_factor = ragConfig.embedding_steering_influence_factor
        self.weighted_bfs = ragConfig.weighted_bfs
        self.additional_top_k = ragConfig.additional_top_k
        self.include_reflections_k = ragConfig.include_reflections_k
        self.rerank = ragConfig.rerank
        self.reranker_model = ragConfig.reranker

    def _encode_and_index_dataset(self):
        if self.use_parentParagraph_embeddings:
            self._set_paragraph_embeddings()

        chunks_to_encode = [chunk for chunk in self.ChunksList if chunk.Embeddings is None]
        print(f"Number of chunks to encode: {len(chunks_to_encode)}")
        chunks_texts = [self.normalizer.normalize(chunk.Text) if self.normalize_text else chunk.Text for chunk in
                        chunks_to_encode]


        t1= time.time()

        # Step 2: Encode documents using a pre-trained model
        document_embeddings = self.encoder_model.encode(chunks_texts, isQuery=False)
        # print("Chunk encoding completed")

        # Convert embeddings to numpy array
        document_embeddings = np.array(document_embeddings)
        document_embeddings_copy = np.array(document_embeddings)
        # for each chunk, add the embedding of the next and previous chunk to it with a weight of 0.5
        if self.use_neighbor_embeddings:
            for i, chunk in enumerate(chunks_to_encode):
                if chunk.PrevRelated is not None:
                    document_embeddings[i] = document_embeddings[i] + self.embedding_steering_influence_factor * document_embeddings_copy[i - 1]
                if chunk.NextRelated is not None:
                    document_embeddings[i] = document_embeddings[i] + self.embedding_steering_influence_factor * document_embeddings_copy[i + 1]

        if self.use_parentParagraph_embeddings:
            for i, chunk in enumerate(chunks_to_encode):
                parentParagraphEmbedding = np.mean([p.Embeddings for p in chunk.Paragraphs],axis=0)
                parentParagraphEmbedding = parentParagraphEmbedding / np.linalg.norm(parentParagraphEmbedding)
                document_embeddings[i] = document_embeddings[i] + self.embedding_steering_influence_factor * parentParagraphEmbedding

        for i, chunk in enumerate(chunks_to_encode):
            chunk.Embeddings = document_embeddings[i]
        # Step 3: Index embeddings using FAISS
        embedding_dimension = document_embeddings.shape[1]
        if self.index is None:
            self.index = faiss.IndexFlatL2(embedding_dimension)

        faiss.normalize_L2(document_embeddings)
        self.index.add(document_embeddings)  # Add document embeddings to the index

        self.time_to_encode_corpus += (time.time()-t1)
        # print("Chunk indexing completed")

    def _set_paragraph_embeddings(self):
        paragraphs_to_encode = [paragraph for paragraph in self.allParagraphs if paragraph.Embeddings is None]
        print(f"Number of paragraphs to encode: {len(paragraphs_to_encode)}")
        paragraphs_texts = [paragraph.Text for paragraph in paragraphs_to_encode]

        # Step 2: Encode paragraphs using a pre-trained model
        paragraph_embeddings = self.encoder_model.encode(paragraphs_texts, isQuery=False)
        print("Paragraph encoding completed")

        # Convert embeddings to numpy array
        paragraph_embeddings = np.array(paragraph_embeddings)

        for i, paragraph in enumerate(paragraphs_to_encode):
            paragraph.Embeddings = paragraph_embeddings[i]


    def _chunkify(self):

        if self.chunker is None:
            self.chunker = ChunkerFactory.create_chunker(splitting_method=self.splitting_method, chunksList=self.ChunksList,
                                                         chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap, sent_merge_merged_chunks=self.sent_merge_merged_chunks)

        self.chunker.chunk_documents(self.DocumentsList)

        if self.log_chunking_report:self.chunker.chunking_report()




    def add_corpus(self, raw_documents_text: list,encode=True):
        self.allParagraphs,self.allSentences=generate_document_structure(rawDocumentsTexts=raw_documents_text,DocumentsList=self.DocumentsList,
                                    max_sentence_len=self.max_sentence_len if self.max_sentence_len != -1 else self.chunk_size)

        print(f"Corpus structure: {len(self.DocumentsList)} documents and {len(self.allParagraphs)} paragraphs and {len(self.allSentences)} sentences")


        self._chunkify()
        if encode:self._encode_and_index_dataset()

    def _retrieve_core(self, query_embedding, top_k):
        if top_k < 1:
            print("Error: top_k is set to 0, which is invalid.")
            return []

        query_embedding = np.array(query_embedding).reshape(1, -1)
        distances, indices = self.index.search(query_embedding, top_k)
        retrieved_chunks = [self.ChunksList[i] for i in indices[0]]
        return retrieved_chunks


    def _check_feature_compatibility(self):
        if self.splitting_method == ChunkingMethod.RECURSIVE and (self.replace_retrieved_chunks_with_parent_paragraph or self.add_neighbor_chunks or self.add_neighbor_chunks_smart):
            print("Error: Recursive splitting method is not compatible with replace_retrieved_chunks_with_parent_paragraph. Please set it to False.")
            self.replace_retrieved_chunks_with_parent_paragraph = False
            self.add_neighbor_chunks_smart = False
            self.add_neighbor_chunks = False

    def retrieve(self, query, top_k=20, force_basics=False):
        # if sum_of_retrieved_token_length_limit>0:
        #     # fixing top_k
        #     top_k = sum_of_retrieved_token_length_limit // self.chunk_size
        #     if self.replace_retrieved_chunks_with_parent_paragraph:
        #         top_k = top_k // 2
        #     if self.include_reflections or self.include_refractions:
        #         top_k = top_k // 2
        #     if self.add_neighbor_chunks or self.add_neighbor_chunks_smart:
        #         top_k = top_k // 2
        #     if self.breath_first_retrival or self.depth_first_retrival or self.weighted_bfs:
        #         top_k = top_k // 2

        self._check_feature_compatibility()


        if top_k<1:
            print("Error: top_k is set to 0, which is invalid.")
            top_k=1

        # Encode the query
        if self.normalize_text:
            query = self.normalizer.normalize(query)

        query_embedding = self.encoder_model.encode([query])

        retrieved_chunks = self._retrieve_core(query_embedding, top_k*5 if self.rerank else top_k)


        if self.rerank:
            if self.reranker_model is None: print("Error: Reranker model is not set. Please set the Reranker model before using it or set rerank=False")

            retrieved_chunks=self.reranker_model.apply_rerank_MRChunks(query=query, chunks=retrieved_chunks)
            retrieved_chunks = retrieved_chunks[: top_k]


        if self.breath_first_retrival and not force_basics:
            additional_chunks = []
            top_k_retrieved_chunks = retrieved_chunks[:top_k // 5]
            for chunk in top_k_retrieved_chunks:
                additional_chunks.extend(self._retrieve_core(chunk.Embeddings, self.additional_top_k))
            retrieved_chunks.extend(additional_chunks)
            retrieved_chunks = remove_duplicates(retrieved_chunks)


        elif self.depth_first_retrival and not force_basics and top_k > 1:
            # repeat retrieval for the first chunk with the original top_k value, depth_first_retrival_k times, each time with the retrieved chunks (like going deeper only in one branch of the tree)
            additional_chunks = []
            # Replace the empty section with:
            current_chunk = retrieved_chunks[0]  # Start with first retrieved chunk
            for _ in range(2):
                level_chunks = self._retrieve_core(current_chunk.Embeddings, top_k // 2)
                additional_chunks.extend(level_chunks)
                current_chunk = level_chunks[0]  # Go deeper with first chunk

            retrieved_chunks.extend(additional_chunks)
            retrieved_chunks = remove_duplicates(retrieved_chunks)

        elif self.weighted_bfs and not force_basics:
            additional_chunks = []
            for i, chunk in enumerate(retrieved_chunks):
                chunk_top_k = top_k // (2 ** (i + 1))
                if chunk_top_k < 1:
                    break
                additional_chunks.extend(self._retrieve_core(chunk.Embeddings, chunk_top_k))

            retrieved_chunks.extend(additional_chunks)
            retrieved_chunks = remove_duplicates(retrieved_chunks)


        if self.include_reflections:
            # for each retrieved chunk, get its reflection based on query and retrived only 1 more chunks with the new vector
            additional_chunks = []
            for chunk in retrieved_chunks:
                reflection = reflect_vector(query_embedding[0], chunk.Embeddings)
                reflection = np.array([reflection], dtype=np.float32)
                faiss.normalize_L2(reflection)
                additional_chunks.extend(self._retrieve_core(reflection, 1))

            retrieved_chunks.extend(additional_chunks)
            retrieved_chunks = remove_duplicates(retrieved_chunks)

        elif self.include_refractions:
            # for each retrieved chunk, newV=q-v and retrive the closest chunk to newV
            additional_chunks = []
            for chunk in retrieved_chunks:
                newV = query_embedding[0] - chunk.Embeddings
                newV = np.array([newV], dtype=np.float32)
                faiss.normalize_L2(newV)

                closest_chunk = self._retrieve_core(newV, 1)
                additional_chunks.extend(closest_chunk)

            retrieved_chunks.extend(additional_chunks)
            retrieved_chunks = remove_duplicates(retrieved_chunks)

        if self.add_neighbor_chunks and not force_basics:
            additional_chunks = []
            for chunk in retrieved_chunks:
                if chunk.PrevRelated is not None:
                    additional_chunks.append(chunk.PrevRelated)
                if chunk.NextRelated is not None:
                    additional_chunks.append(chunk.NextRelated)
            retrieved_chunks.extend(additional_chunks)

        elif self.add_neighbor_chunks_smart and not force_basics:
            # only add the next and previous chunk if their embedding added to the original chunk embedding gets it closer(cosine sim) to query embedding
            additional_chunks = [chunk for chunk in retrieved_chunks]

            for chunk in retrieved_chunks:

                def check_add(neighbour_chunk,chunk0,current_depth):
                    current_depth+=1
                    orig_similarity = cosine_similarity(query_embedding[0], chunk0.Embeddings)
                    combined_embedding = (chunk0.Embeddings + neighbour_chunk.Embeddings) / 2
                    combined_similarity = cosine_similarity(query_embedding[0], combined_embedding)
                    if combined_similarity > orig_similarity:
                        if neighbour_chunk not in additional_chunks:
                            additional_chunks.append(neighbour_chunk)
                        if current_depth<self.add_neighbor_chunks_k:
                            if neighbour_chunk.PrevRelated is not None:
                                check_add(neighbour_chunk.PrevRelated,chunk0,current_depth)
                            if neighbour_chunk.NextRelated is not None:
                                check_add(neighbour_chunk.NextRelated,chunk0,current_depth)




                if chunk.PrevRelated is not None:
                    check_add(chunk.PrevRelated,chunk,0)

                if chunk.NextRelated is not None:
                    check_add(chunk.NextRelated,chunk,0)

            # remove retrieved_chunks from additional_chunks
            additional_chunks = [chunk for chunk in additional_chunks if chunk not in retrieved_chunks]


            retrieved_chunks.extend(additional_chunks)

        retrieved_chunks = remove_duplicates(retrieved_chunks)


        # retrieved_chunks ---> retrieved_chunks_texts

        if self.replace_retrieved_chunks_with_parent_paragraph:
            paragraphs = [paragraph for chunk in retrieved_chunks for paragraph in chunk.Paragraphs]

            paragraphs = remove_duplicates(paragraphs)
            retrieved_chunks_texts = [paragraph.Text for paragraph in paragraphs]

        else:
            retrieved_chunks_texts = [chunk.Text for chunk in retrieved_chunks]

        # if sum_of_retrieved_token_length_limit > 0:
        #     total_tokens = 0
        #     filtered_chunks = []
        #     for chunk in retrieved_chunks_texts:
        #         c_len = token_len(chunk)
        #         filtered_chunks.append(chunk)
        #         if total_tokens + c_len > sum_of_retrieved_token_length_limit:
        #             break
        #         total_tokens += c_len
        #     retrieved_chunks_texts = filtered_chunks


        return retrieved_chunks_texts

    def _ask_notTool(self, query, top_k=30, include_prompt=True):
        if self.answer_mode=='none':
            self.answer_mode = 'classic'
        elif self.answer_mode=='tool':
            print("changing mode to classic, chat history is cleared")
            self.llm.reset_history()

        # encode query -> retrieve top_k chunks -> generate answer

        retrieved_docs = self.retrieve(query, top_k)

        prompt,response = self.llm.rag_generate(query=query, retrieved_chunks=retrieved_docs)


        if include_prompt:
            answer = prompt + "\n\n# Answer:\n" + response
        else:
            answer = response

        return answer

    def ask(self, query, top_k=30, include_prompt=False,useTool=False):
        if self.llm is None:
            print("Error: LLM is not set. Please set the LLM before asking a question. or use retrieve()")
            return ""

        if useTool:
            return self._ask_tool(query)
        else:
            return self._ask_notTool(query, top_k=top_k, include_prompt=include_prompt)

    def _ask_tool(self, query):
        print("using tool")
        if self.answer_mode=='none':
            self.answer_mode = 'tool'
        elif self.answer_mode=='classic':
            print("changing mode to tool, chat history is cleared")
            self.llm.reset_history()

        response = self.llm.generate(prompt=query,tool_function= self.retrieve_interface)
        return response

    def clear_history(self):
        self.llm.reset_history()

    def retrieve_interface(self, query:str, top_k:int) -> str:
        """retrieves k chunks based on query.
        The chunks are then merged and returned as a single string.
        if the retrieved chunks didn't contain the information you needed, try to increase the top_k value or use different query.
        Args:
            query: The query to retrieve chunks for.
            top_k: The number of chunks to retrieve. recommended to be larger than 20.
        """
        retrieved_chunks=self.retrieve(query=query, top_k=top_k)

        retrieved_chunks_text=LLMIdentity.merge_chunks(retrieved_chunks=retrieved_chunks)

        retrieved_chunks_text += f"\n if the retrieved chunks didn't contain the information you needed, try to increase the top_k value or use different query. call the tool again right now with function_call before talking to the user."

        return retrieved_chunks_text






def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
