"""
sentry_datadog_helpers.raven.processors
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
:copyright: (c) 2015 by Ernest W. Durbin III
:license: BSD, see LICENSE for more details.
"""
from __future__ import absolute_import

from raven.processors import Processor

try:
    import datadog
    HAS_DD = True
except ImportError:
    HAS_DD = False

class DataDogTagProcessor(Processor):

    def __init__(self, client):
        self.dd_config = {}
        if HAS_DD:
        try:
            self.dd_config = datadog.util.config.get_config()
            self.has_dd = True
        except datadog.util.config.CfgNotFound:
            pass
        self.tags = {}
        for tag in filter(None, self.dd_config.get('tags', '').split(', ')):
            k, v = tag.replace('"', '').strip().partition(":")[::2]
            if v == '':
                self.tags['data_dog_tags'] = self.tags.get('data_dog_tags', []) + [k]
            else:
                self.tags[k] = v
        super(DataDogTagProcessor, self).__init__(client)

    def process(self, data, **kwargs):
        data['tags'].update(self.tags)
        if HAS_DD:
            datadog.statsd.increment('sentry.exception_captured')
        return super(DataDogTagProcessor, self).process(data, **kwargs)
