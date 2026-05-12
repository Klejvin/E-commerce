from django.shortcuts import render ,redirect, get_object_or_404
from .models import *
from django.db.models import Q
from django.http import JsonResponse
import time
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import views as auth_views
from django.contrib import messages
from django.contrib.auth.models import User
import re
from django.core.mail import send_mail
from .models import Order, Item

# Create your views here.

def home(request):
    # .all() merr te gjitha informacionet nga class
    # .all() => tek html cikli for in
    allItems = Item.objects.all()
    allCat = Category.objects.all()
    context = {"allItems":allItems, "allCat":allCat}
    return render(request, "home.html", context)

def about(request):
    allCat = Category.objects.all()
    context = {"allCat":allCat}
    return render(request, "about.html", context) 

def contact(request):
    allCat = Category.objects.all()
    context = {"allCat":allCat}
    return render(request, "contact.html",context)

def allitems(request):
    allItems = Item.objects.all()
    allCat = Category.objects.all()
    context = {"allItems": allItems,"allCat":allCat}
    return render(request, "allitems.html",context)

def detailItem(request, id):
    # .get() merr nje informacion
    infoItem = Item.objects.get(pk=id)
    allCat = Category.objects.all()
    context={"infoItem":infoItem,"allCat":allCat}
    return render(request, "detailItem.html", context)

def category(request, slug):
    # .get() merr nje informacion
    infoCategory = Category.objects.get(category_slug=slug)
    allCat = Category.objects.all()
    # .filter() merr informacionet nga class qe plotesojne kushtin
    # .filter() => tek html cikli for in
    itemsCat = Item.objects.filter(item_category= infoCategory)
    context={"infoCategory":infoCategory,"allCat":allCat, "itemsCat":itemsCat}
    return render(request, "category.html", context)


def search_results(request):
    query = request.GET.get('q') # Marrim fjalën nga input-i 'q'
    results = Item.objects.none()
    
    if query:
        # Filtrojmë: kërko në Titull OSE në Përshkrim (icontains = s'ka rëndësi gërma e madhe/vogël)
        results = Item.objects.filter(
           Q(item_name__icontains=query) | Q(item_description__icontains=query)
        )
    
    return render(request, 'search_results.html', {'query': query, 'results': results})    

import time # Sigurohu që ke bërë import time në fillim të skedarit

import time
from django.shortcuts import get_object_or_404, redirect

def add_to_cart(request, id):
    if request.method == 'POST':
        variant_id = request.POST.get('variant_id')
        selected_color = request.POST.get('color', 'Pa Ngjyrë')
        
        if variant_id:
            variant = get_object_or_404(ProductVariant, id=variant_id)
            item = variant.item
            base_price = float(variant.price)
            
            # KONTROLLI KYÇ: Nëse varianti s'ka ulje, shiko te Item (Produkti)
            discount = variant.discount_percentage if variant.discount_percentage > 0 else item.discount_percentage
            
            if discount > 0:
                final_price = base_price - (base_price * (discount / 100))
            else:
                final_price = base_price
            
            final_size = variant.size_ml
        else:
            item = get_object_or_404(Item, id=id)
            final_price = item.get_discounted_price # Përdor @property nga modeli Item
            final_size = request.POST.get('size', 'Pa Masë')

        cart = request.session.get('cart', {})
        
        # Krijojmë çelës unik që të mos ketë konflikte në shportë
        unique_key = f"{id}_{variant_id if variant_id else 'no'}_{selected_color}_{time.time()}"

        cart[unique_key] = {
            'item_id': item.id,
            'variant_id': variant_id,
            'name': item.item_name,
            'price': round(float(final_price), 2), # KËTU RUHET ÇMIMI I ULUR
            'image': item.item_image.url,
            'size': final_size,
            'color': selected_color,
            'quantity': 1,
        }
        
        request.session['cart'] = cart
        request.session.modified = True
        return redirect('cart_page')
        
def cart_page(request):
    cart = request.session.get('cart', {})
    allCat = Category.objects.all()
    
    # LLOGARITJA E SAKTË: Çmimi * Sasinë për çdo produkt
    total = sum(float(item['price']) * int(item.get('quantity', 1)) for item in cart.values())
    
    # Llogarisim edhe numrin total të produkteve për ikonën e shportës (badge)
    cart_count = sum(int(item.get('quantity', 1)) for item in cart.values())
    
    context = {
        'cart': cart, 
        'total': total,
        'cart_count': cart_count, # Këtë përdore te ikona e shportës në Navbar
        'allCat': allCat
    }
    return render(request, 'cart.html', context)

