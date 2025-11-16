from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout 
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from store.models import Book  ,Category,CartItem,Order,OrderItem
from django.contrib import messages
from .forms import BookForm , SignupForm
from django.db.models import Q




def home(request):
    return render(request, "store/home.html")



def book_list(request):
    books = Book.objects.all()
    categories = Category.objects.all()
    query = request.GET.get('search', '')  # get search text


    # Category filtering by NAME (not ID)
    category_name = request.GET.get("category")
    if category_name:
        books = books.filter(category__name__iexact=category_name)
        # ya agar lowercase slug type field hai toh:
        # books = books.filter(category__name__icontains=category_name)

    # Price filtering
    min_price = request.GET.get("min_price")
    max_price = request.GET.get("max_price")
    
    if min_price and max_price:
        try:
            min_price = int(min_price)
            max_price = int(max_price)
            books = books.filter(price__gte=min_price, price__lte=max_price)
        except ValueError:
            pass

    # Sort filtering
    sort_by = request.GET.get("sort")
    if sort_by == "bestseller":
        books = books.order_by('-id')  # ya tumhara bestseller logic
    elif sort_by == "new":
        books = books.order_by('-id')  # ya '-id' for latest
    
     # Cart count calculation
    if request.user.is_authenticated:
        cart_count = CartItem.objects.filter(user=request.user).count()
    else:
        cart_count = 0
        
    if query:
        books = books.filter(
            Q(title__icontains=query) |
            Q(author__icontains=query) |
            Q(isbn__icontains=query)
        )

    context = {
        'books': books,
        'query': query,
    }    
        
    return render(request, "store/book_list.html", {
        "books": books,
        "categories": categories,
        "cart_count": cart_count,
        
    },context)


def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return render(request, "store/book_detail.html", {"book": book})


@login_required
def add_book(request):
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("book_list")
    else:
        form = BookForm()
    return render(request, "store/add_book.html", {"form": form})


def register(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = SignupForm()
    return render(request, "store/register.html", {"form": form})


def user_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("home")
    else:
        form = AuthenticationForm()
    return render(request, "store/login.html", {"form": form})


def user_logout(request):
    logout(request)
    return redirect("home")





@login_required
def view_cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.total_price for item in cart_items)
    return render(request, "store/cart.html", {"cart_items": cart_items, "total_price": total_price})



@login_required
def add_to_cart(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, book=book)

    if not created:
        cart_item.quantity += 1
        cart_item.save()
        messages.info(request, f"Quantity updated for '{book.title}'")
    else:
        messages.success(request, f"'{book.title}' added to your cart")

    return redirect("view_cart")  



@login_required
def update_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
    if request.method == "POST":
        quantity = int(request.POST.get("quantity", 1))
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
            messages.success(request, "Cart updated successfully")
        else:
            cart_item.delete()
            messages.info(request, "Item removed from cart")
    return redirect("view_cart")



@login_required
def delete_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
    cart_item.delete()
    messages.warning(request, "Item removed from your cart")
    return redirect("view_cart")


@login_required
def checkout(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total = sum(item.book.price * item.quantity for item in cart_items)

    if request.method == "POST":
        full_name = request.POST.get('full_name')
        address = request.POST.get('address')
        city = request.POST.get('city')
        pincode = request.POST.get('pincode')
        phone = request.POST.get('phone')
        payment_method = request.POST.get('payment_method')

        # Create order
        order = Order.objects.create(
            user=request.user,
            full_name=full_name,
            address=address,
            city=city,
            pincode=pincode,
            phone=phone,
            payment_method=payment_method,
            total=total
        )

        # Add cart items to order items
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                book=item.book,
                quantity=item.quantity,
                price=item.book.price
            )

        cart_items.delete()

        messages.success(request, "Your order has been placed successfully!")
        return redirect('order_success')

    return render(request, 'store/checkout.html', {
        'cart_items': cart_items,
        'total': total
    })


@login_required
def order_success(request):
    return render(request, 'store/order_success.html')

@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'store/my_orders.html', {'orders': orders})

