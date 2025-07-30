#!/bin/python3

# Copyright 2025, A Baldwin
#
# This file is part of libifcb.
#
# libifcb is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# libifcb is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with libifcb.  If not, see <http://www.gnu.org/licenses/>.

'''
sample.py

An interface for image data from the IFCB sensor
'''

import argparse
import os
import re
import csv
import struct
import json
from PIL import Image
import numpy as np
from .utils import to_snake_case

class TriggerEvent:
    def __init__(self, raw, rois, index):
        self.raw = raw
        self.rois = rois
        self.index = index

class ROI:
    def __init__(self, trigger_list, roi_fp, fp_offset, w, h, x, y, index, trigger_index):
        self.__trigger_list = trigger_list
        self.__roi_fp = roi_fp
        self.__fp_offset = fp_offset
        self.x = x
        self.y = y
        self.width = w
        self.height = h
        self.index = index
        self.trigger_index = trigger_index

    def __get_image(self):
        if self.__roi_fp is None:
            return None
        self.__roi_fp.seek(self.__fp_offset)
        imdata = self.__roi_fp.read(self.width * self.height)
        imdata_reform = np.reshape(np.frombuffer(imdata, dtype=np.uint8), (self.height, self.width))
        image = Image.fromarray(imdata_reform, "L")
        return image

    def __get_trigger(self):
        if self.__trigger_list is None:
            return None
        return self.__trigger_list[self.trigger_index]

    image = property(
            fget = __get_image,
            doc = "Dynamically generated image object"
        )

    trigger = property(
            fget = __get_trigger,
            doc = "Dynamically get trigger object"
        )

class ROIReader:
    # header = {}
    # adc_data = []
    # __adc_format_map = {}
    __close_adc = False
    __close_roi = False

    def __to_snake_case_ifcb_preprocess(self, str_in):
        # A quick fix for some questionable variable naming from old IFCB models
        str_inter = str_in.replace("MCC", "MCC_")
        str_inter = str_inter.replace("ROI", "ROI_")
        str_inter = str_inter.replace("ADC", "ADC_")
        str_inter = str_inter.replace("DAC", "DAC_")
        str_inter = str_inter.replace("DAQ", "DAQ_")
        str_inter = str_inter.replace("PMT", "PMT_")
        str_inter = str_inter.replace("TCP", "TCP_")
        str_inter = str_inter.replace("ROI", "ROI_")
        str_inter = str_inter.replace("UV", "UV_")
        str_inter = str_inter.replace("HKTRIGGER", "HK_Trigger_")
        str_inter = str_inter.replace("grabtimestart", "Grab_Time_Start")
        str_inter = str_inter.replace("grabtimeend", "Grab_Time_End")
        str_inter = str_inter.replace("STartPoint", "Start_Point")
        str_inter = str_inter.replace("trigger", "Trigger")
        str_inter = str_inter.replace("volt", "Volt")
        str_inter = str_inter.replace("high", "High")
        str_inter = str_inter.replace("grow", "Grow")
        return to_snake_case(str_inter)

    def __header_file_to_dict(self, lines):
        o_dict = {}
        for line in lines:
            m = re.search("^([^:]+):\\s?", line)
            if m is not None: # Only needed for very old IFCB data that might be mangled
                key = self.__to_snake_case_ifcb_preprocess(m.group(1))
                value = line[len(m.group(0)):]
                o_dict[key] = value.rstrip()
        return o_dict

    def __init__(self, hdr_fp, adc_fp, roi_fp):
        close_hdr = False
        if type(hdr_fp) == str:
            hdr_fp = open(hdr_fp, "r")
            close_hdr = True
        if type(adc_fp) == str:
            adc_fp = open(adc_fp, "r")
            close_adc = True
        if type(roi_fp) == str:
            roi_fp = open(roi_fp, "rb")
            self.__close_roi = True
        self.__roi_fp = roi_fp

        header_lines = hdr_fp.readlines()
        if close_hdr:
            hdr_fp.close()
        self.header = self.__header_file_to_dict(header_lines)
        self.__adc_format_map = list(csv.reader([self.header["adc_file_format"]], skipinitialspace=True))[0]

        self.adc_data = []
        reader = csv.DictReader(adc_fp, fieldnames=self.__adc_format_map, skipinitialspace=True)
        for row in reader:
            adc_data_row = {}
            for key in row:
                adc_data_row[self.__to_snake_case_ifcb_preprocess(key)] = row[key]
            self.adc_data.append(adc_data_row)
        if close_adc:
            hdr_fp.close()

        trigger_list = {}
        self.rows = []
        self.rois = []
        self.triggers = []
        roi_index = 1
        for adc_row in self.adc_data:
            tn = adc_row["trigger_number"]
            if tn not in trigger_list:
                trigger_list[tn] = {}
                trigger_list[tn]["rois"] = []
            trigger_list[tn]["raw_properties"] = adc_row
            if int(adc_row["roi_x"]) != 0:
                roi_def = ROI(self.triggers, roi_fp, int(adc_row["start_byte"]),int(adc_row["roi_width"]),int(adc_row["roi_height"]),int(adc_row["roi_x"]),int(adc_row["roi_y"]), roi_index, int(tn))
                trigger_list[tn]["rois"].append(roi_def)
                self.rois.append(roi_def)
                self.rows.append(roi_def)
            else:
                self.rows.append(ROI(self.triggers, None, 0, 0, 0, 0, 0, roi_index, int(tn)))
            roi_index += 1

        for trigger_idx in trigger_list.keys():
            trigger_def = trigger_list[trigger_idx]
            te = TriggerEvent(trigger_def["raw_properties"], trigger_def["rois"], int(trigger_idx))
            self.triggers.append(te)
