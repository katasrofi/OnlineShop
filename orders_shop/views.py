from django.shortcuts import render, get_object_or_404, redirect
from payments import get_payment_model, RedirectNeeded
from .models import OrderItem

# Define  the payment 
Payment = get_payment_model()

# Create your views here.
def checkout_order(request, pk):
    order = get_object_or_404(OrderItem, id=pk, user=request.user)

    # Check the existing payment
    payment_qs = Payment.objects.filter(order_product=order).first()
    if payment_qs:
        payment = payment_qs
    else:
        payment = Payment.objects.create(
            variant="default",
            description=f"Total payment for order #{order.pk}",
            total=order.total_price,
            currency="USD",
            delivery=0,
            tax=0,
            order=order,
            billing_email=request.user.email,
        )

    try:
        return redirect(payment.get_process_url())
    except RedirectNeeded as redirect_to:
        return redirect(str(redirect_to))

