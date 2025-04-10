from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, permissions
from .models import Category, Transaction, Budget
from .serializers import CategorySerializer, TransactionSerializer, BudgetSerializer,TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.db.models import Sum
from django.db.models.functions import TruncMonth

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def monthly_summary(request):
    user = request.user

    # Aggregate income and expenses by month
    transactions = Transaction.objects.filter(user=user).annotate(month=TruncMonth('date')).values('month', 'type').annotate(total=Sum('amount')).order_by('month')

    # Aggregate budget by month
    budgets = Budget.objects.filter(user=user).values('month').annotate(total_budget=Sum('amount')).order_by('month')

    # Prepare the response
    summary = {}
    for transaction in transactions:
        month = transaction['month'].strftime('%Y-%m')
        if month not in summary:
            summary[month] = {'income': 0, 'expense': 0, 'budget': 0, 'savings': 0}
        if transaction['type'] == 'income':
            summary[month]['income'] += transaction['total']
        elif transaction['type'] == 'expense':
            summary[month]['expense'] += transaction['total']

    for budget in budgets:
        month = budget['month']
        if month not in summary:
            summary[month] = {'income': 0, 'expense': 0, 'budget': 0, 'savings': 0}
        summary[month]['budget'] += budget['total_budget']

    # Calculate savings
    for month, data in summary.items():
        data['savings'] = data['income'] - data['expense']

    return Response(summary)




@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def dashboard_summary(request):
    user = request.user
    total_income = Transaction.objects.filter(user=user, type='income').aggregate(Sum('amount'))['amount__sum'] or 0
    total_expense = Transaction.objects.filter(user=user, type='expense').aggregate(Sum('amount'))['amount__sum'] or 0
    total_budget = Budget.objects.filter(user=user).aggregate(Sum('amount'))['amount__sum'] or 0

    remaining_budget = total_budget - total_expense

    return Response({
        'total_income': total_income,
        'total_expense': total_expense,
        'total_budget': total_budget,
        'remaining_budget': remaining_budget
    })
# class CategoryViewSet(viewsets.ModelViewSet):
#     queryset = Category.objects.all()  # 👈 Add this line
#     serializer_class = CategorySerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         return Category.objects.filter(user=self.request.user)

#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)
class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()  # 👈 Add this line
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class BudgetViewSet(viewsets.ModelViewSet):
    queryset = Budget.objects.all()  # 👈 Add this line
    serializer_class = BudgetSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Budget.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data['user_id'] = self.user.id
        return data

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


# class CategoryViewSet(viewsets.ModelViewSet):
#     serializer_class = CategorySerializer
#     permission_classes = [permissions.IsAuthenticated]
#     def get_queryset(self):
#         return Category.objects.filter(user=self.request.user)
#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)

# class TransactionViewSet(viewsets.ModelViewSet):
#     serializer_class = TransactionSerializer
#     permission_classes = [permissions.IsAuthenticated]
#     def get_queryset(self):
#         return Transaction.objects.filter(user=self.request.user)
#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)

# class BudgetViewSet(viewsets.ModelViewSet):
#     serializer_class = BudgetSerializer
#     permission_classes = [permissions.IsAuthenticated]
#     def get_queryset(self):
#         return Budget.objects.filter(user=self.request.user)
#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)


# from django.shortcuts import render
# from rest_framework import viewsets, permissions
# from .models import Category, Transaction, Budget
# from .serializers import CategorySerializer, TransactionSerializer, BudgetSerializer

# class CategoryViewSet(viewsets.ModelViewSet):
#     queryset = Category.objects.all()  # Required for router
#     serializer_class = CategorySerializer
#     permission_classes = [permissions.IsAuthenticated]

#     # def get_queryset(self):
#     #     return Category.objects.filter(user=self.request.user)
#     def get_queryset(self):
#         print("User:", self.request.user)
#         return Category.objects.filter(user=self.request.user)


#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)

#     def create(self, request, *args, **kwargs):
#         print("Incoming data:", request.data)
#         serializer = self.get_serializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save(user=request.user)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         else:
#             print("Validation errors:", serializer.errors)
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class TransactionViewSet(viewsets.ModelViewSet):
#     queryset = Transaction.objects.all()  # Required for router
#     serializer_class = TransactionSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         return Transaction.objects.filter(user=self.request.user)

#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)

# class BudgetViewSet(viewsets.ModelViewSet):
#     queryset = Budget.objects.all()  # Required for router
#     serializer_class = BudgetSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         return Budget.objects.filter(user=self.request.user)

#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)
