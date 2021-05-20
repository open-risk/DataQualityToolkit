# encoding: utf-8

# (c) 2018-2019 Open Risk, all rights reserved
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

""" The DQToolkit module provides the objects implementing the Data Quality Toolkit functionality

* DataSource and derived objects implement sources of tabular data (currently excel sheets, wikitables)
* Rule implements the validation rules

"""

import pandas as pd
import numpy as np


#
# Generic DataSource Class
#

class DataSource(object):
    """ The _`DataSource` object implements a generic source of tabular data


    """

    def __init__(self):
        self.df = {}
        self.col_names = {}
        self.col_length = {}
        self.col_datatypes = {}
        self.status = {}
        self.results = {}
        self.frame_names = {}
        self.frame_no = 1

    def describe(self, verbosity=0):
        """ Describe the obtained dataframes

        :return: 
        """

        for frame in range(self.frame_no):
            print("\n")
            print("=" * 80)
            print("Frame: ", frame, " Data Types")
            print(self.df[frame].dtypes)
            print("-" * 80)
            print("Frame: ", frame, " Summary Statistics")
            print("-" * 80)
            if verbosity == 0:
                print("Column Names: ", self.col_names[frame])
                print("Row Count: ", self.col_length[frame])
            else:
                print(self.df[frame].describe())

    def validate(self, column, Validation_Rule, frame=0):
        """ Validate desired frame / column against the activated validation rule.
        When applicable, it returns a list of Booleans (True/False)

        :param column:
        :param Validation_Rule:
        :param frame:
        :return:
        """

        series = self.df[frame][column]
        msg, validation_list = Validation_Rule.apply(series)
        if validation_list:
            self.status[frame][column] = msg
            self.results[frame][column] = validation_list
        else:
            self.status[frame][column] = msg

    def validate_frame(self, Validation_Rule, frame=0):
        """ Validate all columns of a frame against the activated validation rule. Returns lists of Booleans (True/False)

        :param Validation_Rule:
        :param frame:
        :return:
        """
        for col in self.col_names[frame]:
            print("-- Validating Column: ", col)
            self.validate(col, Validation_Rule, frame)

    def validate_all(self, Validation_Rule):
        """ Validate all columns of all frames frame against the activated validation rule.
        Returns lists of Booleans (True/False)

        :param Validation_Rule:
        :return:
        """
        for frame in range(self.frame_no):
            print("Validating Frame: ", frame)
            self.validate_frame(Validation_Rule, frame)

    def validation_summary(self):
        """ Display a summary of the validation outcomes for a given frame

        :return:
        """
        print("\n")
        print('{:<20}'.format("Column"), '{:<20}'.format("Validation Status"), '{:<20}'.format("True / False Count"))
        print("=" * 80)
        for frame in range(self.frame_no):
            for col in self.col_names[frame]:
                if self.status[frame][col] == 'Validated':
                    print(self.results[frame][col])
                    true_count = sum(self.results[frame][col])
                    false_count = len(self.results[frame][col]) - true_count
                    print('{:<20}'.format(col), '{:<20}'.format(self.status[frame][col]),
                          'True: {:<10}'.format(true_count),
                          'False: {:<10}'.format(false_count))
                else:
                    print('{:<20}'.format(col), '{:<20}'.format(self.status[frame][col]))


#
#  Excel sheet Datasource
#

class XLSDataSource(DataSource):
    """ The _`XLSDataSource` object implements an excel sheet data source.
    It treats each excel sheet as a distinct table
    The class inherits from DataSource_


    """

    def __init__(self, filename, header_row):
        """ Create a new xls data source

        :param filename: the excel filename
        :type header_row: the row with the column names (must be the same for all sheets)

        :Example:

        .. code-block:: python

            filename = "../datasets/EBA_Sample.xlsx"
            header_row = 2
            MySource = XLSDataSource(filename, header_row)

        """
        DataSource.__init__(self)
        # Read the excel file from disk
        self.xls = pd.ExcelFile(filename, engine="openpyxl")
        # Frame names are the sheet names
        self.frame_names = self.xls.sheet_names
        # Number of sheets / frames
        self.frame_no = len(self.frame_names)
        # The header row (values start immediately below)
        self.header_row = header_row

        # Create the dataframes (one per sheet)
        for frame in range(self.frame_no):
            self.df[frame] = pd.read_excel(self.xls, self.frame_names[frame], header=self.header_row)
            self.col_names[frame] = list(self.df[frame])
            self.results[frame] = {}
            self.col_length[frame] = self.df[frame].shape[0]
            self.status[frame] = {}

    # def validate_frame(self, Validation_Rule):
    #     for frame in range(self.frame_no):
    #
    #         for col in self.col_names[frame]:
    #             series = self.df[frame][col]
    #             self.results[self.sheet_names[frame]][col] = Validation_Rule.apply(series)


