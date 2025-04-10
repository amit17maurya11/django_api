# from rest_framework.routers import DefaultRouter
# from .views import CategoryViewSet, TransactionViewSet, BudgetViewSet

# router = DefaultRouter()
# router.register(r'categories', CategoryViewSet)
# router.register(r'transactions', TransactionViewSet)
# router.register(r'budgets', BudgetViewSet)



# urlpatterns = router.urls
from rest_framework.routers import DefaultRouter
from django.urls import path  # Import path for function-based views
from .views import CategoryViewSet, TransactionViewSet, BudgetViewSet, monthly_summary,dashboard_summary  # Import monthly_summary

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'transactions', TransactionViewSet)
router.register(r'budgets', BudgetViewSet)

urlpatterns = router.urls

# Add the monthly_summary endpoint
urlpatterns += [
    path('monthly-summary/', monthly_summary, name='monthly-summary'),
        path('dashboard-summary/', dashboard_summary, name='dashboard-summary'),
]