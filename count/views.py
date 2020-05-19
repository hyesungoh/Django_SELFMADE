from django.shortcuts import render
from datetime import datetime

# Create your views here.
def count_home(request):
    if request.method == "POST":
        date_format = "%Y-%m-%d"
        start_day = datetime.strptime(request.POST["start_day"], date_format) 
        end_day =datetime.strptime(request.POST["end_day"], date_format)
        present_day =datetime.strptime(request.POST["present_day"], date_format)

        remain_days = end_day - present_day
        return render(request, 'count/count_home.html', {"remain_days": remain_days})
    else:
        return render(request, 'count/count_home.html')