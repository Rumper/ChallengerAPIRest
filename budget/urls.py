from django.urls import path, re_path
from budget.api import BudgetsAPI, BudgetAPI, BudgetSuggest
from budget.views import home

budget_urlpatterns = [
    path('', home),
    path('api/1.0/budgets/', BudgetsAPI.as_view()),
    re_path('^api/1.0/budgets/(?P<email>[\w.@+-]+)/$', BudgetsAPI.as_view()),

    path('api/1.0/budget/', BudgetAPI.as_view()),
    path('api/1.0/budget/<slug:uuid>/', BudgetAPI.as_view()),

    path('api/1.0/suggest_categories/<slug:uuid>/', BudgetSuggest.as_view())
]
