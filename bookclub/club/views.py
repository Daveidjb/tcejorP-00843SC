from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Avg, Count, F, ExpressionWrapper, fields
from .models import Reading, Book, Member, Genre
from .forms import ReadingForm
from django.db.models import Avg, Count, F, ExpressionWrapper, DurationField
from django.db.models.functions import TruncDate
from .models import Reading, Book, Member, Genre
from .forms import ReadingForm
from .forms import ReadingForm, BookForm, AuthorForm, MemberForm
from .models import Reading, Book, Member, Genre, Author


def reading_list(request):
    readings = Reading.objects.select_related('book', 'member', 'book__author').order_by('-id')
    return render(request, 'club/reading_list.html', {'readings': readings})

def reading_create(request):
    form = ReadingForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('reading_list')
    return render(request, 'club/reading_form.html', {'form': form, 'title': 'Add Reading'})

def reading_edit(request, pk):
    reading = get_object_or_404(Reading, pk=pk)
    form = ReadingForm(request.POST or None, instance=reading)
    if form.is_valid():
        form.save()
        return redirect('reading_list')
    return render(request, 'club/reading_form.html', {'form': form, 'title': 'Edit Reading'})

def reading_delete(request, pk):
    reading = get_object_or_404(Reading, pk=pk)
    if request.method == 'POST':
        reading.delete()
        return redirect('reading_list')
    return render(request, 'club/reading_confirm_delete.html', {'reading': reading})



def report(request):

    genres  = Genre.objects.order_by('name')
    members = Member.objects.order_by('last_name')

    genre_id   = request.GET.get('genre')
    member_id  = request.GET.get('member')
    status     = request.GET.get('status')
    start_from = request.GET.get('start_from')
    start_to   = request.GET.get('start_to')

    readings = Reading.objects.select_related('book', 'book__genre', 'book__author', 'member')

    if genre_id:
        readings = readings.filter(book__genre_id=genre_id)
    if member_id:
        readings = readings.filter(member_id=member_id)
    if status:
        readings = readings.filter(status=status)
    if start_from:
        readings = readings.filter(start_date__gte=start_from)
    if start_to:
        readings = readings.filter(start_date__lte=start_to)

    total      = readings.count()
    completed  = readings.filter(status='completed').count()
    avg_rating = readings.filter(rating__isnull=False).aggregate(Avg('rating'))['rating__avg']
    completion_rate = round((completed / total * 100), 1) if total > 0 else 0


    finished = readings.filter(status='completed', end_date__isnull=False)
    avg_days = None
    if finished.exists():
        total_days = sum(
            (r.end_date - r.start_date).days for r in finished
        )
        avg_days = round(total_days / finished.count(), 1)

    context = {
        'genres':          genres,
        'members':         members,
        'status_choices':  Reading.STATUS_CHOICES,
        'readings':        readings.order_by('-start_date'),
        'total':           total,
        'completed':       completed,
        'avg_rating':      round(avg_rating, 2) if avg_rating else None,
        'completion_rate': completion_rate,
        'avg_days':        avg_days,
        'filters': {
            'genre_id':   genre_id,
            'member_id':  member_id,
            'status':     status,
            'start_from': start_from,
            'start_to':   start_to,
        }
    }
    return render(request, 'club/report.html', context)
def book_list(request):
    books = Book.objects.select_related('author', 'genre').order_by('title')
    return render(request, 'club/book_list.html', {'books': books})

def book_create(request):
    form = BookForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('book_list')
    return render(request, 'club/book_form.html', {'form': form, 'title': 'Add Book'})

def book_edit(request, pk):
    book = get_object_or_404(Book, pk=pk)
    form = BookForm(request.POST or None, instance=book)
    if form.is_valid():
        form.save()
        return redirect('book_list')
    return render(request, 'club/book_form.html', {'form': form, 'title': 'Edit Book'})

def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('book_list')
    return render(request, 'club/book_confirm_delete.html', {'book': book})

def author_create(request):
    form = AuthorForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('book_list')
    return render(request, 'club/book_form.html', {'form': form, 'title': 'Add Author'})
def member_list(request):
    members = Member.objects.order_by('last_name')
    return render(request, 'club/member_list.html', {'members': members})

def member_create(request):
    form = MemberForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('member_list')
    return render(request, 'club/member_form.html', {'form': form, 'title': 'Add Member'})

def member_edit(request, pk):
    member = get_object_or_404(Member, pk=pk)
    form = MemberForm(request.POST or None, instance=member)
    if form.is_valid():
        form.save()
        return redirect('member_list')
    return render(request, 'club/member_form.html', {'form': form, 'title': 'Edit Member'})

def member_delete(request, pk):
    member = get_object_or_404(Member, pk=pk)
    if request.method == 'POST':
        member.delete()
        return redirect('member_list')
    return render(request, 'club/member_confirm_delete.html', {'member': member})