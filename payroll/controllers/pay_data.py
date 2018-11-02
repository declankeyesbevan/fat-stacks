from collections import namedtuple

import numpy
import pandas

from payroll.controllers.data import Data
from payroll.models.pay import Pay


class PayData:

    def __init__(self):
        self._pay = Pay(Data().load_data('pays.txt'))
        self._data = self._pay.data
        self._data['date'] = self._data['date'].astype('datetime64[ns]')

    @property
    def data(self):
        return self._data

    def employee_pay_total(self, employee_id):
        return self._data.loc[self._data['employee_id'] == employee_id]

    @classmethod
    def employee_pay_per_range(cls, pay, range_start, range_end):
        return pay[pay['date'].isin(pandas.date_range(range_start, range_end))]

    def all_pay_per_range(self, range_start, range_end):
        the_range = self._data[self._data['date'].isin(pandas.date_range(range_start, range_end))]
        all_employees = set(the_range['employee_id'])
        individual_pays = [self.employee_pay_total(employee) for employee in all_employees]
        individual_pay_per_range = [
            self.employee_pay_per_range(pay, range_start, range_end) for pay in individual_pays]
        kinds = ['gross', 'tax']
        individual_cumulatives = []
        for kind in kinds:
            individual_cumulatives.append([
                pandas.Series(numpy.cumsum(the_range[kind].values))
                for the_range in individual_pay_per_range
            ])
        for index, individual_cumulative in enumerate(individual_cumulatives):
            joined = pandas.concat(individual_cumulative)
            the_range[f'{kinds[index]}_sub_total'] = joined.values
        gross_total = sum(the_range['gross'])
        tax_total = sum(the_range['tax'])
        AllInfo = namedtuple('AllInfo', 'subtotals gross_grand_total tax_grand_total')
        return AllInfo(the_range, round(gross_total, 2), round(tax_total, 2))
