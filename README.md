# ROS GUI Robot Connector (starter)

This starter app opens a small GUI with:

- A text box for robot name.
- A **Connect** button.
- An **Open robotAPI container** button.

On Windows, the app opens a new Command Prompt terminal window when the app starts.

- Clicking **Connect** sends:

```bash
ssh -tt gideon@<robot_name>
```

- Clicking **Open robotAPI container** sends:

```bash
docker exec -it gideon_robot_api_cont bash
```

Both commands are sent to the same terminal window.

## Run

```bash
python app.py
```

> Note: Terminal auto-open and command send are implemented for Windows (`cmd`).
