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

Requires `datadog` and a `dd-agent` configuration in a standard
location on the host the client is running from.

To enable, add `sentry_datadog_helpers.raven.processors.DataDogTagProcessor`
to the configured `processors` for your `raven-python` client.

#### Install

`pip install sentry-datadog-helpers[raven]`

#### Configuration

```
from raven import Client

client = Client(processors=['sentry_datadog_helpers.raven.processors.DataDogTagProcessor'])
```

#### Flask Configuration

```
from raven.contrib.flask import Sentry

sentry = Sentry()
app.config['SENTRY_PROCESSORS'] = ['sentry_datadog_helpers.raven.processors.DataDogTagProcessor']
sentry.init_app(app)
```

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
