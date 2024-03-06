import re

from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from .forms import *

words = []


def handle_uploaded_file(f):
    with open(f"uploads/{f.name}", "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    with open(f'uploads/{f.name}', 'r') as file:
        text = file.read()
        text = re.sub(r'[.,!?]', '', text)
        words.extend(text.split())


def index(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        word_form = WordcountForm(request.POST)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
        count = None
    else:
        form = UploadFileForm()
        word_form = WordcountForm()
        count = request.GET.get('count')
        action = request.GET.get('clear')
        global words
        if action == 'clear':
            words = []
    return render(request, 'app/index.html', {'form': form,
                                              'word_form': word_form,
                                              'count': count})


def wordcount(request):
    if request.method == 'POST':
        form = WordcountForm(request.POST)
        if form.is_valid():
            word = form.cleaned_data['word']
            count = words.count(word)
        return redirect(reverse_lazy('index') + f'?count={count}')
    return redirect('index')
