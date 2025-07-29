from abc import ABC, abstractmethod
from enum import Enum

from MetaRagTool.RAG.DocumentStructs import MRDocument, MRChunk, MRSentence

class ChunkingMethod(Enum):
    SENTENCE_MERGER_CROSS_PARAGRAPH = 'sentence_merger_cross_paragraph'
    SENTENCE = 'sent'
    PARAGRAPH = 'paragraph'
    DOCUMENT = 'document'
    RECURSIVE = 'recursive'
    SENTENCE_MERGER = 'sentence_merger'

class Chunker(ABC):
    def __init__(self, splitting_method: ChunkingMethod, chunksList:list, chunk_size: int = 90, chunk_overlap: int = 3):
        self.splitting_method = splitting_method
        self.chunksList = chunksList
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap


    def chunk_texts(self, texts: list):
        from MetaRagTool.RAG.DocumentStructs import generate_document_structure
        documentLists=[]
        allParagraphs,allSentences=generate_document_structure(rawDocumentsTexts=texts, DocumentsList=documentLists, max_sentence_len=self.chunk_size)
        print(f"Corpus structure: {len(documentLists)} documents and {len(allParagraphs)} paragraphs and {len(allSentences)} sentences")

        return self.chunk_documents(documentLists)



    def chunk_documents(self, documents: list) -> list:
        for doc in documents:
            if doc.isChunked:
                continue

            doc.isChunked = True
            self._chunk_document_core(doc)


        for chunk in self.chunksList:
            chunk.Length = token_len(chunk.Text)

        return self.chunksList



    @abstractmethod
    def _chunk_document_core(self, document: MRDocument):
        pass

    def chunking_report(self):
        import matplotlib.pyplot as plt
        import numpy as np

        chunk_sizes = [token_len(chunk.Text) for chunk in self.chunksList]
        total_chunks = len(chunk_sizes)
        avg_chunk_size = sum(chunk_sizes) / total_chunks if total_chunks > 0 else 0
        max_chunk_size = max(chunk_sizes) if total_chunks > 0 else 0
        min_chunk_size = min(chunk_sizes) if total_chunks > 0 else 0
        median_chunk_size = np.median(chunk_sizes) if total_chunks > 0 else 0
        std_chunk_size = np.std(chunk_sizes) if total_chunks > 0 else 0
        # chunk_size_distribution = np.histogram(chunk_sizes, bins='auto') if total_chunks > 0 else ([], [])

        print(f"Chunking Report:")
        print(f"Total number of chunks: {total_chunks}")
        print(f"Average chunk size: {avg_chunk_size:.2f} tokens")
        print(f"Maximum chunk size: {max_chunk_size} tokens")
        print(f"Minimum chunk size: {min_chunk_size} tokens")
        print(f"Median chunk size: {median_chunk_size:.2f} tokens")
        print(f"Standard deviation of chunk size: {std_chunk_size:.2f} tokens")

        plt.clf()
        plt.hist(chunk_sizes, bins='auto', edgecolor='black')
        plt.title('Chunk Size Distribution')
        plt.xlabel('Chunk Size (tokens)')
        plt.ylabel('Frequency')
        plt.show()

        return plt





class SentenceChunker(Chunker):
    def __init__(self, chunksList:list, chunk_size: int = 90, chunk_overlap: int = 3):
        super().__init__(ChunkingMethod.SENTENCE, chunksList, chunk_size, chunk_overlap)


    def _chunk_document_core(self, document: MRDocument):
        prevChunk = None
        for sentence in document.Sentences:
            newChunk = MRChunk(document=document, text=sentence.Text)
            newChunk.AddParagraph(sentence.Paragraph)
            newChunk.AddSentence(sentence)
            self.chunksList.append(newChunk)
            if prevChunk is not None:
                prevChunk.NextRelated = newChunk
                newChunk.PrevRelated = prevChunk
            prevChunk = newChunk

class ParagraphChunker(Chunker):
    def __init__(self, chunksList:list, chunk_size: int = 90, chunk_overlap: int = 3):
        super().__init__(ChunkingMethod.PARAGRAPH, chunksList, chunk_size, chunk_overlap)

    def _chunk_document_core(self, document: MRDocument):
        prevChunk = None
        for paragraph in document.Paragraphs:
            newChunk = MRChunk(document=document, text=paragraph.Text)
            newChunk.AddParagraph(paragraph)
            for sentence in paragraph.Sentences:
                newChunk.AddSentence(sentence)

            self.chunksList.append(newChunk)
            if prevChunk is not None:
                prevChunk.NextRelated = newChunk
                newChunk.PrevRelated = prevChunk
            prevChunk = newChunk


class DocumentChunker(Chunker):
    def __init__(self, chunksList:list, chunk_size: int = 90, chunk_overlap: int = 3):
        super().__init__(ChunkingMethod.DOCUMENT, chunksList, chunk_size, chunk_overlap)

    def _chunk_document_core(self, document: MRDocument):
        newChunk = MRChunk(document=document, text=document.Text)
        for paragraph in document.Paragraphs:
            newChunk.AddParagraph(paragraph)
            for sentence in paragraph.Sentences:
                newChunk.AddSentence(sentence)

        self.chunksList.append(newChunk)



