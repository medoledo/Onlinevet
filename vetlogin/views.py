from django.shortcuts import render , redirect , get_object_or_404
from django.http import HttpResponse , HttpResponseForbidden
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .models import Owner
from birds.forms import BirdForm, BirddailypriceForm
from birds.models import Bird, Birddailyprice , DoneBird
from prices.models import Item , Category
from prices.forms import ItemForm , CategoryForm
import pandas as pd
from datetime import date  # Add this import
from userhours.models import UserHours , UserProfile
from userhours.forms import UserHoursForm , UserProfileForm
from owners.models import Owner
from owners.forms import Owner , OwnerForm , PetTypeForm
from invoice.forms import Invoice 
import json
from django.http import JsonResponse
from django.db.models import Sum
from openpyxl import Workbook
from django.utils.timezone import now
from usercreation.forms import UserForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.utils.dateparse import parse_date
from newvisit.models import Visit
from newvisit.forms import VisitForm , Visit
from django.utils import timezone
from datetime import datetime
from django.db.models import Q
from django.db import transaction
from bought.models import Bought
from bought.forms import BoughtForm
from django.db.models.functions import TruncMonth
from datetime import datetime, timedelta
import calendar


ALLOWED_USERS = ["medoledo144", "M-Mustafa"]

def user_restricted(view_func):
    """Decorator to restrict access to specific users only"""
    def wrapper(request, *args, **kwargs):
        if request.user.username not in ALLOWED_USERS:
            return HttpResponseForbidden("You are not authorized to access this page.")
        return view_func(request, *args, **kwargs)
    return wrapper





# Create your views here.
def vetlogin(request):  # Function name changed here
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/home/')  # Redirect after login
        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'vetlogin/login.html')
@login_required(login_url='/login/')
def home(request):
    return render(request, 'homepage/home.html')


@login_required(login_url='/login/')
@user_restricted
def pricesedit(request):
 
    query = request.GET.get('search', '')
    query_category = request.GET.get('category', '')
    low_stock = request.GET.get('low_stock', '')
    sort_exp = request.GET.get('sort_exp', '')
    show_expired = request.GET.get('show_expired', '')

    items = Item.objects.filter(is_deleted=False)  # Exclude deleted items

    if query:
        items = items.filter(name__icontains=query)

    if query_category:
        items = items.filter(category__name=query_category)

    if low_stock:
        items = items.filter(quantity__lt=5)

    if sort_exp:
        items = items.order_by('exp')  # Nearest expiration date first

    if show_expired:
        items = items.filter(exp__lt=now().date())  # Show only expired items

    categories = Category.objects.all()

    # If it's an AJAX request, return results as JSON
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        items_data = [{
            'id': item.id,
            'name': item.name,
            'category': item.category.name,
            'price': item.price,
            'quantity': item.quantity,
            'exp': item.exp.strftime("%Y-%m-%d"),
            'is_expired': item.exp < now().date()  # Check if expired
        } for item in items]

        return JsonResponse({'items': items_data})

    return render(request, 'pricespage/prices_edit.html', {
        'items': items,
        'query': query,
        'query_category': query_category,
        'categories': categories,
    })
    
@login_required(login_url='/login/')
@user_restricted
def deleted_items(request):
    # Get only deleted items
    deleted_items = Item.objects.filter(is_deleted=True)

    return render(request, 'pricespage/deleted_items.html', {
        'deleted_items': deleted_items
    })
    
@login_required(login_url='/login/')
@user_restricted
def restore_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)

    # Restore the item
    item.is_deleted = False
    item.save()

    # Redirect to the deleted items page
    return redirect('deleted_items')
    
    
    
    

