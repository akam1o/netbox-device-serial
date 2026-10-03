# netbox-device-serial

A NetBox plugin that redirects `/device-serial/<serial>/` to the device page.

## Requirements

- NetBox 3.5 or later (tested on 4.7.2)

## Features

| URL | Behavior |
|---|---|
| `/device-serial/<serial>/` | Redirects to `/dcim/devices/<pk>/` |

- Case-insensitive serial number matching (`serial__iexact`)
- Multiple devices with the same serial → filtered device list
- No match → 404
- Respects NetBox object permissions

## Installation

### netbox-docker

```bash
# Copy the plugin to a persistent location
sudo mkdir -p /opt/netbox-plugins
sudo cp -r netbox-device-serial /opt/netbox-plugins/

# Enable the plugin
sudo sed -i 's|# PLUGINS = \["netbox_bgp"\]|PLUGINS = ["netbox_device_serial"]|' \
  /opt/netbox-docker/configuration/plugins.py
```

Add a volume mount to `docker-compose.override.yml` for both `netbox` and
`netbox-worker` services:

```yaml
volumes:
  - /opt/netbox-plugins/netbox-device-serial/netbox_device_serial:/opt/netbox/venv/lib/python3.14/site-packages/netbox_device_serial:z,ro
```

Then recreate the containers:

```bash
cd /opt/netbox-docker && sudo docker compose up -d
```

> **Note**: The exact site-packages path depends on the Python version in the
> container. Check with `docker exec <container> python3 -c "import sysconfig;
> print(sysconfig.get_paths()['purelib'])"`.

### Standard NetBox installation

```bash
sudo -u netbox /opt/netbox/venv/bin/pip install /path/to/netbox-device-serial
```

Then add to `configuration.py`:

```python
PLUGINS = ['netbox_device_serial']
```

And restart NetBox.

## Uninstall

Remove the plugin from `PLUGINS` and the volume mount, then recreate the
containers.

## License

MIT
