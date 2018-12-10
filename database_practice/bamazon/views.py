from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.template import loader
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.forms.models import  model_to_dict
from django.forms import ModelForm
from .models import Item, Departments

class ItemForm(ModelForm):
    class Meta:
        model = Item
        fields = ['product_name','department_name','price','stock']

class DepartmentForm(ModelForm):
    class Meta:
        model = Departments
        fields = ['department_name','over_head_costs']


def index(request):
    context = {}
    context['items'] = Item.objects.all()
    return render(request,"bamazon/index.html",context)

def item_json(request,item_id):
    newItem = model_to_dict(get_object_or_404(Item,id=item_id))
    return JsonResponse(newItem)

def item_details(request,item_id):
    item = get_object_or_404(Item,id=item_id)
    department = get_object_or_404(Departments,department_name=item.department_name)
    context = {"item": item}
    if (request.POST):
        amount = int(request.POST.get('amount'))
        if amount <= item.stock and amount > 0:
            item.stock -= amount
            department.product_sales += amount*item.price
            item.save()
            department.save()
            return redirect("bamazon:manager_view")
        else:
            context["error"] = "Please input a valid amount"
            return render(request,'bamazon/details.html', context)
    
    
    return render(request,"bamazon/details.html",context)

def add_item_view(request):
    form = ItemForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("bamazon:add_item")
    return render(request, "bamazon/add.html", {'form': form})


def manager_view(request,sortBy):
    if(sortBy == "low"):
        items = Item.objects.filter(stock__lte=5)
    else:
        items = Item.objects.all()
    context = {"items": items}
    return render(request,'bamazon/managerindex.html',context)


def supervisor_view(request):
    departments = Departments.objects.all()
    print(departments)
    for department in departments: 
        department.total_profit = department.product_sales - department.over_head_costs
    context = {"departments": departments}
    return render(request,"bamazon/supervisorindex.html",context)


def create_department(request):
    form = DepartmentForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("bamazon:supervisor_view")
    return render(request, "bamazon/adddepartment.html",{'form':form})