import datetime as dt


class Record:
    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment
        if date is None:
            self.date = dt.date.today()
        else:
            self.date = dt.datetime.strptime(date, '%d.%m.%Y').date()


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []
        self.current_date = dt.date.today()
        self.days_ago = self.current_date - dt.timedelta(7)

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        day_stats = []
        for record in self.records:
            if record.date == self.current_date:
                day_stats.append(record.amount)
        return sum(day_stats)

    def get_week_stats(self):
        week_stats = []
        for record in self.records:
            if self.days_ago <= record.date <= self.current_date:
                week_stats.append(record.amount)
        return sum(week_stats)


class CashCalculator(Calculator):
    rub = 1
    dollar = 64.70
    euro = 69.11

    def get_today_cash_remained(self, currency):
        currencies = {'usd': ('dollars', self.dollar),
                      'eur': ('euros', self.euro),
                      'rub': ('руб', self.rub)}
        delta_cash = self.limit - self.get_today_stats()
        name, rate = currencies.get(currency)
        delta_cash = delta_cash / rate
        if delta_cash == 0:
            message = f'На сегодня деньги кончились!'
        elif delta_cash > 0:
            message = f'На сегодня денег осталось: {round(delta_cash, 3)} {name}'
        else:
            delta_cash < 0
            message = f'Сегодня Вы ушли в долг: {round(delta_cash, 3)} {name}'
        return message


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):
        delta_calories = self.limit - self.get_today_stats()
        if delta_calories > 0:
            message = f'Сегодня можно съесть что-нибудь ещё, но с общей калорийностью не более {delta_calories} Ккал'
        else:
            message = f'Сегодня Вы достаточно кушали!'
        return message


cash_calculator = CashCalculator(500)
cal_calculator = CaloriesCalculator(1500)
cash_calculator.add_record(Record(amount=350, comment='куриное филе'))
cal_calculator.add_record(Record(amount=500, comment='завтрак'))
cal_calculator.add_record(Record(amount=100, comment='перекус'))
print(cash_calculator.get_today_cash_remained('eur'))
print(cal_calculator.get_calories_remained())
