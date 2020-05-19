from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from .models import Book, Comment, Tag, Genre, Chapter
from .forms import BookForm, ChapterForm
from django.utils import timezone
import datetime


def home(request):
	return render(request, "home/home_page.html", {'user': request.user.is_authenticated})



def popular(request):
	now = datetime.datetime.now()
	year = [timezone.now() - timezone.timedelta(365), timezone.now()]
	month = [timezone.now() - timezone.timedelta(30), timezone.now()]
	week = [timezone.now() - timezone.timedelta(7), timezone.now()]
	books_y = Book.objects.filter(pub_date__range=year).order_by("-views")
	books_m = Book.objects.filter(pub_date__range=month).order_by("-views")
	books_w = Book.objects.filter(pub_date__range=week).order_by("-views")
	return render(request, "home/section.html", {'user': request.user.is_authenticated, "title": "Популярные", "books_y": books_y, "books_m": books_m, "books_w": books_w})

def book_create(request):
	if not request.user.is_authenticated:
		return redirect("/")
	if request.method == "POST":
		form = BookForm(request.POST)
		if form.is_valid():
			book = Book()
			data = form.cleaned_data
			book.title = data["title"] 
			book.image = data["image"] 
			book.description = data["description"] 
			book.price = data["price"] 
			book.tags = data["tags"] 
			book.genres = data["genres"] 
			book.author_name_id = request.user.id
			book.save()
			return redirect('/')
	return render(request, "home/book_create.html", {'user': request.user.is_authenticated, "form": BookForm()})

def get_tag(request, slug):
	tag = get_object_or_404(Tag, slug=slug)
	books = tag.books.all
	return render(request, "home/for_column_view.html", {'user': request.user.is_authenticated, "title": tag, "books": books})

def get_genre(request, slug):
	genre = get_object_or_404(Genre, slug=slug)
	books = genre.books.all
	return render(request, "home/for_column_view.html", {'user': request.user.is_authenticated, "title": genre, "books": books})

def tag_list(request):
	tags = Tag.objects.all
	return render(request, "home/tag_list.html", {'user': request.user.is_authenticated, "title": "Теги", "tags": tags})

def genre_list(request):
	genres = Genre.objects.all
	return render(request, "home/genre_list.html", {'user': request.user.is_authenticated, "title": "Жанры", "genres": genres})

def rec_book(request):
	books = Book.objects.order_by('-pub_date')
	return render(request, "home/section.html", {'user': request.user.is_authenticated, "title": "Недавние", "books": books})

def book(request, book_id):
	book = get_object_or_404(Book, id=book_id)
	book.views += 1
	book.save()
	chapters = Chapter.objects.filter(book_id=book_id).order_by("-number")
	chapters_ = chapters[::-1]
	return render(request, "home/book.html", {'user': request.user.is_authenticated, "book": book, "chapters": chapters, "chapters_": chapters_})

def chapter(request, book_id, number):
	chapters = Chapter.objects.filter(book_id=book_id)
	chapter = chapters.get(number=number)
	book = get_object_or_404(Book, id=book_id)
	book.views += 1
	book.save()
	next_ = False
	back_ = False
	try:
		a = chapters.get(number=(number + 1))
		next_ = a
	except:
		pass

	try:
		a = chapters.get(number=(number - 1))
		back_ = a
	except:
		pass
	print(back_, next_)
	return render(request, "home/only_text.html", {'user': request.user.is_authenticated, "chapter": chapter, "next_": next_, "back_": back_})