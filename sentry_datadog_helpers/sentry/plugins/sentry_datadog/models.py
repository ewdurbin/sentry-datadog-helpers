"""
sentry_datadog_helpers.sentry.plugins.sentry_datadog.models
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2015 by Ernest W. Durbin III
:license: BSD, see LICENSE for more details.
"""
from __future__ import absolute_import

import ast

import sentry

from django import forms
from django.utils.safestring import mark_safe

from django.conf import settings

from django.template import Context
from django.template import Template

from sentry.plugins import register
from sentry.plugins.bases.notify import NotificationPlugin
from sentry.plugins.bases.notify import NotificationConfigurationForm

from datadog import initialize
from datadog.api.base import CreateableAPIResource


class DataDogEvent(CreateableAPIResource):

    _class_name = 'event'
    _class_url = '/events'
    _plural_class_name = 'events'
    _json_name = 'event'

    @classmethod
    def create(cls, **params):
        return super(DataDogEvent, cls).create(**params)

NOTSET = object()

ERROR_TEMPLATE = """
%%%
{% spaceless %}
{% autoescape off %}
A new event has been recorded in Sentry: `{{ event.message }}`

[view in sentry]({{ link }})

{% if interfaces %}{% for label, _, text in interfaces %}
### {{ label }}

```
{{ text }}
```

{% endfor %}
{% endif %}
{% endautoescape %}
{% endspaceless %}
%%%
"""

ALERT_TEMPLATE = """
{% spaceless %}
{% autoescape off %}
A new alert has been reported in Sentry:

    {{ alert.message }}

Details
-------

{{ link }}

Date: {{ alert.datetime }}
Project: {{ alert.project.name }}
{% endautoescape %}
{% endspaceless %}
"""


class DataDogOptionsForm(NotificationConfigurationForm):
    SENTRY_DATADOG_API_KEY = forms.CharField(
        help_text='Datadog app_key',
        initial=getattr(settings, 'SENTRY_DATADOG_API_KEY', None),
        widget=forms.TextInput(attrs={'class': 'span8'}))
    SENTRY_DATADOG_APP_KEY = forms.CharField(
        help_text='Datadog api_key',
        initial=getattr(settings, 'SENTRY_DATADOG_APP_KEY', None),
        widget=forms.TextInput(attrs={'class': 'span8'})


class DatadogPlugin(NotificationPlugin):
    title = 'Datadog'
    conf_key = 'datadog'
    slug = 'datadog'
    version = sentry.VERSION
    author = "Ernest W. Durbin III"
    author_url = "https://github.com/ewdurbin/sentry-datadog-helpers"
    project_default_enabled = True
    project_conf_form = DataDogOptionsForm

    def is_configured(self, project, **kwargs):
        if self.get_option('SENTRY_DATADOG_API_KEY', project):
            api_key = True
        elif sentry.options.get('SENTRY_DATADOG_API_KEY'):
            api_key = True
        else:
            api_key = False

        if self.get_option('SENTRY_DATADOG_APP_KEY', project):
            app_key = True
        elif sentry.options.get('SENTRY_DATADOG_APP_KEY'):
            app_key = True
        else:
            app_key = False

        return all([api_key, app_key])

    def _send_datadog_event(self, title, text, context, project):
        if not self.is_configured(project):
            return False
        tags = dict(context.get('tags'))
        data_dog_tags = ast.literal_eval(tags.pop('data_dog_tags', '[]'))
        kv_type_tags = ["%s:%s" % (k, v) for k, v in tags.iteritems()]
        tags = data_dog_tags + kv_type_tags
        # TODO aggregation_key =
        alert_type = 'error'
        source_type_name = 'sentry'

        api_key = self.get_option('SENTRY_DATADOG_API_KEY', project) or \
            sentry.options.get('SENTRY_DATADOG_API_KEY')
        app_key = self.get_option('SENTRY_DATADOG_APP_KEY', project) or \
            sentry.options.get('SENTRY_DATADOG_APP_KEY')

        options = {
            'api_key': api_key,
            'app_key': app_key,
        }

        initialize(**options)

        DataDogEvent.create(title=title, text=text, tags=tags,
                            alert_type=alert_type,
                            source_type_name=source_type_name,
                            attach_host_name=False)

    def on_alert(self, alert):
        project = alert.project
        title = '[{0} {1}] ALERT: {2}'.format(
            project.team.name,
            project.name,
            alert.message,
        )

        context = {
            'alert': alert,
            'link': alert.get_absolute_url(),
        }

        text = Template(ALERT_TEMPLATE).render(Context(context))

        self._send_datadog_event(title, text, context, project)

    def should_notify(self, group, event):
        return super(DatadogPlugin, self).should_notify(group, event)

    def notify(self, notification):
        event = notification.event
        group = event.group
        project = group.project

        interface_list = []
        for interface in event.interfaces.itervalues():
            body = interface.to_email_html(event)
            if not body:
                continue
            text_body = interface.to_string(event)
            interface_list.append(
                (interface.get_title(), mark_safe(body), text_body)
            )

        title = '[%s]: %s' % (project.team.name,
                              event.message)

        link = group.get_absolute_url()

        context = {
            'project_label': project.team.name,
            'group': group,
            'event': event,
            'tags': event.get_tags(),
            'link': link,
            'interfaces': interface_list,
        }

        text = Template(ERROR_TEMPLATE).render(Context(context))

        self._send_datadog_event(title, text, context, project)


register(DatadogPlugin)
