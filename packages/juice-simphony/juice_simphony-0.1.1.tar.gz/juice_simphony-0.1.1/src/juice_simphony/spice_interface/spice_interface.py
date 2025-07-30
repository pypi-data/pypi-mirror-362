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
import json

# --------------
#  Class kernel
# --------------
class kernel():
    def __init__(self, mnemonic, name, path):
        self.mnemonic = mnemonic
        self.name     = name
        self.path     = path


# --------------------
#  Class kernels_list
# --------------------
class kernels_list():
    def __init__(self, toolkit_version = "", skd_version = "", metakernel = ""):
        self.toolkit_version = toolkit_version
        self.skd_version     = skd_version
        self.metakernel      = metakernel
        self._size           = 0
        self._kernels_list   = {}

    # toolkit_version
    @property
    def toolkit_version(self):
        return self._toolkit_version

    @toolkit_version.setter
    def toolkit_version(self, toolkit_version):
        self._toolkit_version = toolkit_version

    # skd_version
    @property
    def skd_version(self):
        return self._skd_version

    @skd_version.setter
    def skd_version(self, skd_version):
        self._skd_version = skd_version

    # metakernel
    @property
    def metakernel(self):
        return self._metakernel
    
    @metakernel.setter
    def metakernel(self, metakernel):
        self._metakernel = metakernel

    # size
    @property
    def size(self):
        return self._size

    # append kernels
    def append(self, mnemonic, name, path):
        self._kernels_list[mnemonic] = kernel(mnemonic, name, path)
        self._size = self._size + 1

    def __getitem__(self, key):
        return self._kernels_list[key]

    def __iter__(self):
        return iter(self._kernels_list)

    def __str__(self):
        out_str = "Number of Kernels: " + str(self.size) + "\n"
        count = 0
        for ker in self._kernels_list:
            count = count +1
            out_str = out_str + "[" + str(count) + "] " + str(self._kernels_list[ker].mnemonic)
            out_str = out_str + " (" + str(self._kernels_list[ker].name) + ") " + "\n"
        return out_str

    def get_json(self,obj):
        return json.loads(json.dumps(obj, default=lambda o: getattr(o, '__dict__', str(o))))


# -------------------
#  Class meta_kernel
# -------------------
class meta_kernel():
    def __init__(self, kernels_list="", absRootPath= ""):
        self._absRootPath  = absRootPath
        self.kernels_list = kernels_list
        self._file_name    = kernels_list.metakernel

    # kernels_list
    @property
    def kernels_list(self):
        return self._kernels_list

    @kernels_list.setter
    def kernels_list(self, kernels_list):
        self._kernels_list = kernels_list

    def __getitem__(self, key):
        return self._kernels_list[key]

    def __str__(self):
        out_str  = "   \\begindata" + "\n"
        out_str += "\n"
        out_str += "     PATH_VALUES       = ( '"+ self._absRootPath +"' )" + "\n"
        out_str += "\n"
        out_str += "     PATH_SYMBOLS      = ( 'KERNELS' )" + "\n"
        out_str += "\n"
        out_str += "     KERNELS_TO_LOAD   = (" + "\n"
        for ker in self._kernels_list:
            out_str += "        '" + "$KERNELS/" + str(self._kernels_list[ker].path) + "'" + "\n"
        out_str += "     )"
        return out_str

    def to_file(self, file_path):
        with open(file_path, 'w') as kernel_file:
            kernel_file.write(str(self))


# ----------------------
#  Class spice_instance
# ----------------------
class instance():
    def __init__(self, toolkit_version, meta_kernel=""):
        self.toolkit_version = toolkit_version
        self.meta_kernel = meta_kernel

    # toolkit_version
    @property
    def toolkit_version(self):
        return self._toolkit_version

    @toolkit_version.setter
    def toolkit_version(self, toolkit_version):
        self._toolkit_version = toolkit_version

    # kernels_list
    @property
    def kernels_list(self):
        return self._kernels_list

    @kernels_list.setter
    def kernels_list(self, kernels_list):
        self._kernels_list = kernels_list

# ----------------------
#  Class spice_toolkit
# ----------------------
class spice_toolkit():
    def __init__(self, toolkit_version, meta_kernel=""):
        self.toolkit_version = toolkit_version

    # toolkit_version
    @property
    def toolkit_version(self):
        return self._toolkit_version

    @toolkit_version.setter
    def toolkit_version(self, toolkit_version):
        self._toolkit_version = toolkit_version


# -----------------------
#  Class spice_interface
# -----------------------
class interface():
    def __init__(self):
        self.params = {}
        self.allowed_toolkit_versions_list = {}
    
    def __getitem__(self, toolkit_version):
        return self._allowed_toolkit_versions_list[toolkit_version]

    def append_allowed_toolkit_version(self, spice_toolkit):
        self.allowed_toolkit_versions_list[spice_toolkit.toolkit_version] = spice_toolkit

    def check_toolkit_version(self,toolkit_version):
        if toolkit_version in self.allowed_toolkit_versions_list:
            return True
        return False

    def add_kernel_list (self, kernelsList):
        self.kernelsList = kernelsList



if __name__ == "__main__":
    Klist = kernels_list("test", "test1", "test2")
    print (Klist)
    Klist.append("kernel1","kernel1_name","kernel1_path")
    print (Klist)
    Klist.append("kernel2","kernel2_name","kernel2_path")
    print (Klist)
    print(Klist.get_json())
