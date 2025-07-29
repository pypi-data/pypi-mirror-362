class MRDocument:
    def __init__(self,text=""):
        self.Paragraphs = []
        self.Sentences = []
        self.Text = text
        self.isChunked = False

    def AddParagraph(self, paragraph):
        if paragraph is None:
            print( "Warning: paragraph is None")
            return
        self.Paragraphs.append(paragraph)

    def AddSentence(self, sentence):
        if sentence is None:
            print( "Warning: sentence is None")
            return
        self.Sentences.append(sentence)



class MRParagraph:
    def __init__(self,document,text=""):
        self.Document = document
        self.Sentences = []
        self.Prev = None
        self.Next = None
        self.Text = text
        self.Embeddings = None

    def AddSentence(self, sentence):
        if sentence is None:
            print( "Warning: sentence is None")
            return
        self.Sentences.append(sentence)

    def SetPrev(self, prev):
        self.Prev = prev

    def SetNext(self, nextParagraph):
        self.Next = nextParagraph


class MRSentence:
    def __init__(self ,document,paragraph,text=""):
        self.Document = document
        self.Paragraph = paragraph
        self.Prev = None
        self.Next = None
        self.Text = text

    def SetPrev(self, prev):
        self.Prev = prev

    def SetNext(self, nextSentence):
        self.Next = nextSentence

class MRChunk:
    def __init__(self,document, text=""):
        self.Text = text
        self.Paragraphs = []
        self.Sentences = []
        self.Document = document
        self.PrevRelated = None
        self.NextRelated = None
        self.Embeddings = None
        self.Length = -1

    def AddParagraph(self, paragraph):
        if paragraph is None:
            print( "Warning: paragraph is None")
            return
        if paragraph not in self.Paragraphs:
            self.Paragraphs.append(paragraph)

    def AddSentence(self, sentence):
        if sentence is None:
            print( "Warning: sentence is None")
            return
        self.Sentences.append(sentence)



    def __str__(self):
        return self.Text

    def __repr__(self):
        return self.Text


def generate_document_structure(rawDocumentsTexts:list, DocumentsList:list, max_sentence_len:int):
    from MetaRagTool.Utils.MRUtils import capped_sent_tokenize

    if max_sentence_len == -1:
        print("Error: max_sentence_len is set to -1, which is invalid.")


    # Generate the document structure
    for documentText in rawDocumentsTexts:
        if len(documentText) < 1:
            continue

        newDoc = MRDocument(documentText)
        DocumentsList.append(newDoc)

        prevParagraph = None
        for paragraphText in documentText.split('\n'):
            if len(paragraphText) < 5:
                continue

            newParagraph = MRParagraph(document=newDoc, text=paragraphText)

            prevSentence = None
            sentences = capped_sent_tokenize(paragraphText, max_sentence_len)
            if len(sentences) < 1:
                continue

            for sentenceText in sentences:

                newSentence = MRSentence(document=newDoc, paragraph=newParagraph, text=sentenceText)
                newParagraph.AddSentence(newSentence)
                newDoc.AddSentence(newSentence)
                if prevSentence is not None:
                    prevSentence.SetNext(newSentence)
                    newSentence.SetPrev(prevSentence)

                prevSentence = newSentence

            newDoc.AddParagraph(newParagraph)
            if prevParagraph is not None:
                prevParagraph.SetNext(newParagraph)
                newParagraph.SetPrev(prevParagraph)

            prevParagraph = newParagraph

    allParagraphs = [paragraph for doc in DocumentsList for paragraph in doc.Paragraphs]
    allSentences = [sentence for doc in DocumentsList for sentence in doc.Sentences]

    return allParagraphs, allSentences
