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
from datetime import datetime
import json
import pickle

# Global Variables
# ---------------------------------------------------

cat_data  = "data"
cat_power = "power"

int_step = {}
int_step[cat_data]  = 1
int_step[cat_power] = 3600

profile_type = {}
profile_type["DATA_RATE"]   = cat_data
profile_type["DATA_VOLUME"] = cat_data
profile_type["POWER"]       = cat_power
profile_type["ENERGY"]      = cat_power

unit_conv_factor = {}

# Data Rates
unit_conv_factor["bps"] = {}
unit_conv_factor["bps"]["bps"]  = 1
unit_conv_factor["bps"]["kbps"] = 1/1000
unit_conv_factor["bps"]["mbps"] = 1/1000000
unit_conv_factor["bps"]["gbps"] = 1/1000000000

unit_conv_factor["kbps"] = {}
unit_conv_factor["kbps"]["bps"]  = 1000
unit_conv_factor["kbps"]["kbps"] = 1
unit_conv_factor["kbps"]["mbps"] = 1/1000
unit_conv_factor["kbps"]["gbps"] = 1/1000000

unit_conv_factor["mbps"] = {}
unit_conv_factor["mbps"]["bps"]  = 1000000
unit_conv_factor["mbps"]["kbps"] = 1000
unit_conv_factor["mbps"]["mbps"] = 1
unit_conv_factor["mbps"]["gbps"] = 1/1000

unit_conv_factor["gbps"] = {}
unit_conv_factor["gbps"]["bps"]  = 1000000000
unit_conv_factor["gbps"]["kbps"] = 1000000
unit_conv_factor["gbps"]["mbps"] = 1000
unit_conv_factor["gbps"]["gbps"] = 1

# Data Volume
unit_conv_factor["bits"] = {}
unit_conv_factor["bits"]["bits"]  = 1
unit_conv_factor["bits"]["kbits"] = 1/1000
unit_conv_factor["bits"]["mbits"] = 1/1000000
unit_conv_factor["bits"]["gbits"] = 1/1000000000

unit_conv_factor["kbits"] = {}
unit_conv_factor["kbits"]["bits"]  = 1000
unit_conv_factor["kbits"]["kbits"] = 1
unit_conv_factor["kbits"]["mbits"] = 1/1000
unit_conv_factor["kbits"]["gbits"] = 1/1000000

unit_conv_factor["mbits"] = {}
unit_conv_factor["mbits"]["bits"]  = 1000000
unit_conv_factor["mbits"]["kbits"] = 1000
unit_conv_factor["mbits"]["mbits"] = 1
unit_conv_factor["mbits"]["gbits"] = 1/1000

unit_conv_factor["gbits"] = {}
unit_conv_factor["gbits"]["bits"]  = 1000000000
unit_conv_factor["gbits"]["kbits"] = 1000000
unit_conv_factor["gbits"]["mbits"] = 1000
unit_conv_factor["gbits"]["gbits"] = 1

# Power
unit_conv_factor["W"] = {}
unit_conv_factor["W"]["W"]  = 1
unit_conv_factor["W"]["kW"] = 1/1000
unit_conv_factor["W"]["MW"] = 1/1000000

unit_conv_factor["kW"] = {}
unit_conv_factor["kW"]["W"]  = 1000
unit_conv_factor["kW"]["kW"] = 1
unit_conv_factor["kW"]["MW"] = 1/1000

unit_conv_factor["MW"] = {}
unit_conv_factor["MW"]["W"]  = 1000000
unit_conv_factor["MW"]["kW"] = 1000
unit_conv_factor["MW"]["MW"] = 1

# Energy
unit_conv_factor["Wh"] = {}
unit_conv_factor["Wh"]["Wh"]  = 1
unit_conv_factor["Wh"]["kWh"] = 1/1000
unit_conv_factor["Wh"]["MWh"] = 1/1000000

