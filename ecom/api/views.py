from django.http import JsonResponse

# Create your views here.

def home(request):
    return JsonResponse({'Hi':'Hello World !','Name':'Rahmat'})