@login_required(login_url='/login/')
def add_category(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('pricesedit')  # Redirect back to the price list page

    categories = Category.objects.all()  # Get all categories
    category_form = CategoryForm()  # Initialize category form
    return render(request, 'pricespage/prices_edit.html', {
        'categories': categories,
        'category_form': category_form
    })


@login_required(login_url='/login/')
def delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    category.delete()
    return redirect('pricesedit')




@login_required(login_url='/login/')
def soldtoday(request):
    today = date.today()  # Get today's date

    # Ensure filtering by the correct date
    invoices = Invoice.objects.filter(date__date=today).order_by('-date')

    total_price = invoices.aggregate(Sum('total_price'))['total_price__sum'] or 0

    return render(request, 'solditemspage/sold_today_items.html', {
        'invoices': invoices,
        'total_price': total_price
    })







@login_required(login_url='/login/')
@user_restricted
def sold_items(request):

    start_date = request.GET.get('start_date', '')
    end_date = request.GET.get('end_date', '')
    category_id = request.GET.get('category', '')

    invoices = Invoice.objects.all()

    if start_date:
        invoices = invoices.filter(date__gte=start_date)
    
    if end_date:
        invoices = invoices.filter(date__lte=end_date)
    
    if category_id:
        category_name = Category.objects.get(id=category_id).name
        invoices = invoices.filter(category=category_name)
    
    invoices = invoices.order_by('-date')
    total_price = invoices.aggregate(Sum('total_price'))['total_price__sum'] or 0
    categories = Category.objects.all()

    return render(request, 'solditemspage/sold_items.html', {
        'invoices': invoices,
        'categories': categories,
        'start_date': start_date,
        'end_date': end_date,
        'category_id': category_id,
        'total_price': total_price
    })
    
    
    
def delete_item(request, item_id):
    item = Item.objects.get(id=item_id)
    item.is_deleted = True
    item.save()
    return redirect('solditemspage/sold_items')
    
    
    
    
@login_required(login_url='/login/')
@user_restricted
def delete_invoice(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id)
    invoice.delete()
    return redirect('sold_items')  # Redirect to the sold items page
    
    
    
    
    
def download_sold_items_excel(request):
    # Get the filtered data based on the request parameters
    start_date = request.GET.get('start_date', '')
    end_date = request.GET.get('end_date', '')
    category_id = request.GET.get('category', '')

    invoices = Invoice.objects.all()

    # Filter by start date if provided
    if start_date:
        invoices = invoices.filter(date__gte=start_date)
    
    # Filter by end date if provided
    if end_date:
        invoices = invoices.filter(date__lte=end_date)
    
    # Filter by category if provided
    if category_id:
        category_name = Category.objects.get(id=category_id).name
        invoices = invoices.filter(category=category_name)
    
    # Order by date, newest first
    invoices = invoices.order_by('-date')

    # Create an Excel workbook and a worksheet
    wb = Workbook()
    ws = wb.active
    ws.title = "Sold Items"

    # Define the column headers
    headers = ['Item', 'Category', 'Price', 'Quantity', 'Discount', 'Total Price', 'Date']
    ws.append(headers)

    # Populate the worksheet with data from invoices
    for invoice in invoices:
        ws.append([
            invoice.item.name,
            invoice.category,
            invoice.price,
            invoice.quantity,
            invoice.discount,
            invoice.total_price,
            invoice.date.strftime('%Y-%m-%d %H:%M:%S')  # Format the date
        ])

    # Set up the response for file download
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="sold_items.xlsx"'

    # Save the workbook to the response
    wb.save(response)
    return response
    
    
    



@login_required(login_url='/login/')
def workhours(request):
    return render(request, 'workhourspage/workhours.html')

# View to display birds list with search functionality

def birds_list(request):
    query = request.GET.get('search', '')  # Search by name
    phone_query = request.GET.get('phone_number', '')  # Search by phone number
    bird_type_filter = request.GET.get('bird_type', '')  # Filter by bird type
    start_date = request.GET.get('start_date', '')  # Filter by start date
    end_date = request.GET.get('end_date', '')  # Filter by end date
    sort_by = request.GET.get('sort_by', 'date_of_payment')  # Default sorting
    order = request.GET.get('order', 'asc')  # Default sorting order

    # Base queryset for birds
    birds = Bird.objects.all()

    # Apply filters if any
    if query:
        birds = birds.filter(name__icontains=query)
    if phone_query:
        birds = birds.filter(phone_number__icontains=phone_query)
    if bird_type_filter:
        birds = birds.filter(bird_type_id=bird_type_filter)
    if start_date:
        birds = birds.filter(date_of_payment__gte=start_date)
    if end_date:
        birds = birds.filter(date_of_payment__lte=end_date)

    # Sorting logic
    if order == 'desc':
        birds = birds.order_by(f'-{sort_by}')
    else:
        birds = birds.order_by(sort_by)

    # Get total quantities for each bird type
    bird_type_totals = Bird.objects.values('bird_type__bird_type') \
                                    .annotate(total_quantity=Sum('quantity')) \
                                    .filter(bird_type__isnull=False)  # Ensure bird_type is not null
    bird_types = Birddailyprice.objects.all()  # Assuming BirdType is stored in Birddailyprice

    return render(request, "birdspage/birds.html", {
        "birds": birds,
        "query": query,
        "phone_query": phone_query,
        "bird_type_filter": bird_type_filter,
        "bird_types": bird_types,
        "start_date": start_date,
        "end_date": end_date,
        "bird_type_totals": bird_type_totals
    })

def mark_done(request, bird_id):
    bird = get_object_or_404(Bird, id=bird_id)  # Fetch bird or return 404 if not found
    
    # Move the bird to done birds
    DoneBird.objects.create(
        name=bird.name,
        phone_number=bird.phone_number,
        bird_type=bird.bird_type,
        quantity=bird.quantity,
        price=bird.price,
        total=bird.total,
        payed_money=bird.payed_money,
        remaining_to_pay=bird.remaining_to_pay,
        date_of_payment=bird.date_of_payment
    )
    
    # Delete the bird from the original table
    bird.delete()

    return redirect('birds_list')


def done_birds(request):
    # Fetch all done birds and order them by done_date (newest first)
    done_birds = DoneBird.objects.all().order_by('-done_date')  # Order by done_date in descending order
    return render(request, 'birdspage/done_birds.html', {'done_birds': done_birds})


def add_bird(request):
    birds = Birddailyprice.objects.all()
    bird_prices = {bird.bird_type: bird.bird_price for bird in birds}

    if request.method == 'POST':
        name = request.POST.get('name')
        phone_number = request.POST.get('phone_number')
        payed_money = float(request.POST.get('payed_money', 0))
        
        bird_types = request.POST.getlist('bird_type')
        quantities = request.POST.getlist('quantity')

        first_row = True  # Track the first row for payed_money handling

        for bird_type_name, quantity in zip(bird_types, quantities):
            bird_type = Birddailyprice.objects.get(bird_type=bird_type_name)
            price = bird_type.bird_price
            quantity = int(quantity)
            total = price * quantity
            
            remaining_to_pay = total - (payed_money if first_row else 0)
            payed = payed_money if first_row else 0
            first_row = False  # Ensure payed_money is only saved for the first row

            Bird.objects.create(
                name=name,
                phone_number=phone_number,
                bird_type=bird_type,
                price=price,
                quantity=quantity,
                payed_money=payed,
                total=total,
                remaining_to_pay=remaining_to_pay
            )

        return redirect('birds_list')

    return render(request, 'birdspage/add_bird.html', {
        'form': BirdForm(),
        'bird_prices': json.dumps(bird_prices),
        'birds': birds,
    })


# View to add a new bird type
def add_bird_type(request):
    if request.method == 'POST':
        form = BirddailypriceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add_bird_type')  # Redirect to refresh the page
    else:
        form = BirddailypriceForm()

    bird_types = Birddailyprice.objects.all()  # Fetch all bird types

    return render(request, 'birdspage/add_bird_type.html', {'form': form, 'bird_types': bird_types})

# View to edit a bird type
def edit_bird_type(request, pk):
    bird_type = get_object_or_404(Birddailyprice, pk=pk)
    if request.method == 'POST':
        form = BirddailypriceForm(request.POST, instance=bird_type)
        if form.is_valid():
            form.save()
            return redirect('add_bird_type')  # Redirect to refresh the page
    else:
        form = BirddailypriceForm(instance=bird_type)

    return render(request, 'birdspage/edit_bird_type.html', {'form': form, 'bird_type': bird_type})

# View to delete a bird type
def delete_bird_type(request, pk):
    bird_type = get_object_or_404(Birddailyprice, pk=pk)
    if request.method == 'POST':
        bird_type.delete()
        return redirect('add_bird_type')  # Redirect after deletion
    return render(request, 'birdspage/delete_bird_type.html', {'bird_type': bird_type})

# View to display bird details and edit
def bird_detail(request, pk):
    bird = get_object_or_404(Bird, pk=pk)
    bird_prices = {bird_type.id: bird_type.bird_price for bird_type in Birddailyprice.objects.all()}
    
    if request.method == 'POST':
        form = BirdForm(request.POST, instance=bird)
        if form.is_valid():
            form.save()
            return redirect('birds_list')  # Redirect to birds list after editing
    else:
        form = BirdForm(instance=bird)

    return render(request, 'birdspage/bird_detail.html', {
        'form': form,
        'bird': bird,
        'bird_prices': bird_prices,  # Pass the prices to the template
    })
    
    
def delete_bird(request, pk):
    bird = get_object_or_404(Bird, pk=pk)
    print(f"Attempting to delete bird with ID {pk}")
    if request.method == 'POST':  # Ensure it's a POST request for deletion
        bird.delete()  # Delete the bird from the database
        print(f"Bird with ID {pk} deleted successfully")
        return redirect('birds_list')  # Redirect to birds list after deletion
    else:
        print("Delete request was not POST")
        return redirect('birds_list')  # Redirect if not a POST request



@login_required
def prices(request):
    query = request.GET.get('search', '')
    query_category = request.GET.get('category', '')
    low_stock = request.GET.get('low_stock', '')
    sort_exp = request.GET.get('sort_exp', '')
    show_expired = request.GET.get('show_expired', '')

    today = now().date()  # Get today's date

    items = Item.objects.filter(is_deleted=False)

    if query:
        items = items.filter(name__icontains=query)

    if query_category:
        items = items.filter(category__name=query_category)

    if low_stock:
        items = items.filter(quantity__lt=5)

    if sort_exp:
        items = items.order_by('exp')

    if show_expired:
        items = items.filter(exp__lt=today)  # Filter only expired items

    categories = Category.objects.all()

    # Handle AJAX request
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'items': [
                {
                    'name': item.name,
                    'category': item.category.name,
                    'price': item.price,
                    'quantity': item.quantity,
                    'exp': item.exp.strftime("%Y-%m-%d"),
                    'is_expired': item.exp < today  # Check if expired
                }
                for item in items
            ]
        })

    return render(request, 'pricespage/prices.html', {
        'items': items,
        'query': query,
        'query_category': query_category,
        'categories': categories,
        'today': today  # Send today's date to the template
    })



