# 4D-Game SDK Structure

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

## GameTemplate

The `GameTemplate` class is the base for the different `Game` classes for controller, gamecontrol and passive elements.

## GameIO

The `GameIO` gives access to the gameloop and communication between devices. It is instanciated in the `Game` class and can be used with `self.game_io`.

## Players

The `Players` class is used by the gamecontrol and passive devices. It provides an easy interface to save the score and the ready flag of all connected controllers.