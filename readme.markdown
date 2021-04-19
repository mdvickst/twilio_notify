---
title: Twilio Notify
description: How to leverage the Twilio Notify API for HomeAssistant Notifications
ha_category:
  - Notifications
ha_release: '0.20'
ha_domain: twilio_notify
ha_iot_class: Cloud Push
ha_platforms:
  - notify
---

The `twilio-notify` notification platform enables sending notifications via SMS, APN, GPN and Facebook Messenger notifications, powered by [Twilio Notify API](https://www.twilio.com/docs/notify)

This is different from the Twilio_SMS notification platform as it allows you to specify tags in your bindings and then alert groups of users with a tag instead of using phone numbers. For example notifications sent with an 'info' tag might only be desired by a few users where notifications sent the emergency tag would be desired by all users. Using the Twilio Notify APIs binding feature we can easily change membership into these groups in a single place rather than on each automation in HA. 

The requirement is that you have setup [Twilio](/integrations/twilio/).

To use this notification platform in your installation, add the following to your `configuration.yaml` file:

```yaml
# Example configuration.yaml entry
notify:
  - name: NOTIFIER_NAME
    platform: twilio_notify
    notify_sid: NOTFY_SERVICE_SID
```

{% configuration %}
notify_sid:
  description: This is the SID of the Notify service you created. Services can be created through the [console](https://console.twilio.com/develop/notify/services?frameUrl=/console/notify/services) or through the Twilio CLI. You should create 1 or more bindings associated with the notify service through the REST API or Twilio CLI. 
  required: true
  type: string
name:
  description: Setting the optional parameter `name` allows multiple notifiers to be created. The notifier will bind to the service `notify.NOTIFIER_NAME`.
  required: false
  default: "`notify.twilio_notify`"
  type: string
{% endconfiguration %}

### Usage

Twilio Notify is a notify platform and thus can be controlled by calling the notify service [as described here](/integrations/notify/). You can specify a **target** argument which is a list of tags you would like to send the message to and/or an **identity** argument under the additional data which you can provide a list of identities from the Twilio Notify service. If only the **target** argument is provided the Twilio Notify API will send the message to all phone numbers which have a binding with that tag included. If an identity is provided is will only send the message to bindings for that identity and if both are provided, the Twilio Notify API will look for the intersection of the two. 


```yaml
# Example automation notification entry using identity
automation:
  - alias: "The sun has set"
    trigger:
      platform: sun
      event: sunset
    action:
       service: notify.twilio_notify
       data:
         message: The sun has set
         data:
           identity:
             - mark

```yaml
# Example automation notification entry using tags
automation:
  - alias: "The sun has set"
    trigger:
      platform: sun
      event: sunset
    action:
       service: notify.twilio_notify
       data:
         message: The sun has set
         target:
           - info
```
