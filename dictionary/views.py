from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect, get_object_or_404
from dictionary.models import *
from django.http import JsonResponse
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required

from Qaamuus.settings import MY_WEB

# Create your views here.
def login(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = auth.authenticate(username=username, password=password)
    next = request.GET.get("next", "/")
    if user is not None:
        auth.login(request, user)
        messages.add_message(request, messages.SUCCESS, 'Logged in successfully')
        return redirect(next)
    else:
        messages.add_message(request, messages.ERROR, 'Incorrect username or password')
        return redirect(next)

def logout(request):
    auth.logout(request)
    messages.add_message(request, messages.SUCCESS, 'Logged out successfully')
    return redirect("/")

@login_required
def add_word(request):
    text = request.POST.get('word')
    category_id = request.POST.get('category_id')
    definition = request.POST.get('definition', '')
    is_valid = True
    if len(text) < 2:
        is_valid = False
        messages.add_message(request, messages.ERROR, 'The word is too short')
    if len(definition) < 2:
        is_valid = False
        messages.add_message(request, messages.ERROR, 'The definition is too short')
    if is_valid:
        word = Word(text=text, definition=definition)
        word.category = Category(pk=1)
        if category_id is not None:
            word.category = Category(pk=category_id)
        word.author = request.user
        word.full_clean()
        word.save()
        messages.add_message(request, messages.SUCCESS, 'Successfully added new word')
        return redirect("/word/"+word.url_text)
    return redirect("/")

@login_required(login_url='/users/login/')
def add_comment(request):
    text = request.POST.get('comment', '')
    about = request.POST.get('about', 0)
    next = request.GET.get('next', '/')
    is_valid = True
    if len(text) < 2:
        is_valid = False
        messages.add_message(request, messages.ERROR, 'The comment is too short')
    if about < 1:
        is_valid = False
        messages.add_message(request, messages.ERROR, 'The comment has no known parent')
        return redirect(next)
    if is_valid:
        word = Word.objects.get(pk=about)
        if word is None:
            messages.add_message(request, messages.ERROR, 'Invalid comment parent')
            return redirect(next)

        new_comment = Comment()
        new_comment.text = text
        new_comment.about = word
        new_comment.author = request.user
        new_comment.save()
        word.comments = Comment.objects.filter(about__pk=about).count()
        word.save()
        messages.add_message(request, messages.SUCCESS, 'Successfully added new comment')
        return redirect("/word/"+word.url_text)
    return redirect("/")



def index(request):
    page_data = {
        "url": MY_WEB["domain_name"] + request.get_full_path(),
        "title": MY_WEB["name"] + ": Aqoon wadaaga ciyaalka xaafada",
        "image": MY_WEB["default_image"],
        "description": MY_WEB["description"],
        "is_home": True,
    }
    word_list = Word.objects.all()
    paginator = Paginator(word_list, 10)

    page = request.GET.get('page')
    try:
        words = paginator.page(page)
    except PageNotAnInteger:
        words = paginator.page(1)
    except EmptyPage:
        words = paginator.page(paginator.num_pages)

    if page is None:
        page = 1

    return render(request, "dictionary/pages/index.html", {"title": "Home", "words": words, "page": page_data, "app": MY_WEB})

def list(request):
    page_data = {
        "url": MY_WEB["domain_name"] + request.get_full_path(),
        "title": MY_WEB["name"] + ": Aqoon wadaaga ciyaalka xaafada",
        "image": MY_WEB["default_image"],
        "description": MY_WEB["description"]
    }
    word_list = Word.objects.all()
    paginator = Paginator(word_list, 20)

    page = request.GET.get('page')
    try:
        words = paginator.page(page)
    except PageNotAnInteger:
        words = paginator.page(1)
    except EmptyPage:
        words = paginator.page(paginator.num_pages)

    return render(request, "dictionary/pages/list.html", {"title": "List", "ishome":"home", "words": words, "page": page_data, "app": MY_WEB})

def detail(request, word_url):
    words = Word.objects.filter(url_text__startswith=word_url)
    comments = None
    title = "Ereyga aad codsatay ma ahan mid jira."
    if len(words) > 0:
        word = words[0]
    else:
        word = None
    page_data = {
        "url": MY_WEB["domain_name"] + request.get_full_path(),
        "title": MY_WEB["name"] + ": Aqoon wadaaga ciyaalka xaafada",
        "image": MY_WEB["default_image"],
        "description": MY_WEB["description"]
    }
    if word is not None:
        title = word.text
        page_data = {
            "url": MY_WEB["domain_name"] + request.get_full_path(),
            "title": MY_WEB["name"] + ": " + word.text,
            "image": MY_WEB["default_image"],
            "description": MY_WEB["description"]
        }
        comments = Comment.objects.filter(about__pk=word.pk)

    return render(request, "dictionary/pages/detail.html", {"title": title, "page": page_data, "word": word, "comments": comments, "app": MY_WEB})

# helper functions
def getCategories():
    categories = Category.objects.all()
    if categories is not None:
        return categories
    return None

def getAllWords(offset=0, limit=10):
    words = Word.objects.filter()[offset:limit]