class SentenceMergerChunker(Chunker):
    def __init__(self, chunksList:list, chunk_size: int = 90, chunk_overlap: int = 3, sent_merge_merged_chunks: bool = True):
        super().__init__(ChunkingMethod.SENTENCE_MERGER, chunksList, chunk_size, chunk_overlap)
        self.sent_merge_merged_chunks = sent_merge_merged_chunks

    def _sent_merger_create_chunk(self, currentChunkText, current_chunk_sentences, document, paragraph, prevChunk):
        if self.sent_merge_merged_chunks and prevChunk is not None and token_len(prevChunk.Text + currentChunkText) < self.chunk_size:
            prevChunk.Text += currentChunkText
            for s in current_chunk_sentences:
                prevChunk.AddSentence(s)
            prevChunk.AddParagraph(paragraph)
        else:
            newChunk = MRChunk(document=document, text=currentChunkText)
            newChunk.AddParagraph(paragraph)
            for s in current_chunk_sentences:
                newChunk.AddSentence(s)
            self.chunksList.append(newChunk)
            if prevChunk is not None:
                prevChunk.NextRelated = newChunk
                newChunk.PrevRelated = prevChunk
            prevChunk = newChunk
        currentChunkText = ""
        current_chunk_sentences = []



        return currentChunkText, current_chunk_sentences, prevChunk




    def _chunk_document_core(self, document: MRDocument):
        prevChunk = None

        for paragraph in document.Paragraphs:
            current_chunk_sentences = []
            currentChunkText = ""
            currentSentence: MRSentence = paragraph.Sentences[0]
            while currentSentence is not None:
                nextText = currentSentence.Text + " "
                # If adding this sentence would exceed chunk_size, finalize current chunk first.
                if token_len(currentChunkText + nextText) > self.chunk_size and currentChunkText.strip():
                    currentChunkText, current_chunk_sentences, prevChunk = self._sent_merger_create_chunk(
                        currentChunkText,
                        current_chunk_sentences,
                        document, paragraph,
                        prevChunk)

                currentChunkText += nextText
                current_chunk_sentences.append(currentSentence)

                # If next sentence is None or we've just reached chunk size, finalize the chunk.
                if currentSentence.Next is None:
                    currentChunkText, current_chunk_sentences, prevChunk = self._sent_merger_create_chunk(
                        currentChunkText,
                        current_chunk_sentences,
                        document, paragraph,
                        prevChunk)

                currentSentence = currentSentence.Next



class SentenceMergerCrossParagraphChunker(Chunker):
    def __init__(self, chunksList:list, chunk_size: int = 90, chunk_overlap: int = 3):
        super().__init__(ChunkingMethod.SENTENCE_MERGER_CROSS_PARAGRAPH, chunksList, chunk_size, chunk_overlap)

    def _chunk_document_core(self, document: MRDocument):
        prevChunk = None
        current_chunk_sentences = []
        currentChunkText = ""

        for idx, sentt in enumerate(document.Sentences):
            # If adding this sentence exceeds chunk_size, create the chunk right away
            if currentChunkText and token_len(currentChunkText + sentt.Text) > self.chunk_size:
                newChunk = MRChunk(document=document, text=currentChunkText)
                for s in current_chunk_sentences:
                    newChunk.AddSentence(s)
                    newChunk.AddParagraph(s.Paragraph)
                self.chunksList.append(newChunk)
                if prevChunk is not None:
                    prevChunk.NextRelated = newChunk
                    newChunk.PrevRelated = prevChunk

                prevChunk = newChunk
                currentChunkText = ""
                current_chunk_sentences = []

            currentChunkText += sentt.Text + " "
            current_chunk_sentences.append(sentt)

            # If it's the last sentence, finalize the current chunk
            if idx == len(document.Sentences) - 1:
                newChunk = MRChunk(document=document, text=currentChunkText)
                for s in current_chunk_sentences:
                    newChunk.AddSentence(s)
                    newChunk.AddParagraph(s.Paragraph)
                self.chunksList.append(newChunk)
                if prevChunk is not None:
                    prevChunk.NextRelated = newChunk
                    newChunk.PrevRelated = prevChunk


class RecursiveChunker(Chunker):
    def __init__(self, chunksList:list, chunk_size: int = 90, chunk_overlap: int = 3):
        from langchain_text_splitters import RecursiveCharacterTextSplitter

        super().__init__(ChunkingMethod.RECURSIVE, chunksList, chunk_size, chunk_overlap)
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            length_function=token_len,
            is_separator_regex=False,
        )

    def _chunk_document_core(self, document: MRDocument):
        text_chunks__for_this_doc = self.splitter.split_text(document.Text)
        for text_chunk in text_chunks__for_this_doc:
            self.chunksList.append(MRChunk(document=document, text=text_chunk))


class ChunkerFactory:
    @staticmethod
    def create_chunker(splitting_method: ChunkingMethod, chunksList: list, chunk_size: int = 90, chunk_overlap: int = 3,sent_merge_merged_chunks: bool = True) -> Chunker:
        if splitting_method == ChunkingMethod.SENTENCE:
            return SentenceChunker(chunksList, chunk_size, chunk_overlap)
        elif splitting_method == ChunkingMethod.PARAGRAPH:
            return ParagraphChunker(chunksList, chunk_size, chunk_overlap)
        elif splitting_method == ChunkingMethod.DOCUMENT:
            return DocumentChunker(chunksList, chunk_size, chunk_overlap)
        elif splitting_method == ChunkingMethod.SENTENCE_MERGER:
            return SentenceMergerChunker(chunksList, chunk_size, chunk_overlap, sent_merge_merged_chunks)
        elif splitting_method == ChunkingMethod.SENTENCE_MERGER_CROSS_PARAGRAPH:
            return SentenceMergerCrossParagraphChunker(chunksList, chunk_size, chunk_overlap)
        elif splitting_method == ChunkingMethod.RECURSIVE:
            return RecursiveChunker(chunksList, chunk_size, chunk_overlap)
        else:
            raise ValueError(f"Unsupported chunking method: {splitting_method}")







from MetaRagTool.Utils.MRUtils import token_len