def remove_from_cart(request, cart_id):
    cart = request.session.get('cart', {})
    
    if cart_id in cart:
        del cart[cart_id]
        request.session['cart'] = cart
        request.session.modified = True
        
    return redirect('cart_page')

def update_cart(request, productId, quantity):
    cart = request.session.get('cart', {})

    if productId in cart:
        if quantity > 0:
            cart[productId]['quantity'] = quantity
        else:
            del cart[productId] # E heqim nëse shkon në 0
            
        request.session['cart'] = cart
        request.session.modified = True

    return redirect('cart_page')






# 1. VIEW PER LOGIN
def loginPage(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('/admin/')
        return redirect('homePage')
    
    if request.method == 'POST':
        u = request.POST.get('username')
        p = request.POST.get('password')
        
        user = authenticate(request, username=u, password=p)
        
        if user is not None:
            login(request, user)
            messages.success(request, f"Mirëseerdhe, {user.username}!")
            
            if user.is_superuser:
                return redirect('/admin/') 
            else:
                return redirect('homePage') 
        else:
            messages.error(request, "Username ose Password i pasaktë.")
            
    return render(request, 'login.html')

# 2. VIEW PER REGJISTRIM (Me validime)
def registerPage(request):
    if request.user.is_authenticated:
        return redirect('homePage')

    if request.method == 'POST':
        fname = request.POST.get('firstName')
        lname = request.POST.get('lastName')
        uname = request.POST.get('username')
        email = request.POST.get('email')
        p1 = request.POST.get('password')
        p2 = request.POST.get('repassword')

        # Kriojmë një context për të mbajtur vlerat e shkruara nëse dështon regjistrimi
        context = {
            'fname': fname,
            'lname': lname,
            'uname': uname,
            'email': email,
        }

        # 1. Kontrolli i gjatësisë së fjalëkalimit
        if len(p1) < 8:
            messages.error(request, "Fjalëkalimi duhet të jetë të paktën 8 karaktere.")
            return render(request, 'register.html', context)
        
        # 2. Kontrolli për shkronjë të madhe
        elif not re.search(r'[A-Z]', p1):
            messages.error(request, "Fjalëkalimi duhet të përmbajë të paktën një shkronjë të madhe.")
            return render(request, 'register.html', context)
        
        # 3. Kontrolli për numër
        elif not re.search(r'[0-9]', p1):
            messages.error(request, "Fjalëkalimi duhet të përmbajë të paktën një numër.")
            return render(request, 'register.html', context)
        
        # 4. Kontrolli nëse fjalëkalimet përputhen
        elif p1 != p2:
            messages.error(request, "Fjalëkalimet nuk përputhen!")
            return render(request, 'register.html', context)
        
        # 5. Kontrolli nëse ekziston username
        elif User.objects.filter(username=uname).exists():
            messages.error(request, "Ky username është i zënë.")
            return render(request, 'register.html', context)

        # 6. KONTROLLI SPECIFIK PER EMAIL (Ndryshimi që kërkove)
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Ky email është përdorur njëherë.")
            return render(request, 'register.html', context)
            
        else:
            # Nëse të gjitha janë OK, krijohet përdoruesi
            user = User.objects.create_user(uname, email, p1)
            user.first_name = fname
            user.last_name = lname
            user.save()
            messages.success(request, "Llogaria u krijua! Po ju ridrejtojmë...")
            return render(request, 'register.html', {'registration_success': True})

    return render(request, 'register.html')

# 3. VIEW PER LOGOUT
def logoutUser(request):
    # Kjo pjesë bën që të gjitha mesazhet e vjetra (si Mirëseerdhe) të fshihen
    storage = messages.get_messages(request)
    for message in storage:
        pass # Duke i kaluar në loop, Django i konsideron si "të shfaqura" dhe i fshin
    
    logout(request)
    messages.success(request, "U çloguat me sukses.") # Ndryshuar nga info në success për ngjyrë jeshile
    return redirect('loginPage')

def itemDetail(request, id):
    # Marrim produktin specifik bazuar në ID
    infoItem = get_object_or_404(Item, id=id)
    
    context = {
        'infoItem': infoItem,
    }
    return render(request, 'item_detail.html', context)



def add_to_cart(request, id):
    if request.method == 'POST':
        # 1. Marrim të dhënat nga POST
        variant_id = request.POST.get('variant_id')
        selected_color = request.POST.get('color', 'Pa Ngjyrë')
        
        # 2. Përcaktojmë produktin dhe çmimin
        if variant_id:
            variant = get_object_or_404(ProductVariant, id=variant_id)
            item = variant.item
            price = float(variant.get_discounted_price) 
            old_price = float(variant.price)
            size = variant.size_ml
        else:
            item = get_object_or_404(Item, id=id)
            price = float(item.get_discounted_price)
            old_price = float(item.item_price)
            size = request.POST.get('size', 'Pa Masë')

        # 3. RREGULLIMI PËR ÇANTAT (Error Fix)
        # Përdorim .item_category siç e ke në models.py
        if item.item_category and item.item_category.category_name:
            if "canta" in item.item_category.category_name.lower():
                size = ""           # Lihet bosh për çantat
                selected_color = "" # Lihet bosh për çantat
        
        # 4. Menaxhimi i Shportës
        cart = request.session.get('cart', {})
        
        # Krijojmë një çelës unik për sesionin
        unique_key = f"{id}_{variant_id}_{time.time()}"

        cart[unique_key] = {
            'item_id': item.id,
            'name': item.item_name,
            'price': price,
            'old_price': old_price,
            'image': item.item_image.url,
            'size': size,
            'color': selected_color,
            'quantity': 1,
        }

        request.session['cart'] = cart
        request.session.modified = True
        
        return redirect(request.META.get('HTTP_REFERER', 'homePage'))



def toggle_wishlist(request, item_id):
    """Shton ose heq një produkt nga Wishlist duke përdorur sessions."""
    
    # Krijojmë listën në session nëse nuk ekziston
    if 'wishlist' not in request.session:
        request.session['wishlist'] = []
    
    wishlist = request.session['wishlist']
    item_id_str = str(item_id) # Sessions i ruajnë çelësat si string

    if item_id_str in wishlist:
        wishlist.remove(item_id_str)
        status = 'removed'
    else:
        wishlist.append(item_id_str)
        status = 'added'
    
    # Markojmë session si të modifikuar që të ruhet në DB
    request.session.modified = True
    
    return JsonResponse({
        'status': status,
        'total_items': len(wishlist)
    })



def wishlist_page(request):
    wishlist_ids = request.session.get('wishlist', [])
    # Marrim produktet që janë në listën e ID-ve të wishlist
    items = Item.objects.filter(id__in=wishlist_ids)
    
    return render(request, 'wishlist.html', {
        'items': items
    })



def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('homePage')

    total = sum(float(item['price']) * item['quantity'] for item in cart.values())

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        full_name = f"{first_name} {last_name}"
        
        address = request.POST.get('address')
        phone = request.POST.get('phone')

        # 1. Krijo porosinë në DB
        order = Order.objects.create(
            user=request.user if request.user.is_authenticated else None,
            full_name=full_name,
            address=address,
            phone_number=phone,
            total_price=total,
            items_json=str(cart)
        )

        # 2. Ndërto mesazhin për Terminalin (VS Code)
        product_details = ""
        for key, item in cart.items():
            product_details += f"- {item['name']} | Masa: {item.get('size', '-')} | Sasia: {item['quantity']} | Çmimi: ${item['price']}\n"

        subject = f"POROSI E RE #{order.id} - {full_name}"
        message = f"""
        KLIENTI: {full_name}
        ADRESA: {address}
        TEL: {phone}
        
        PRODUKTET:
        {product_details}
        
        TOTALI: ${total}
        """

        # 3. Dërgo email-in në Terminal
        send_mail(
            subject,
            message,
            'noreply@dyqani.com',
            ['admin@dyqani.com'],
            fail_silently=False,
        )

        # 4. Pastro shportën dhe dërgo te faqja e suksesit
        request.session['cart'] = {}
        request.session.modified = True
        return render(request, 'success.html')

    return render(request, 'checkout.html', {'total': total})