import subprocess
import sys
import tkinter as tk
from tkinter import messagebox


class RobotConnectorApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("ROS Robot Connector")
        self.root.geometry("560x180")
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
        connect_button.grid(row=1, column=1, pady=(6, 0), sticky="e")

        open_api_button = tk.Button(
            frame,
            text="Open robotAPI container",
            command=self.open_robot_api_container,
        )
        open_api_button.grid(row=1, column=2, pady=(6, 0), sticky="e")

        self.status_var = tk.StringVar(value="Ready")
        tk.Label(frame, textvariable=self.status_var, fg="#444").grid(
            row=2, column=0, columnspan=3, pady=(12, 0), sticky="w"
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
            self.status_var.set("Failed to open terminal.")
            messagebox.showerror("Terminal Error", f"Could not open terminal: {exc}")

    def _send_command_to_terminal(self, command: str, status_text: str) -> None:
        if self.terminal_process is None or self.terminal_process.stdin is None:
            messagebox.showerror(
                "No terminal",
                "The terminal is not available. This feature requires running on Windows.",
            )
            self.status_var.set("Terminal not available.")
            return

        try:
            self.terminal_process.stdin.write(command + "\n")
            self.terminal_process.stdin.flush()
            self.status_var.set(status_text)
        except Exception as exc:
            self.status_var.set("Failed to send command.")
            messagebox.showerror("Command Error", f"Could not send command: {exc}")

    def connect_to_robot(self) -> None:
        robot_name = self.robot_name_var.get().strip()
        if not robot_name:
            messagebox.showwarning("Missing robot name", "Please enter a robot name.")
            return

        # -tt forces pseudo-terminal allocation to avoid stdin not-a-terminal warnings.
        command = f"ssh -tt gideon@{robot_name}"
        self._send_command_to_terminal(command, f"Sent: {command}")

    def open_robot_api_container(self) -> None:
        command = "docker exec -it gideon_robot_api_cont bash"
        self._send_command_to_terminal(command, f"Sent: {command}")


if __name__ == "__main__":
    root = tk.Tk()
    app = RobotConnectorApp(root)
    root.mainloop()
