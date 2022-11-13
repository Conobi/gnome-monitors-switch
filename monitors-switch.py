#!/usr/bin/env python3

import dbus, argparse, json

parser = argparse.ArgumentParser(description='Gnome Monitors Switch - Save and load Gnome monitors configuration')
parser.add_argument('filename', metavar='config_name', nargs=1, help='Name of the config to save or load. It will be saved as <config_name>.json.', type=str)
parser.add_argument('-s', '--save', action='store_true', help='Save current monitors configuration')
parser.add_argument('-l', '--load', action='store_true', help='Load and apply the saved configuration')
parser.add_argument('-p', '--persistent', action='store_true', help='To keep the configuration persistent')

args = parser.parse_args()

def get_display_config():
	bus = dbus.SessionBus()
	dc = bus.get_object('org.gnome.Mutter.DisplayConfig',
						'/org/gnome/Mutter/DisplayConfig')
	dc_iface = dbus.Interface(dc, dbus_interface='org.gnome.Mutter.DisplayConfig')
	return (dc_iface.GetCurrentState())

def build_display_config(display_config, persistent):
	_, monitors, lms, _ = display_config
	def build_monitors(connector, monitors):
		submonitors = []
		for monitor in monitors:
			mode_id = monitor[1][0]
			if (monitor[0] == connector):
				for mode in monitor[1]:
					if len(mode[6]) and mode[6]['is-current'] == True:
							new_mode = []
							new_mode.append(monitor[0][0])
							mode_id = mode[0]
							new_mode.append(mode_id)
							new_mode.append(monitor[2])
							submonitors.append(new_mode)
		return (submonitors)

	new_lms = []

	for lm in lms:
		new_lms.append([
						lm[0],
						lm[1],
						lm[2],
						lm[3],
						lm[4],
						build_monitors(lm[5][0], monitors),
			])
	return (persistent, new_lms, {})

def apply_display_config(builded_config):
	bus = dbus.SessionBus()
	dc = bus.get_object('org.gnome.Mutter.DisplayConfig',
						'/org/gnome/Mutter/DisplayConfig')
	dc_iface = dbus.Interface(dc, dbus_interface='org.gnome.Mutter.DisplayConfig')
	persistent, new_lms, properties = builded_config
	serial, *_ = get_display_config()
	return(dc_iface.ApplyMonitorsConfig(serial, persistent, new_lms, properties))

if not (args.filename and (args.save or args.load)):
	parser.error('you must save or load a config file.')

elif (args.filename and args.save and args.load):
	parser.error('cannot save and load at the same time. Choose one.')

if (args.filename and args.save):
	with open(args.filename[0] + '.json', 'w') as outfile:
		data_builded = build_display_config(get_display_config(), args.persistent + 1)
		json.dump(data_builded, outfile, indent=2)
	print('The config has been saved in ' + args.filename[0] + '.json.')

if (args.filename and args.load):
	with open(args.filename[0] + '.json', 'r') as infile:
		apply_display_config(json.load(infile))
	print('The config has been loaded and applied.')
