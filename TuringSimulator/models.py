from django.db import models
from django.contrib.auth.models import User
from turing_utils.scripts.turing_machine import InstructionBox, Instruction, TuringMachine
from .validators import validate_file_extension
from django.urls import reverse
from turing_utils.scripts.excel_utils import generate_instructions_from_xlsx_file
import boto3
from openpyxl import load_workbook


s3 = boto3.resource('s3')

FILES_PATH = 'excel_files/'
AWS_EXCEL_FILE_PATH = 'https://turing-machine-files-bucket.s3.us-east-2.amazonaws.com/excel_files/'
DEFAULT_EXCEL_FILE_PATH = AWS_EXCEL_FILE_PATH + 'default_excel.xlsx'


def parse_to_InstructionBox(value):
    instructions = value.split('|')
    instr_list = []
    for instr in instructions:
        dct = eval(instr)
        keys = tuple(dct)
        instr_tuple = tuple([dct[key] for key in keys])
        instr_list.append(Instruction(instr_tuple))
    return InstructionBox(instr_list)


def parse_to_query(obj):
    # {'s_in': a, 'q_in': b, 's_out': c, 'q_out': d, 'step': e}|{'s_in': ...
    return str(obj)


class TuringMachineDB(models.Model):
    title = models.CharField(max_length=100)
    is_decisive = models.BooleanField(default=False)
    instructions = models.FileField(upload_to='excel_files', default=DEFAULT_EXCEL_FILE_PATH, validators=[validate_file_extension])
    number_of_states = models.IntegerField()
    alphabet = models.CharField(max_length=100)
    starting_index = models.IntegerField(default=1)
    empty_sign = models.CharField(max_length=1, default='#')
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    initial_number_of_states = models.IntegerField(default=0)
    initial_alphabet = models.CharField(max_length=100, default='')
    excel_empty = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('machine-detail', kwargs={'pk': self.pk})


class ExampleDB(models.Model):
    machine = models.ForeignKey(TuringMachineDB, on_delete=models.CASCADE)
    content = models.CharField(max_length=50)
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    example_steps = models.TextField(default='None')
    last_value = models.CharField(default='None', max_length=5)

    def __str__(self):
        return self.content

    def get_absolute_url(self):
        return reverse('machine-detail', kwargs={'pk': self.machine_id})

    def format_content(self):
        list_content = list(str(self.content))
        empty_sign = str(self.machine.empty_sign)
        if list_content[0] != empty_sign:
            list_content.insert(0,empty_sign)
        if list_content[-1] != empty_sign:
            list_content.append(empty_sign)
        return list_content

    def prepare_steps_text(self, updated_start=None):
        workbook = load_workbook(self.machine.instructions)
        instructions = generate_instructions_from_xlsx_file(ready_workbook=workbook)
        examples = list()
        examples.append(self.format_content())
        index = int(self.machine.starting_index) if updated_start == None else int(updated_start)
        print(index)
        machine_obj = TuringMachine(
            index,
            'q0',
            instructions,
            examples,
            is_decisive=self.machine.is_decisive,
            empty_sign=self.machine.empty_sign
        )
        output, last_value = machine_obj.start_machine()
        self.example_steps = output.getvalue()
        if self.machine.is_decisive:
            self.last_value = str(last_value)


