
# LED Test Game

This basic example creates a game with one player. When the player presses a button on his gamepad an LED lights up.

The source coder for this example can be found in the *examples* folder of this repository.

## Setup

In order for the game to work you need the following hardware:

| Description      | Amount |
| ---------------- | ------ |
| Raspberry Pi     | 2      |
| Gamepad          | 1      |
| LED              | 1      |
| 220 Ohm Resistor | 1      |

One Raspberry Pi is used as controller one as gamecontrol.

First connect the LED to GPIO Pin 17 of your controller with the resistor in series. Next pair your gamepad with the controller using USB or Bluetooth.

### Raspberry Pi

Setup two Raspberry Pi's with Raspbian OS and pull the repository of the SDK onto each device.

Install the required python packages using pip

```bash
pip3 install -r requirements.txt
```

In order to use MQTT for the communication you need to setup a MQTT broker as explained [here](https://mosquitto.org/blog/2013/01/mosquitto-debian-repository/)

### config.toml

Create a config.toml for your controller and gamecontrol. For this you need to find the path to your input device (gamepad).

!!! NOTE
    You can check the inputs using

    ```bash
    cat /dev/input/your/device
    ```

    If you get any output when pressing a button on your gamepad it got the right path.

Your config files should look something like this:

**gamecontrol**
```toml
seats=[1]

[MQTT]
broker_ip="192.168.1.20"
borker_port="1883"
```

**controller**
```toml
seat=1

[CONTROLLER]
input_device="/dev/input/event1"

[MQTT]
broker_ip="192.168.1.20"
borker_port="1883"
```

### PYTHONPATH

In order to be able to import the SDK into your programs the path to the SDK has to be added to your `PYTHONPATH`

```bash
export PYTHONPATH="path/to/sdk/repository/:PYTHONPATH"
```

!!! success ""
    Now you should be ready to go

## Code

The *ledTestGame* folder contains two python files. One for the controller and one for the gamecontrol.

### Controller

The controller code consists of two `Switch` classes and a `Game` class.

The `LEDSwitch` class is used to handle the input during the game. It turns on the LED and increases the score using a callback method.

The `ReadySwitch` class is for handling logic when the player presses ready on his gamepad. In this case there is no logic needed other than starting the game therefore the class is empty.

`LedTestGame` is the root of the game. In this class alle `Input` classes are registered. In addition a `update_score()` method is defined. This method increases the score and publishes the new score over MQTT using `game_io`.

The game is started when `LedTestGame.run()` is executed.

!!! NOTE
    Don't forget to define the right path to your config.toml

### Gamecontrol

The gamecontrol code has only one class called `LedTestGame`. This class overwrites the method `on_score()` which is executed every time a player scores a point. When this happens the points of all players are compared against the maximum score. If someone reaches it the game ends.

The game is started when `LedTestGame.run()` is executed.

!!! NOTE
    Don't forget to define the right path to your config.toml