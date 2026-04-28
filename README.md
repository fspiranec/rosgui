# ROS GUI Robot Connector (starter)

This starter app opens a small GUI with:

- A text box for robot name.
- A **Connect** button.

On Windows, the app opens a new Command Prompt terminal window when the app starts.
When you click **Connect**, it sends:

```bash
ssh gideon@<robot_name>
```

to that terminal.

## Run

```bash
python app.py
```

> Note: Terminal auto-open and command send are implemented for Windows (`cmd`).
