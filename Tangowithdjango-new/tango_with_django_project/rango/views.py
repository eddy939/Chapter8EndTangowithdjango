from django.shortcuts import render
from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm

# Create your views here.
from django.http import HttpResponse

def add_page(request, category_name_slug):

    try:
        cat = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
                cat = None

    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if cat:
                page = form.save(commit=False)
                page.category = cat
                page.views = 0
                page.save()
                # probably better to use a redirect here.
                return category(request, category_name_slug)
        else:
            print form.errors
    else:
        form = PageForm()

    context_dict = {'form':form, 'category': cat, 'category_name_slug': category_name_slug }

    return render(request, 'rango/add_page.html', context_dict)


def add_category(request):
    # A HTTP POST?
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        #Have we been provided with a valid form?
        if form.is_valid():
            #Save the new category to the database.
            form.save(commit=True)
            cat = form.save(commit = True)
            print cat.slug

            #Now call the index() vies.
            #The user will be shown the homepage.
            return index(request)
        else:
            # The supplied form contained errors - just print them to the terminal.
            print form.errors
    else:
        # If the request was not a POST, display the form to enter details
        form = CategoryForm()

    #Bad form (or form details), no form supplied..
    #Render the form with error messages (if any).

    
    return  render(request, 'rango/add_category.html', {'form': form})

def category(request, category_name_slug):

    #create a context dictionary which we can pass to the template rendering engine.
    context_dict = {}

    try:
        # Can we find a category name slug with the given name?
        # If we can't, the .get() method raises a DoesNotExist exception.
        # So the .get() method returns one model instance or raises an exception
        category = Category.objects.get(slug=category_name_slug)
        context_dict['category_name'] = category.name
        context_dict['category_name_slug'] = category_name_slug

        #Retrieve all of the associated pages.
        #Note that filter returns >= 1 model instance.
        pages = Page.objects.filter(category=category)

        #Adds our results list to the template context under name pages
        context_dict['pages'] = pages
        # We also add the category object from the database to the context dictionary
        # We'll use this in the template to verify that the category exists
        context_dict['category'] = category
    except Category.DoesNotExist:
        #We get there if we didn't find the specified category
        #Don't do anything - the template displays the "no category" message for us.
        pass

    # Go render the response and return it to the client.
    print context_dict
    return render(request, 'rango/category.html', context_dict)

def clean(self):
    cleaned_data = self.cleaned_data
    url = cleaned_data.get('url')

    # If url is not empty and doesn't start with 'http://', prepend 'http://'.
    if url and not url.startswith('http://'):
        url = 'http://' + url
        cleaned_data['url'] = url

    return cleaned_data




def index(request):

    # Construct a dictionary to pass to the template engine as its context.
    #Not the key boldmessage is the same as {{ boldmessage }} in the template!

    category_list = Category.objects.order_by('-likes')[:10]
    context_dict = {'categories': category_list}

    #Return a rendered response to send to the client.
    #We make use of the shortcut function to make our lives easier
    #Note that the first parameter is the template we wish to use

    return render(request, 'rango/index.html', context_dict)

def about(request):

    # construct a dictionary to pass to the template engine as its context.
    #Not the key boldmessage is the same as {{ boldmessage )) in the template!

    context_dict = {'boldmessage': "You are doing great buddy!"}

    #Return a rendered response to send to the client.
    #WE make use of th eshortcut function to make our lives easier
    #Note that the first parameter is the template we wish to use

    return render(request, 'rango/about.html', context_dict)