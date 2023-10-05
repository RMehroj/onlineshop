from django.shortcuts import render, redirect, HttpResponseRedirect 
from . import models
from django.views import View 
  
 
class Index(View): 
    def post(self, request): 
        product = request.POST.get('product') 
        remove = request.POST.get('remove') 
        cart = request.session.get('cart') 
        if cart: 
            quantity = cart.get(product) 
            if quantity: 
                if remove: 
                    if quantity <= 1: 
                        cart.pop(product) 
                    else: 
                        cart[product] = quantity-1
                else: 
                    cart[product] = quantity+1
  
            else: 
                cart[product] = 1
        else: 
            cart = {} 
            cart[product] = 1
  
        request.session['cart'] = cart 
        print('cart', request.session['cart']) 
        return redirect('homepage') 
  
    def get(self, request): 
        # print() 
        return HttpResponseRedirect(f'/store{request.get_full_path()[1:]}') 
  
  
def store(request): 
    cart = request.session.get('cart') 
    if not cart: 
        request.session['cart'] = {} 
    product = None
    categories = models.Category.get_all_categories() 
    categoriesPK = request.GET.get('categories') 
    if categoriesPK: 
        product = models.Product.get_all_product_by_categories(categoriesPK) 
    else: 
        product = models.Product.get_all_product() 
  
    data = {} 
    data['products'] = product
    data['categories'] = categories 
  
    print('you are : ', request.session.get('email')) 
    return render(request, 'index.html', data) 
