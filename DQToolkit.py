# encoding: utf-8

# (c) 2018 Open Risk, all rights reserved
#
# DataQualityToolkit is licensed under the Apache 2.0 license a copy of which is included
# in the source distribution of TransitionMatrix. This is notwithstanding any licenses of
# third-party software included in this distribution. You may not use this file except in
# compliance with the License.
#
# Unless required by applicable law or agreed to in writing, software distributed under
# the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
# either express or implied. See the License for the specific language governing permissions and
# limitations under the License.

""" This module is part of the DataQualityToolkit package.

"""

import pandas as pd
import numpy as np


#
# DataSource Class
#

class DataSource(object):

    def __init__(self, filename, header_row):
        self.xls = pd.ExcelFile(filename)
        # Names of the sheets
        self.sheet_names = self.xls.sheet_names
        # Number of sheets
        self.frame_no = len(self.sheet_names)
        # The header row (values start immediately below)
        self.header_row = header_row
        self.df = {}
        self.col_names = {}
        self.results = {}
        self.result_no = 0
        for frame in range(self.frame_no):
            self.df[frame] = pd.read_excel(self.xls, self.sheet_names[frame], header=self.header_row)
            self.col_names[frame] = list(self.df[frame])

    def validate_all(self, Validation_Rule):
        for frame in range(self.frame_no):
            self.results[self.sheet_names[frame]] = {}
            for col in self.col_names[frame]:
                series = self.df[frame][col]
                self.results[self.sheet_names[frame]][col] = Validation_Rule.apply(series)
                self.result_no += 1


class Rule(object):

    def __init__(self):
        self.active_rule = None
        self.args = None
        self.rule_dict = {
            'R1': ('IsPopulated',),
            'R2': ('IsPositive',),
            'R3': ('IsAtLeast', (10,)),
            'R4': ('IsAtMost', (10,)),
            'R5': ('InRange', (0, 1)),
            'R6': ('IsType', ('int',)),
            'R7': ('IsString',)
        }

    def rule_data(self, rule_name):
        return self.rule_dict[rule_name]

    def activate(self, rule_name):
        self.active_rule = self.rule_data(rule_name)[0]
        if len(self.rule_data(rule_name)) > 1:
            self.args = self.rule_data(rule_name)[1]

    # Apply
    def apply(self, series):
        # print(type(series))
        # print(self.active_rule)      
        # Escape empty frames
        if len(series) == 0:
            result = None
            return result
        else:
            rule = getattr(Rule, self.active_rule)
            result = series.apply(rule, args=self.args)
            return list(result.values)

    #
    # Rule Functions
    #
    def IsPopulated(x):
        return not pd.isnull(x)

    def IsPositive(x):
        if isinstance(x, (int, float)):
            if x < 0:
                return False
            else:
                return True
        else:
            return [np.NaN]

    def IsAtLeast(x, *args):
        a = args[0]
        if isinstance(x, (int, float)):
            if a <= x:
                return True
            else:
                return False
        else:
            return [np.NaN]

    def IsAtMost(x, *args):
        a = args[0]
        if isinstance(x, (int, float)):
            if x <= a:
                return True
            else:
                return False
        else:
            return [np.NaN]

    def InRange(x, *args):
        a = args[0]
        b = args[1]
        if isinstance(x, (int, float)):
            if a <= x <= b:
                return True
            else:
                return False
        else:
            return [np.NaN]

    def IsType(x, *args):
        control_type = args[0]
        if type(x).__name__ == control_type:
            return True
        else:
            return False

    def IsString(x):
        if not (isinstance(x, (int, float)) or type(x).__name__ in ['Timestamp', 'time', 'datetime']) and len(x) > 0:
            return True
        else:
            return False

    def InList(x, *args):
        if x in args:
            return True
        else:
            return False