# Display the form to add a new item
@login_required(login_url='/login/')
@user_restricted
def add_item(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            form.save()  # Save the new item to the database
            return redirect('pricesedit')  # Redirect back to the price list page
    else:
        form = ItemForm()  # If it's a GET request, just show the empty form
    
    return render(request, 'pricespage/add_item.html', {'form': form})

# Display and edit an item
@login_required(login_url='/login/')
@user_restricted
def edit_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)  # Fetch the item by ID

    if request.method == 'POST':
        form = ItemForm(request.POST, instance=item)  # Pre-fill the form with existing item data
        if form.is_valid():
            form.save()  # Save the updated item data
            return redirect('pricesedit')  # Redirect to the price list page
    else:
        form = ItemForm(instance=item)  # Display the form with existing item data
    
    return render(request, 'pricespage/edit_item.html', {'form': form, 'item': item})


@login_required(login_url='/login/')
@user_restricted
def delete_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    if request.method == "POST":
        item.delete()
        return redirect('pricesedit')  # Redirect to the price list after deletion
    return render(request, 'pricespage/edit_item.html', {'item': item})
    
@login_required(login_url='/login/')
@user_restricted   
def download_price_list(request):
    # Get all non-deleted items from the database, including expiration date
    items = Item.objects.filter(is_deleted=False).values('name', 'category__name', 'price', 'quantity', 'exp')
    
    # Create a DataFrame from the query result
    df = pd.DataFrame(items)

    
    # Create an HTTP response with the appropriate content type for Excel
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=price_list.xlsx'
    
    # Write the DataFrame to the response as an Excel file
    df.to_excel(response, index=False, engine='openpyxl')
    
    return response

    
    
    
    
    # Display owners list
