from collections import namedtuple

import pandas

from payroll.controllers.employee_data import EmployeeData
from payroll.controllers.pay_data import PayData


class Join:

    def __init__(self):
        self._employees = EmployeeData()
        self._pays = PayData()
        self._gross_by_year = {}
        self._tax_by_year = {}
        self._net_by_year = {}

    def join_employee_to_pay(self, employee_id):
        try:
            employee_id = int(employee_id)
        except ValueError:
            raise
        else:
            employee_name = self._employees.employee_name(employee_id)
            if employee_name:
                employee_pay = self._pays.employee_pay_total(employee_id)
                years = list(set(employee_pay['date'].apply(lambda x: x.strftime('%Y'))))
                years.sort()
                FinancialYear = namedtuple('FinancialYear', 'start end')
                years_paid = [
                    FinancialYear(f'{int(year)}-07-01', f'{int(year) + 1}-06-30') for year in years]
                pay_pear_year = [
                    self._pays.employee_pay_per_range(
                        employee_pay,
                        years_paid[index].start,
                        years_paid[index].end
                    ) for index, _ in enumerate(years_paid)
                ]
                total_gross = [pay['gross'].sum() for pay in pay_pear_year]
                self._gross_by_year = dict(zip(years, map(lambda x: round(x, 2), total_gross)))
                total_tax = [pay['tax'].sum() for pay in pay_pear_year]
                self._tax_by_year = dict(zip(years, map(lambda x: round(x, 2), total_tax)))

                for year, gross in self._gross_by_year.items():
                    net = gross - self._tax_by_year.get(year)
                    self._net_by_year.update({year: round(net, 2)})

                values = {
                    'gross': self._gross_by_year,
                    'tax': self._tax_by_year,
                    'net': self._net_by_year,
                }
                EmployeePay = namedtuple('EmployeePay', 'name, values')
            else:
                return None
            return EmployeePay(employee_name, pandas.DataFrame.from_dict(values))
