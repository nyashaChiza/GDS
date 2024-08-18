from django.utils import timezone
from datetime import datetime
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.decorators import login_required
from accounts.models import Site
from billing.models import BillingProfile, SubscriptionPlan, Invoice, Payment
from integration.models import Integration
from paynow import Paynow

# Constants
PAYMENT_ID_PARAM = 'payment_id'
AMOUNT_PARAM = 'amount'
TRANSACTION_REFERENCE_PARAM = 'transaction_reference'
ERROR_MESSAGE_PARAM = 'error_message'
ERROR_CODE_PARAM = 'error_code'
UNKNOWN_VALUE = 'Unknown'

@login_required
def payment_success(request):
    payment_id = request.GET.get(PAYMENT_ID_PARAM, UNKNOWN_VALUE)
    amount = request.GET.get(AMOUNT_PARAM, UNKNOWN_VALUE)
    transaction_reference = request.GET.get(TRANSACTION_REFERENCE_PARAM, UNKNOWN_VALUE)

    context = {
        'payment_id': payment_id,
        'amount': amount,
        'transaction_reference': transaction_reference,
    }

    messages.success(request, f"Payment Successful! ID: {payment_id}, Amount: {amount}")
    return render(request, 'billing/payment_success.html', context)

@login_required
def payment_failed(request):
    error_message = request.GET.get(ERROR_MESSAGE_PARAM, UNKNOWN_VALUE)
    error_code = request.GET.get(ERROR_CODE_PARAM, UNKNOWN_VALUE)

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
        messages.warning(request, "You do not have the right role to perform this action.")
        return redirect('site_list')


@login_required
def payment_page(request, site_uuid):
    site = get_object_or_404(Site, uuid=site_uuid)
    billing_profile = site.company.bill_profiles.first()

    if not billing_profile or not billing_profile.subscription_plan:
        messages.error(request, "Billing profile or subscription plan is missing.")
        return redirect('select_subscription_plan', billing_profile_pk=billing_profile.pk)

    paynow_integration = Integration.objects.first()

    # Ensure sensitive data is securely decrypted and handled
    paynow = Paynow(
        paynow_integration.decrypt_data(paynow_integration.integration_id),
        paynow_integration.decrypt_data(paynow_integration.integration_key),
        paynow_integration.decrypt_data(paynow_integration.result_url),
        paynow_integration.decrypt_data(paynow_integration.return_url)
    )

    # Create the Invoice
    invoice = Invoice.objects.create(
        billing_profile=billing_profile,
        amount_due=billing_profile.subscription_plan.price_per_site,
        due_date=timezone.now() + timezone.timedelta(days=30),
        currency='USD',  # Assuming USD; adjust according to your needs
        status='Pending'
    )

    # Create the Payment entry
    payment = Payment.objects.create(
        invoice=invoice,
        payment_method='Mobile Money',  # or another method as appropriate
    )

    # Add payment details to Paynow
    paynow_payment = paynow.create_payment(f"Payment for {site.name} site", request.user.email)
    paynow_payment.add(f"Subscription for {site.name} site", billing_profile.subscription_plan.price_per_site)

    # Send payment request
    response = paynow.send(paynow_payment)
    settings.LOGGER.info(f"Paynow response: {response}")

    if response.success:
        # Store the poll URL for future reference
        payment.poll_url = response.poll_url
        payment.invoice.status = 'Paid'
        payment.invoice.payment_date = datetime.today()
        payment.invoice.paid = True
        payment.invoice.save()
        site.status = 'Active'
        site.save()
        payment.save()

        # Redirect to Paynow for payment completion
        return redirect(response.redirect_url)
    else:
        # Handle failed payment initialization
        payment.invoice.status = 'Pending' 
        payment.invoice.save()

        payment.status = 'Failed' 
        payment.save()
        messages.error(request, "There was an error initiating the payment.")
        return redirect('payment_failed')


@login_required
def payment_status_update(request):
    payment_id = request.GET.get('payment_id')
    payment = get_object_or_404(Payment, uuid=payment_id)

    # Retrieve the Paynow integration
    paynow_integration = Integration.objects.first()
    paynow = Paynow(
        paynow_integration.decrypt_data(paynow_integration.integration_id),
        paynow_integration.decrypt_data(paynow_integration.integration_key)
    )

    # Query Paynow for the payment status
    response = paynow.check_payment_status(payment.poll_url)

    if response.paid:
        # Update payment and invoice as paid
        payment.invoice.status = 'Paid'
        payment.invoice.payment_date = timezone.now()
        payment.invoice.paid = True
        payment.invoice.save()

        payment.status = 'confirmed'
        payment.save()

        messages.success(request, "Payment was successful and invoice has been updated.")
        return redirect('payment_success')
    else:
        # Payment failed or is still pending
        payment.invoice.status = 'Pending' if response.pending else 'Overdue'
        payment.invoice.save()

        payment.status = 'failed' if not response.pending else 'pending'
        payment.save()

        messages.error(request, "Payment failed or is still pending. Please try again.")
        return redirect('payment_failed')