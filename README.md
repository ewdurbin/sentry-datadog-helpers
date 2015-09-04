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

### sentry_datadog_helpers.raven.processors.DataDogTagProcessor

Processor for [raven](https://github.com/getsentry/raven-python)
which attempts to find a [Datadog](https://www.datadoghq.com)
agent configuration on the system. If found, the `tags` key is
loaded, and sent along with all events to the Sentry server.

Requires `datadog` and a `dd-agent` configuration in a standard
location on the host the client is running from.

To enable, add `sentry_datadog_helpers.raven.processors.DataDogTagProcessor`
to the configured `processors` for your `raven-python` client.

See `processors` under [Client Arguments](https://docs.getsentry.com/hosted/clients/python/advanced/#client-arguments)

## Server

