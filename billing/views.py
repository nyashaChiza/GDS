from django.shortcuts import render
from django.contrib import messages

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