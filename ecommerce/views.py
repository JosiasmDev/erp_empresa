from django.shortcuts import render

def ecommerce_dashboard(request):
    return render(request, 'ecommerce/dashboard.html', {})