@login_required(login_url='/login/')
def owners(request):
    # Get the search parameters from GET request
    search_name = request.GET.get('search_name', '')
    search_number = request.GET.get('search_number', '')

    # Filter owners by name and phone number if search parameters are provided
    owners = Owner.objects.all()

    if search_name:
        owners = owners.filter(name__icontains=search_name)  # Filter by name (case-insensitive)

    if search_number:
        owners = owners.filter(phone_number__icontains=search_number)  # Filter by phone number (case-insensitive)

    return render(request, 'ownerspage/owners.html', {'owners': owners})

# Add a new owner
@login_required(login_url='/login/')
def add_owner(request):
    if request.method == 'POST':
        form = OwnerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('owners')  # Redirects to the owners page after saving
    else:
        form = OwnerForm()
    return render(request, 'ownerspage/add_owner.html', {'form': form})


@login_required(login_url='/login/')
def add_pet_type(request):
    if request.method == 'POST':
        form = PetTypeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('owners')  # Redirects to the owners list after adding the pet type
    else:
        form = PetTypeForm()
    return render(request, 'ownerspage/add_pet_type.html', {'form': form})


@login_required(login_url='/login/')
def edit_owner(request, owner_id):
    owner = get_object_or_404(Owner, id=owner_id)
    if request.method == 'POST':
        form = OwnerForm(request.POST, instance=owner)
        if form.is_valid():
            form.save()
            return redirect('owners')
    else:
        form = OwnerForm(instance=owner)
    return render(request, 'ownerspage/edit_owner.html', {'form': form, 'owner': owner})
    
     
@login_required
def delete_owner(request, owner_id):
    owner = get_object_or_404(Owner, id=owner_id)
    if request.method == 'POST':
        owner.delete()
        messages.success(request, 'Owner deleted successfully.')
        return redirect('owners')  # Redirect back to the owners list page
    return render(request, 'ownerspage/confirm_delete.html', {'owner': owner})
    
@login_required(login_url='/login/')
@user_restricted    
def download_owners(request):
    # Get the filter parameters from the request
    search_name = request.GET.get('search_name', '')
    search_number = request.GET.get('search_number', '')

    # Start with all owners
    owners = Owner.objects.all().select_related('pet_type')

    # Apply filters if any
    if search_name:
        owners = owners.filter(name__icontains=search_name)

    if search_number:
        owners = owners.filter(phone_number__icontains=search_number)

    # Fetch the filtered owners data, including the pet type name
    owners_data = owners.values(
        'name', 
        'phone_number', 
        'pet_name', 
        'pet_type__name',  # Accessing the related pet_type name
        'sex'
    )

    # Create a DataFrame from the filtered owners data
    df = pd.DataFrame(owners_data)

    # Rename the column for better clarity
    df.rename(columns={'pet_type__name': 'pet_type'}, inplace=True)

    # Create an HTTP response with the appropriate content type for Excel
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=owners_list_filtered.xlsx'

    # Write the DataFrame to the response as an Excel file
    df.to_excel(response, index=False, engine='openpyxl')

    return response
    

