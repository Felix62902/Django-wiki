from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from . import util
from .forms import CreateNewEntry
import markdown2
import random

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def page(request, entry):
    # check if entry exists
    try:
        # convert markdown to html
        content =  markdown2.markdown(util.get_entry(entry))
    except TypeError:
        # raise Http404("Page not found")
        return render(request, "encyclopedia/error404.html" )
    
        # to distinguish if user went to the URL or searched something that leads them to it
    return render(request, "encyclopedia/pages.html", {
        "title": entry,
        "content": content })

def search(request):
    if request.method == "POST":
        query = request.POST['q']
        content = util.get_entry(query)
        if(content):
            return HttpResponseRedirect("/wiki/" + str(query))
        else:
            # if query does not exist, render a search result page with that query as substring
            allEntries = util.list_entries()
            filteredEntries = []
            for entry in allEntries:
                if (query.lower() in entry.lower()):
                    filteredEntries.append(entry)
            return render(request, "encyclopedia/searchresults.html", {"content": filteredEntries})


def addNewPage(request):
    if request.method == "POST":
                # add form data to existing db
        formTitle = request.POST['t']
        formContent = request.POST['c']
        if util.get_entry(formTitle):
                errorMessage = "Error: Title already exists, form not added."
                return render(request, "encyclopedia/newpage.html",{"error": errorMessage})
                # return
            # if form is valid, save data to db
        else:
            util.save_entry(formTitle, formContent)
            return render(request, "encyclopedia/pages.html", {
               "title": formTitle, 
               "content": formContent})
         # create a new Form
        #  newForm = CreateNewEntry()
    else:

        # unencrypt data
        return render(request, "encyclopedia/newpage.html", {})


         

def edit(request):
     if request.method == "POST":
          title= request.POST.get("title")
          content = util.get_entry(title)
          return render(request, "encyclopedia/edit.html", 
                        {"title": title, 
                         "content": content})
     
     
def save_edit(request):
     if request.method == "POST":
          title= request.POST['title']
          content = request.POST['newContent']
          util.save_entry(title, content)
          htmlContent = markdown2.markdown(util.get_entry(title))
          return render(request, "encyclopedia/pages.html", {
               "title": title, 
               "content": htmlContent})
     
def random_entry(request):
    allEntries = util.list_entries()
    randomEntry = random.choice(allEntries)
    return HttpResponseRedirect(f"/wiki/{randomEntry}")