# Config File

To configure the game sdk a config.toml can be created. The path to it can be set when executing `Game.run(config_path="path/to/your/config.toml")`. The default path is `/home/pi/Gamecontrol/config.toml`

## Structure

**Example**
```toml
seats=[1,2,3]

[MQTT]
broker_ip="192.168.1.20"
borker_port="1883"
username="mqtt"
password="secret"
```

- `list[int] seats`: List of controller id's
### MQTT
Configuration to connect to the mqtt broker of the gamecontrol

- `str broker_ip`: Adress to your mqtt broker
- `str broker_port`(Optional): MQTT Port of your broker (default `1883`)
- `str username`(Optional): Username for authentifikation (default `NONE`)
- `str password`(Optional): Password for authentifikation (default `NONE`)