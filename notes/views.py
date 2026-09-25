# notes/views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import StickyNote
from .forms import StickyNoteForm


def note_list(request):
    """View to display a list of all sticky notes.

    :param request: HTTP request object.
    :return: Rendered template with a list of notes.
    """
    notes = StickyNote.objects.all()

    context = {
        "notes": notes,
        "page_title": "My Sticky Notes",
    }
    return render(request, "notes/note_list.html", context)


def note_detail(request, pk):
    """View to display the details of a specific sticky note.

    :param request: HTTP request object.
    :param pk: Primary key of the note.
    :return: Rendered template with details of the specified note.
    """
    note = get_object_or_404(StickyNote, pk=pk)
    return render(request, "notes/note_detail.html", {"note": note})


def note_create(request):
    """View to create a new sticky note.

    :param request: HTTP request object.
    :return: Rendered template for creating a new note, or a redirect on success.
    """
    if request.method == "POST":
        form = StickyNoteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("note_list")
    else:
        form = StickyNoteForm()
    return render(request, "notes/note_form.html", {"form": form})


def note_update(request, pk):
    """View to update an existing sticky note.

    :param request: HTTP request object.
    :param pk: Primary key of the note to be updated.
    :return: Rendered template for updating the specified note, or a redirect on success.
    """
    note = get_object_or_404(StickyNote, pk=pk)
    if request.method == "POST":
        form = StickyNoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            return redirect("note_list")
    else:
        form = StickyNoteForm(instance=note)
    return render(request, "notes/note_form.html", {"form": form})


def note_delete(request, pk):
    """View to delete an existing sticky note.

    :param request: HTTP request object.
    :param pk: Primary key of the note to be deleted.
    :return: Confirmation page on GET, redirect to the note list after deletion on POST.
    """
    note = get_object_or_404(StickyNote, pk=pk)
    if request.method == "POST":
        note.delete()
        return redirect("note_list")
    return render(request, "notes/note_confirm_delete.html", {"note": note})
