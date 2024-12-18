from .models.Paper import Paper, Embedding_Function
from pgvector.django import CosineDistance
from .models.Message import Message
from .models.GloveraUser import GloveraUser

class DB_Helper:
    @classmethod
    def get_papers(cls):
        return Paper.objects.all().values_list('title')
    
    @classmethod
    def query(cls, query: str):
        query_embeddings = Embedding_Function.embed([query])[0]
        papers = Paper.objects.annotate(
            distance = CosineDistance('abstract_embeddings', query_embeddings)
        ).order_by("distance")[:12]
        return papers.values_list('abstract')
    
    @classmethod
    def get_chat_messages(cls, chat_id: str):
        chat_messages = Message.objects.filter(chat=chat_id).order_by('created_at')
        print('All Chat Messages: -> ', chat_messages.__str__())
        messages = [message.json() for message in chat_messages]
        return messages
    
    @classmethod
    def create_glovera_user(cls, degree: str, spec: str, college: str, percent: str, backlogs: str, total_exp: str):
        GloveraUser(
            name="Kartikeya Sharma", 
            email='s.kartikeya18@gmail.com', 
            mobile=7578062409,
            bachlors=degree, 
            bachlors_program=spec, 
            univ=college, 
            percentage=percent,
            backlogs=backlogs,
            work_exp=total_exp
        ).save()