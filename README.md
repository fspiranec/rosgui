# PDK assistant

This app opens a small Windows-focused GUI to send robot commands in one terminal.

## Layout

- Robot name field + **Connect**
- **API Frame**
  - **Start Robot_API**
  - **Open Robot_API**
  - **Run Roslaunch**
- **Tilt Frame**
  - **Tilt System- State**

## Commands sent

- **Connect**

```bash
ssh -tt gideon@<robot_name>
```

- **Start Robot_API**

```bash
ssh -tt gideon@<robot_name>
docker start gideon_robot_api_cont
```

- **Open Robot_API**

```bash
ssh -tt gideon@<robot_name>
docker exec -it gideon_robot_api_cont bash
```

- **Run Roslaunch**

```bash
ssh -tt gideon@<robot_name>
docker exec -it gideon_robot_api_cont bash
roslaunch trailerbot_mitsubishi_ros trailerbot_mitsubishi_ros_node_karbon_beckhoff.launch
```

- **Tilt System- State**

```bash
ssh -tt gideon@<robot_name>
docker exec -it gideon_robot_api_cont bash
rostopic echo /mitsubishi_atul1/robot/tilt_system/state
```

## Run

```bash
python app.py
```

> Note: Terminal auto-open and command sending are implemented for Windows (`cmd`).
