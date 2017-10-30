# Thanks @mmozeiko for creating this Script <3
#!/usr/bin/env python3

import os
import re
import csv
import sys
import hmac
import header
import hashlib
import struct
import urllib.request
import urllib.error
import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom

def keyfile():
	#read File
	with open ("keys.cfg", "r") as r:
		key_dig = r.readlines()
	key_dig[4] = key_dig[4].upper()
	#Hashcheck
	hash_2 = hashlib.sha1((key_dig[4]).encode("utf-8"))
	if "3d059b28eb079add2676e9db181d794de1235908" != hash_2.hexdigest():
		sys.exit("The key is wrong !")
	else:
		update_key = key_dig[4]
	print(update_key)
	return key_dig
key_dig = keyfile()
# http://wololo.net/talk/viewtopic.php?f=54&t=44091
KEY = bytes(key_dig[4], encoding='utf-8')


def title2info(title):
  h = hmac.new(KEY, ("np_" + title).encode("ascii"), hashlib.sha256)
  url = "http://gs-sec.ww.np.dl.playstation.net/pl/np/%s/%s/%s-ver.xml" % (title, h.hexdigest(), title)

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
  header, version, key_table, data_table, count = struct.unpack_from("<IIIII", sfo)
  assert header == 0x46535000
  assert version == 0x00000101

  ret = {}
  for i in range(count):
    key_offset, param_type, param_len, param_maxlen, data_offset = struct.unpack_from("<HHIII", sfo, 0x14 + 0x10 * i)

    key_end = sfo.find(b"\0", key_table + key_offset)
    key = struct.unpack_from("%ds" % (key_end - (key_table + key_offset)), sfo, key_table + key_offset)
    key = key[0].decode("ascii")

    if param_type == 0x0204:
      value = struct.unpack_from("%ds" % (param_len - 1), sfo, data_table + data_offset)
      ret[key] = value[0].decode("utf-8")
    elif param_type == 0x0404:
      assert param_len == 4
      value = struct.unpack_from("<I", sfo, data_table + data_offset)
      ret[key] = value[0]
    else:
      assert not "unknown type"

  return ret


def get_pkg_start(pkg, size):
  req = urllib.request.Request(pkg, headers={"Range": "bytes=0-%d" % size})
  with urllib.request.urlopen(req) as f:
    return f.read()


def get_info(patchurl):
  MaxVersion = "99.99"

  data = get_pkg_start(patchurl, 16*1024)

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
      sfo_offset, sfo_size = struct.unpack_from(">II", data, meta_offset + 8)
      break
    meta_offset += 8 + meta_size

  if sfo_offset is None:
    print(patchurl)
    print("cannot find sfo in pkg")
    return MaxVersion

  if sfo_offset + sfo_size > len(data):
    print(patchurl)
    print("sfo is not in beginning of pkg [%d..%d]" % (sfo_offset, sfo_offset + sfo_size-1))
    return MaxVersion

  sfo = parse_sfo(data[sfo_offset:sfo_offset+sfo_size])
  fw = sfo["PSP2_DISP_VER"]

  name = sfo["STITLE"] if "STITLE" in sfo else sfo["TITLE"]
  name = name.strip()

  m = re.match(r"(\d+\.\d\d).*", fw)
  return m.group(1), name


def get_supported(xml, supported = "03.60"):
  packages = list(ET.fromstring(xml).findall("./tag/package"))
  for p in reversed(packages):
    patchurl = p.attrib["url"]
    size = p.attrib["size"]
    version = p.attrib["version"]
    fw, name = get_info(patchurl)
    if fw <= supported:
      return patchurl, size, version.lstrip("0"), fw.lstrip("0"), name

  return None

def patch(title):
  xml = title2info(title)
  if xml is None:
    return 0
  else:
    supported = get_supported(xml)
    if supported is None:
      return 0
    else:
      patchurl, size, version, fw, name = supported
      return patchurl