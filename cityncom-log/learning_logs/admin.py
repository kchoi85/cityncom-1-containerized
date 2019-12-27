from django.contrib import admin
from learning_logs.models import Topic, Entry, Document

# Register your models here.

admin.site.register(Topic)
admin.site.register(Entry)
admin.site.register(Document)