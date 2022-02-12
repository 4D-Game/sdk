# 4D-Game SDK

The 4D-Game SDK allows you to create a physical Game which can be controlled with a Gamepad over a Raspberry Pi. To create a game, every Player (Gamepad) gets it's own Raspberry Pi (**Controller**). The control of the Game is done by one Raspberry Pi called the **Gamecontrol**.

## Gameloop

The course of every game can be described by a state machine called the gameloop. It is consisting of the _idle-_, _start-_, _run-_ and _end-_States which are controlled by the **Gamecontrol**.

```mermaid
stateDiagram-v2
    [*] --> idle
    idle --> start: when all ready
    start --> run: when all ready
    run --> end
    end --> idle: when all ready
```
### States
#### Idle
The gameloop starts in the _idle_-State, waiting until every controller send a ready message. When this happens the state is changed to _start_.

#### Start
The start state is used to initialize different devices needed for the game and get everything into starting position. The state is changed to _run_ when every controller sent a ready message.

#### Run
This is the state where the actual game is played. Player can gain or loose points or a timer is running to end the game after a certain time. When the condition for the end of a game/round is met, the state is changed to _end_.

#### End
In this state devices needed for the game can be deinitialized so they are not running in idle state. When every controller is ready, the gamecontrol switches back to _idle_.

## Communication

All communication between different Devices is done with MQTT. The following structure is used:

!!! NOTE
    The setup of a MQTT Broker is needed to use the SDK

### MQTT Structure

![MQTT Structure](assets/mqtt_structure_dark.svg)

## Class Structure

The 4D-Game SDK is based on the classes shown below. The structure is extended by the classes specifically used for controller, gamecontrol or passive devices. Those classes are explained in the coresponding section.

```mermaid
classDiagram
  class GameTemplate{
    +dict config
    -bool _is_running
    -GameState _game_state
    -GameIO _game_io
    +GameState game_state()
    +GameIO game_io()
    +on_init()
    +on_pregame()
    +on_start()
    -_on_end()
    +on_end()
    -_on_exit(Exception err)
    +on_exit(Exception err)
    -_run()
    +run(str conf_path, int log_level)
  }

  class LogLevel~enum.Enum~{
    +CRITICAL = 50
    +ERROR = 40
    +WARNING = 30
    +INFO = 20
    +DEBUG = 10
    +NOTSET = 0
  }
  GameTemplate ..> LogLevel

  class GameIO{
    +Client client
    +__init__(dict mqtt_conf)
    +connect()
    +subscribe(list topics)
    +subscribe_to_status()
    +publish(str topic, dict payload)
    +ready(int seat)
    +score(int score, int seat)
    +set_game_state(GameState state)
  }
  GameTemplate ..> GameIO

  class GameState~enum.Enum~{
    IDLE = "idle"
    START = "start"
    RUN = "run"
    END = "end"
  }
  GameIO ..> GameState
  GameTemplate ..> GameState

  class Players {
    -dict ready
    -dict score
    +dict ready
    +dict score
    +set_ready(int seat, bool ready)
    +set_score(int seat, int score)
    +reset_ready()
    +reset()
  }
```

### GameTemplate

The `GameTemplate` class is the base for the different `Game` classes for controller, gamecontrol and passive elements.

### GameIO

The `GameIO` gives access to the gameloop and communication between devices. It is instanciated in the `Game` class and can be used with `self.game_io`.

### Players

The `Players` class is used by the gamecontrol and passive devices. It provides an easy interface to save the score and the ready flag of all connected controllers.

## Create a game

A simple game consists at least of:

- 1x Controller
- 1x Gamecontrol

The number of Controller can be increased up to 8.[^1]

You can also have an element in your game that get's all information but doesn't interact with the game loop (e.g. A display to show the score of a player). For this the **passive sdk** can be used. The number of passive devices is not restricted.[^2]

To learn how to get started with the different parts of the sdk see the following sections:

- [Controller - Getting Started](controller-sdk/index.md)
- [Gamecontrol - Getting Started](gamecontrol-sdk/index.md)
- [Passive - Getting Started](passive-sdk/index.md)

[^1]: Tested with 8 but it should work with more.
[^2]: Only tested with one.