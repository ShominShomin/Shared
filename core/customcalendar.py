from calendar import HTMLCalendar, month_name
from datetime import date


class CustomCalendar(HTMLCalendar):

    def __init__(self):
        super(CustomCalendar, self).__init__()

    def formatday(self, day, weekday):
        if day != 0:
            cssclass = self.cssclasses[weekday]
            if date.today() == date(self.year, self.month, day):
                cssclass += ' today'
            return self.day_cell(cssclass, day)
        return self.day_cell('noday', '')

    def formatmonth(self, year, month):
        self.year, self.month = year, month
        return super(CustomCalendar, self).formatmonth(year, month)

    def day_cell(self, cssclass, body):
        if not body:
            return '<td class="%s">%s</td>' % (cssclass, body)
        else:
            url = str(body)
            return '<td class="%s"><a href="%s">%s</a></td>' % (cssclass, url, body)

    def formatmonthname(self, theyear, themonth, withyear=True):
        if withyear:
            s = '%s %s' % (month_name[themonth], theyear)
        else:
            s = '%s' % month_name[themonth]
        return '<tr><th name="monthName" colspan="7" class="monthName">%s</th></tr>' % s
