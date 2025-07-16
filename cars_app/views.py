from django.db.models import Q  # ← أضف هذا في الأعلى
from django.shortcuts import render, redirect, get_object_or_404
from .forms import CarForm
from .models import Car

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if username == 'admin' and password == '1234':
            request.session['user'] = username
            return redirect('car_list')
        else:
            return render(request, 'login.html', {'error': 'بيانات غير صحيحة'})
    return render(request, 'login.html')

def add_car(request):
    if 'user' not in request.session:
        return redirect('login')

    if request.method == 'POST':
        form = CarForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('car_list')
    else:
        form = CarForm()
    return render(request, 'add_car.html', {'form': form})



from django.db.models import F
from django.core.paginator import Paginator
from .models import Car

def car_list(request):
    if 'user' not in request.session:
        return redirect('login')

    query = request.GET.get('q', '')
    sort = request.GET.get('sort', 'name')
    order = request.GET.get('order', 'asc')
    per_page = request.GET.get('per_page', '50')

    try:
        per_page = int(per_page)
        if per_page not in [5, 10, 50, 100]:
            per_page = 5
    except ValueError:
        per_page = 5

    # ✅ إجمالي السجلات في القاعدة قبل التصفية
    total_count = Car.objects.count()

    # تصفية حسب البحث إن وجد
    cars = Car.objects.filter(name__icontains=query) if query else Car.objects.all()

    if order == 'desc':
        cars = cars.order_by(f'-{sort}')
    else:
        cars = cars.order_by(sort)

    paginator = Paginator(cars, per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'car_list.html', {
        'cars': page_obj,
        'query': query,
        'sort': sort,
        'order': order,
        'per_page': per_page,
        'page_obj': page_obj,
        'result_count': cars.count(),  # ✅ عدد النتائج بعد التصفية
        'total_count': total_count     # ✅ العدد الكلي
    })

def delete_car(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    car.delete()
    return redirect('car_list')

def edit_car(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    if request.method == 'POST':
        form = CarForm(request.POST, instance=car)
        if form.is_valid():
            form.save()
            return redirect('car_list')
    else:
        form = CarForm(instance=car)
    return render(request, 'add_car.html', {'form': form})

def logout_view(request):
    request.session.flush()  # يحذف كل بيانات الجلسة
    return redirect('login')  # يعيد المستخدم لصفحة تسجيل الدخول

