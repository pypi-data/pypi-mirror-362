# *************************************************************************** #
# This file is subject to the terms and conditions defined in the             #
# file 'LICENSE.txt', which is part of this source code package.              #
#                                                                             #
# No part of the package, including this file, may be copied, modified,       #
# propagated, or distributed except according to the terms contained in       #
# the file 'LICENSE.txt'.                                                     #
#                                                                             #
# (C) Copyright European Space Agency, 2025                                   #
# *************************************************************************** #
from jinja2 import Template
import os
from datetime import datetime
from xml.etree import ElementTree as et
import xml.etree.cElementTree as etree
from xml.dom import minidom
from copy import deepcopy

from juice_simphony.CompositionEngine.Scenario.common.fileHandleEps1 import fileHandleEps1
from juice_simphony.CompositionEngine.Scenario.common.fileName import fileName
from juice_simphony.CompositionEngine.Scenario.common.fileHandleXML import fileHandleXML

class xml_attitude(fileHandleXML):

    def __init__(self, path, xml_att_struct, params = 0):
        self.params = {}
        if params!=0: 
            self.params.update(params)
        self.path       = path
        self.rootPath   = path
        self.xml_att_struct = xml_att_struct
        self.params["prefix"]  = "PTR"
        self.params["type"]    = "SOC"
        self.params["desc"]    = ""
        self.params["version"] = "SXXPYY"
        self.params["ext"]     = "ptx"
        self.fileName  = ""
        self.template  = 0
        self.startTime = self.params["startTime"]
        self.endTime   = self.params["endTime"]
        self.time_format = "%Y-%m-%dT%H:%M:%S"
        fileName.__init__(self, self.params)

    def indent(self, elem, level=0):
        i = "\n" + level*"  "
        j = "\n" + (level-1)*"  "
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = i + "  "
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
            for subelem in elem:
                self.indent(subelem, level+1)
            if not elem.tail or not elem.tail.strip():
                elem.tail = j
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = j
        return elem    

    def writeTimelineHeader(self):
        self.writeHeader(self.params["scenarioID"], "JUICE SEGMENTATION ATTITUDE")
        #comment = etree.Comment(' === Some Comment === ')
        #root.insert(1, comment)  # 1 is the index where comment is inserted
        self.insertEmptyLine()

    def write_xml_body(self):
        #print (etree.tostring(self.xml_filtered_att, encoding='utf8', method='xml'))
        #self.indent(self.xml_filtered_att)
        xmlstr = minidom.parseString(etree.tostring(self.xml_filtered_att,encoding="unicode")).toprettyxml(indent = "   ")
        line_list = [s for s in xmlstr.splitlines() if s.strip("\r\n").strip()]
        xmlstr = os.linesep.join(line_list)
        # COMMENTED by PE
        #print(xmlstr)
        self.fileHdl.write(xmlstr)
#       et.indent(self.xml_filtered_att, space='    ', level=0)
#       self.fileHdl.write(et.tostring(self.xml_filtered_att,encoding="unicode"))

    def writeContent(self):
        self.writeTimelineHeader()
        self.xml_filtered_att = self.filterPtr(self.xml_att_struct, self.startTime, self.endTime)
        self.write_xml_body()

    def filterPtr(self, xml_struct_att, start_time, end_time, cut_block = True):
        start_time_dt = datetime.strptime(start_time, self.time_format)
        end_time_dt   = datetime.strptime(end_time,   self.time_format)

        # Get timeline node
        timeline = next(xml_struct_att.iter("timeline"))
        xml_block_list = list(xml_struct_att.iter("block"))
        xml_block_list_out = []
        #xml_block_list_len = len(xml_block_list)
        num_of_filtered_blocks = 0
        for index,xml_block in enumerate(xml_block_list):
            if (xml_block.attrib["ref"] == "SLEW"): continue
            # xml_seg = next(xml_block.iter("segmentation"), None)
            # if not xml_seg == None:
            xml_seg_start_time_dt = datetime.strptime(xml_block.find('startTime').text.strip(), self.time_format)
            xml_seg_end_time_dt   = datetime.strptime(xml_block.find('endTime').text.strip(),   self.time_format)
            intersect, cutted_block, xml_cut_start_time_dt, xml_cut_end_time_dt = self.intersectTimeRange(start_time_dt, end_time_dt, xml_seg_start_time_dt, xml_seg_end_time_dt, cut_block)
            if intersect:
                if num_of_filtered_blocks >= 1:
                    if xml_block_list[index-1].attrib["ref"] == "SLEW":
                        xml_block_list_out.append(xml_block_list[index-1])
                num_of_filtered_blocks = num_of_filtered_blocks + 1
                if cutted_block:
                    xml_block_start_time = next(xml_block.iter("startTime"), None)
                    if not xml_block_start_time == None: 
                        xml_block_start_time.text  = datetime.strftime(xml_cut_start_time_dt, "%Y-%m-%dT%H:%M:%S")
                    xml_block_end_time = next(xml_block.iter("endTime"), None)
                    if not xml_block_end_time == None: 
                        xml_block_end_time.text = datetime.strftime(xml_cut_end_time_dt, "%Y-%m-%dT%H:%M:%S")
                xml_block_list_out.append(xml_block)
                last_block_end_time = xml_cut_end_time_dt
        last_block = xml_block_list_out[-1]
        xml_block_end_time = next(last_block.iter("endTime"), None)
        if not xml_block_end_time == None: 
           xml_block_end_time.text = datetime.strftime(last_block_end_time, "%Y-%m-%dT%H:%M:%S")
        else:
            end_time_el = et.Element("endTime")
            end_time_el.text = datetime.strftime(last_block_end_time, "%Y-%m-%dT%H:%M:%S")
            last_block.append(end_time_el)
        timeline.clear()
        timeline.attrib["frame"] = "SC";
        timeline.extend(xml_block_list_out)

        return xml_struct_att

    def intersectTimeRange(self, startTime, endTime, xml_seg_start_time, xml_seg_end_time, cut_block = True):
        cutted_block = False
        if endTime <= xml_seg_start_time: # st et xml_st xml_et
            return (False, cutted_block, xml_seg_start_time, xml_seg_end_time)
        else: 
            if xml_seg_end_time <= startTime: # xml_st xml_et st et 
              return (False, cutted_block, xml_seg_start_time, xml_seg_end_time)
            else: 
                if cut_block:
                   if endTime < xml_seg_end_time:  # xml_st et xml_et
                      # Cut block end time
                      xml_seg_end_time = endTime
                      cutted_block = True
                   if startTime > xml_seg_start_time:  # xml_st st xml_et
                      # Cut block start time
                      xml_seg_start_time = startTime
                      cutted_block = True
                return (True, cutted_block, xml_seg_start_time, xml_seg_end_time)

if __name__ == "__main__":
    xml_doc = et.parse(R"Z:\VALIDATION\simphony\pcm\phs_pcm_test_004\input\TMP\CREMA_5_0.xml")
    root = xml_doc.getroot()

    params = {}
    params["scenarioID"] = "SJS0003C30A"
    params["startTime"]  = "2032-09-01T01:00:00"
    params["endTime"]    = "2032-09-28T08:00:00"
    #xml_att_file = xml_attitude(path="Z:\VALIDATION\simphony\pcm\phs_pcm_test_001\scenario_generator\output", xml_att_struct=xml_doc.getroot(), params=params)
    #xml_att_file.genFile()