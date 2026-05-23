import random
import markdown2
from django.shortcuts import render, redirect
from django.urls import reverse
from . import util

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    content = util.get_entry(title)
    if content is None:
        return render(request, "encyclopedia/error.html", {
            "message": "Page not found"
        })
    else:
        html_content = markdown2.markdown(content)
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": html_content
        })

def search(request):
    query = request.GET.get("q", "").strip()
    if not query:
        return redirect("index")
    
    entries = util.list_entries()
    # check for exact match
    if query in entries:
        return redirect("entry", title=query)
    
    # case-insensitive partial match
    results = [entry for entry in entries if query.lower() in entry.lower()]
    return render(request, "encyclopedia/search_results.html", {
        "query": query,
        "results": results
    })

def new_page(request):
    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        content = request.POST.get("content", "").strip()
        
        if not title or not content:
            return render(request, "encyclopedia/new.html", {
                "error": "Title and content cannot be empty."
            })
        
        if title in util.list_entries():
            return render(request, "encyclopedia/new.html", {
                "error": "Page already exists."
            })
        
        util.save_entry(title, content)
        return redirect("entry", title=title)
    
    return render(request, "encyclopedia/new.html")

def random_page(request):
    entries = util.list_entries()
    if not entries:
        return redirect("index")
    title = random.choice(entries)
    return redirect("entry", title=title)

def edit_page(request, title):
    content = util.get_entry(title)
    if content is None:
        return render(request, "encyclopedia/error.html", {
            "message": "Page not found"
        })
    
    return render(request, "encyclopedia/edit.html", {
        "title": title,
        "content": content
    })

def save_edit(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        util.save_entry(title, content)
        return redirect("entry", title=title)
    return redirect("index")
