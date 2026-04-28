# PDK assistant

This app opens a small Windows-focused GUI to send robot commands in one terminal.

## Startup behavior

- The Python console window is hidden on Windows when possible.
- The command terminal is **not** opened on app start.
- The terminal opens only when you click a button that sends a command.

## Layout order

1. **API**
2. **BRAIN**
3. **SAFETY**
4. **TILT**

## Commands sent

- **Connect**

```bash
ssh -tt gideon@<robot_name>
```

### API

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

### BRAIN

- **Stop Brain Start App**

```bash
ssh -tt gideon@<robot_name>
docker stop brain_start_app
```

- **Stop Brain**

```bash
ssh -tt gideon@<robot_name>
docker stop brain_cont
```

### SAFETY

- **Send Brain State Reference** (uses the nearby 2-digit value field)

```bash
ssh -tt gideon@<robot_name>
docker exec -it gideon_robot_api_cont bash
rostopic pub -r 500 /mitsubishi_atul1/robot/safety_system/command safety_ros_msgs/SafetySystemMonitoringCaseCommandMsg "ReferenceMonitoringCase: <x>"
```

### TILT

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

> Note: Terminal automation is implemented for Windows (`cmd`).
