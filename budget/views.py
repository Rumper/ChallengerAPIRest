from django.shortcuts import render
# Create your views here.


def home(request):
    return render(
        request,
        '../templates/index.html',
        context={'urls': [
                    {
                        'url': "/api/1.0/budgets/",
                        'method': ["GET", "POST"],
                    },
                    {
                        'url': "/api/1.0/budget/",
                        'method': ["POST", "PUT", "DELETE"],
                    },
                    {
                        'url': "/api/1.0/suggest_budget/",
                        'method': ["POST"],
                    }
                ]})
