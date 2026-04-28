# PDK assistant

This starter app opens a small GUI with:

- A text box for robot name.
- A **Connect** button.
- An **Open RobotAPI container** button.
- A **Get tilt status** button.

On Windows, the app opens a new Command Prompt terminal window when the app starts.
If that terminal window is closed, the app automatically opens a new one on the next button click.

## Buttons

- **Connect** sends:

```bash
ssh -tt gideon@<robot_name>
```

- **Open RobotAPI container** sends (in order, in the same terminal):

```bash
ssh -tt gideon@<robot_name>
docker exec -it gideon_robot_api_cont bash
```

- **Get tilt status** sends (in order, in the same terminal):

```bash
ssh -tt gideon@<robot_name>
docker exec -it gideon_robot_api_cont bash
rostopic echo /mitsubishi_atul1/robot/tilt_system/state
```

## Run

```bash
python app.py
```

> Note: Terminal auto-open and command send are implemented for Windows (`cmd`).
