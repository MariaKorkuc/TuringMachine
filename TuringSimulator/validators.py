import os
from django.core.exceptions import ValidationError
from django.db.models import Q


def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.xlsx']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension.')


def validate_example_with_alphabet(example, alphabet):
    for letter in list(example):
        if letter not in list(alphabet):
            return False
    return True


def validate_example_excel_filled_out(machine):
    return not machine.excel_empty


def validate_example_avoid_duplicates(examples, example_cont, user_id, machine_id):
    existing_examples = examples.filter(Q(Q(author_id=user_id) | Q(author_id=1)) & Q(machine_id=machine_id))
    for ex in existing_examples:
        if example_cont == ex.content:
            return False
    return True


def validate_machine_avoid_duplicates(machines, user_id, machine_title):
    existing_machines = machines.filter(author_id=user_id)
    for mach in existing_machines:
        if mach.title == machine_title:
            return False
    return True


def validate_machine_avoid_duplicates_update(machine_id, machines, user_id, machine_title):
    existing_machines = machines.filter(author_id=user_id).exclude(id=machine_id)
    for mach in existing_machines:
        if mach.title == machine_title:
            return False
    return True