from django.contrib import admin
from .models import Profile
from .models import PressureFrame
from .models import ThreadComment
# Register your models here.
admin.site.register(Profile)
admin.site.register(PressureFrame)
admin.site.register(ThreadComment)