unit_conv_factor["kWh"] = {}
unit_conv_factor["kWh"]["Wh"]  = 1000
unit_conv_factor["kWh"]["kWh"] = 1
unit_conv_factor["kWh"]["MWh"] = 1/1000

unit_conv_factor["MWh"] = {}
unit_conv_factor["MWh"]["Wh"]  = 1000000
unit_conv_factor["MWh"]["kWh"] = 1000
unit_conv_factor["MWh"]["MWh"] = 1

unit_rates_to_volume = {}

# Data
unit_rates_to_volume["bps"]  = "bits"
unit_rates_to_volume["kbps"] = "kbits"
unit_rates_to_volume["mbps"] = "mbits"
unit_rates_to_volume["gbps"] = "gbits"

# Power
unit_rates_to_volume["W"]  = "Wh"
unit_rates_to_volume["kW"] = "kWh"
unit_rates_to_volume["MW"] = "MWh"

unit_volume_to_rates = {}

# Data
unit_volume_to_rates["bits" ] = "bps" 
unit_volume_to_rates["kbits"] = "kbps"
unit_volume_to_rates["mbits"] = "mbps"
unit_volume_to_rates["gbits"] = "gbps"

# Power
unit_volume_to_rates["Wh" ] = "W" 
unit_volume_to_rates["kWh"] = "kW"
unit_volume_to_rates["MWh"] = "MW"

# Simphony to MAPPS unit conversion
unit_simph_to_mapps = {}
unit_simph_to_mapps["bits"]  = "bits"
unit_simph_to_mapps["kbits"] = "kbits"
unit_simph_to_mapps["mbits"] = "Mbits"
unit_simph_to_mapps["gbits"] = "Gbits"

unit_simph_to_mapps["bps"]  = "bits/s"
unit_simph_to_mapps["kbps"] = "Kbits/s"
unit_simph_to_mapps["mbps"] = "Mbits/s"
unit_simph_to_mapps["gbps"] = "Gibits/s"

unit_simph_to_mapps["W"]  = "W"
unit_simph_to_mapps["kW"] = "W"
unit_simph_to_mapps["MW"] = "W"

unit_simph_to_mapps["Wh"]  = "Wh"
unit_simph_to_mapps["kWh"] = "kWh"
unit_simph_to_mapps["MWh"] = "MWh"

# ---------------------------------------------------

class res_value(object):
   def __init__(self, value, unit):
      self.value = value
      self.unit  = unit

class resource_entry(object):
    def __init__(self):
       self.time = 0
       self.instant     = res_value(0.0, "kbps")
       self.volume      = res_value(0.0, "kbits")
       self.accumulated = res_value(0.0, "kbits")

class resource_unit(object):
   def __init__(self, rates_unit, volume_unit, acc_unit):
      self.rates  = rates_unit
      self.volume = volume_unit
      self.acc    = acc_unit

