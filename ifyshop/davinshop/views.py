from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Category, Product
from django.core.paginator import Paginator, EmptyPage, InvalidPage

# Create your views here.
def index(request):
    text_var ='This is my first django app webpage.'
    return HttpResponse(text_var)

#create category view

def allProdCat(request, c_slug=None):
    c_page = None
    products_list = None
    if c_slug != None:
        c_page = get_object_or_404(Category,slug=c_slug)
        products_list = Product.objects.filter(category=c_page,available=True)
    else:
        products_list = Product.objects.all().filter(available=True)
    # '''Pagination Code'''
    paginator = Paginator(products_list, 4)
    try:
        page = int(request.GET.get('page','1'))
    except:
        page = 1
    try:
        products = paginator.page(page)
    except (EmptyPage, InvalidPage):
        products = paginator.page(paginator.num_pages)
    return render(request,'davinshop/category.html',{'category':c_page,'products':products})

# def ProdCatDetails(request, c_slug, product_slug):
#     #print(c_slug,product_slug)
#     category = get_object_or_404(Category, slug=c_slug)
#     product = get_object_or_404(Product, slug=product_slug, category_id=category.id)
#     try:
#         product = Product.objects.filter(category=c_slug, slug=product_slug)
#     except Exception as e:
#         raise e
#     return render(request,'davinshop/product.html', {'product':product})

def ProdCatDetails(request, c_slug, product_slug):
    # category = Category.objects.get(slug=c_slug)
    category = get_object_or_404(Category, slug=c_slug)
    # products = Product.objects.get(slug=product_slug, category=category)
    product = get_object_or_404(Product, slug =product_slug, category=category)
#     # This also works with filter
#     # products = Product.objects.filter(slug=product_slug, category=category_id)
#     # But filter returns a list and you have to use products[0]
    return render(request,'davinshop/product.html', {'product': product})
# #     try:
# #         product = Product.objects.filter(category=c_slug, slug=product_slug)
# #     except Exception as e:
# #         raise e
# #     return render(request,'davinshop/product.html', {'product':product})