class WikiDataSource(DataSource):
    """ The _`WWWDataSource` object implements a wikitable data source
    The class inherits from DataSource_

    """

    def __init__(self, url):
        """ Create a new web data source

        :param url: the webpage hosting the wikitable (must be accessible)

        .. note:: The initialization in itself does not validate if the web page is accessible

        .. note:: Because wikitables (and html tables more generally) do not store type metadata the
        assumption is that there is a specific row in the table (second row) that stores type information
        in pandas format. During initialization, there is a validatin step

        :Example:

        .. code-block:: python

            url = "https://en.wikipedia.org/wiki/List_of_data_breaches"
            MySource = WWWDataSource(url)

        """
        DataSource.__init__(self)
        # TODO Current implementation assumes there is only single table per wiki page (index 0)
        # Read the wikitable from the URL and create the dataframe
        self.df[0] = pd.read_html(url, attrs={"class": "wikitable"}, header=0)[0]
        self.col_datatypes = list(self.df[0].iloc[1])
        print(self.col_datatypes)
        print(self.df[0].dtypes)

        self.df[0].drop(self.df[0].index[[0, 1]], inplace=True)
        self.col_names[0] = list(self.df[0])

        # self.df[0].drop(self.df[0].index[1])
        # self.df[0].reindex()

        # self.df[0].drop(self.df[0].index[1])
        # self.df[0].reindex()

        print(self.df[0].head(2))

        # c = 0
        # for col in self.df[0].columns:
        #     self.df[0][col] = self.df[0][col].astype(self.col_datatypes[c])
        #     c +=1

        # pd.to_numeric(self.df[0])

        # Determine column length
        self.col_length[0] = self.df[0].count

        # Initialize status / results
        self.status[0] = {}
        for col in self.col_names[0]:
            self.status[0][col] = 'Not Validated'
        self.results[0] = {}


class Rule(object):
    """ The _`Rule` object implements a collection of validation rules


    """

    def __init__(self):
        """ Create a new collection of Rules

        """
        self.active_rule = None
        self.active_rule_name = None
        self.active_rule_args = None
        self.rule_dict = {
            'R1': ('IsPopulated', None, "Tests for the existence of data"),
            'R2': ('IsPositive', None, "Tests for positivity (x>0)"),
            'R3': ('IsAtLeast', (10,), "Tests greater than (x>=a)"),
            'R4': ('IsAtMost', (10,), "Tests less than (x<=a)"),
            'R5': ('InRange', (0, 1), "Tests range (a <= x < = b)"),
            'R6': ('IsType', ('int',), "Tests data type"),
            'R7': ('IsString', None, "Tests for string type"),
            'R8': ('IsNonNegative', None, "Tests for non-negativity (x>=0)"),
        }

    def rule_data(self, rule_name):
        """ Access rule data by rule name

        :param rule_name:
        :return:
        """
        if rule_name is None:
            print('Please provide a rule name')
        else:
            return self.rule_dict[rule_name]

    def show_rules(self):
        """ Display all the currently available Validation Rules

        """
        print("\n")
        print("=" * 80)
        print('{:<9}'.format("Rule_Name"), '{:<15}'.format("Function"), "Description")
        print("=" * 80)
        for rule_name in sorted(self.rule_dict.keys()):
            print('{:^9}'.format(rule_name), '{:<15}'.format(self.rule_dict[rule_name][0]),
                  self.rule_dict[rule_name][2])

    def activate(self, rule_name):
        """ Configure the Validation Rule that will be applied

        """
        self.active_rule = self.rule_data(rule_name)[0]
        self.active_rule_name = rule_name
        # If there are arguments
        if len(self.rule_data(rule_name)) > 1:
            self.active_rule_args = self.rule_data(rule_name)[1]

    def show_active_rule(self):
        print("\nCurrently Active Rule: ", self.active_rule_name, self.active_rule, self.active_rule_args)

    # Apply a validation rule to a series
    def apply(self, series):
        """ Apply series against the activated validation rule.
        When applicable, it returns a list of Booleans (True/False)
        """
        # Escape empty frames
        if len(series) == 0:
            result = None
            msg = "Empty Series"
            return msg, result
        else:
            rule = getattr(Rule, self.active_rule)
            result = series.apply(rule, args=self.active_rule_args)
            result_list = list(result.values)
            print(result_list)
            # Check that the rule application is valid
            IsValid = True
            # Test that all results are boolean
            for value in range(len(result_list)):
                # print(type(result_list[value]))
                if np.isnan(result_list[value]):
                    IsValid = False
            if IsValid:
                msg = 'Validated'
                return msg, result_list
            else:
                msg = 'Rule Not Applicable'
                return msg, None

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
            return np.NaN

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
