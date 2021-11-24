import json

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.http import JsonResponse
from django.templatetags.static import static


from .models import Product, Order, OrderItem


def banners_list_api(request):
    # FIXME move data to db?
    return JsonResponse([
        {
            'title': 'Burger',
            'src': static('burger.jpg'),
            'text': 'Tasty Burger at your door step',
        },
        {
            'title': 'Spices',
            'src': static('food.jpg'),
            'text': 'All Cuisines',
        },
        {
            'title': 'New York',
            'src': static('tasty.jpg'),
            'text': 'Food is incomplete without a tasty dessert',
        }
    ], safe=False, json_dumps_params={
        'ensure_ascii': False,
        'indent': 4,
    })


def product_list_api(request):
    products = Product.objects.select_related('category').available()

    dumped_products = []
    for product in products:
        dumped_product = {
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'special_status': product.special_status,
            'description': product.description,
            'category': {
                'id': product.category.id,
                'name': product.category.name,
            },
            'image': product.image.url,
            'restaurant': {
                'id': product.id,
                'name': product.name,
            }
        }
        dumped_products.append(dumped_product)
    return JsonResponse(dumped_products, safe=False, json_dumps_params={
        'ensure_ascii': False,
        'indent': 4,
    })


@api_view(['POST'])
def register_order(request):
    content, response_status = None, None
    data = request.data
    if 'products' not in data:
        content = {'products': 'Обязательное поле'}
    elif data['products'] == None:
        content = {'products': 'Это поле не может быть пустым.'}
    elif not isinstance(data['products'], list):
        content = {'products': 'Ожидался list со значениями, но был получен "{}".'.format(type(data['products']).__name__)}
    elif not data['products']:
        content = {'products': 'Этот список не может быть пустым.'}

    if content:
        response_status = status.HTTP_406_NOT_ACCEPTABLE

    order = Order.objects.create(firstname=data['firstname'],
                                 lastname=data['lastname'],
                                 phonenumber=data['phonenumber'],
                                 address=data['address'])
    products = data['products']
    for product in products:
        OrderItem.objects.create(order=order,
                                 product=Product.objects.get(id=product['product']),
                                 quantity=product['quantity']
                                 )
    return Response(content, status=response_status or status.HTTP_200_OK)
