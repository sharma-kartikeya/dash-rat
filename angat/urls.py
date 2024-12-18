from django.urls import path
from . import views

urlpatterns = [
    path("", view=views.home, name='home'),
    path("papers", view=views.get_papers, name='papers'),
    path("scrap", view=views.scrap_papers, name='scrap'),
    path("query", view=views.query, name="query"),
    path("start", view=views.start, name='start'),
    path("openai", view=views.openai, name='openai'),
    path("scrap_programs", view=views.scrap_program, name='scrap_programs'),
    path("get_all_eligibilties", view=views.get_all_eligibilties, name="get_all_eligibilties")
]