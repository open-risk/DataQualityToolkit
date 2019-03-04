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

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from DQToolkit import Rule
from DQToolkit import WWWDataSource

# Set the remote URL where we will fetch data from (obviously it must be accessible!)
url = "https://en.wikipedia.org/wiki/List_of_data_breaches"

# Instantiate a validation rule object
MyRule = Rule()
# Check the available rules
MyRule.rule_data()

MyRule.activate('R4')

# Instantiate a datasource object
MySource = WWWDataSource(url)
MySource.validate_all(MyRule)
r = []
theta = []
colors = []
dt = 2 * np.pi / MySource.result_no
dr = 0.02
ts = 0


for col in MySource.results:
    ts = ts + dt
    rs = 0.1
    if MySource.results[col] is not None:
        for point in MySource.results[col]:
            rs = rs + dr
            r.append(rs)
            theta.append(ts)
            if point == np.True_:
                colors.append('azure')
            else:
                colors.append('greenyellow')

fig = plt.figure(facecolor='#0B0050')
fig.suptitle('OpenCPM::DQToolkit', fontsize=20, color='azure')
ax = fig.add_subplot(111, polar=True, facecolor='#0B0050')
ax.set_xticklabels([])
ax.set_yticklabels([])
c = plt.scatter(theta, r, c=colors, s=2, cmap=cm.hsv)
c.set_alpha(0.75)
plt.savefig('Test.png', facecolor='#0B0050')