class resource_profile(object):
    def __init__(self, category, unit):
       self.unit       = unit
       self.category   = category
       self.start_time = 0
       self.end_time   = 0
       self.res_profile = []

    def append_profile_instant_value(self, time, value):
       entry = resource_entry()
       entry.time    = time
       entry.instant.unit  = self.unit.rates
       entry.instant.value = value.value * unit_conv_factor[value.unit][self.unit.rates]

       # Check if the profile is empty
       if not self.res_profile:
          self.start_time   = time
          self.end_time     = time
          entry.volume      = res_value(0.0, "kbits")
          entry.accumulated = res_value(0.0, "kbits")
       else:
          last_entry = self.res_profile[-1]

          # If time is not greather than last entry profile
          if time <= last_entry.time: 
             self.res_profile.pop(-1)
             if not self.res_profile:
                self.start_time   = time
                self.end_time     = time
                entry.volume      = res_value(0.0, "kbits")
                entry.accumulated = res_value(0.0, "kbits")
             else:
                last_entry = self.res_profile[-1]

          # Update the end time and calculate volumes
          self.end_time      = time
          rate_volume_unit   = unit_rates_to_volume[last_entry.instant.unit]
          entry.volume.unit  = self.unit.volume
          vol_unit_factor    = unit_conv_factor[rate_volume_unit][self.unit.volume]
          entry.volume.value = (time - last_entry.time).total_seconds() / int_step[self.category] * last_entry.instant.value * vol_unit_factor
          entry.accumulated.unit  = self.unit.acc
          acc_unit_factor         = unit_conv_factor[entry.volume.unit][self.unit.acc]
          entry.accumulated.value = (last_entry.accumulated.value + entry.volume.value) * acc_unit_factor

       # Append entry
       self.res_profile.append(entry)

    def get_value(self, time):
       time_entry = resource_entry()
       if time < self.start_time:
          time_entry.time = time
          return time_entry
       
       for entry in self.res_profile:
          if time < entry.time:
             time_entry.instant.value = prev_value
             rate_volume_unit         = unit_rates_to_volume[time_entry.instant.unit]
             time_entry.volume.unit   = unit_conv_factor[rate_volume_unit][self.unit.volume]
             time_entry.volume.value  = (time - prev_time).total_seconds() / int_step[self.category] * time_entry.value
             time_entry.accumulated.unit  = unit_conv_factor[time_entry.volume.unit][self.unit.acc]
             time_entry.accumulated.value = prev_acc.value + time_entry.volume.value
             break
          prev_time  = entry.time
          prev_value = entry.value
          prev_acc   = entry.accumulated

       return time_entry

