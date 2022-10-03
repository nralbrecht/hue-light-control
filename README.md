# Hue Light Control

Regulate the brightness of a Phillips Hue light depending on the measured brightness by a Philips Hue - Ambient light sensor

## Functions
- Turn on the lamp when a configured brightness is measured
- Turn up the brightness until the wanted brightness is reached
- The wanted brightness can be changed with a GUI during the runtime
- Choose the color temperature depending on the content of the monitor

## Usage
First install python dependencys.
```bash
pip install -r requirements.txt
```

Than modify the `config.json` to your liking.

Finally run the application with:
```bash
python app.py
```
