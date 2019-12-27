"""Defines URL patternsfor learning_logs"""

from django.conf.urls import url

from . import views

app_name = 'learning_logs'

urlpatterns = [
    # Homepage
    url(r'^$', views.index, name='index'),

    # Show all topics
    url(r'^topics/$', views.topics, name='topics'),

    # Show individual  topics
    url(r'^topics/(?P<topic_id>\d+)/$', views.topic, name='topic'),

    # Page for adding a new topic (form)
    url(r'^new_topics/$', views.new_topic, name='new_topic'),

    # Deleting a topic
    url(r'^del_topic/(?P<topic_id>\d+)/$', views.del_topic, name='del_topic'),

    # Deleting an entry
    url(r'^del_entry/(?P<entry_id>\d+)/$', views.del_entry, name='del_entry'),

    # Uploading a file
    url(r'^files/$', views.files, name='files'),
    url(r'^files_upload/$', views.files_upload, name='files_upload'),


    # Page for adding a new entry
    url(r'^new_entry/(?P<topic_id>\d+)/$', views.new_entry, name='new_entry'),

    # Page for editing an entry
    url(r'^edit_entry/(?P<entry_id>\d+)/$', views.edit_entry, name='edit_entry'),
]