# View to display sold items




@login_required(login_url='/login/')
def user_hours_page(request):
    # Get all user profiles from the database
    user_profiles = UserProfile.objects.all()
    names_choices = [(profile.id, profile.name) for profile in user_profiles]

    # Get the filter parameters from the GET request
    selected_name = request.GET.get('name')
    from_date = request.GET.get('from_date')
    to_date = request.GET.get('to_date')

    # Start with all user hours
    hours = UserHours.objects.all()

    # Apply name filter
    if selected_name:
        hours = hours.filter(user_id=selected_name)

    # Apply from_date filter (if valid) on arrival_time
    if from_date:
        from_date = parse_date(from_date)
        if from_date:
            hours = hours.filter(arrival_time__date__gte=from_date)

    # Apply to_date filter (if valid) on arrival_time
    if to_date:
        to_date = parse_date(to_date)
        if to_date:
            hours = hours.filter(arrival_time__date__lte=to_date)

    # Order the user hours by arrival_time (newest first)
    hours = hours.order_by('-arrival_time')

    return render(request, 'userhourspage/userhours.html', {
        'names_choices': names_choices,  # Pass choices correctly
        'hours': hours,
    })



@login_required(login_url='/login/')
def add_user_hours(request):
    if request.method == 'POST':
        form = UserHoursForm(request.POST)
        if form.is_valid():
            form.save()  # Save the new user hours to the database
            return redirect('userhours')  # Redirect to the user hours page after saving
    else:
        form = UserHoursForm()

    return render(request, 'userhourspage/add_userhours.html', {'form': form})


@login_required(login_url='/login/')
@user_restricted
def add_user_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST)
        if form.is_valid():
            form.save()  # Save the new user profile to the database
            return redirect('userhours')  # Redirect back to the user hours page
    else:
        form = UserProfileForm()

    return render(request, 'userhourspage/add_userprofile.html', {'form': form})




    
@login_required(login_url='/login/')
@user_restricted
def edit_user_hours(request, pk):
    user_hour = get_object_or_404(UserHours, pk=pk)  # Get the specific user hour instance

    if request.method == 'POST':
        form = UserHoursForm(request.POST, instance=user_hour)  # Bind the form to the instance
        if form.is_valid():
            form.save()  # Save the updated data
            return redirect('userhours')  # Redirect to the user hours list page
    else:
        form = UserHoursForm(instance=user_hour)  # Pre-populate the form with existing data
 
    return render(request, 'userhourspage/edit_userhours.html', {
        'form': form,
        'user_hour': user_hour  # Pass the user_hour instance to the template
    })


@login_required(login_url='/login/')
@user_restricted
def manage_names(request):
    users = UserProfile.objects.all()
    return render(request, 'userhourspage/manage_names.html', {'users': users})


@login_required(login_url='/login/')
@user_restricted
def delete_name(request, user_id):
    user = get_object_or_404(UserProfile, id=user_id)
    user.delete()
    return redirect('manage_names')






@login_required(login_url='/login/')
@user_restricted
def download_user_hours_excel(request):
    # Get the filter value from the GET request
    filter_name = request.GET.get('name', None)
    
    if filter_name:
        # If a filter is applied, filter the UserHours objects based on the name
        hours = UserHours.objects.filter(user__name=filter_name).values('user__name', 'arrival_time', 'left_time', 'total_hours')
    else:
        # If no filter is applied, show all UserHours objects
        hours = UserHours.objects.all().values('user__name', 'arrival_time', 'left_time', 'total_hours')

    # Convert to DataFrame
    df = pd.DataFrame(list(hours))

    # Ensure datetime fields are timezone-unaware (remove timezone)
    if 'arrival_time' in df.columns:
        df['arrival_time'] = df['arrival_time'].apply(lambda x: x.replace(tzinfo=None) if x else x)
    if 'left_time' in df.columns:
        df['left_time'] = df['left_time'].apply(lambda x: x.replace(tzinfo=None) if x else x)

    # Rename columns to be more user-friendly
    df.rename(columns={
        'user__name': 'User Name',
        'arrival_time': 'Arrival Time',
        'left_time': 'Left Time',
        'total_hours': 'Total Hours',
    }, inplace=True)

    # Create an Excel response
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="user_hours.xlsx"'

    # Write to Excel using the Pandas ExcelWriter
    with pd.ExcelWriter(response, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='User Hours')

    return response


