from typing import Optional, Callable, List
import os, time
from agentbox.sandbox.filesystem.watch_handle import FilesystemEvent
from agentbox.sandbox_sync.commands_ssh.command_ssh import SSHCommands
from agentbox import SandboxException


class SSHSyncWatchHandle:
    """
    Watch filesystem events by polling over SSH.
    """

    def __init__(
        self,
        commands: SSHCommands,
        path: str,
        on_event: Callable[[FilesystemEvent], None],
        on_exit: Optional[Callable[[Exception], None]] = None,
        recursive: bool = False,
    ):
        self._commands = commands
        self._path = path
        self._on_event = on_event
        self._on_exit = on_exit
        self._recursive = recursive
        self._running = True
        self._last_state = {}

    def stop(self):
        """
        Stop watching the directory.
        """
        self._running = False

    def _get_file_state(self):
        """
        Get current state of files in the directory.
        """
        try:
            if self._recursive:
                cmd = f"find {self._path} -type f -o -type d 2>/dev/null || true"
            else:
                cmd = f"ls -la {self._path} 2>/dev/null || true"

            result = self._commands.run(cmd)
            if result.exit_code != 0:
                raise Exception(f"Error getting file state: {result.stderr}")

            current_state = {}
            for line in result.stdout.strip().split('\n'):
                if not line.strip():
                    continue
                if self._recursive:
                    file_path = line.strip()
                    if file_path.endswith('/'):
                        current_state[file_path] = 'dir'
                    else:
                        current_state[file_path] = 'file'
                else:
                    parts = line.strip().split()
                    if len(parts) >= 8:
                        file_type = parts[0][0]
                        file_name = parts[-1]
                        if file_name not in ['.', '..']:
                            file_path = os.path.join(self._path, file_name)
                            current_state[file_path] = 'dir' if file_type == 'd' else 'file'
            return current_state
        except Exception:
            return {}

    def _detect_changes(self, old_state, new_state):
        """
        Detect new/deleted files.
        """
        changes = []

        for path, file_type in new_state.items():
            if path not in old_state:
                changes.append(FilesystemEvent(name=os.path.basename(path), type=file_type))

        for path, file_type in old_state.items():
            if path not in new_state:
                changes.append(FilesystemEvent(name=os.path.basename(path), type=file_type))

        return changes

    def watch_loop(self, interval=1):
        """
        Start the loop: keep checking filesystem and call on_event on changes.
        """
        try:
            while self._running:
                current_state = self._get_file_state()
                changes = self._detect_changes(self._last_state, current_state)

                for change in changes:
                    if self._on_event:
                        self._on_event(change)

                self._last_state = current_state
                time.sleep(interval)
        except Exception as e:
            if self._on_exit:
                self._on_exit(e)

    def get_new_events(self) -> List[FilesystemEvent]:
        """
        Get the latest events that have occurred in the watched directory
        since the last call, by comparing current state to the last state.
        """
        if not self._running:
            raise SandboxException("The watcher is already stopped")

        current_state = self._get_file_state()
        changes = self._detect_changes(self._last_state, current_state)

        # 更新 last_state
        self._last_state = current_state

        return changes

