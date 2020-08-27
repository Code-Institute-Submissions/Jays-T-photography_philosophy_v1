from django.shortcuts import render, get_object_or_404
from django.contrib import messages

from .models import UserProfile
from .forms import UserProfileForm

from checkout.models import Order


def profile(request):

    profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Shipping Address updated successfully')

    form = UserProfileForm(instance=profile)
    orders = profile.user_order_history.all()

    template = 'user_profiles/profile.html'
    context = {
        'form': form,
        'orders': orders,
        'from_profile_page': True,
    }

    return render(request, template, context)


def order_history(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)

    messages.info(request, (
        f'This is not a new confirmation, this was for order number: {order_number}. '
        'A confirmation email was sent on the original order date.'
    ))

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
        'from_profile_order_history': True,
    }

    return render(request, template, context)
