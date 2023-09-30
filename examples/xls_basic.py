# encoding: utf-8

# (c) 2018-2023 Open Risk, all rights reserved
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

""" This file is part of the DataQualityToolkit package.

"""

from DQToolkit import Rule
from DQToolkit import XLSDataSource

filename = "../datasets/EBA_Sample.xlsx"
header_row = 2

# Instantiate a validation rule object
MyRule = Rule()
MyRule.activate('R1')

# Instantiate a datasource object
MySource = XLSDataSource(filename, header_row)

# Summary of the data we received
MySource.describe(verbosity=0)

# Validate everything against the activated rule
# MySource.validate_all(MyRule)

# Display a validation summary
# MySource.validation_summary()
