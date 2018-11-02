# Fat Stacks Payroll

## About
Dev challenge for a job application which tests object-oriented programming in Python.

A very simple object-oriented payroll app which displays a user interface, allowing a user to login
and be verified using the attached `authentication.txt` file. Once verified the user can then query
the employee and pay data (`employees.txt`, `pays.txt`), where the app must display and process a series
of menu and sub-menu options.

## Requires

    python3.6

## Prerequisites

### Database
The following files are considered the "database" and hence are Git ignored:

    authentication.txt
    employees.txt
    pays.txt

Sample versions of these files are in the [examples](examples) directory.

These files must be placed in the root directory i.e. `fat-stacks`

## Installation
Unzip fat-stacks.zip

    cd fat-stacks
    pip3 install virtualenv
    virtualenv env
    . env/bin/activate
    pip install -r requirements.txt
    export PYTHONPATH=`pwd`

## Run
    chmod a+x run_fat_stacks.py
    python run_fat_stacks.py
