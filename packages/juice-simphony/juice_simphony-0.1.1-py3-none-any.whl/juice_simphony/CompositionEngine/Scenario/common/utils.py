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
import os
import shutil
from zipfile import ZipFile


def createFolder(rootPath, folderName):
    folderPath = os.path.normpath(os.path.join(rootPath, folderName))
    os.makedirs(folderPath, exist_ok=True)
    #print('Folder ' + folderName + ' created at ' + folderPath)
    return folderPath


def copyFile(source, destination):
    shutil.copyfile(source, destination)


def removeFolderTree(path):
    if os.path.exists(path):
        shutil.rmtree(path)


def getFolderFromZip ():
    test = 1


def name2acronym(name):
    
    instrument_dict = {
    'SOC':       'SOC',
    '3GM':       '3GM',
    'GALA':      'GAL',
    'JANUS':     'JAN',
    'JMAG':      'MAG',
    'JMC':       'JMC',
    'MAJIS':     'MAJ',
    'NAVCAM':    'NAV',
    'PEP':       'PEP',
    'PRIDE':     'PRI',
    'RIME':      'RIM',
    'RPWI':      'RPW',
    'SWI':       'SWI',
    'UVS':       'UVS',
    'JUICE':     'JUI'
    }

    return instrument_dict[name]