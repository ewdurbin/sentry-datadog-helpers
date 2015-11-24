"""
sentry_datadog_helpers.raven.processors
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
:copyright: (c) 2015 by Ernest W. Durbin III
:license: BSD, see LICENSE for more details.
"""
from __future__ import absolute_import

from raven.processors import Processor


class DataDogTagProcessor(Processor):

    def __init__(self, client):
        self.dd_config = {}
        self.has_dd = False
        try:
            import datadog
            try:
                self.dd_config = datadog.util.config.get_config()
                self.has_dd = True
            except datadog.util.config.CfgNotFound:
                pass
        except ImportError:
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
        if self.has_dd:
            from datadog import statsd
            statsd.increment('sentry.exception_captured')
        return super(DataDogTagProcessor, self).process(data, **kwargs)
