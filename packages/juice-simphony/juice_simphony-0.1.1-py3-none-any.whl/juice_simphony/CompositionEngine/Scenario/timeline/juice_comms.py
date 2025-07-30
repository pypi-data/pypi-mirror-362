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
import re
from juice_simphony.CompositionEngine.Scenario.common.fileHandleTml import fileHandleTml


class juice_comms(fileHandleTml):

    def __init__(self, path, exp_name, params=0):
        self.params = {}
        if params != 0:
            self.params.update(params)
        self.path = path
        self.rootPath = path
        self.exp_name = exp_name
        self.params["prefix"] = "ITL"
        self.params["type"] = self.exp_name
        self.params["desc"] = "COMMS"
        self.params["version"] = "SXXPYY"
        self.params["ext"] = "itl"
        self.fileName = ""
        self.template = 0
        self.writeVersion = False
        self.writeTimeWindow = False
        fileHandleTml.__init__(self, path)



    def generate_comms_text(self, input_file):
        pattern = re.compile(r'\(COUNT=(\d+)\)')
        counts = []

        # Step 1: Extract unique COUNT values
        with open(input_file, 'r') as f:
            for line in f:
                match = pattern.search(line)
                if match:
                    count = int(match.group(1))
                    if count not in counts:
                        counts.append(count)

        # Step 2: Define the template
        template = [
            "MAL_DL_START    (COUNT={count}) JUICE OBS_START  X_HGA_DOWNLINK",
            "MAL_DL_20_START (COUNT={count}) JUICE OBS_END    X_HGA_DOWNLINK",
            "MAL_DL_20_START (COUNT={count}) JUICE OBS_START  X_KA_HGA_DOWNLINK",
            "MAL_DL_20_END   (COUNT={count}) JUICE OBS_END    X_KA_HGA_DOWNLINK",
            "MAL_DL_20_END   (COUNT={count}) JUICE OBS_START  X_HGA_DOWNLINK",
            "MAL_DL_END      (COUNT={count}) JUICE OBS_END    X_HGA_DOWNLINK"
        ]

        # Step 3: Assemble lines into a single string
        output_lines = []
        for count in sorted(counts):
            for line in template:
                output_lines.append(line.format(count=count))
            output_lines.append("")  # Blank line between blocks

        return '\n'.join(output_lines)

    def writeTimelineHeader(self, writeVersion, writeTimeWindow):
        self.writeHeader(self.params["scenarioID"], "JUICE COMMS TIMELINE")
        self.insertEmptyLine()

        if writeVersion == True:
            self.insertVersion()
            self.insertEmptyLine()

        if writeTimeWindow == True:
            self.insertTimeWindow(self.params["timeline"]["startTime"], self.params["timeline"]["endTime"])

    def writeContent(self):
        self.writeTimelineHeader(self.writeVersion, self.writeTimeWindow)
        scenario_id = self.params["scenario_id"]
        downlink_file = f"EVT_{scenario_id}_DOWNLINK.evf"
        input_file = os.path.join(self.rootPath, "../ENVIRONMENT/EVENTS/GEOMETRY", downlink_file)
        comms_text = self.generate_comms_text(input_file)
        for line in comms_text.splitlines():
            self.insertLine(line)
