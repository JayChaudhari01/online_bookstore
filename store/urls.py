from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path("", views.home, name="home"),
    path("books/", views.book_list, name="book_list"),
    path("books/<int:pk>/", views.book_detail, name="book_detail"),
    path("books/add/", views.add_book, name="add_book"),
    path("register/", views.register, name="register"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/add/<int:book_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/<int:item_id>/', views.update_cart, name='update_cart'),
    path('cart/delete/<int:item_id>/', views.delete_from_cart, name='delete_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('order-success/', views.order_success, name='order_success'),
    path('my-orders/', views.my_orders, name='my_orders'),
    path('profile/', views.user_profile, name='user_profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),




     path('password-reset/', 
         auth_views.PasswordResetView.as_view(template_name="store/password_reset.html"), 
         name="password_reset"),

    path('password-reset/done/', 
         auth_views.PasswordResetDoneView.as_view(template_name="store/password_reset_done.html"), 
         name="password_reset_done"),

    path('reset/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(template_name="store/password_reset_confirm.html"), 
         name="password_reset_confirm"),

    path('reset/done/', 
         auth_views.PasswordResetCompleteView.as_view(template_name="store/password_reset_complete.html"), 
         name="password_reset_complete"),
]
