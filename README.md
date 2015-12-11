sentry-datadog-helpers
======================

[Sentry](https://github.com/getsentry/sentry) helpers which enhance
and encourage integration with [Datadog](https://www.datadoghq.com)
in your installation.

# Installation

```bash
$ pip install sentry-datadog-helpers
```

# Configuration

## Client

### `sentry_datadog_helpers.raven.processors.DataDogTagProcessor`

Processor for [raven](https://github.com/getsentry/raven-python)
which attempts to find a [Datadog](https://www.datadoghq.com)
agent configuration on the system. If found, the `tags` key is
loaded, and sent along with all events to the Sentry server.

Additionally, a metric `sentry.exception_captured` is incremented
in datadog's statsd.

Requires `datadog` and a `dd-agent` configuration in a standard
location on the host the client is running from.

To enable, add `sentry_datadog_helpers.raven.processors.DataDogTagProcessor`
to the configured `processors` for your `raven-python` client.

#### Install

`pip install sentry-datadog-helpers[raven]`

#### Basic Configuration

```python
import raven

RAVEN_PROCESSORS = list(raven.conf.defaults.PROCESSORS) + \
                  ['sentry_datadog_helpers.raven.processors.DataDogTagProcessor']
client = raven.Client(processors=RAVEN_PROCESSORS)
```

#### Flask Configuration

```python
import raven
from raven.contrib.flask import Sentry

RAVEN_PROCESSORS = list(raven.conf.defaults.PROCESSORS) + \
                   ['sentry_datadog_helpers.raven.processors.DataDogTagProcessor']

sentry = Sentry()
app.config['SENTRY_PROCESSORS'] = RAVEN_PROCESSORS
sentry.init_app(app)
```

### Django Configuration

```python
INSTALLED_APPS = INSTALLED_APPS + ['raven.contrib.django.raven_compat']
import raven

RAVEN_CONFIG = {
    'processors': list(raven.conf.defaults.PROCESSORS) + [
        'sentry_datadog_helpers.raven.processors.DataDogTagProcessor'
    ],
}
```

### Logging Integration

```python
import raven

RAVEN_PROCESSORS = list(raven.conf.defaults.PROCESSORS)  + \
                   ['sentry_datadog_helpers.raven.processors.DataDogTagProcessor']

sentry_handler = {
        'level': 'ERROR',
        'class': 'raven.handlers.logging.SentryHandler',
        'processors': RAVEN_PROCESSORS,
    }
```

Add the `sentry_handler` to your logging DictConfig and enable it for a logger with appropriate level

See `processors` under [Client Arguments](https://docs.getsentry.com/hosted/clients/python/advanced/#client-arguments)

## Server

A Sentry sentry notifcation plugin is available which will forward
notifications to Datadog, complete with any tags.

### Install

`pip install sentry-datadog-helpers[sentry]`

### Configure

```
INSTALLED_APPS = INSTALLED_APPS + ('sentry.plugins.sentry_datadog',)

# To enable for *ALL PROJECTS*
#SENTRY_OPTIONS['SENTRY_DATADOG_API_KEY'] = 'deadbeefmyapikeydeadbeef'
#SENTRY_OPTIONS['SENTRY_DATADOG_APP_KEY'] = 'beefdeadbeefmyappkeydeadbeefdead'
```
