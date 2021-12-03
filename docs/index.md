# 4D-Game SDK

The 4D-Game SDK allows you to create a physical Game wich can be controlled with a Gamepad over a Raspberry Pi. To create a game, every Player (Gamepad) gets it's own Raspberry Pi (**Controller**). The control of the Game is done by one Raspberry Pi called the **Gamecontrol**.

## Gameloop

The course of every game can be described by a state machine called the gameloop. It is consisting of the _idle-_, _start-_, _run-_ and _end-_States wich are controlled by the **Gamecontrol**.

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

### MQTT Structure

![MQTT Structure](../assets/mqtt_structure_dark.svg)