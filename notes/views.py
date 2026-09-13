from django.shortcuts import render, redirect
from .models import Note, Tag

def get_tag_from_request(request):
    tag_name = request.POST.get('tag', '').strip()
    if not tag_name:
        return None
    tag, created = Tag.objects.get_or_create(name=tag_name)
    return tag

def index(request):
    if request.method == "POST":
        title = request.POST.get('titulo')
        content = request.POST.get('detalhes')
        tag = get_tag_from_request(request)
        Note.objects.create(title=title, content=content, tag=tag)
        return redirect('index')
    else:
        all_notes = Note.objects.all()
        return render(request, 'notes/index.html', {'notes': all_notes})

def delete(request, note_id):
    note = Note.objects.get(pk=note_id)
    note.delete()
    return redirect('index')

def edit(request, note_id):
    note = Note.objects.get(pk=note_id)
    if request.method == 'POST':
        note.title = request.POST.get('titulo')
        note.content = request.POST.get('detalhes')
        note.tag = get_tag_from_request(request)
        note.save()
        return redirect('index')
    else:
        return render(request, 'notes/edit.html', {'note': note})

def tags(request):
    all_tags = Tag.objects.all()
    return render(request, 'notes/tags.html', {'tags': all_tags})

def tag_detail(request, tag_id):
    tag = Tag.objects.get(pk=tag_id)
    notes = Note.objects.filter(tag=tag)
    return render(request, 'notes/tag_detail.html', {'tag':tag, 'notes':notes})