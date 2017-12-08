#!/usr/bin/env python3
# -*- encoding: utf-8 -*-#
# Thanks @mmozeiko for creating this Script <3
# (modified by myself)

import re
import hmac
import hashlib
import struct
import urllib.request
import urllib.error
import xml.etree.ElementTree as ET
import setup_keys

"""
download updates for games and get the key
by the config file (hopefully)
"""


# Here could be some things improved...(but at least I got it working)
KEY = setup_keys.setup()
KEY = bytes(KEY[5], encoding='utf-8')
KEY = KEY.split()
KEY = b''.join(KEY)
KEY = KEY.decode('utf-8')
KEY = bytes.fromhex(KEY)


def title2info(title):
    """
    get link and xml of the tid
    """
    h = hmac.new(KEY, ("np_" + title).encode("ascii"), hashlib.sha256)
    url = "http://gs-sec.ww.np.dl.playstation.net/pl/np/%s/%s/%s-ver.xml" % (
        title, h.hexdigest(), title)

    try:
        with urllib.request.urlopen(url) as f:
            data = f.read()
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None
        raise e

    if data:
        return data.decode("utf-8")

    return None


def parse_sfo(sfo):
    """
    parse sfo ?
    """
    header, version, key_table, data_table, count = struct.unpack_from(
        "<IIIII", sfo)
    assert header == 0x46535000
    assert version == 0x00000101

    ret = {}
    for i in range(count):
        key_offset, param_type, param_len, param_maxlen, data_offset = struct.unpack_from(
            "<HHIII", sfo, 0x14 + 0x10 * i)

        key_end = sfo.find(b"\0", key_table + key_offset)
        key = struct.unpack_from(
            "%ds" % (key_end - (key_table + key_offset)), sfo, key_table + key_offset)
        key = key[0].decode("ascii")

        if param_type == 0x0204:
            value = struct.unpack_from(
                "%ds" % (param_len - 1), sfo, data_table + data_offset)
            ret[key] = value[0].decode("utf-8")
        elif param_type == 0x0404:
            assert param_len == 4
            value = struct.unpack_from("<I", sfo, data_table + data_offset)
            ret[key] = value[0]
        else:
            assert not "unknown type"

    return ret


def get_pkg_start(pkg, size):
    """
    download pkg data
    """
    req = urllib.request.Request(pkg, headers={"Range": "bytes=0-%d" % size})
    with urllib.request.urlopen(req) as f:
        return f.read()


def get_info(patchurl):
    """
    extract Infos
    """
    MaxVersion = "99.99"

    data = get_pkg_start(patchurl, 16 * 1024)

    magic1 = struct.unpack_from(">I", data)[0]
    magic2 = struct.unpack_from(">I", data, 192)[0]
    if magic1 != 0x7f504b47 or magic2 != 0x7f657874:
        print(patchurl)
        print("corrupted pkg?")
        return MaxVersion

    meta_offset, meta_count = struct.unpack_from(">II", data, 8)
    sfo_offset = None
    for i in range(meta_count):
        meta_type, meta_size = struct.unpack_from(">II", data, meta_offset)
        if meta_type == 14:
            sfo_offset, sfo_size = struct.unpack_from(
                ">II", data, meta_offset + 8)
            break
        meta_offset += 8 + meta_size

    if sfo_offset is None:
        print(patchurl)
        print("cannot find sfo in pkg")
        return MaxVersion

    if sfo_offset + sfo_size > len(data):
        print(patchurl)
        print("sfo is not in beginning of pkg [%d..%d]" % (
            sfo_offset, sfo_offset + sfo_size - 1))
        return MaxVersion

    sfo = parse_sfo(data[sfo_offset:sfo_offset + sfo_size])
    fw = sfo["PSP2_DISP_VER"]

    name = sfo["STITLE"] if "STITLE" in sfo else sfo["TITLE"]
    name = name.strip()

    m = re.match(r"(\d+\.\d\d).*", fw)
    return m.group(1), name


def get_supported(xml, supported="03.60"):
    """
    search for the latest patch on 03.60 (Henkaku Firmware)
    """
    packages = list(ET.fromstring(xml).findall("./tag/package"))
    for p in reversed(packages):
        patchurl = p.attrib["url"]
        size = p.attrib["size"]
        version = p.attrib["version"]
        fw, name = get_info(patchurl)
        if fw <= supported:
            return patchurl

    return None


def patch(title):
    """
    final function to export the Link for the PKG File
    """
    xml = title2info(title)
    if xml is None:
        return 0
    else:
        supported = get_supported(xml)
        if supported is None:
            return 0
        else:
            patchurl = supported
            return patchurl