class timeline_resources(object):
   def __init__(self):
     self.inst_profile = {}
     self.inst_profile[cat_data]  = {}
     self.inst_profile[cat_power] = {}
     
     self.inst_type_profile = {}
     self.inst_type_profile[cat_data]  = {}
     self.inst_type_profile[cat_power] = {}

     self.ins_type_list      = {}
     self.inst_group_map     = {}
     self.defs_config        = self.getDefinitionsConfig()

   def initResourceProfiles(self):
        data_prof_unit  = resource_unit("kbps", "kbits", "kbits")
        power_prof_unit = resource_unit("W", "Wh", "Wh")

        for inst_type_defs in self.defs_config["instrument_types"]:
            self.inst_type_profile[cat_data][inst_type_defs["mnemonic"]]  = resource_profile(cat_data,  data_prof_unit)
            self.inst_type_profile[cat_power][inst_type_defs["mnemonic"]] = resource_profile(cat_power, power_prof_unit)

        for inst_defs in self.defs_config["instruments"]:
            self.inst_profile[cat_data][inst_defs["mnemonic"]]  = resource_profile(cat_data, data_prof_unit)
            self.inst_profile[cat_power][inst_defs["mnemonic"]] = resource_profile(cat_power, power_prof_unit)

   def getInstrumentTypeDefs(self):
        json_string = """{
        "instrument_types": [
             {
               "name": "Geophysics",
               "mnemonic": "GEOPHYSICS",
               "instrument_set": [
                 "3GM",
                 "GALA",
                 "RIME"
               ]
             },
             {
               "name": "Remote Sensing",
               "mnemonic": "REMOTE_SENSING",
               "instrument_set": [
                 "JANUS",
                 "MAJIS",
                 "UVS"
               ]
             },
             {
               "name": "In-Situ",
               "mnemonic": "IN_SITU",
               "instrument_set": [
                 "JMAG",
                 "PEPHI",
                 "PEPLO",                 
                 "PRIDE",
                 "RADEM",
                 "RPWI",
                 "SWI"
               ]
             },
             {
               "name": "Navigation",
               "mnemonic": "NAVIGATION",
               "instrument_set": [
                 "JMC",
                 "NAVCAM"
               ]
             }
           ]}"""
        return json.loads(json_string)
      
   def getInstruments(self):
        json_string = """{
        "instruments": [
               {
                 "name": "3GM",
                 "mnemonic": "3GM"
               },
               {
                 "name": "GALA",
                 "mnemonic": "GALA"
               },
               {
                 "name": "JANUS",
                 "mnemonic": "JANUS"
               },
               {
                 "name": "JMAG",
                 "mnemonic": "JMAG"
               },
               {
                 "name": "JMC",
                 "mnemonic": "JMC"
               },
               {
                 "name": "MAJIS",
                 "mnemonic": "MAJIS"
               },
               {
                 "name": "NAVCAM",
                 "mnemonic": "NAVCAM"
               },
               {
                 "name": "PEPHI",
                 "mnemonic": "PEPHI"
               },
               {
                 "name": "PEPLO",
                 "mnemonic": "PEPLO"
               },               
               {
                 "name": "PRIDE",
                 "mnemonic": "PRIDE"
               },
               {
                 "name": "RADEM",
                 "mnemonic": "RADEM"
               },
               {
                 "name": "RIME",
                 "mnemonic": "RIME"
               },
               {
                 "name": "RPWI",
                 "mnemonic": "RPWI"
               },
               {
                 "name": "SWI",
                 "mnemonic": "SWI"
               },
               {
                 "name": "UVS",
                 "mnemonic": "UVS"
               }
             ]}"""
        return json.loads(json_string)

   def getDefinitionsConfig(self):
        json_string = """{
        "targets": [
          {
            "name": "Ring and satellites",
            "mnemonic": "RING_AND_SATELLITES"
          },
          {
            "name": "Plasma",
            "mnemonic": "PLASMA"
          },
          {
            "name": "Callisto",
            "mnemonic": "CALLISTO"
          },
          {
            "name": "Europa",
            "mnemonic": "EUROPA"
          },
          {
            "name": "Ganymede",
            "mnemonic": "GANYMEDE"
          },
          {
            "name": "Jupiter atmosphere",
            "mnemonic": "JUPITER_ATMOSPHERE"
          },
          {
            "name": "Navigation",
            "mnemonic": "NAVIGATION"
          }
        ],
        "instruments": [
          {
            "name": "3GM",
            "mnemonic": "3GM"
          },
          {
            "name": "GALA",
            "mnemonic": "GALA"
          },
          {
            "name": "JANUS",
            "mnemonic": "JANUS"
          },
          {
            "name": "JMAG",
            "mnemonic": "JMAG"
          },
          {
            "name": "JMC",
            "mnemonic": "JMC"
          },
          {
            "name": "MAJIS",
            "mnemonic": "MAJIS"
          },
          {
            "name": "NAVCAM",
            "mnemonic": "NAVCAM"
          },
          {
            "name": "PEPHI",
            "mnemonic": "PEPHI"
          },
          {
            "name": "PEPLO",
            "mnemonic": "PEPLO"
          },          
          {
            "name": "PRIDE",
            "mnemonic": "PRIDE"
          },
          {
            "name": "RADEM",
            "mnemonic": "RADEM"
          },
          {
            "name": "RIME",
            "mnemonic": "RIME"
          },
          {
            "name": "RPWI",
            "mnemonic": "RPWI"
          },
          {
            "name": "SWI",
            "mnemonic": "SWI"
          },
          {
            "name": "UVS",
            "mnemonic": "UVS"
          }
        ],
        "units": [
          {
            "name": "bits per second",
            "mnemonic": "bps",
            "category": "DATA_RATE"
          },
          {
            "name": "kilobits per second",
            "mnemonic": "kbps",
            "category": "DATA_RATE"
          },
          {
            "name": "megabits per second",
            "mnemonic": "mbps",
            "category": "DATA_RATE"
          },
          {
            "name": "bits",
            "mnemonic": "bits",
            "category": "DATA_VOLUME"
          },
          {
            "name": "kilobits",
            "mnemonic": "kbits",
            "category": "DATA_VOLUME"
          },
          {
            "name": "megabits",
            "mnemonic": "mbits",
            "category": "DATA_VOLUME"
          },
          {
            "name": "gigabits",
            "mnemonic": "gbits",
            "category": "DATA_VOLUME"
          },
          {
            "name": "Watts",
            "mnemonic": "W",
            "category": "POWER"
          },
          {
            "name": "kilo Watts",
            "mnemonic": "kW",
            "category": "POWER"
          },
          {
            "name": "watt hour",
            "mnemonic": "Wh",
            "category": "ENERGY"
          },
          {
            "name": "kilowatt hour",
            "mnemonic": "kWh",
            "category": "ENERGY"
          }
        ],
        "instrument_types": [
          {
            "name": "Geophysics",
            "mnemonic": "GEOPHYSICS",
            "instrument_set": [
              "3GM",
              "GALA",
              "PRIDE",
              "RIME"
            ]
          },
          {
            "name": "Remote Sensing",
            "mnemonic": "REMOTE_SENSING",
            "instrument_set": [
              "JANUS",
              "MAJIS",
              "SWI",
              "UVS"
            ]
          },
          {
            "name": "In-Situ",
            "mnemonic": "IN_SITU",
            "instrument_set": [
              "JMAG",
              "PEP",
              "RADEM",
              "RPWI"
            ]
          },
          {
            "name": "Navigation",
            "mnemonic": "NAVIGATION",
            "instrument_set": [
              "JMC",
              "NAVCAM"
            ]
          }
        ],
        "resource_categories": [
          {
            "name": "Data rate",
            "mnemonic": "DATA_RATE",
            "category_type": "data"
          },
          {
            "name": "Data volume",
            "mnemonic": "DATA_VOLUME",
            "category_type": "data"
          },
          {
            "name": "Power",
            "mnemonic": "POWER",
            "category_type": "power"
          },
          {
            "name": "Energy",
            "mnemonic": "ENERGY",
            "category_type": "power"
          }
        ],
        "slew_policies": [
          {
            "name": "FLEXIBLE_BLOCK",
            "mnemonic": "FLEXIBLE_BLOCK"
          },
          {
            "name": "KEEP_BLOCK",
            "mnemonic": "KEEP_BLOCK"
          },
          {
            "name": "KEEP_START",
            "mnemonic": "KEEP_START"
          },
          {
            "name": "KEEP_END",
            "mnemonic": "KEEP_END"
          }
        ],
        "timelines": [
          {
            "name": "Prime",
            "mnemonic": "PRIME"
          },
          {
            "name": "Generic",
            "mnemonic": "GENERIC"
          },
          {
            "name": "Working Group 1",
            "mnemonic": "WG1"
          },
          {
            "name": "Working Group 2",
            "mnemonic": "WG2"
          },
          {
            "name": "Working Group 3",
            "mnemonic": "WG3"
          },
          {
            "name": "Working Group 4",
            "mnemonic": "WG4"
          },
          {
            "name": "Working Group X",
            "mnemonic": "WGX"
          },
          {
            "name": "Local",
            "mnemonic": "LOCAL"
          }
        ],
        "platform_power_profiles": [
          {
            "name": "NOMINAL",
            "mnemonic": "NOMINAL",
            "power": 400
          },
          {
            "name": "DOWNLINK",
            "mnemonic": "DOWNLINK",
            "power": 580
          },
          {
            "name": "FLYBY",
            "mnemonic": "FLYBY",
            "power": 450
          },
          {
            "name": "ECLIPSE",
            "mnemonic": "ECLIPSE",
            "power": 300
          },
          {
            "name": "JOI",
            "mnemonic": "JOI",
            "power": 300
          }
        ],
        "version": "0.0.0"
      }"""
        return json.loads(json_string)

   def buildConfigMap(self):

      # Build instrument type list
      self.ins_type_list = {}
      for inst_type in self.defs_config["instrument_types"]:
         self.ins_type_list[inst_type["mnemonic"]] = inst_type

      # Build instrument group
      for inst in self.defs_config["instruments"]:

         self.inst_group_map[inst["mnemonic"]] = inst
         self.inst_group_map[inst["mnemonic"]]["groupList"] = []
         
         for instType in self.defs_config["instrument_types"]:
            for typeInst in instType["instrument_set"]:
                if inst["mnemonic"] == typeInst:
                    self.inst_group_map[inst["mnemonic"]]["groupList"].append(instType["mnemonic"])

   def calculate_inst_type_profile_resources(self, segment_definition, segment_instance):
      resource_list = []

      # If overwritten flag is set to true the resources
      # defined in the segment instance will overwrite completely
      # the resource defined in the segment definition
      if segment_instance["overwritten"]:
          resource_list = segment_instance["resources"]
      elif ("resources" in segment_definition):
          resource_list = segment_definition["resources"]
                        
      inst_type_map = {}
      for inst in self.defs_config["instruments"]:
         if not inst["mnemonic"] in inst_type_map: 
            inst_type_map[inst["mnemonic"]] = ""

      for resource_instance in resource_list:
         entry_time = segment_instance["startDatetime"] #datetime.strptime(segment_instance["start"],"%Y-%m-%dT%H:%M:%S.000Z")
         entry_profile_type = profile_type[resource_instance["category"]]
         if resource_instance["category"] == "DATA_VOLUME" or resource_instance["category"] == "ENERGY":
            segment_duration = (segment_instance["origEndDatetime"] - segment_instance["origStartDatetime"]).total_seconds()
            res_val = resource_instance["value"] / segment_duration / int_step[entry_profile_type]
            res_unit = unit_volume_to_rates[resource_instance["unit"]]
            entry_instant_res_value = res_value(res_val, res_unit)
         else:
            res_unit = resource_instance["unit"]
            entry_instant_res_value = res_value(resource_instance["value"], resource_instance["unit"])
         inst_type_profile_list = self.inst_type_profile[entry_profile_type][resource_instance["instrument_type"]]
         inst_type_profile_list.append_profile_instant_value(entry_time, entry_instant_res_value)
         
         entry_time = segment_instance["endDatetime"] #datetime.strptime(segment_instance["end"],"%Y-%m-%dT%H:%M:%S.000Z")
         entry_instant_res_value = res_value(0.0,res_unit)
         inst_type_profile_list.append_profile_instant_value(entry_time, entry_instant_res_value)

         # Build instrument/instrument type map
         for inst in self.ins_type_list[resource_instance["instrument_type"]]["instrument_set"]:
             if inst in inst_type_map:
                 if inst_type_map[inst] == "":
                      inst_type_map[inst] = resource_instance["target"]
             else: inst_type_map[inst] = resource_instance["target"]
         for inst in self.defs_config["instruments"]:
             if not inst["mnemonic"] in inst_type_map:
                 inst_type_map[inst["mnemonic"]] = ""
      segment_instance["instTypeMap"] = inst_type_map

   
   def calculate_inst_profile_resources(self, segment_definition, segment_instance):
      resource_list = []

      # If overwritten flag is set to true the resources
      # defined in the segment instance will overwrite completely
      # the resource defined in the segment definition
      if segment_instance["instrument_overwritten"]:
          resource_list = segment_instance["instrument_resources"]
      elif ("instrument_resources" in segment_definition):
          resource_list = segment_definition["instrument_resources"]

      for resource_instance in resource_list:
         entry_time = segment_instance["startDatetime"] # datetime.strptime(segment_instance["start"],"%Y-%m-%dT%H:%M:%S.000Z")
         entry_profile_type = profile_type[resource_instance["category"]]

         if resource_instance["category"] == "DATA_VOLUME" or resource_instance["category"] == "ENERGY":
            segment_duration = (segment_instance["origEndDatetime"] - segment_instance["origStartDatetime"]).total_seconds()
            #segment_duration = (datetime.strptime(segment_instance["end"],"%Y-%m-%dT%H:%M:%S.000Z") - datetime.strptime(segment_instance["start"],"%Y-%m-%dT%H:%M:%S.000Z")).total_seconds()
            res_val   = resource_instance["value"] / segment_duration / int_step[entry_profile_type]
            res_unit  = unit_volume_to_rates[resource_instance["unit"]]
            entry_instant_res_value = res_value(res_val, res_unit)
         else:
            res_unit = resource_instance["unit"]
            entry_instant_res_value = res_value(resource_instance["value"], res_unit)

         inst_profile_list = self.inst_profile[entry_profile_type][resource_instance["instrument"]]
         inst_profile_list.append_profile_instant_value(entry_time, entry_instant_res_value)
         
         entry_time = segment_instance["endDatetime"] # datetime.strptime(segment_instance["end"],"%Y-%m-%dT%H:%M:%S.000Z")
         entry_instant_res_value = res_value(0.0, res_unit)
         inst_profile_list.append_profile_instant_value(entry_time, entry_instant_res_value)
      
   def generate_profiles(self, segment_definitions, segment_timeline):
      self.segment_timeline    = segment_timeline
      self.segment_definitions = segment_definitions

      self.buildConfigMap()
      self.initResourceProfiles()

      # Extract the profiles from the segments timeline
      # ------------------------------------------------

      for seg_cnt in range(len(self.segment_timeline["segment_timeline"])):

            # Save segment instance
            segment_instance = self.segment_timeline["segment_timeline"][seg_cnt]
            self.segment_timeline["segment_timeline"][seg_cnt]["inst_type_map"] = {}

            # Get segment definition
            # If the segment definition doesn't exist skip
            if segment_instance["segment_definition"] in self.segment_definitions["scenario"]["list"]:
               segment_definition = self.segment_definitions["scenario"]["list"][segment_instance["segment_definition"]]
            elif segment_instance["segment_definition"] in self.segment_definitions["trajectory"]["list"]:
               segment_definition = self.segment_definitions["trajectory"]["list"][segment_instance["segment_definition"]]
            else:
               continue

            # --------------------
            # Calculate resources
            # --------------------
            self.calculate_inst_type_profile_resources(segment_definition, segment_instance)
            self.calculate_inst_profile_resources(segment_definition, segment_instance)




