from django.shortcuts import render

# Create your views here.


def MainPageView(request):
    return render(request, template_name='tea/main-page.html')
