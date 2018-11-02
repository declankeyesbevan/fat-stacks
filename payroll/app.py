from datetime import datetime

import pandas

from payroll.controllers.authenticate import Authenticate
from payroll.controllers.employee_data import EmployeeData
from payroll.controllers.join import Join
from payroll.controllers.pay_data import PayData
from payroll.views.tui import TUI


class App:

    _MAIN_SELECTIONS = {
        'e': EmployeeData(),
        'p': PayData(),
        'x': None,
    }
    _EMPLOYEE_SUB_SELECTIONS = {
        'i': Join(),
        'x': None,
    }
    _PAY_SUB_SELECTIONS = {
        'd': PayData(),
        'x': None,
    }
    _PAY_OPTION_SELECTIONS = {
        's': True,
        'x': None,
    }
    _MESSAGES = {
        'exit_application': "Or Exit (X) application?",
        'exit_menu': "Or Exit (X) menu?",
        'valid': "Error: please enter valid choice\n",
    }

    def __init__(self):
        self._running = False
        self._tui = TUI()
        self._authentication = Authenticate(self._tui)
        self._join = Join()
        self._pay_data = PayData()
        self.start()

    def start(self):
        try:
            self._running = True
            self._welcome_menu_display()
            self._app_loop()
        except Exception as exc:
            self._tui.print_message(f"Unknown exception occurred: {exc}")

    def _welcome_menu_display(self):
        self._tui.print_message("Welcome to Fat Stacks Payroll Software")
        self._tui.print_message("--------------------------------------")
        self._tui.print_message("Please log-in to continue")

    def _app_loop(self):
        authenticated = False
        while self._running:
            if not authenticated:
                authenticated = self._authentication.authenticate_user()
            if authenticated:
                main_choice = self._main_menu()
                if main_choice is None:
                    self._running = False
                else:
                    if isinstance(main_choice, EmployeeData):
                        self._tui.print_message("Employees\n")
                        self._tui.pretty_print(main_choice.data.values, main_choice.data.columns)
                        self._running = self._employee_sub_menu()
                    elif isinstance(main_choice, PayData):
                        self._running = self._pay_sub_menu()
            else:
                self._running = False
        else:
            self._tui.print_message("Exiting")

    def _main_menu(self):
        viewing = True
        while viewing:
            self._tui.print_message("Main Menu")
            self._tui.print_message("---------")
            self._tui.print_message("View Employees (E) or Pays (P) report?")
            self._tui.print_message(self._MESSAGES.get('exit_application'))
            main_selection = self._tui.get_input("Enter 'E', 'P' or 'X':\n")
            try:
                main_choice = self._MAIN_SELECTIONS[main_selection.lower()]
            except KeyError:
                self._tui.print_message(self._MESSAGES.get('valid'))
            else:
                if main_choice is None:
                    return
                return main_choice

    def _employee_sub_menu(self):
        viewing = True
        while viewing:
            self._tui.print_message("Employee Sub Menu")
            self._tui.print_message("-----------------")
            self._tui.print_message("Select employee by ID (I)?")
            self._tui.print_message(self._MESSAGES.get('exit_menu'))
            sub_selection = self._tui.get_input("Enter 'I' or 'X':\n")
            try:
                sub_choice = self._EMPLOYEE_SUB_SELECTIONS[sub_selection.lower()]
            except KeyError:
                self._tui.print_message(self._MESSAGES.get('valid'))
            else:
                if sub_choice is None:
                    viewing = False
                else:
                    employee_id = self._tui.get_input("Enter employee ID:\n")
                    self._employee_sub_display(sub_choice, employee_id)
        else:
            return True

    def _employee_sub_display(self, sub_choice, employee_id):
        try:
            joined = sub_choice.join_employee_to_pay(employee_id)
        except ValueError:
            self._tui.print_message("Employee ID: must be integer\n")
        else:
            if joined is None:
                self._tui.print_message(f"Employee ID: {employee_id} not found\n")
            else:
                self._tui.print_message(joined.name)
                self._tui.pretty_print(joined.values, joined.values.columns)

    def _pay_sub_menu(self):
        viewing = True
        while viewing:
            self._tui.print_message("Pay Menu")
            self._tui.print_message("--------")
            self._tui.print_message("Enter Date (D) Range?")
            self._tui.print_message(self._MESSAGES.get('exit_menu'))
            sub_selection = self._tui.get_input("Enter 'D' or 'X':\n")
            try:
                sub_choice = self._PAY_SUB_SELECTIONS[sub_selection.lower()]
            except KeyError:
                self._tui.print_message(self._MESSAGES.get('valid'))
            else:
                if sub_choice is None:
                    viewing = False
                else:
                    self._pay_sub_display(sub_choice)
        else:
            return True

    def _pay_sub_display(self, sub_choice):
        dates = self._tui.get_input("Enter pay range in format DD/MM/YYYY DD/MM/YYYY\n")
        try:
            the_range = [
                datetime.strptime(date, '%d/%m/%Y').strftime('%Y-%m-%d')
                for date in dates.split(' ')
            ]
        except ValueError:
            self._tui.print_message("Incorrect date format\n")
        else:
            all_pays = sub_choice.all_pay_per_range(the_range[0], the_range[1])
            self._tui.print_message("Sub-totals")
            self._tui.pretty_print(all_pays.subtotals, all_pays.subtotals.columns)
            self._tui.print_message("Gross Grand-Total")
            self._tui.print_message(all_pays.gross_grand_total)
            self._tui.print_message("Tax Grand-Total")
            self._tui.print_message(all_pays.tax_grand_total)

            self._pay_option_menu(all_pays)

    def _pay_option_menu(self, all_pays):
        viewing = True
        while viewing:
            self._tui.print_message("Pay Option Menu")
            self._tui.print_message("---------------")
            self._tui.print_message("View sub-totals (S) only?")
            self._tui.print_message(self._MESSAGES.get('exit_menu'))
            option_selection = self._tui.get_input("Enter 'S' or 'X':\n")
            try:
                option_choice = self._PAY_OPTION_SELECTIONS[option_selection.lower()]
            except KeyError:
                self._tui.print_message(self._MESSAGES.get('valid'))
            else:
                if option_choice is None:
                    viewing = False
                else:
                    self._pay_option_display(all_pays)
        else:
            return True

    def _pay_option_display(self, all_pays):
        viewing = True
        while viewing:
            gross_series = [
                all_pays.subtotals['employee_id'], all_pays.subtotals['gross_sub_total']]
            gross_sub_total = pandas.concat(gross_series, axis=1)
            self._tui.print_message("Gross Sub Totals")
            self._tui.pretty_print(gross_sub_total, gross_sub_total.columns)

            tax_series = [all_pays.subtotals['employee_id'], all_pays.subtotals['tax_sub_total']]
            tax_sub_total = pandas.concat(tax_series, axis=1)
            self._tui.print_message("Tax Sub Totals")
            self._tui.pretty_print(tax_sub_total, tax_sub_total.columns)

            self._tui.print_message("Exit (X) to Pay Option Menu")
            exit_selection = self._tui.get_input("Enter 'X' when ready:\n")
            if exit_selection.lower() == 'x':
                viewing = False
        else:
            return
