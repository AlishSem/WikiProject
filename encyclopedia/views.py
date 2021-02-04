from django.shortcuts import render
from . import util
import markdown
import requests
from django import forms
from django.urls import reverse
from django.http import HttpResponseRedirect
from random import randint



class SearchForm(forms.Form):
    query = forms.CharField(label="", widget=forms.TextInput(attrs={'placeholder': 'Search Wiki',
                                                                    'style': 'width:100%'}))



def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": SearchForm()
        
    })

def entry(request, title):
    if request.method == "POST":
        title = request.POST["title"]
        filee = request.POST["content"]
        filee = markdown.markdown(filee) 
        util.save_entry(title,filee)
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "filee": filee
        })
    else:
        filee = util.get_entry(title)
        if filee:
            filee = markdown.markdown(filee)
            return render(request, "encyclopedia/entry.html", {
                "title": title,
                "filee": filee
            })
        else:
            return render(request, "encyclopedia/error.html")





def search(request):
    if request.method == "POST":
        entries_found = []  # List of entries that match query
        entries_all = util.list_entries()  # All entries
        form = SearchForm(request.POST)  # Gets info from form
        # Check if form fields are valid
        if form.is_valid():
            # Get the query to search entries/pages
            query = form.cleaned_data["query"]
            # Check if any entries/pages match query
            # If exists, redirect to entry/page
            for entry in entries_all:
                if query.lower() == entry.lower():
                    title = entry
                    entry = util.get_entry(title)
                    entry = markdown.markdown(entry)
                    return render(request, "encyclopedia/entry.html", {
                        "title": title,
                        "filee": entry
                    })
                # Partial matches are displayed in a list
                if query.lower() in entry.lower():
                    entries_found.append(entry)
            # Return list of partial matches
            return render(request, "encyclopedia/search.html", {
                "results": entries_found,
                "item": query,
                "form": SearchForm()
            })


def newpage(request):
    if request.method == "POST":
        title = request.POST["title"]
        content = request.POST["content"]
        if util.get_entry(title):
            return render(request, "encyclopedia/exists.html")
        else:
            util.save_entry(title, content)
            return render(request, "encyclopedia/newpage.html")
    else:
        return render(request, "encyclopedia/newpage.html")

    
def edit(request, title):
    filee = util.get_entry(title)
    return render(request, "encyclopedia/edit.html", {
        "title":title,
        "filee": filee

    })

def random(request):
    a = len(util.list_entries()) - 1
    b = randint(0,a)
    title = util.list_entries()[b]
    return entry(request, title)






        
