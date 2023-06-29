from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.urls import reverse


class Item(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    entry_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    last_update_date = models.DateTimeField(auto_now=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        existing_items = Item.objects.filter(user=self.user, name=self.name)
        if self.pk:  # Exclude the current item being updated from the query
            existing_items = existing_items.exclude(pk=self.pk)
        if existing_items.exists():
            raise ValidationError("An item with the same name already exists.")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('item-create')


class Expense(models.Model):
    items = models.ManyToManyField(Item)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    expense_method = models.ForeignKey('ExpenseMethod', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    entry_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    last_update_date = models.DateTimeField(auto_now=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.amount <= 0:
            raise ValidationError("Amount must be greater than 0.")

        if self.pk:
            # Updating an existing expense
            old_expense = Expense.objects.filter(pk=self.pk).first()
            if old_expense:
                if self.expense_method != old_expense.expense_method:
                    # Expense method has been changed
                    if self.amount > self.expense_method.balance:
                        raise ValidationError("Amount exceeds the available balance for this method.")
                    self.expense_method.balance -= self.amount
                    self.expense_method.save()

                    old_expense.expense_method.balance += old_expense.amount
                    old_expense.expense_method.save()

                else:
                    # Expense method remains the same
                    if self.amount < old_expense.amount:
                        difference = old_expense.amount - self.amount
                        self.expense_method.balance += difference
                    elif self.amount > old_expense.amount:
                        difference = self.amount - old_expense.amount
                        if difference > self.expense_method.balance:
                            raise ValidationError("Amount exceeds the available balance.")
                        self.expense_method.balance -= difference
                    self.expense_method.save()
        else:
            # Creating a new expense
            if self.amount > self.expense_method.balance:
                raise ValidationError("Amount exceeds the available balance.")
            self.expense_method.balance -= self.amount
            self.expense_method.save()

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        expense_method = self.expense_method
        expense_method.balance += self.amount
        expense_method.save()

        super().delete(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('expense-list')


class ExpenseMethod(models.Model):
    name = models.CharField(max_length=20, unique=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    entry_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    last_update_date = models.DateTimeField(auto_now=True, null=True, blank=True)

    def save(self, *args, **kwargs):

        if self.balance < 0:
            raise ValidationError("Balance cannot be below 0.")

        if self.pk:
            original_expense_method = ExpenseMethod.objects.get(pk=self.pk)
            original_balance = original_expense_method.balance

            total_expense = Expense.objects.filter(expense_method=original_expense_method).aggregate(models.Sum('amount'))[
                'amount__sum']
            if total_expense is None:
                total_expense = 0

            original_expense_method.balance += total_expense - original_balance

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('expense-method-list')