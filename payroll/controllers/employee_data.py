from payroll.controllers.data import Data
from payroll.models.employee import Employee


class EmployeeData:

    def __init__(self):
        self._employee = Employee(Data().load_data('employees.txt'))
        self._data = self._employee.data

    @property
    def data(self):
        return self._data

    def employee_name(self, employee_id):
        employee = self._data.loc[self._data['id'] == employee_id]
        display = employee['first_name'] + [' '] + employee['last_name']
        return ' '.join(display)
