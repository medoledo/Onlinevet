from django.contrib import admin
from django.urls import path, include
from vetlogin import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', include('vetlogin.urls')),
    path('', include('vetlogin.urls')),  # Assuming you have URLs in the loginpage app
    path('home/', views.home, name='home'),
    path('prices/', views.prices, name='prices'),
    path('pricesedit/', views.pricesedit, name='pricesedit'),
    path('soldtoday/', views.soldtoday, name='sold_today_items'),

    path('sold-items/', views.sold_items, name='sold_items'),
    path('workhours/', views.workhours, name='workhours'),
    path('add_user/', views.add_user, name='add_user'),

   
   


   
   
   
   
    path('birds/', views.birds_list, name='birds_list'),
    path('add_bird/', views.add_bird, name='add_bird'),
    path('add_bird_type/', views.add_bird_type, name='add_bird_type'),
    path('edit-bird-type/<int:pk>/', views.edit_bird_type, name='edit_bird_type'),
    path('delete-bird-type/<int:pk>/', views.delete_bird_type, name='delete_bird_type'),
    path('bird/<int:pk>/', views.bird_detail, name='bird_detail'),
    path('bird/<int:pk>/delete/', views.delete_bird, name='delete_bird'),  # Add this line
    path('bird/<int:bird_id>/mark_done/', views.mark_done, name='mark_done'),
    path('done_birds/', views.done_birds, name='done_birds'),


    # Item related URLs
    path('items/', views.prices, name='prices'),  # Display all items
    path('items/add/', views.add_item, name='add_item'),  # Form to add new item
    path('items/edit/<int:item_id>/', views.edit_item, name='edit_item'),  # Edit item
    path('download-price-list/', views.download_price_list, name='download_price_list'),
    path('delete-item/<int:item_id>/', views.delete_item, name='delete_item'),



    path('owners/', views.owners, name='owners'),
    path('owners/add/', views.add_owner, name='add_owner'),
    path('owners/edit/<int:owner_id>/', views.edit_owner, name='edit_owner'),
    path('add_pet_type/', views.add_pet_type, name='add_pet_type'),  # New URL for adding pet type
    path('delete_owner/<int:owner_id>/', views.delete_owner, name='delete_owner'),
    path('download_owners/', views.download_owners, name='download_owners'),



    
    path('user_hours/', views.user_hours_page, name='userhours'),
    path('add_user_hours/', views.add_user_hours, name='add_user_hours'),
    path('add_user_profile/', views.add_user_profile, name='add_user_profile'),
    path('edit_user_hours/<int:pk>/', views.edit_user_hours, name='edit_user_hours'),
    path('download_user_hours_excel/', views.download_user_hours_excel, name='download_user_hours_excel'),
    path('manage_names/', views.manage_names, name='manage_names'),
    path('delete_name/<int:user_id>/', views.delete_name, name='delete_name'),

    path('create/', views.create_invoice, name='create_invoice'),
    path('get-items/<int:category_id>/', views.get_items_by_category, name='get_items_by_category'),

    path('sold-items/download/', views.download_sold_items_excel, name='download_sold_items_excel'),
    path('delete-invoice/<int:invoice_id>/', views.delete_invoice, name='delete_invoice'),

    
    
    
    
    path('add_category/', views.add_category, name='add_category'),
    path('delete_category/<int:category_id>/', views.delete_category, name='delete_category'),




    path('edit_user/<int:user_id>/', views.edit_user, name='edit_user'),
    path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('user_hours/delete/<int:pk>/', views.delete_user_hours, name='delete_user_hours'),


    path('deleted-items/', views.deleted_items, name='deleted_items'),
    path('restore-item/<int:item_id>/', views.restore_item, name='restore_item'),
    


    path('visits/', views.visits_list, name='visits_list'),
    path('visits/add/', views.add_visit, name='add_visit'),
    path('visits/<int:visit_id>/', views.view_visit, name='view_visit'),
    path('owner/details/<int:owner_id>/', views.get_owner_details, name='get_owner_details'),  # New URL to fetch owner details
    path('owner/search/', views.search_owners, name='search_owners'),
    path('visits/<int:visit_id>/edit/', views.edit_visit, name='edit_visit'),


    path('next_check/', views.next_check, name='next_check'),
    
    path('bought/', views.bought, name='bought'),
    path('boughttoday/', views.bought_today, name='bought_today'),
    path('bought/add/', views.add_bought_item, name='add_bought_item'),
    path('bought/download/', views.download_bought_excel, name='download_bought_excel'),
    path('bought/edit/<int:item_id>/', views.edit_bought_item, name='edit_bought_item'),
    path('bought/delete/<int:item_id>/', views.delete_bought_item, name='delete_bought_item'),

    path('dashboard/', views.dashboard, name='dashboard'),

]
