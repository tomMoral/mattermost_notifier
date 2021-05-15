# mattermost_notifier


Mattermost notifier for experiments on distant cluster.


## Config

This function needs to have access to the API_KEY for the mattermost webhooks.

### Generate the API key

* Login to your Mattermost team site and go to **Account Settings** -> **Integrations**.
* Next to **Incoming Webhooks** click **Edit**.
* Select the channel or private group to receive webhook payloads, then click **Add** to create the webhook
* The API key is the last part of the URL (eg: u2x8rkfugj8zbqby9pw3huqnyc)


### Provide the API key:

It can be provided via different mechanism:

* It can be passed explicitely in the function as `api_key` argument.
* It can be set globally for the process with the environment variable `MATTERHOOK_API_KEY`.
* It can be set in a config file `matterhook.cfg`, either in the current directory or in `$HOME/.config/`. The config file should have the structure:

```config
[matterhook]
api_key = XXX
```
