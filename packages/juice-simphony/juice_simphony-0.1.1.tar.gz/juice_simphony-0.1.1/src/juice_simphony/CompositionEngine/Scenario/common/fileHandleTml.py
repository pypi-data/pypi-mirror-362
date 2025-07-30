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
from juice_simphony.CompositionEngine.Scenario.common.fileHandleEps import fileHandleEps

class fileHandleTml(fileHandleEps):
    def __init__(self, path, params=0):
        if params!= 0: self.params.update(params)
        self.path = path
        self.fileName = ""
        fileHandleEps.__init__(self, self.path, self.params)

    def insertInitPM (self, param, par_pad, value, value_pad, comment):
        self.fileHdl.write(f'Init_PM: { param : <{par_pad}} {value:<{value_pad}.2f} # {comment}\n')

    def insertInitMS (self, exp, exp_pad, module, module_pad, mode, mode_pad, comment):
        self.fileHdl.write(f'Init_MS: { exp : <{exp_pad}}{ module : <{module_pad}}{ mode : <{mode_pad}} # {comment}\n')

    def insertRequestEntry(self,date, exp, mode, action, par_label, par_value, comment):
        comment_lines = comment.splitlines()
        for comment_line in comment_lines:
            if comment_line != "": self.fileHdl.write(f'# {comment_line}\n')
        if 'Z' in date:
           self.fileHdl.write(f'{date} {exp} {mode} {action} ({par_label} = {par_value:12.7f})\n')
        else:
           self.fileHdl.write(f'{date}Z {exp} {mode} {action} ({par_label} = {par_value:12.7f})\n')

    def insertLine(self,text):
        self.fileHdl.write(text + "\n")
''''
# Spacecrat platform initialization
# ------------------------------------

Init_PM: BATTERY_DOD 0.0    # Battery DoD
Init_MS: JUICE DST_X_R NOM  # Antena Receiver always ON
Init_MS: JUICE PLATFORM ON  # Platform ON to enable platform power consumption


# Set platform profile
# ---------------------
2032-01-09T16:44:04Z JUICE  *  SET_POWER (VALUE=572.9135779720983)
'''''
if __name__ == '__main__':

    param       = "BATTERY_DOD"
    par_pad     = 8
    value       = 0.0
    value_pad  = 8
    comment     = "Antena Receiver always ON"
    print(f'Init_PM: { param : <{par_pad}} {value:<{value_pad}.2f} # {comment}')

    exp         = "JUICE"
    exp_pad     = 8
    module      = "DST_X_R"
    module_pad  = 9
    mode        = "NOM"
    mode_pad    = 5
    comment     = "Antena Receiver always ON"
    print(f'Init_PM: { exp : <{exp_pad}} { module : <{module_pad}} { mode : <{mode_pad}} # {comment}')

    exp         = "JUICE"
    exp_pad     = 8
    module      = "PLATFORM"
    module_pad  = 9
    mode        = "ON"
    mode_pad    = 5
    comment     = "Platform ON to enable platform power consumption"
    print(f'Init_PM: { exp : <{exp_pad}} { module : <{module_pad}} { mode : <{mode_pad}} # {comment}')

    date      = "2032-01-09T16:44:04Z"
    exp       = "JUICE"
    mode      = " * "
    action    = "SET_POWER"
    par_label = "VALUE"
    par_value = 572.9135779720983
    comment     = "This is coming from R[001]"
    print(f'Comment: {comment}')
    # 2032-01-09T16:44:04Z JUICE  *  SET_POWER (VALUE=572.9135779720983)
    print(f'{date} {exp} {mode} {action} ({par_label} = {par_value:18.13f})')