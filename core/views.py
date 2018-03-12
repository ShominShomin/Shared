from django.shortcuts import render
from django.shortcuts import render_to_response
from django.utils.safestring import mark_safe
from calendar import HTMLCalendar, month_name
from datetime import date
from itertools import groupby
from .models import Item

from django.utils.html import conditional_escape as esc

def home_page(request):
    return render(request, 'home.html')

def reservation_page(request):
    return render(request, 'reservation.html')

def room_page(request):
    return render(request, 'room.html')

def reservation_auth_page(request):
    return render(request, 'reservation_auth.html')

def confirm_order_page(request):
    return render(request, 'confirm_order.html')

def check_reservation_page(request):
    return render(request, 'check_reservation.html')


class WorkoutCalendar(HTMLCalendar):

    def __init__(self, workouts):
        super(WorkoutCalendar, self).__init__()
        self.workouts = self.group_by_day(workouts)

    def formatday(self, day, weekday):
        if day != 0:
            cssclass = self.cssclasses[weekday]
            if date.today() == date(self.year, self.month, day):
                cssclass += ' today'
            if day in self.workouts:
                cssclass += ' filled'
                body = ['<ul>']
                for workout in self.workouts[day]:
                    body.append('<li>')
                    body.append('<a href="%s">' % workout.get_absolute_url())
                    body.append(esc(workout.title))
                    body.append('</a></li>')
                body.append('</ul>')
                return self.day_cell(cssclass, '%d %s' % (day, ''.join(body)))
            return self.day_cell(cssclass, day)
        return self.day_cell('noday', '')

    def formatmonth(self, year, month):
        self.year, self.month = year, month
        return super(WorkoutCalendar, self).formatmonth(year, month)

    def group_by_day(self, workouts):
        field = lambda workout: workout.my_date.day
        return dict([(day, list(items)) for day, items in groupby(workouts, field)])

    def day_cell(self, cssclass, body):
        return '<td class="%s">%s</td>' % (cssclass, body)

    def formatmonthname(self, theyear, themonth, withyear=True):
        if withyear:
            s = '%s %s' % (month_name[themonth], theyear)
        else:
            s = '%s' % month_name[themonth]
        return '<tr><th colspan="7" class="monthName">%s</th></tr>' % s


def calendar(request, year, month):
    year = int(year)
    month = int(month)
    my_workouts = Item.objects.order_by('my_date').filter(my_date__year=year,    my_date__month=month)
    cal = WorkoutCalendar(my_workouts).formatmonth(year, month)
    return render_to_response('reservation.html', {'calendar': mark_safe(cal),})