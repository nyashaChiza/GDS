from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from accounts.models import Site
from django.contrib.auth.decorators import login_required
from billing.models import BillingProfile, SubscriptionPlan

def payment_success(request):
    payment_id = request.GET.get('payment_id', 'Unknown')
    amount = request.GET.get('amount', 'Unknown')
    transaction_reference = request.GET.get('transaction_reference', 'Unknown')

    context = {
        'payment_id': payment_id,
        'amount': amount,
        'transaction_reference': transaction_reference,
    }

    messages.success(request, f"Payment Successful! ID: {payment_id}, Amount: {amount}")
    return render(request, 'billing/payment_success.html', context)


def payment_failed(request):
    error_message = request.GET.get('error_message', 'Unknown error')
    error_code = request.GET.get('error_code', 'Unknown code')

    context = {
        'error_message': error_message,
        'error_code': error_code,
    }

    messages.error(request, f"Payment Failed! Error: {error_message}")
    return render(request, 'billing/payment_failed.html', context)

@login_required
def select_subscription_plan(request, billing_profile_pk):
    if request.user.role == "Admin":
        billing_profile = get_object_or_404(BillingProfile, pk=billing_profile_pk, company=request.user.company)

        if request.method == 'POST':
            plan_id = request.POST.get('subscription_plan')
            if plan_id:
                subscription_plan = get_object_or_404(SubscriptionPlan, id=plan_id)
                billing_profile.subscription_plan = subscription_plan
                billing_profile.save()

                messages.success(request, f"Subscription plan '{subscription_plan.name}' selected for {billing_profile.company.name}.")
                return redirect('site_list')
            else:
                messages.error(request, "Please select a subscription plan.")

        plans = SubscriptionPlan.objects.all()
        return render(request, 'billing/pricing.html', {'billing_profile': billing_profile, 'plans': plans})
    else:
        messages.warning(request, "You do not have the right role to perform this action")
        return redirect('site_list')

@login_required
def payment_page(request, site_uuid):
    # Get the site for which the payment is being made
    site = get_object_or_404(Site, uuid=site_uuid)
    bill_profile = site.company.bill_profiles.first()
    
    # Here you would implement the payment logic
    # For now, just render a template or return a message
    return render(request, 'billing/payment_page.html', {'site': site})
