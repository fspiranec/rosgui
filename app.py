import subprocess
import sys
import tkinter as tk
from tkinter import messagebox


class RobotConnectorApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("PDK assistant")
        self.root.geometry("760x320")
        self.terminal_process: subprocess.Popen[str] | None = None

        self._build_ui()
        self._open_windows_terminal()

    def _build_ui(self) -> None:
        main = tk.Frame(self.root, padx=16, pady=16)
        main.pack(fill=tk.BOTH, expand=True)

        robot_row = tk.Frame(main)
        robot_row.pack(fill=tk.X)

        tk.Label(robot_row, text="Robot name:").pack(side=tk.LEFT)

        self.robot_name_var = tk.StringVar()
        entry = tk.Entry(robot_row, textvariable=self.robot_name_var, width=36)
        entry.pack(side=tk.LEFT, padx=(8, 8), fill=tk.X, expand=True)
        entry.focus_set()

        connect_button = tk.Button(robot_row, text="Connect", command=self.connect_to_robot)
        connect_button.pack(side=tk.RIGHT)

        api_frame = tk.LabelFrame(main, text="API Frame", padx=12, pady=12)
        api_frame.pack(fill=tk.X, pady=(14, 10))

        tk.Button(
            api_frame,
            text="Start Robot_API",
            command=self.start_robot_api,
            width=20,
        ).pack(side=tk.LEFT, padx=(0, 8))

        tk.Button(
            api_frame,
            text="Open Robot_API",
            command=self.open_robot_api_container,
            width=20,
        ).pack(side=tk.LEFT, padx=(0, 8))

        tk.Button(
            api_frame,
            text="Run Roslaunch",
            command=self.run_roslaunch,
            width=20,
        ).pack(side=tk.LEFT)

        tilt_frame = tk.LabelFrame(main, text="Tilt Frame", padx=12, pady=12)
        tilt_frame.pack(fill=tk.X, pady=(0, 10))

        tk.Button(
            tilt_frame,
            text="Tilt System- State",
            command=self.get_tilt_status,
            width=20,
        ).pack(side=tk.LEFT)

        self.status_var = tk.StringVar(value="Ready")
        tk.Label(main, textvariable=self.status_var, fg="#444").pack(anchor="w", pady=(8, 0))

    def _open_windows_terminal(self) -> None:
        if sys.platform != "win32":
            self.status_var.set("Terminal auto-open works on Windows only.")
            return

        try:
            self.terminal_process = subprocess.Popen(
                ["cmd", "/K"],
                stdin=subprocess.PIPE,
                text=True,
                creationflags=subprocess.CREATE_NEW_CONSOLE,
            )
            self.status_var.set("Terminal opened.")
        except Exception as exc:
            self.terminal_process = None
            self.status_var.set("Failed to open terminal.")
            messagebox.showerror("Terminal Error", f"Could not open terminal: {exc}")

    def _ensure_terminal(self) -> bool:
        if sys.platform != "win32":
            self.status_var.set("Terminal automation is available on Windows only.")
            return False

        if self.terminal_process is None or self.terminal_process.poll() is not None:
            self._open_windows_terminal()

        return self.terminal_process is not None and self.terminal_process.stdin is not None

    def _send_command_to_terminal(self, command: str) -> None:
        if not self._ensure_terminal():
            messagebox.showerror("No terminal", "Could not create or access a terminal window.")
            return

        assert self.terminal_process is not None and self.terminal_process.stdin is not None

        try:
            self.terminal_process.stdin.write(command + "\n")
            self.terminal_process.stdin.flush()
            self.status_var.set(f"Sent: {command}")
        except (BrokenPipeError, OSError, ValueError):
            self.terminal_process = None
            if not self._ensure_terminal():
                self.status_var.set("Terminal unavailable.")
                return

            assert self.terminal_process is not None and self.terminal_process.stdin is not None
            self.terminal_process.stdin.write(command + "\n")
            self.terminal_process.stdin.flush()
            self.status_var.set(f"Sent (new terminal): {command}")
        except Exception as exc:
            self.status_var.set("Failed to send command.")
            messagebox.showerror("Command Error", f"Could not send command: {exc}")

    def _robot_name(self) -> str | None:
        robot_name = self.robot_name_var.get().strip()
        if not robot_name:
            messagebox.showwarning("Missing robot name", "Please enter a robot name.")
            return None
        return robot_name

    def _send_ssh_then(self, *commands: str) -> None:
        robot_name = self._robot_name()
        if robot_name is None:
            return

        self._send_command_to_terminal(f"ssh -tt gideon@{robot_name}")
        for command in commands:
            self._send_command_to_terminal(command)

    def connect_to_robot(self) -> None:
        self._send_ssh_then()

    def start_robot_api(self) -> None:
        self._send_ssh_then("docker start gideon_robot_api_cont")

    def open_robot_api_container(self) -> None:
        self._send_ssh_then("docker exec -it gideon_robot_api_cont bash")

    def run_roslaunch(self) -> None:
        self._send_ssh_then(
            "docker exec -it gideon_robot_api_cont bash",
            (
                "roslaunch trailerbot_mitsubishi_ros "
                "trailerbot_mitsubishi_ros_node_karbon_beckhoff.launch"
            ),
        )

    def get_tilt_status(self) -> None:
        self._send_ssh_then(
            "docker exec -it gideon_robot_api_cont bash",
            "rostopic echo /mitsubishi_atul1/robot/tilt_system/state",
        )


if __name__ == "__main__":
    root = tk.Tk()
    app = RobotConnectorApp(root)
    root.mainloop()
