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
import requests
from requests.exceptions import HTTPError
import json
import urllib

class shtRestClient(object):
    def __init__(self, server):
        self.httpServer   = server
        self.baselineLink = self.httpServer + "/" + "rest_api"
        self.reqHeader = dict()
        #return super().__init__(*args, **kwargs)

    def setApiKey(self, key):
        self.apikey = key
        self.reqHeader['Authorization'] = 'JWT ' + self.apikey

    def postJson(self, command, json_post, header):
        if header:
            headerParams = self.reqHeader
        else:
            headerParams = ""

        try:
           response = requests.post(self.baselineLink + "/" + command, 
                                   headers=headerParams, json=json_post)
           response.raise_for_status()
        except HTTPError as http_err:
           print(f'HTTP error occurred: {http_err}')
           return dict()
        except Exception as err:
           print(f'Other error occurred: {err}')
           return dict()
        return response.json()

    def getJson(self,command):
        try:
           response = requests.get(self.baselineLink + "/" + command, 
                                   headers=self.reqHeader)
           response.raise_for_status()
        except HTTPError as http_err:
           print(f'HTTP error occurred: {http_err}')
           return dict()
        except Exception as err:
           print(f'Other error occurred: {err}')
           return dict()
        return response.json()

    def getPlanList(self):
        json_response = self.getJson("plan")
        return json_response

    def getTrajEngSegments(self, crema_id):
        json_response = self.getJson("trajectory" + "/" + crema_id + "/" + "engineering_segments")
        return json_response

    def getTrajEngSegmentTypes(self, crema_id):
        # /rest_api/trajectory/{mnemonic}/engineering_segment_types         
        json_response = self.getJson("trajectory" + "/" + crema_id + "/" + "engineering_segment_types")
        return json_response

    def getTrajSegmentDefinitions(self, crema_id):
        json_response = self.getJson("trajectory" + "/" + crema_id + "/" + "segment_definition")
        return json_response

    def getCremaPlanList(self, crema_id):
        json_response = self.getJson("trajectory" + "/" + crema_id + "/" + "plan")
        return json_response

    def genPlanTimeline(self, id, startTime="", endTime=""):
        if (startTime=="") and (endTime==""):
            params = {}
        else:
            params = {'start': startTime + "Z", 'end': endTime + "Z", 'mode': 'open'}

        urlText  = "plan_simphony/timeline"
        urlText += "/"
        urlText += str(id)
        if bool(params):
            urlText += "/?"
            urlText += urllib.parse.urlencode(params)
        print (urlText)
        json_response = self.getJson(urlText)
        return json_response

    def getSegmentDefintion(self, seg_id):
        json_response = self.getJson("segment_definition" + "/" + seg_id)
        return json_response

    def getObservationDefintionsList(self):
        json_response = self.getJson("observation_definition")
        return json_response

    def getObservationDefintion(self, obs_id):
        json_response = self.getJson("observation_definition" + "/" + obs_id)
        return json_response

    def downloadFile(self,filePath):
        # Test
        #filePath = R'Z:\VALIDATION\simphony\pcm\phs_pcm_test_004\input\TMP\CREMA_5_0.xml'
        #with open(filePath) as f:
        #    return f.read()
        text_response = self.getFile(filePath)
        return text_response

    def getXmlPtrFilePath(self, id, startTime="", endTime=""):
        if (startTime=="") and (endTime==""):
            params = {}
        else:
            params = {'start': startTime + "Z", 'end': endTime + "Z", 'mode': 'open'}

        urlText  = "plan"                                                                                   
        urlText += "/"
        urlText += str(id)
        urlText += "/"
        urlText += "ptr"
        if bool(params):
            urlText += "/?"
            urlText += urllib.parse.urlencode(params)
        print (urlText)
        json_response = self.getJson(urlText)
        return json_response


    def getFile(self,filePath):
        try:
           response = requests.get(filePath, 
                                   headers=self.reqHeader)
           response.raise_for_status()
        except HTTPError as http_err:
           print(f'HTTP error occurred: {http_err}')
           return dict()
        except Exception as err:
           print(f'Other error occurred: {err}')
           return dict()
        return response.content

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
          "PEPHI",
          "PEPLO",
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

    def getFile(self, fileUrl):
        try:
           #self.setApiKey(self.getApiKey())
           response = requests.get(fileUrl, 
                                   headers=self.reqHeader, 
                                   allow_redirects=True)
           response.raise_for_status()

        except HTTPError as http_err:
           print(f'HTTP error occurred: {http_err}')
           return dict()
        except Exception as err:
           print(f'Other error occurred: {err}')
           return dict()
        return response.content.decode()

def build_url(base_url, path, args_dict):
    
    url_parts = list(urllib.parse.urlparse(base_url))
    url_parts[2] = path
    url_parts[4] = urllib.parse.urlencode(args_dict)
    return urllib.parse.urlunparse(url_parts)