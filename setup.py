#!/usr/bin/python

# Copyright 2011 Tomo Krajina
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import distutils.core as mod_distutilscore
import oneapi as mod_oneapi

mod_distutilscore.setup(
    name = 'oneapi-python',
    version = mod_oneapi.AbstractOneApiClient.VERSION,
    description = 'Infobip OneApi Python library',
    license = 'Apache License, Version 2.0',
    author = 'Infobip Ltd.',
    author_email = 'plugins@infobip.com',
    url = 'https://github.com/infobip/oneapi-python',
    packages = [
        'oneapi',
    ],
    keywords = [
	'infobip',
	'oneapi',
	'sms',
	'api'
    ]
)

