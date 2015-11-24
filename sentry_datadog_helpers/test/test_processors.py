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

    @mock.patch('datadog.statsd')
    def test_no_datadog_processor(self, mock1):
        proc = DataDogTagProcessor(mock.Mock())
        result = proc.process({'tags': {}})
        self.assertEqual(result, {'tags': {}})
        mock1.assert_not_called()

    @surrogate('datadog.util.config.get_config')
    @mock.patch('datadog.util.config.get_config', return_value={'tags': '"foo:bar", "baz:fuzz"'})
    @mock.patch('datadog.statsd.increment')
    def test_with_datadog_processor(self, mock1, mock2):
        proc = DataDogTagProcessor(mock.Mock())
        result = proc.process({'tags': {}})
        self.assertEqual(result, {'tags': {'foo': 'bar', 'baz': 'fuzz'}})
        mock1.assert_called_once_with('sentry.exception_captured')

    @surrogate('datadog.util.config.get_config')
    @mock.patch('datadog.util.config.get_config', return_value={'tags': '"foo", "baz"'})
    @mock.patch('datadog.statsd.increment')
    def test_with_datadog_processor_raw_tags(self, mock1, mock2):
        proc = DataDogTagProcessor(mock.Mock())
        result = proc.process({'tags': {}})
        self.assertEqual(result, {'tags': {'data_dog_tags': ['foo', 'baz']}})
        mock1.assert_called_once_with('sentry.exception_captured')
