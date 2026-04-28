import subprocess
import sys
import tkinter as tk
from tkinter import messagebox


class RobotConnectorApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("PDK assistant")
        self.root.geometry("680x220")
        self.terminal_process: subprocess.Popen[str] | None = None

        self._build_ui()
        self._open_windows_terminal()

    def _build_ui(self) -> None:
        frame = tk.Frame(self.root, padx=16, pady=16)
        frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(frame, text="Robot name:").grid(row=0, column=0, sticky="w")

        self.robot_name_var = tk.StringVar()
        entry = tk.Entry(frame, textvariable=self.robot_name_var, width=32)
        entry.grid(row=1, column=0, padx=(0, 10), pady=(6, 0), sticky="we")
        entry.focus_set()

        connect_button = tk.Button(frame, text="Connect", command=self.connect_to_robot)
        connect_button.grid(row=1, column=1, padx=(0, 8), pady=(6, 0), sticky="e")

        open_api_button = tk.Button(
            frame,
            text="Open RobotAPI container",
            command=self.open_robot_api_container,
        )
        open_api_button.grid(row=1, column=2, padx=(0, 8), pady=(6, 0), sticky="e")

        tilt_button = tk.Button(
            frame,
            text="Get tilt status",
            command=self.get_tilt_status,
        )
        tilt_button.grid(row=1, column=3, pady=(6, 0), sticky="e")

        self.status_var = tk.StringVar(value="Ready")
        tk.Label(frame, textvariable=self.status_var, fg="#444").grid(
            row=2, column=0, columnspan=4, pady=(12, 0), sticky="w"
        )

        frame.columnconfigure(0, weight=1)

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
            messagebox.showerror(
                "No terminal",
                "Could not create or access a terminal window.",
            )
            return

        assert self.terminal_process is not None and self.terminal_process.stdin is not None

        try:
            self.terminal_process.stdin.write(command + "\n")
            self.terminal_process.stdin.flush()
            self.status_var.set(f"Sent: {command}")
        except (BrokenPipeError, OSError, ValueError):
            # Handles closed terminal (including Windows Errno 22 invalid argument).
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

    def connect_to_robot(self) -> None:
        robot_name = self._robot_name()
        if robot_name is None:
            return

        self._send_command_to_terminal(f"ssh -tt gideon@{robot_name}")

    def open_robot_api_container(self) -> None:
        robot_name = self._robot_name()
        if robot_name is None:
            return

        self._send_command_to_terminal(f"ssh -tt gideon@{robot_name}")
        self._send_command_to_terminal("docker exec -it gideon_robot_api_cont bash")

    def get_tilt_status(self) -> None:
        robot_name = self._robot_name()
        if robot_name is None:
            return

        self._send_command_to_terminal(f"ssh -tt gideon@{robot_name}")
        self._send_command_to_terminal("docker exec -it gideon_robot_api_cont bash")
        self._send_command_to_terminal(
            "rostopic echo /mitsubishi_atul1/robot/tilt_system/state"
        )


if __name__ == "__main__":
    root = tk.Tk()
    app = RobotConnectorApp(root)
    root.mainloop()
