# -*- coding: utf-8 -*-

import mock
import sys
import unittest

import raven

from sentry_datadog_helpers.raven.processors import DataDogTagProcessor

from utils import surrogate


class DataDogTagProcessorTestCase(unittest.TestCase):

    def test_no_datadog_module(self):
        try:
            client = raven.Client('http://public:secret@sentry.local/1',
                                  processors=['sentry_datadog_helpers.raven.processors.DataDogTagProcessor'])
        except Exception as e:
            self.fail("DataDogTagProcessor failed without datadog module: %s" % (e))

    def test_no_datadog_processor(self):
        proc = DataDogTagProcessor(mock.Mock())
        result = proc.process({'tags': {}})
        self.assertEqual(result, {'tags': {}})

    def test_with_datadog_processor(self):
        with surrogate('datadog.util.config.get_config'):
            with mock.patch('datadog.util.config.get_config',
                            return_value={'tags': '"foo:bar", "baz:fuzz"'}):
                proc = DataDogTagProcessor(mock.Mock())
                result = proc.process({'tags': {}})
                self.assertEqual(result, {'tags': {'foo': 'bar', 'baz': 'fuzz'}})
