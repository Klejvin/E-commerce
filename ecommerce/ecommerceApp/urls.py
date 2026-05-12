from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [
path("", views.home, name="homePage"),
path('about/', views.about, name="aboutPage"),
path('allitems/', views.allitems, name="allitemsPage"),
path('detail_info/<id>', views.detailItem, name="detailItemPage"),
path('detail_category/<slug>', views.category, name="categoryPage"),
path('search/', views.search_results, name='search_results'),
path('add-to-cart/<int:id>/', views.add_to_cart, name='add_to_cart'),
path('cart/', views.cart_page, name='cart_page'),
path('remove-from-cart/<str:cart_id>/', views.remove_from_cart, name='remove_from_cart'),
path('login/', views.loginPage, name='loginPage'),
path('register/', views.registerPage, name='registerPage'),
path('logout/', views.logoutUser, name='logout'),

    # Password Reset
path('password_reset/', auth_views.PasswordResetView.as_view(template_name="password_reset.html"), name='password_reset'),
path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name="password_reset_done.html"), name='password_reset_done'),
path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="password_reset_confirm.html"), name='password_reset_confirm'),
path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="password_reset_complete.html"), name='password_reset_complete'),
# Kjo është URL-ja që do të thërrasë HTMX sa herë që shkruan në search
path('search/', views.search_results, name='search_results'),
path('toggle-wishlist/<int:item_id>/', views.toggle_wishlist, name='toggle_wishlist'),
path('wishlist/', views.wishlist_page, name='wishlist_page'),
path('checkout/', views.checkout, name='checkout'),

    
    
]