@login_required(login_url='/login/')
@user_restricted
def delete_user_hours(request, pk):
    user_hour = get_object_or_404(UserHours, pk=pk)  # Get the specific user hour instance

    if request.method == 'POST':  # Ensure it's a POST request for deletion
        user_hour.delete()  # Delete the user hours instance
        return redirect('userhours')  # Redirect to the user hours list page

    # If it's a GET request, redirect back to the edit page
    return redirect('edit_user_hours', pk=pk)



@login_required(login_url='/login/')
def get_items_by_category(request, category_id):
    # Fetch all items in the selected category, including those with zero quantity
    items = Item.objects.filter(category_id=category_id, is_deleted=False).order_by('name')  # Order by name (alphabetically)

    # Prepare item data for dropdown
    item_data = [
        {
            'id': item.id,
            'name': f"{item.name} (out of stock)" if item.quantity == 0 else item.name,
            'price': item.price,
            'exp': item.exp,
            'out_of_stock': item.quantity == 0  # Flag to indicate out of stock
        }
        for item in items
    ]

    return JsonResponse({'items': item_data})




# views.py
@login_required
def create_invoice(request):
    categories = Category.objects.all()

    if request.method == 'POST':
        categories_selected = request.POST.getlist('category[]')
        items = request.POST.getlist('item[]')
        prices = request.POST.getlist('price[]')
        quantities = request.POST.getlist('quantity[]')
        discounts = request.POST.getlist('discount[]')
        total_prices = request.POST.getlist('total_price[]')
        expirations = request.POST.getlist('exp[]')

        error_message = None

        if not categories_selected or not items or not prices or not quantities or not discounts or not total_prices or not expirations:
            error_message = "All fields must be filled in."
            return render(request, 'invoicepage/invoice.html', {'error_message': error_message, 'categories': categories})

        for category_id, item_id, price, quantity, discount, total_price, exp in zip(
            categories_selected, items, prices, quantities, discounts, total_prices, expirations
        ):
            try:
                item = Item.objects.get(id=item_id)
            except Item.DoesNotExist:
                error_message = f"Item with ID {item_id} does not exist."
                return render(request, 'invoicepage/invoice.html', {'error_message': error_message, 'categories': categories})

            if item.quantity < float(quantity):
                error_message = f"Insufficient stock for {item.name}. Available stock: {item.quantity}"
                return render(request, 'invoicepage/invoice.html', {'error_message': error_message, 'categories': categories})

            discount_value = float(discount) if discount else 0
            total_price_calculated = (float(price) * float(quantity)) - discount_value

            item.quantity -= float(quantity)
            item.save()

            # Create the invoice
            Invoice.objects.create(
                category=Category.objects.get(id=category_id).name,
                item=item,
                price=price,
                quantity=quantity,
                discount=discount,
                total_price=total_price_calculated,
                exp=exp
            )

        # Redirect to sold_today_items.html after invoice creation
        return redirect('sold_today_items')  # Use the URL name of the sold_today_items view

    return render(request, 'invoicepage/invoice.html', {'categories': categories})








@login_required(login_url='/login/')
@user_restricted
def add_user(request):
    if request.method == 'POST':
        # Handle user creation
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username and password:
            user = User.objects.create_user(username=username, password=password)
            user.save()
            messages.success(request, 'User created successfully.')
            return redirect('add_user')  # Redirect to the same page to show updated list

    # Fetch all users
    users = User.objects.all()

    return render(request, 'adduserspage/add_user.html', {'users': users})




@login_required(login_url='/login/')
@user_restricted
def delete_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        
        # Prevent deletion of 'medoledo144' and 'M-Mustafa'
        if user.username in ["medoledo144", "M-Mustafa"]:
            messages.error(request, f"You cannot delete the user '{user.username}'.")
        else:
            user.delete()
            messages.success(request, f'User "{user.username}" deleted successfully.')
    except User.DoesNotExist:
        messages.error(request, 'User not found.')

    return redirect('add_user')  # Redirect back to the same page after deletion




@login_required(login_url='/login/')
@user_restricted
def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)

    
    # Prevent medoledo144 from editing
    if user.username == 'medoledo144':
        return HttpResponseForbidden("You cannot edit the medoledo144 user.")
    
    if request.user.username not in ALLOWED_USERS:
        return HttpResponseForbidden("You do not have permission to perform this action.")
    
    if request.method == 'POST':
        # Check if the password change is requested
        if 'change_password' in request.POST:
            password_form = PasswordChangeForm(user=user, data=request.POST)
            if password_form.is_valid():
                password_form.save()
                messages.success(request, 'Password updated successfully.')
                return redirect('edit_user', user_id=user.id)
            else:
                messages.error(request, 'Error updating password.')
        else:
            # Update the username
            username_form = UserChangeForm(request.POST, instance=user)
            if username_form.is_valid():
                username_form.save()
                messages.success(request, 'Username updated successfully.')
                return redirect('edit_user', user_id=user.id)
    else:
        # Create the forms for editing username and password
        username_form = UserChangeForm(instance=user)
        password_form = PasswordChangeForm(user=user)

    return render(request, 'adduserspage/edit_user.html', {
        'user': user,
        'username_form': username_form,
        'password_form': password_form,
    })




