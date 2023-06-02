from django.shortcuts import render

def main_page(request):
    return render(request, 'main_app/index.html')


def page_not_found(request, exception):
    return render(request, 'page404.html', status=404)
