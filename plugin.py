#!/usr/bin/env python3
# -*- encoding: utf-8 -*-#
import urllib.request


def download(url, file_name):
    urllib.request.urlretrieve(url, file_name)


def plg_down():
    de3 = "http://cfw.guide/vita/files/de3.mp4"
    vita_shell = "https://github.com/TheOfficialFloW/VitaShell/releases/download/1.76/VitaShell.vpk"
    homebrew_browser = "https://github.com/devnoname120/vhbb/releases/download/0.80/VitaHBBrowser.vpk"
    nonpdrm = "https://github.com/TheOfficialFloW/NoNpDrm/releases/download/v1.1/nonpdrm.skprx"
    nopsm = "https://github.com/frangarcj/NoPsmDrm/releases/download/v1.2/nopsmdrm.skprx"
    Adrenaline = "https://github.com/TheOfficialFloW/Adrenaline/releases/download/v6/Adrenaline.vpk"
    sd2vita = "https://github.com/Applelo/SwitchSD2Vita/releases/download/1.2/Switch.SD2Vita.vpk"
    usbmc = "https://github.com/yifanlu/usbmc/releases/download/v4/usbmc_installer.vpk"


def config_txt():
    print("dummy")


def translations():
    dragon_psp = "http://www.filepup.net/get/uEyiejm1459366812/1511004412/7D2020_English_Patch_0.91.rar"
