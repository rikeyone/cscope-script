#!/usr/bin/python
# coding=utf-8
#===============================================================================
#
# This script searchs images that need to be signed by Meizu.
#
# Copyright (c) 2017-2018 Zhuhai Meizu Technologies. All Rights Reserved.
# Zhuhai Meizu Tech Co.ltd Proprietary and Confidential.
#
# Author:       xiehaocheng
# Email:        xiehaocheng@meizu.com
# Date:         2018-7-19
#===============================================================================

import os
import sys
import time
import commands
import shutil
import subprocess
import re
import xml.etree.ElementTree as ET
from optparse import OptionParser

class Binary():
    name=""
    src=""
    dest=""
    sign_id=""
    frombase=""

class SignImageFilter:
    def __init__(self, content_xml, sectool_xml, config_xml = "config.xml"):
        self.dl_file_map = {}
        self.dl_file = []
        self.file_ref_map = {}
        self.file_ref = []
        self.build_image_map = {}
        self.build_image = []
        self.sign_id_map = {}
        self.sign_image_map = {}
        self.sign_binary = []
        self.config_binary = []
        self.mismatch_list = []
        self.add_list = []
        self.remove_list = []
        self.content_xml = content_xml
        self.sectool_xml = sectool_xml
        self.config_xml = config_xml
        self.content_tree = ET.parse(self.content_xml)
        self.sectool_tree = ET.parse(self.sectool_xml)
        self.config_tree = ET.parse(self.config_xml)
        self.__parse_xmls()

    def __xml_find_parent(self, tree, path, element, children, layer=0):
        '''element is children's tag.'''
        for parent in tree.iterfind(path):
            if parent.tag == element and parent.text == children:
                return parent
            else:
                for pparent in parent.getiterator():
                    if pparent.tag == element and pparent.text == children:
                        return parent
        return None

    def __parse_download_file(self):
        for el in self.content_tree.iterfind("builds_flat/build/download_file"):
            if el.get("storage_type") != None and el.get("storage_type") != "ufs":
                continue
            if el.find("file_name").text:
                name = el.find("file_name").text
                parent = self.__xml_find_parent(self.content_tree, "builds_flat/build", "file_name", name)
                f = parent.find("linux_root_path").text + el.find("file_path").text + name
                self.dl_file_map[name] = f
                self.dl_file.append(f)
        for el in self.content_tree.iterfind("builds_flat/build/device_programmer"):
            if el.find("file_name").text:
                name = el.find("file_name").text
                parent = self.__xml_find_parent(self.content_tree, "builds_flat/build", "file_name", name)
                f = parent.find("linux_root_path").text + el.find("file_path").text + name
                self.dl_file_map[name] = f
                self.dl_file.append(f)

    def __parse_file_ref(self):
        for el in self.content_tree.iterfind("builds_flat/build/file_ref"):
            if el.find("file_name").text:
                name = el.find("file_name").text
                parent = self.__xml_find_parent(self.content_tree, "builds_flat/build", "file_name", name)
                f = parent.find("linux_root_path").text + el.find("file_path").text + name
                self.file_ref_map[name] = f
                self.file_ref.append(f)

    def __merge_build_file(self):
        self.build_image_map = dict(self.dl_file_map.items() + self.file_ref_map.items())
        self.build_image = self.dl_file + self.file_ref

    def __parse_sign_ids(self):
        for el in self.sectool_tree.iterfind("images_list/image"):
            if el.get("sign_id"):
                sign_id = el.get("sign_id")
                self.sign_id_map[sign_id] = el.get("name")

    def __parse_custom_config(self):
        for el in self.config_tree.find("sign/sign_binary"):
            cb = Binary()
            cb.name = el.get("name")
            cb.src = el.get("src")
            cb.dest = el.get("dest")
            if cb.dest == "": cb.dest = cb.src[0:cb.src.rfind("/")+1]
            cb.sign_id = el.get("sign_id")
            cb.frombase = el.get("frombase")
            self.config_binary.append(cb)

    def __parse_xmls(self):
        self.__parse_download_file()
        self.__parse_file_ref()
        self.__merge_build_file()
        self.__parse_sign_ids()
        self.__parse_custom_config()

    def search(self):
        # populate sign binary list
        for id in self.sign_id_map:
            for image in self.build_image_map:
                if self.sign_id_map[id] == image:
                    self.sign_image_map[image] = self.build_image_map[image]
                    sb = Binary()
                    sb.sign_id = id
                    sb.src = self.build_image_map[image]
                    self.sign_binary.append(sb)

        # populate add list
        for i in self.sign_binary:
            match = False
            for j in self.config_binary:
                if i.sign_id == j.sign_id:
                    match = True
                    break
            if not match:
                self.add_list.append(i)

        #populate mismatch_list
        for i in self.sign_binary:
            for j in self.config_binary:
                if i.sign_id == j.sign_id and i.src != j.src:
                    self.mismatch_list.append(i)
                    break

        # populate remove_list
        for i in self.config_binary:
            match = False
            for j in self.sign_binary:
                if i.sign_id == j.sign_id:
                    match = True
                    break
            if not match:
                self.remove_list.append(i)

    def report(self):
        print "\n" +30 * "=" + " SIGN ID " + 30 * "=" + "\n"
        for id in self.sign_id_map:
            print "%s%s" % (id.ljust(50), self.sign_id_map[id])
        print "\n" + 30 * "=" + " BUILD IMAGE " + 30 * "="
        for image in self.build_image_map:
            print "%s%s" % (image.ljust(60), self.build_image_map[image])
        print "\n" + 30 * "=" + " SUMMARY(SIGN TARGET) " + 30 * "=" + "\n"
        print "Total Num:%s\n" %(len(self.sign_image_map))
        for image in self.sign_image_map:
            print "%s%s" % (image.ljust(60), self.sign_image_map[image])
        if len(self.add_list) > 0:
            print "\n" + 30 * "=" + " ADD IMAGE " + 30 * "=" + "\n"
            print "%s%s" % (str("SIGN_ID").ljust(60), str("IMAGE PATH\n"))
            for binary in self.add_list:
                print "%s%s" % (binary.sign_id.ljust(60), binary.src)
        if len(self.remove_list) > 0:
            print "\n" + 30 * "=" + " REMOVE IMAGE " + 30 * "=" + "\n"
            print "%s%s" % (str("SIGN_ID").ljust(60), str("IMAGE PATH\n"))
            for binary in self.remove_list:
                print "%s%s" % (binary.sign_id.ljust(60), binary.src)
        if len(self.mismatch_list) > 0:
            print "\n" + 30 * "=" + " MISMATCH IMAGE " + 30 * "=" + "\n"
            print "%s%s" % (str("SIGN_ID").ljust(60), str("IMAGE PATH\n"))
            for binary in self.mismatch_list:
                print "%s%s" % (binary.sign_id.ljust(60), binary.src)

    def get_sectool_sign_id(self):
        return self.sign_id_map

    def get_build_image(self):
        return self.build_image_map

    def get_build_image_to_sign(self):
        return self.sign_image_map


def main():
    parser = OptionParser()
    parser.add_option("--content", "-c", action="store",
                      dest="content_xml", default=False, help="contents.xml file path. Eg. -c contents.xml")
    parser.add_option("--sectool", "-s", action="store",
                      dest="sectool_xml", default=False, help="sectool config .xml file path. Eg. -s sm8150_secimage.xml")
    parser.add_option("--config", "-f", action="store",
                      dest="config_xml", default=False,
                      help="custom config .xml file path. Eg. -f config.xml")
    parser.add_option("--output", "-o", action="store",
                      dest="output", default=False, help="output file Eg. -o output")
    (options, args) = parser.parse_args()
    if len(sys.argv) < 2:
        print parser.print_help()
        return 0
    if options.config_xml:
        filter = SignImageFilter(options.content_xml, options.sectool_xml, options.config_xml)
    else:
        filter = SignImageFilter(options.content_xml, options.sectool_xml)
    filter.search()
    filter.report()
    filter.get_sectool_sign_id()
    filter.get_build_image()
    filter.get_build_image_to_sign()


if __name__ == "__main__":
    sys.exit(main())