@login_required
def visits_list(request):
    visits = Visit.objects.all()
    
    # Filter by Owner Name
    owner_name = request.GET.get('owner_name', '')
    if owner_name:
        visits = visits.filter(owner__name__icontains=owner_name)

    # Filter by Phone Number
    phone_number = request.GET.get('phone_number', '')
    if phone_number:
        visits = visits.filter(owner__phone_number__icontains=phone_number)

    # Filter by Visit Date Range
    from_date = request.GET.get('from_date', '')
    to_date = request.GET.get('to_date', '')
    
    if from_date and to_date:
        # Filter visits based on visit_date within the given range
        visits = visits.filter(visit_date__range=[from_date, to_date])
    elif from_date:
        # Filter visits with visit_date greater than or equal to from_date
        visits = visits.filter(visit_date__gte=from_date)
    elif to_date:
        # Filter visits with visit_date less than or equal to to_date
        visits = visits.filter(visit_date__lte=to_date)

    # Sorting the visits by visit date (newest first)
    visits = visits.order_by('-visit_date')

    return render(request, 'newvisitspage/new_visit.html', {'visits': visits})

@login_required
def add_visit(request):
    owners = Owner.objects.all()
    if request.method == 'POST':
        form = VisitForm(request.POST)
        if form.is_valid():
            visit = form.save(commit=False)

            # Ensure pet_name and pet_type are taken from the associated Owner model
            owner = form.cleaned_data['owner']
            visit.pet_name = owner.pet_name
            visit.pet_type = owner.pet_type  # Set the correct pet_type value
            visit.sex = owner.sex  # Automatically use sex from Owner
            
            visit.by_user = request.user.username
            visit.save()
            return redirect('visits_list')
        else:
            print("Form Errors:", form.errors)  # Print form errors for debugging
    else:
        form = VisitForm()

    return render(request, 'newvisitspage/add_visit.html', {'form': form, 'owners': owners})





@login_required
def view_visit(request, visit_id):
    visit = get_object_or_404(Visit, id=visit_id)
    return render(request, 'newvisitspage/visit_details.html', {'visit': visit})


@login_required(login_url='/login/')
def get_owner_details(request, owner_id):
    owner = Owner.objects.get(id=owner_id)
    owner_data = {
        'phone_number': owner.phone_number,
        'pet_name': owner.pet_name,
        'pet_type': owner.pet_type.name,
        'sex': owner.sex,
    }
    return JsonResponse(owner_data)

@login_required(login_url='/login/')
def search_owners(request):
    query = request.GET.get('q', '')  # Get the search query parameter 'q'
    owners = Owner.objects.filter(name__icontains=query)[:10]  # Filter owners by name and limit the results

    results = [{"id": owner.id, "text": owner.name} for owner in owners]

    return JsonResponse({"results": results})

@login_required
def edit_visit(request, visit_id):
    visit = get_object_or_404(Visit, id=visit_id)

    if request.method == 'POST':
        form = VisitForm(request.POST, instance=visit)
        if form.is_valid():
            form.save()
            return redirect('view_visit', visit_id=visit.id)
    else:
        form = VisitForm(instance=visit)

    return render(request, 'newvisitspage/edit_visit.html', {'form': form, 'visit': visit})


    
@login_required
def next_check(request):
    # Get today's date
    today = timezone.localdate()  # Get the current date (without time part)
    
    # Filter visits where the next_check_date is today's date
    visits = Visit.objects.filter(next_check_date=today)
    
    return render(request, 'nextcheckpage/next_check.html', {'visits': visits})




@login_required(login_url='/login/')
def bought_today(request):
    # Get today's date
    today = datetime.now().date()

    # Filter items where the date_of_buying date matches today's date
    items = Bought.objects.filter(date_of_buying__date=today)

    # Calculate total bought amount for today
    total_bought = items.aggregate(Sum('total_price'))['total_price__sum'] or 0

    return render(request, 'boughtpage/bought_today.html', {
        'items': items,
        'total_bought': total_bought
    })









