import json
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import update_session_auth_hash
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render
from django.http import JsonResponse, HttpResponse
from .forms import RegisterForm, ItemForm, OrderForm, CustomPasswordChangeForm
from django.db import transaction
from django.urls import reverse
from .models import Orders, OrderItems, Items
from django.utils import timezone


def is_staff(user):
    return user.is_staff

def is_superuser(user):
    return user.is_superuser

def is_active(user):
    return user.is_active


@login_required
@user_passes_test(is_active)
def home(request):
    if request.user.is_superuser and request.user.is_staff:
        # User is a manager
        return render(request,'manager/manager_Dashboard.html')
    elif request.user.is_staff and not request.user.is_superuser:
        # User is a provider
        return render(request,'service_provider/provider_Dashboard.html')
    else:
        # User is a customer
        return render(request,'customer/customer_Dashboard.html')


def register(response):
    if response.method == "POST":
        form = RegisterForm(response.POST)
        if form.is_valid():
            # form.save()
            return redirect('home')
    else:
        form = RegisterForm()

    return render(response, "registration/register.html", {'form': form})

@login_required
@user_passes_test(is_active)
def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('password_change_done')
    else:
        form = CustomPasswordChangeForm(user=request.user)
    return render(request, 'registration/change_password.html', {'form': form})


@login_required
@user_passes_test(is_superuser)
def ItemsUpload(request):
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                image_file = form.cleaned_data['ItemImage']
                if not image_file.name.lower().endswith(('.png', '.jpg', '.jpeg','.heic', '.mp4','.mp3','.pdf')):
                    raise ValidationError("Only PNG, JPG, JPEG, or GIF files are allowed.")
            except KeyError:
                pass  # No file uploaded
            else:
                # form.instance.sender = request.user.username  # Set sender to logged-in user's username
                form.save()
                return redirect('home')
    else:
        form = ItemForm()
    return render(request, 'manager/upload_Items.html', {'form': form})


@login_required
@user_passes_test(is_active)
def create_order(request):
    if request.method == 'POST':
        items = []
        total_amount = 0
        for key, value in request.POST.items():
            if key.startswith('item_'):
                item_id = int(key.split('_')[1])
                quantity = int(value)
                if quantity > 0:
                    item = Items.objects.get(pk=item_id)
                    items.append({'item': item, 'quantity': quantity, 'price': item.ItemPrice})
                    total_amount += item.ItemPrice * quantity

        order_form = OrderForm({'PaymentMethod': 'Cash', 'TotalAmount': total_amount})
        if order_form.is_valid() and items:
            try:
                order = order_form.save(request.user, items)

                # Set the OrderTime field to the current time in the Africa/Dar_es_Salaam time zone
                order.OrderTime = timezone.now().astimezone(timezone.get_fixed_timezone(180))
                order.save()

                return redirect(reverse('order_history'))
            except:
                pass
    else:
        order_form = OrderForm()
        items = Items.objects.all()

    return render(request, 'customer/test_menu.html', {'order_form': order_form, 'items': items})

@login_required
@user_passes_test(is_active)
def order_history(request):
    orders = Orders.objects.filter(CustomerID=request.user)
    order_details = []
    for order in orders:
        order_items = OrderItems.objects.filter(OrderID=order)
        order_details.append({
            'order': order,
            'items': order_items,
            'item_ids': [item.ItemID for item in order_items],
            'item_Qnt': [item.Quantity for item in order_items],
            'Status': [item.Status for item in order_items],
        })
    return render(request, 'customer/order_history.html', {'order_details': order_details})


@login_required
@user_passes_test(is_staff)
def view_orders(request):
    orders = Orders.objects.all()
    order_items = OrderItems.objects.filter(OrderID__in=[order.OrderID for order in orders],
                                            Status='pending'
                                            )

    context = {
        'orders': orders,
        'order_items': order_items,
    }
    return render(request, 'service_provider/pending_list.html', context)


@login_required
@user_passes_test(is_staff)
def update_order_item_status(request, order_item_id):
    if request.method == 'POST':
        order_item = get_object_or_404(OrderItems, id=order_item_id)
        order_item.Status = 'Expired'
        order_item.save()
        return JsonResponse({'message': 'Order item status updated successfully'})
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)


@login_required
@user_passes_test(is_staff)
def update_item(request, item_id):
    item = get_object_or_404(Items, ItemID=item_id)
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            return redirect('item_list')  # Redirect to the list of items after updating
    else:
        form = ItemForm(instance=item)
    return render(request, 'manager/update_item.html', {'form': form, 'item': item})


@login_required
@user_passes_test(is_staff)
def delete_item(request, item_id):
    item = get_object_or_404(Items, ItemID=item_id)
    if request.method == 'POST':
        item.delete()
        return redirect('item_list')  # Redirect to the list of items after deletion
    return render(request, 'manager/delete_item.html', {'item': item})


@login_required
@user_passes_test(is_staff)
def item_list(request):
    items = Items.objects.all()
    return render(request, 'manager/view_menu.html', {'items': items})