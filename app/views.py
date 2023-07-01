import io
from datetime import datetime

import openpyxl
import csv

import pandas as pd
from django.contrib import messages
from django.contrib.auth import logout
from django.core.exceptions import ValidationError
from django.db import transaction
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.views import View

from django.contrib.auth.views import PasswordResetView
from django.urls import reverse_lazy

from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Expense, ExpenseMethod, Item

from .forms import CustomUserCreationForm, ExpenseForm, UploadForm

# Create your views here.

class SignupView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'signup.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

class CustomPasswordResetView(PasswordResetView):
    template_name = 'password_reset.html'
    # success_url = reverse_lazy('password-reset-done')
    success_url = reverse_lazy('login')

class CustomLoginView(LoginView):
    template_name = 'login.html'

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('expense_list.html')

class ExpenseListView(LoginRequiredMixin, ListView):
    model = Expense
    template_name = 'expense_list.html'
    context_object_name = 'expenses'

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user).order_by('-id')


class ExpenseCreateView(LoginRequiredMixin, CreateView):
    model = Expense
    form_class = ExpenseForm
    template_name = 'expense_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        try:
            return super().form_valid(form)
        except ValidationError as e:
            form.add_error(None, e)
            return self.form_invalid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class ExpenseUpdateView(LoginRequiredMixin, UpdateView):
    model = Expense
    form_class = ExpenseForm
    template_name = 'expense_form.html'

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def form_valid(self, form):
        try:
            return super().form_valid(form)
        except ValidationError as e:
            form.add_error(None, e)
            return self.form_invalid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

class ExpenseDeleteView(LoginRequiredMixin, DeleteView):
    model = Expense
    template_name = 'expense_confirm_delete.html'
    context_object_name = 'expense'
    success_url = reverse_lazy('expense-list')

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        expense = self.get_object()
        context['expense'] = expense
        return context

class UploadView(LoginRequiredMixin, View):
    def get(self, request):
        form = UploadForm()
        return render(request, 'upload.html', {'form': form})

    def post(self, request):
        form = UploadForm(request.POST, request.FILES)

        if form.is_valid():
            file = request.FILES['file']
            workbook = openpyxl.load_workbook(file)
            worksheet = workbook.active
            rows = worksheet.iter_rows(values_only=True)

            with transaction.atomic():
                for row in rows:
                    items = row[0]
                    amount = row[1]
                    expense_method_name = row[2]
                    entry_date = row[3]
                    last_update_date = row[4]

                    if not items:
                        continue  # Skip empty rows

                    # Create or get the item
                    item, _ = Item.objects.get_or_create(name=items, user=request.user)

                    # Create or get the expense method
                    expense_method, _ = ExpenseMethod.objects.get_or_create(
                        name=expense_method_name,
                        defaults={'balance': 100000, 'user': request.user}
                    )

                    if entry_date:
                        entry_date = datetime.strptime(str(entry_date), "%Y-%m-%d %H:%M:%S")
                    else:
                        entry_date = datetime.now()

                    if last_update_date:
                        last_update_date = datetime.strptime(str(last_update_date), "%Y-%m-%d %H:%M:%S")
                    else:
                        last_update_date = datetime.now()

                    print("1")
                    print(entry_date)
                    print(last_update_date)

                    # Create the expense
                    expense = Expense(
                        amount=amount,
                        expense_method=expense_method,
                        entry_date=entry_date,
                        last_update_date=last_update_date,
                        user=request.user)

                    try:
                        print("2")
                        print(expense.entry_date)
                        print(expense.last_update_date)

                        expense.save()

                        print("3")
                        print(expense.entry_date)
                        print(expense.last_update_date)

                        expense.items.set([item])
                    except ValidationError as e:
                        form.add_error(None, e)  # Add error to the form

            if form.errors:
                # If there are errors, render the template with the form containing the error messages
                return render(request, 'upload.html', {'form': form})

            messages.success(request, 'Expense data uploaded successfully.')
            return redirect('expense-list')

        return render(request, 'upload.html', {'form': form})

class ExpenseMethodListView(LoginRequiredMixin, ListView):
    model = ExpenseMethod
    template_name = 'expense_method_list.html'
    context_object_name = 'expense_methods'

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class ExpenseMethodCreateView(LoginRequiredMixin, CreateView):
    model = ExpenseMethod
    template_name = 'expense_method_form.html'
    fields = ['name', 'balance']

    def form_valid(self, form):
        form.instance.user = self.request.user
        try:
            return super().form_valid(form)
        except ValidationError as e:
            form.add_error(None, e)
            return self.form_invalid(form)

class ExpenseMethodUpdateView(LoginRequiredMixin, UpdateView):
    model = ExpenseMethod
    template_name = 'expense_method_form.html'
    fields = ['name', 'balance']

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def form_valid(self, form):
        try:
            return super().form_valid(form)
        except ValidationError as e:
            form.add_error(None, e)
            return self.form_invalid(form)

class ExpenseMethodDeleteView(LoginRequiredMixin, DeleteView):
    model = ExpenseMethod
    template_name = 'expense_method_confirm_delete.html'
    context_object_name = 'expense_method'
    success_url = reverse_lazy('expense-method-list')

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        expense_method = self.get_object()
        context['expense_method'] = expense_method
        return context


# class ItemListView(LoginRequiredMixin, ListView):
#     model = Item
#     template_name = 'item_list.html'
#     context_object_name = 'items'
#
#     def get_queryset(self):
#         return super().get_queryset().filter(user=self.request.user).order_by('-id')

class ItemCreateView(LoginRequiredMixin, CreateView):
    model = Item
    template_name = 'item_form.html'
    fields = ['name']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['items'] = Item.objects.order_by('-id').filter(user=self.request.user)
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        try:
            return super().form_valid(form)
        except ValidationError as e:
            form.add_error(None, e)
            return self.form_invalid(form)

class ItemUpdateView(LoginRequiredMixin, UpdateView):
    model = Item
    template_name = 'item_form.html'
    fields = ['name']

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['items'] = Item.objects.order_by('-id').filter(user=self.request.user)
        return context

    def form_valid(self, form):
        try:
            return super().form_valid(form)
        except ValidationError as e:
            form.add_error(None, e)
            return self.form_invalid(form)

class ItemDeleteView(LoginRequiredMixin, DeleteView):
    model = Item
    template_name = 'item_confirm_delete.html'
    success_url = reverse_lazy('item-create')

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

