from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import Topic, Entry, Document
from .forms import TopicForm, EntryForm, DocumentForm
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.shortcuts import get_object_or_404, redirect, render


# Create your views here.
def index(request):
    """The homepage for Learning Log"""
    return render(request, 'learning_logs/index.html')

@login_required
def topics(request):
    """Show all topics"""
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)

@login_required
def topic(request, topic_id):
    """Show single topics and all its entries"""
    topic = Topic.objects.get(id=topic_id)
    #topic = get_object_or_404(Topic, id=topic_id) requires from django.shortcuts import render, get_object_or_404
    # Make sure the topic belongs to the current user.
    if topic.owner != request.user:
        raise Http404

    entries = topic.entry_set.order_by('-date_added')
    context = {'topic':topic, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)

@login_required
def new_topic(request):
    """Add a new topic"""
    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = TopicForm()
    else:
        # POST data submitted; process data.
        form = TopicForm(request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return HttpResponseRedirect(reverse('learning_logs:topics'))

    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)

@login_required
def del_topic(request, topic_id):
    """Delete a topic"""
    topic = Topic.objects.get(id=topic_id)
    #topic = Topic.objects.filter(id=topic_id) - also works
    if topic.delete():
        return redirect('/topics')
    context = {'topic': topic}
    return render(request, 'learning_logs/topics.html', context)

@login_required
def new_entry(request, topic_id):
    """Add a new entry for a individual topic"""
    topic = Topic.objects.get(id=topic_id)

    if request.method != 'POST':
        form = EntryForm()
    else:
        form = EntryForm(request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            # commit = False is to tell Django to create a new entry and store it as new_entry without saving to database yet
            new_entry.topic = topic
            new_entry.save()
            return HttpResponseRedirect(reverse('learning_logs:topic', args=[topic_id]))
    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
    """Edit an existing entry"""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    if topic.owner != request.user:
        raise Http404

    if request.method != 'POST':
        form = EntryForm(instance=entry)
    else:
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('learning_logs:topics'))

    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'learning_logs/edit_entry.html', context)

@login_required
def del_entry(request, entry_id):
    """Delete an existing entry"""
    entry = Entry.objects.get(id=entry_id)
    if entry.delete():
        return redirect('/topics')
    context = {'entry': entry}
    return render(request, 'learning_logs/topics.html/', context)

@login_required
def files(requests):
    uploads = Document.objects.all()
    return render(requests, 'learning_logs/files.html', {'uploads': uploads})

@login_required
def files_upload(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/files')
    else:
        form = DocumentForm()
    return render(request, 'learning_logs/files_upload.html', {
        'form': form
    })