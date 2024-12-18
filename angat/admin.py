from django.contrib import admin
from .models.Paper import Paper
from .models.Chat import Chat
from .models.Message import Message
from .models.GloveraUser import GloveraUser
from .models.AcedemicProgram import AcedemicProgram
from .models.University import University

# Register your models here.
admin.site.register(Paper)
admin.site.register(Chat)
admin.site.register(Message)
admin.site.register(GloveraUser)
admin.site.register(AcedemicProgram)
admin.site.register(University)