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
import configparser
from jinja2 import Template
import os
from juice_simphony.CompositionEngine.Scenario.common.fileName import fileName

class fileHandle(fileName):

    def __init__(self, path, params=0):
        if params!= 0: self.params.update(params)
        self.path = path
        self.fileName = ""
        fileName.__init__(self)

    def genFile(self):
        
        # Generate file name
        self.fileName = self.genBaseFileName() + "." + self.params["ext"]
        destFilePath = os.path.join(self.path, self.fileName)
        #destFilePath = self.path

        # Open File
        self.fileHdl  = open(destFilePath, "w")

        # Write Content
        self.writeContent()

        # Close File
        self.fileHdl.close()

        return destFilePath

    def loadRefFile(self, filePath):
        with open(filePath) as tplFile:
            self.template = Template(tplFile.read())

    def writeContent(self):
         a=1

    def writeHeader(self, title, shortDesc, description=""):
        self.fileHdl.write(             "#----------------------------------------------------------------------------------------------------#\n")
        self.fileHdl.write(             "#                                                                                                    #\n")
        self.fileHdl.write('#{:^100s}#\n'.format(title))
        self.fileHdl.write('#{:^100s}#\n'.format(shortDesc))
        self.fileHdl.write(             "#                                                                                                    #\n")
        self.fileHdl.write(             "#----------------------------------------------------------------------------------------------------#\n")
        
        if description != "":
           self.fileHdl.write ("\n")
           
           self.fileHdl.write          ("#----------------------------------------------------------------------------------------------------#\n")
           self.fileHdl.write          ("# DESCRIPTION:\n")
           self.fileHdl.write          (description + "\n")
           self.fileHdl.write          ("#----------------------------------------------------------------------------------------------------#\n")
        
    def insertEmptyLine(self):
        self.fileHdl.write("\n")

    def insertComment(self,text):
        self.fileHdl.write("# " + text + "\n")
