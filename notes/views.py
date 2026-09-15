from django.shortcuts import render, redirect
from .models import Note, Tag

def get_tag_from_request(request):
    tags_str = request.POST.get('tags', '').strip()
    if not tags_str:
        return []
    tag_names = [t.strip() for t in tags_str.split(',') if t.strip()]
    note_tags = []
    for name in tag_names:
        tag, created = Tag.objects.get_or_create(name=name)
        note_tags.append(tag)
    return note_tags

def index(request):
    if request.method == "POST":
        title = request.POST.get('titulo')
        content = request.POST.get('detalhes')
        note = Note.objects.create(title=title, content=content)
        note_tags = get_tag_from_request(request)
        note.tags.set(note_tags)
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
        note.save()
        note_tags = get_tag_from_request(request)
        note.tags.set(note_tags)
        return redirect('index')
    else:
        return render(request, 'notes/edit.html', {'note': note})

def tags(request):
    all_tags = Tag.objects.all()
    return render(request, 'notes/tags.html', {'tags': all_tags})

def tag_detail(request, tag_id):
    tag = Tag.objects.get(pk=tag_id)
    notes = Note.objects.filter(tags=tag)
    return render(request, 'notes/tag_detail.html', {'tag':tag, 'notes':notes})