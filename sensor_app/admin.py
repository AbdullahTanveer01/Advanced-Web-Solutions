from django.contrib import admin

from .models import PressureFrame, Profile, ThreadComment

admin.site.register(Profile)
admin.site.register(PressureFrame)
admin.site.register(ThreadComment)

