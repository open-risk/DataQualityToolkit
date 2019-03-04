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

""" This file is part of the DataQualityToolkit package.

"""

from DQToolkit import Rule
from DQToolkit import WWWDataSource

# Set the remote URL where we will fetch data from (obviously it must be accessible!)
url = "https://en.wikipedia.org/wiki/List_of_data_breaches"
url = "https://www.openriskmanual.org/wiki/Data_Breaches_List"

# Instantiate a validation rule object
MyRule = Rule()
# Lets check the available rules
MyRule.show_rules()

# Lets try first to see if fields are populated (R1)
MyRule.activate('R1')
# Double check we have the desired active rule
MyRule.show_active_rule()

# Instantiate a datasource object
MySource = WWWDataSource(url)

# # Summary the data we received
# MySource.describe(verbosity=1)
#
# # Validate the first column (Entity)
# MySource.validate('Entity', MyRule)
#
# # Validate everything against the activated rule
# MySource.validate_all(MyRule)
#
# # Display a validation summary
# MySource.validation_summary()