if __name__ == "__main__":
   t_res = timeline_resources()
   t_res.buildConfigMap()

   with open(R'Z:\VALIDATION\simphony\pcm\profiles\phs_pcm_test_006\inputs\timeline.json') as json_file:
      seg_timeline = json.load(json_file)
   with open(R'Z:\VALIDATION\simphony\pcm\profiles\phs_pcm_test_006\inputs\segment_definitions.json') as json_file:
      seg_definitions = json.load(json_file)

   t_res.generate_profiles(seg_definitions, seg_timeline)

   #json_t_res = json.dumps(t_res.__dict__)
   #print(json_t_res)

   #with open(R'Z:\Resources\data.txt', 'w') as outfile:
   #   json.dump(self.instTypeProfile, outfile, indent=4, default=str)
   a = 1

   #res_profile = resource_profile(profile_type["POWER"],"test")
   #time = datetime.fromisoformat("2020-01-10T00:10:00")
   #res_profile.append_profile_value(time,10)
   #
   #time = datetime.fromisoformat("2020-01-10T01:30:00")
   #res_profile.append_profile_value(time,20)
   #
   #time = datetime.fromisoformat("2020-01-10T01:10:00")
   #res_profile.append_profile_value(time,10)
   #
   #profile = res_profile.get_value(datetime.fromisoformat("2020-01-10T00:10:00")) 
   #
   #
   #res_profile = resource_profile(profile_type["DATA_VOLUME"],"test")
   #time = datetime.fromisoformat("2020-01-10T00:10:00")
   #res_profile.append_profile_value(time,10)
   #
   #time = datetime.fromisoformat("2020-01-10T00:11:00")
   #res_profile.append_profile_value(time,20)
   #
   #time = datetime.fromisoformat("2020-01-10T00:12:00")
   #res_profile.append_profile_value(time,10)
