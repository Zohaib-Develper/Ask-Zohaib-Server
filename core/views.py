from rest_framework.views import APIView
from rest_framework.response import Response
from core.services.llm_service import LLMService
from core.services.load_faiss import faiss_service, embedding_service


llm_service = LLMService()

# Create your views here.
class ChatApiView(APIView):
    def post(self, request):
        question = request.data.get('question')
        if not question:
            return Response({"error": "Question field is required"}, status = 400)
        query_vector = embedding_service.get_embedding(question)
        chunks = faiss_service.search(query_vector=query_vector)
        print("Chunks: ", chunks)
        print("Question: ", question)
        answer = llm_service.get_answer(question,'\n'.join(chunks))
        print("Answer from llm: ", answer)
        return Response({"answer": answer})