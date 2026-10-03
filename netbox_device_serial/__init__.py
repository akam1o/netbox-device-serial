try:
    # NetBox 3.4+
    from netbox.plugins import PluginConfig
except ImportError:
    # NetBox 3.3 and earlier
    from extras.plugins import PluginConfig


class DeviceSerialConfig(PluginConfig):
    name = 'netbox_device_serial'
    verbose_name = 'Device Serial Access'
    description = 'Access devices by serial number instead of ID'
    version = '0.1.0'
    base_url = 'device-serial'
    # NetBox 3.5+: middleware that redirects /<serial>/ to the device page
    middleware = ['netbox_device_serial.middleware.SerialRedirectMiddleware']
    required_settings = []
    default_settings = {}


config = DeviceSerialConfig
