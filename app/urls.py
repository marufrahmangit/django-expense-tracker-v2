from django.urls import path

from django.conf import settings
from django.conf.urls.static import static

from .views import (
    CustomLoginView, CustomPasswordResetView, SignupView, LogoutView,
    ExpenseListView, ExpenseCreateView, ExpenseUpdateView, ExpenseDeleteView,
    ExpenseMethodListView, ExpenseMethodCreateView, ExpenseMethodUpdateView, ExpenseMethodDeleteView,
    # ItemListView,
    ItemCreateView, ItemUpdateView, ItemDeleteView, UploadView
)

urlpatterns = [
    # path('', HomeView.as_view(), name='home'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('password-reset/', CustomPasswordResetView.as_view(), name='password-reset'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('', ExpenseListView.as_view(), name='expense-list'),
    # path('expenses/', ExpenseListView.as_view(), name='expense-list'),
    path('expenses/create/', ExpenseCreateView.as_view(), name='expense-create'),
    path('expenses/<int:pk>/update/', ExpenseUpdateView.as_view(), name='expense-update'),
    path('expenses/<int:pk>/delete/', ExpenseDeleteView.as_view(), name='expense-delete'),
    path('expense-methods/', ExpenseMethodListView.as_view(), name='expense-method-list'),
    path('expense-methods/create/', ExpenseMethodCreateView.as_view(), name='expense-method-create'),
    path('expense-methods/<int:pk>/update/', ExpenseMethodUpdateView.as_view(), name='expense-method-update'),
    path('expense-methods/<int:pk>/delete/', ExpenseMethodDeleteView.as_view(), name='expense-method-delete'),
    path('items/', ItemCreateView.as_view(), name='item-list'),
    path('items/create/', ItemCreateView.as_view(), name='item-create'),
    path('items/<int:pk>/update/', ItemUpdateView.as_view(), name='item-update'),
    path('items/<int:pk>/delete/', ItemDeleteView.as_view(), name='item-delete'),

    path('upload/', UploadView.as_view(), name='upload'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)