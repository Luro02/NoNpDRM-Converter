#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# https://www.bggofurther.com/2015/01/create-an-interactive-command-line-menu-using-python/
# This tool won't work in Visual Studio Code (as an example).
# I don't know why this is the case but just run it in cmd.exe
import sys
import os
import collections
import ctypes
from subprocess import Popen, PIPE
import locale
import gui  # <-- change name !!
import header
from hurry.filesize import alternative, size  # pip install hurry.filesize
from prompt_toolkit import prompt
from prompt_toolkit.styles import style_from_dict
from prompt_toolkit.token import Token

# set locale to default to get thousands separators
locale.setlocale(locale.LC_ALL, '')

# Pointer to large unsigned integer
PULARGE_INTEGER = ctypes.POINTER(ctypes.c_ulonglong)
kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
kernel32.GetDiskFreeSpaceExW.argtypes = (
    ctypes.c_wchar_p,) + (PULARGE_INTEGER,) * 3


def get_size(start_path='.'):
    """
    https://stackoverflow.com/questions/1392413/calculating-a-directory-size-using-python
    """
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)

    return size(total_size, system=alternative)


def get_size2(string):
    value = size(string, system=alternative)
    return value


def cutit(s, n):
    """
    cute function that removes chars
    s = string
    n = char to remove
    """
    return s[n:]


class UsageTuple(collections.namedtuple('UsageTuple', 'total, used, free')):
    def __str__(self):
        # Add thousands separator to numbers displayed
        return '{}, {}, {}'.format(*self)


def disk_usage(path):
    try:
        # allows str or bytes (or os.PathLike in Python 3.6+)
        path = os.fsdecode(path)
    except AttributeError:  # fsdecode() not added until Python 3.2
        pass

    # Define variables to receive results when passed as "by reference" arguments
    _, total, free = ctypes.c_ulonglong(), ctypes.c_ulonglong(), ctypes.c_ulonglong()

    success = kernel32.GetDiskFreeSpaceExW(
        path, ctypes.byref(_), ctypes.byref(total), ctypes.byref(free))
    if not success:
        error_code = ctypes.get_last_error()
    if not success:
        windows_error_message = ctypes.FormatError(error_code)
        raise ctypes.WinError(error_code, '{} {!r}'.format(
            windows_error_message, path))

    used = total.value - free.value
    return UsageTuple(total.value, used, free.value)


def drive_parser(letter):
    total, used, free = disk_usage(letter)
    total = get_size2(total)
    free = get_size2(free)
    return free, total


def get_bottom_toolbar_tokens(cli):
    free, total = drive_parser('D:/')
    return [(Token.Toolbar, '   app folder: {}  patch folder: {} SDCard: {} of {} free'.format(get_size('app'), get_size('patch'), free, total))]


def input(string):  # it's intendet to redefine input() XD
    style = style_from_dict({
        Token.Toolbar: '#ffffff bg:#333333',
    })
    output = prompt(
        string, get_bottom_toolbar_tokens=get_bottom_toolbar_tokens, style=style)
    return output


# Main definition - constants
menu_actions = {}
sub_menu = {}
selection = []
name, titleid = gui.send_variables()
# =======================
#     MENUS FUNCTIONS
# =======================


def clearscreen(numlines=100):
    """
    Clear the console.numlines is an optional argument used only as a fall-back.
    """
    # Thanks to Steven D'Aprano, http://www.velocityreviews.com/forums
    if os.name == "posix":
        # Unix/Linux/MacOS/BSD/etc
        os.system('clear')
    elif os.name in ("nt", "dos", "ce"):
        # DOS/Windows
        os.system('CLS')
    else:
        # Fallback for other operating systems.
        print('\n' * numlines)


def syscmd(cmd):
    """
    executes the given command with a better way than using
    os.system() (I don't know why but it seems to be bad practice !)
    It also returns the exe output instead of printing it :)
    """
    cmoa = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
    output, error = cmoa.communicate()
    return output, error

# Main menu


def main_menu():
    clearscreen()
    print("1.Start the download")
    print("2.Update Database")
    print("3.Search for Games")
    print("4.Load the queue from 'input.txt'")
    print("5.View the queue")
    print("6.Exit")

    choice = input(">> ")
    exec_menu(choice)

    return

# Execute menu


def exec_menu(choice):
    clearscreen()
    ch = choice.lower()
    if ch == '':
        menu_actions['main_menu']()
    else:
        try:
            menu_actions[ch]()
        except KeyError:
            print("Invalid selection, please try again.\n")
            menu_actions['main_menu']()
    return


def start_download():
    clearscreen()
    if selection == []:
        print("Nothing to download.")
        input('\n<press enter>')
        menu_actions['main_menu']()
    else:
        for tid in selection:
            header.start_download(tid, 'psv')
        input('\n<press enter>')
        menu_actions['main_menu']()


def update_database():
    clearscreen()
    header.initial_setup()
    input('\n<press enter>')
    menu_actions['main_menu']()


def search():
    search_input, selected = gui.start_searching(None)
    for item in selected:
        selection.append(item)
    menu_actions['main_menu']()


def load():
    clearscreen()
    if header.exists('input.txt') is False:
        print("Enter the Filename:")
        filename = header.input_txt(input(">> "))
    else:
        filename = 'input.txt'
    list1 = header.input_txt(filename)
    for item in list1:
        selection.append(item)
    input('\n<press enter>')
    menu_actions['main_menu']()


def view():
    for item in selection:
        position = titleid.index(item)
        print(name[position], '[' + item + ']')
    input('\n<press enter>')
    menu_actions['main_menu']()
# Exit program


def exit():
    sys.exit()


# =======================
#    MENUS DEFINITIONS
# =======================

# Menu definition
menu_actions = {
    'main_menu': main_menu,
    '1': start_download,
    '2': update_database,
    '3': search,
    '4': load,
    '5': view,
    '6': exit,
}
sub_menu = {
    'home': search,
}
# =======================
#      MAIN PROGRAM
# =======================

# Main Program
if __name__ == "__main__":
    # Launch main menu
    main_menu()