@login_required(login_url='/login/')
@user_restricted
def bought(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':  # Check if it's an AJAX request
        query = request.GET.get('search', '')
        start_date = request.GET.get('start_date', '')
        end_date = request.GET.get('end_date', '')

        items = Bought.objects.all()

        if query:
            items = items.filter(item__icontains=query)
        
        if start_date:
            items = items.filter(date_of_buying__gte=start_date)
        
        if end_date:
            items = items.filter(date_of_buying__lte=end_date)

        data = list(items.values('id', 'item', 'price', 'quantity', 'total_price', 'date_of_buying'))
        return JsonResponse({'items': data})  # Send JSON response

    else:
        query = request.GET.get('search', '')
        start_date = request.GET.get('start_date', '')
        end_date = request.GET.get('end_date', '')

        items = Bought.objects.all()

        if query:
            items = items.filter(item__icontains=query)
        
        if start_date:
            items = items.filter(date_of_buying__gte=start_date)
        
        if end_date:
            items = items.filter(date_of_buying__lte=end_date)

        total_bought = Bought.objects.aggregate(Sum('total_price'))['total_price__sum'] or 0
        return render(request, 'boughtpage/bought.html', {
            'items': items,
            'query': query,
            'start_date': start_date,
            'end_date': end_date,
            'total_bought': total_bought
        })

@login_required(login_url='/login/')
def add_bought_item(request):
    if request.method == "POST":
        form = BoughtForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('bought_today')
    else:
        form = BoughtForm()
    return render(request, 'boughtpage/add_bought_item.html', {'form': form})

@login_required(login_url='/login/')
def download_bought_excel(request):
    query = request.GET.get('search', '').strip()
    start_date = request.GET.get('start_date', '').strip()
    end_date = request.GET.get('end_date', '').strip()

    items = Bought.objects.all()

    # Apply filters
    if query:
        items = items.filter(item__icontains=query)
    
    if start_date:
        items = items.filter(date_of_buying__gte=start_date)
    
    if end_date:
        items = items.filter(date_of_buying__lte=end_date)

    # Convert queryset to DataFrame
    data = list(items.values('item', 'price', 'quantity', 'total_price', 'date_of_buying'))
    df = pd.DataFrame(data)

    # Convert timezone-aware datetime fields to naive (if applicable)
    if 'date_of_buying' in df.columns:
        df['date_of_buying'] = df['date_of_buying'].apply(lambda x: x.replace(tzinfo=None) if pd.notnull(x) else x)

    # Prepare the response
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="filtered_bought_items.xlsx"'

    # Write DataFrame to Excel
    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)

    return response

@login_required(login_url='/login/')
@user_restricted
def edit_bought_item(request, item_id):
    item = get_object_or_404(Bought, id=item_id)
    
    if request.method == 'POST':
        form = BoughtForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('bought')  # Redirect to bought items page
    else:
        form = BoughtForm(instance=item)

    return render(request, 'boughtpage/edit_bought.html', {'form': form, 'item': item})

@login_required(login_url='/login/')
@user_restricted
def delete_bought_item(request, item_id):
    item = get_object_or_404(Bought, id=item_id)
    item.delete()
    return redirect('bought')



@login_required(login_url='/login/')
@user_restricted
def dashboard(request):
    try:
        # Get the current month and year
        current_month = datetime.now().month
        current_year = datetime.now().year

        # Get selected values (convert to int, default to full year if month is empty)
        selected_month = request.GET.get('month')
        selected_year = int(request.GET.get('year', current_year))

        if selected_month:  
            # If a month is selected, filter by that month
            selected_month = int(selected_month)
            first_day = f"{selected_year}-{selected_month:02d}-01"
            last_day = f"{selected_year}-{selected_month:02d}-{calendar.monthrange(selected_year, selected_month)[1]}"
        else:
            # If no month is selected, filter for the whole year
            first_day = f"{selected_year}-01-01"
            last_day = f"{selected_year}-12-31"

        # Convert dates to datetime objects
        start_date = datetime.strptime(first_day, "%Y-%m-%d")
        end_date = datetime.strptime(last_day, "%Y-%m-%d") + timedelta(days=1)  # Ensure full last day coverage

        # Get filtered total sold, bought, and profit
        total_sold = Invoice.objects.filter(date__gte=start_date, date__lt=end_date).aggregate(total_sold=Sum('total_price'))['total_sold'] or 0
        total_bought = Bought.objects.filter(date_of_buying__gte=start_date, date_of_buying__lt=end_date).aggregate(total_bought=Sum('total_price'))['total_bought'] or 0
        total_profit = total_sold - total_bought

    except Exception as e:
        print(f"Error calculating dashboard values: {e}")
        total_sold = total_bought = total_profit = 0

    # Get list of available months and years
    months = [(i, datetime(2000, i, 1).strftime('%B')) for i in range(1, 13)]
    years = list(range(datetime.now().year - 5, datetime.now().year + 1))

    # Pass data to the template
    return render(request, 'dashboardpage/dashboard.html', {
        'total_sold': total_sold,
        'total_bought': total_bought,
        'total_profit': total_profit,
        'months': months,
        'years': years,
        'selected_month': int(selected_month) if selected_month else "",  # Keep empty if whole year
        'selected_year': selected_year,
    })



@login_required(login_url='/login/')
def workhours(request):
    return render(request, 'workhourspage/workhours.html')



    

def logout_view(request):
    logout(request)
    return redirect('/login/')  # Redirect back to login page