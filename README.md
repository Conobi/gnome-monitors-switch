<h1 align="center"><br>Gnome Monitors Switch</h1>

An alternative to [gnome-randr](https://gitlab.com/Oschowa/gnome-randr), which doesn't work anymore, and to [gnome-randr-rust](https://github.com/maxwellainatchi/gnome-randr-rust), which doesn't support setting off a screen ([see here](https://github.com/maxwellainatchi/gnome-randr-rust/issues/13)) for now (30/08/22).
It let you to save and load your monitors layouts to a `json` file, which is convenient when using a KVM or if you need to switch between different hardware configurations.

Tested on `Ubuntu 22.04.1 LTS x86_64`, with `GNOME Shell 42.2` (Wayland version).

## Usage
```
❯ python3 monitors-switch.py --help
usage: monitors-switch.py [-h] [-s] [-l] [-p] config_name

Gnome Monitors Switch - Save and load Gnome monitors configuration

positional arguments:
  config_name       Name of the config to save or load. It will be saved as <config_name>.json.

options:
  -h, --help        show this help message and exit
  -s, --save        Save current monitors configuration
  -l, --load        Load and apply the saved configuration
  -p, --persistent  To keep the configuration persistent
```

## Method used
I simply parse the output of the `GetCurrentState` dbus method to get the current displays configuration, and convert it to a data structure pushable to `ApplyMonitorsConfig`.
The dbus object documentation is [available here](https://github.com/GNOME/mutter/blob/42.4/data/dbus-interfaces/org.gnome.Mutter.DisplayConfig.xml).
It looks like these methods are going to be deprecated, howewer I already made a future-proof GetResources/ApplyConfiguration implementation (not pushed though).

