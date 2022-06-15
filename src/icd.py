import numpy as np
# import pandas as pd
import re

# https://stackoverflow.com/questions/71410627/python-icd-10-regexv

def icd9_checker(string):
    """
    quality checks for icd9. Raise assertion error for incorrectly formatted icd9 codes
    :param string: the icd9 string to parse
    :return: None.
    """

    str_len = len(string)
    if str_len > 3:
        assert string[3] == '.', "ICD9 is more than 3 digits, but the 4th char is not '.'"

    icd9_convention = re.compile(r'(?i)[EV0-9][0-9][0-9](?:\.[0-9]{0:2)?') # If first char is alphabet, can only be E or V
    assert icd9_convention.match(string), 'ICD9 quality check fail.'


def create_regex_icd9(diag_string):
    """
    creates regular expression given the icd9 string.
    :param diag_string: assumes form of [0-9][0-9][0-9].x, where x indicates all subgroups are valid diagnoses
    :return content: the regular expression result compatible with PostgreSQL regex.
    """
    icd9_checker(diag_string)  # run quality checks
    str_list = diag_string.split('.')  # splits icd9 code by '.'
    content = ""
    for char in str_list[0]: # basic icd
        content += f'[{char}]'

    content += '\\.'  # adds '.'

    for char in str_list[1]:  # sub icd
        if char == 'x': break
        content += f'[{char}]'
    #TODO: what if 296.x?
    content = r'(?i)' + content + '[0-9]{0,1}'  # (?i) ignores cases
    print(content)
    return content
# '296.2x'


def icd9_finder(string, icd_rx):
    """
    finds icd codes matching the regular expression
    :param string: the icd to check whether matches the icd9
    :param icd_rx: regex from icd9
    :return: bool. whether the string matches the diagnoses or not
    """
    len_str = len(string)
    icd9_rx = re.compile(icd_rx)

    # icd9_rx = re.compile(r'(?i)[EV0-9][0-9][0-9]\.([0-9]{1,2})') # '.' is not optional in ICD9

    if icd9_rx.fullmatch(string):
        #TODO: need to translate to PostgreSQL regex
        print(f'{string} is a valid psychiatric diagnosis !')
    else:
        print(f'{string} is NOT a valid psychiatric diagnosis !')

def main():
    DESIRED_ICD = "296.2x"
    print("Desired ICD:", DESIRED_ICD)
    rx = create_regex_icd9(DESIRED_ICD)

    icd_checklist = ['296.29', '296.22', '296.233', '393.29', '343.33']
    # GT: T, T, F, F, F
    for icd in icd_checklist:
        icd9_finder(icd, rx)

# icd9_finder("296.22", "296.2x")


if __name__ == "__main__":
    main()

"""
296.2x, 296.3x, 300.4x, 309.0x, 309.1x, 311.xx
"""
