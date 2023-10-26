from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import MenuItem, Order, OrderItem
from .forms import ProfileForm
import json
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from paystackapi.transaction import Transaction
from django.db.models import Sum, F
from decimal import Decimal
import logging  
import uuid  # Import the uuid module


@login_required
def profile(request):
    return render(request, 'profile.html')

def home(request):
    items = MenuItem.objects.all()[:4]
    context = {
        'items': items
    }
    return render(request, 'index.html', context)

def contact(request):
    return render(request, 'contact.html')


@login_required
def menu(request):
    items = MenuItem.objects.all()
    context = {
        'items': items
    }
    return render(request, 'menu.html', context)

@login_required
def cart(request):
    order = Order.objects.get(user=request.user, ordered=False)
    order_items = order.orderitem_set.all()

    if order_items.exists():  # Check if there are items in the cart
        total_quantity = order_items.aggregate(Sum('quantity'))['quantity__sum']
        total_amount = order_items.aggregate(
            total_price=Sum(F('item__price') * F('quantity'))
        )['total_price']

        if total_amount is None:
            total_amount = 0.00

        context = {
            'order_items': order_items,
            'total_quantity': total_quantity,
            'total_amount': total_amount,
        }
        return render(request, 'cart.html', context)
    else:
        # No items in the cart, render a different template
        return render(request, 'empty_cart.html')
    

@login_required
def add_to_cart(request, item_id):
    item = get_object_or_404(MenuItem, id=item_id)

    order, created = Order.objects.get_or_create(user=request.user, ordered=False)

    order_item, item_created = OrderItem.objects.get_or_create(
        order=order,
        item=item,
        user=request.user,
        defaults={'quantity': 1, 'ordered': False}
    )

    if not item_created:
        order_item.quantity += 1
        order_item.save()

    # Update total_quantity and total_amount of the order
    order.total_quantity = sum(item.quantity for item in order.orderitem_set.filter(ordered=False))
    order.total_amount = sum(item.item.price * item.quantity for item in order.orderitem_set.filter(ordered=False))
    order.save()

    return redirect('menu')

@login_required
def decrement_quantity(request, item_id):
    item = get_object_or_404(MenuItem, id=item_id)
    order_item = OrderItem.objects.get(item=item, user=request.user, ordered=False)
    
    if order_item.quantity > 1:
        order_item.quantity -= 1
        order_item.save()

        # Update the total quantity and total amount in the order
        order = Order.objects.get(user=request.user, ordered=False)
        order.total_quantity -= 1
        order.total_amount -= order_item.item.price
        order.save()

        return JsonResponse({'success': True})
    else:
        order_item.delete()

        # Update the total quantity and total amount in the order
        order = Order.objects.get(user=request.user, ordered=False)
        order.total_quantity -= 1
        order.total_amount -= order_item.item.price
        order.save()

        return JsonResponse({'success': True})

@login_required
def increment_quantity(request, item_id):
    item = get_object_or_404(MenuItem, id=item_id)
    order_item = OrderItem.objects.get(item=item, user=request.user, ordered=False)
    
    order_item.quantity += 1
    order_item.save()

    # Update the total quantity and total amount in the order
    order = Order.objects.get(user=request.user, ordered=False)
    order.total_quantity += 1
    order.total_amount += order_item.item.price
    order.save()

    return JsonResponse({'success': True})

@login_required
def remove_from_cart(request, item_id):
    order_item = get_object_or_404(OrderItem, id=item_id, user=request.user, ordered=False)
    order_item.delete()
    return JsonResponse({'success': True})




@login_required
def checkout(request):
    order = Order.objects.filter(user=request.user, is_completed=False).first()
    context = {
        'order': order,
        'paystack_public_key': settings.PAYSTACK_PUBLIC_KEY,
    }
    return render(request, 'checkout.html', context)

@login_required
@csrf_exempt
def place_order(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            full_name = data.get('full_name', '')
            address = data.get('address', '')
            phone = data.get('phone', '')

            order = Order.objects.get(user=request.user, is_completed=False)

            # Update the order with shipping details
            order.full_name = full_name
            order.address = address
            order.phone = phone
            order.is_completed = True  # Mark the order as completed
            order.save()

            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    return JsonResponse({'success': False, 'message': 'Invalid request method.'})


@login_required
@csrf_exempt
def create_paystack_transaction(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print("Received data:", data)  # Print the received data for debugging
            full_name = data.get('full_name', '')
            address = data.get('address', '')
            phone = data.get('phone', '')
            total_amount = data.get('total_amount', '')
            items = data.get('items', [])

            print("Full Name:", full_name)
            print("Address:", address)
            print("Phone:", phone)
            print("Total Amount:", total_amount)
            print("Items:", items)

            # Create a Paystack transaction and get the authorization URL
            unique_reference = f'ORDER-{request.user.id}-{uuid.uuid4().hex}'  # Add a unique identifier
            response = Transaction.initialize(reference=unique_reference,
                                            email=request.user.email,
                                            amount=int(float(total_amount) * 100))

            print("Paystack API response:", response)  # Print the Paystack API response for debugging

            if response.get('status'):
                authorization_url = response.get('data', {}).get('authorization_url', '')

                # Save the order details to the database
                order = Order.objects.get(user=request.user, ordered=False)

                for item_data in items:
                    item_id = item_data.get('item_id', None)
                    quantity = item_data.get('quantity', 0)

                    if item_id and quantity > 0:  # Ensure valid item ID and quantity
                        item = MenuItem.objects.get(pk=item_id)
                        OrderItem.objects.create(order=order, item=item, quantity=quantity)

                # Update order details
                order.full_name = full_name
                order.address = address
                order.phone = phone
                order.total_amount = total_amount
                order.payment_reference = response.get('data', {}).get('reference', '')
                order.save()

                return JsonResponse({'success': True, 'authorization_url': authorization_url})
            else:
                return JsonResponse({'success': False, 'message': 'Failed to create Paystack transaction.'})
        except Exception as e:
            logging.error(f"Exception occurred: {str(e)}")
            return JsonResponse({'success': False, 'message': 'An error occurred.'})
    return JsonResponse({'success': False, 'message': 'Invalid request method.'})



@login_required
def payment_success(request):
    reference = request.GET.get('reference')
    if reference:
        # Retrieve the order based on the payment reference
        order = Order.objects.get(payment_reference=reference)

        # Mark the order as 'ordered' to indicate successful payment
        order.ordered = True
        order.save()

        return render(request, 'payment_success.html')
    return redirect('core:checkout')

@login_required
def payment_error(request):
    return render(request, 'payment_error.html')

@login_required
def payment_canceled(request):
    return render(request, 'payment_canceled.html')

