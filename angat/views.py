from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, JsonResponse
from .scraper import scrap_papers_
from django.views.decorators.csrf import csrf_exempt
import json
from .db_helper import DB_Helper
from .llm_model import LLM_Model, LocalLLM, openAiChat
from rest_framework import serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from .react_loop.ReAct_Loop import agentic_loop
from .scrap_univ import scrap_program_csv
from .models.AcedemicProgram import AcedemicProgram

# Create your views here.
def home(request: HttpRequest) -> HttpResponse:
    return HttpResponse('Angat ka pranam svikar kare!')

def scrap_papers(request: HttpRequest) -> HttpResponse:
    response = scrap_papers_()
    return HttpResponse(response)

def get_papers(request: HttpRequest) -> JsonResponse:
    papers = DB_Helper.get_papers()
    return JsonResponse(list(papers), safe=False)

class QuerySerializer(serializers.Serializer):
    chat_id = serializers.CharField()
    query = serializers.CharField()

def start(requst):
    response = LocalLLM.call()
    return JsonResponse(response)

def scrap_program(request):
    scrap_program_csv()
    return HttpResponse('CSV scraped!')

def get_all_eligibilties(request):
    eligibilties = AcedemicProgram.objects.all().values_list('name', 'eligibility')
    return JsonResponse(list(eligibilties), safe=False)

@api_view(['POST'])
def openai(request: Request) -> Response:
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    if user_message := body['user_message']:
        agentic_loop(user_message)
    else:
        openAiChat.cold_start(force=True)
    response_chat = openAiChat.messages
    return Response(response_chat)

@api_view(['POST'])
def query(request: Request) -> JsonResponse:
    serializer = QuerySerializer(data=request.data)
    if serializer.is_valid():
        chat_id = serializer.validated_data.get('chat_id')
        query = serializer.validated_data.get('query')
        model_response = LLM_Model.llm_call(chat_id=chat_id, query=query)
        return Response(model_response)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)