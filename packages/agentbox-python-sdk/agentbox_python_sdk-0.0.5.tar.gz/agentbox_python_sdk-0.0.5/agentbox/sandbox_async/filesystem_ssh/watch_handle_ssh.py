import asyncio
import inspect
import os
from typing import Any, Optional

from agentbox.sandbox.filesystem.watch_handle import FilesystemEvent
from agentbox.sandbox_async.utils import OutputHandler
from agentbox.sandbox_async.commands_ssh.command_ssh import SSHCommands


class SSHAsyncWatchHandle:
    """
    SSH-based handle for watching a directory in the sandbox filesystem.

    Use `.stop()` to stop watching the directory.
    """

    def __init__(
        self,
        commands: SSHCommands,
        path: str,
        on_event: OutputHandler[FilesystemEvent],
        on_exit: Optional[OutputHandler[Exception]] = None,
        recursive: bool = False,
    ):
        self._commands = commands
        self._path = path
        self._on_event = on_event
        self._on_exit = on_exit
        self._recursive = recursive
        self._running = True
        self._last_state = {}

        self._wait = asyncio.create_task(self._handle_events())

    async def stop(self):
        """
        Stop watching the directory.
        """
        self._running = False
        self._wait.cancel()

    async def _get_file_state(self):
        """Get current state of files in the directory"""
        try:
            # Use find command to get file list
            if self._recursive:
                cmd = f"find {self._path} -type f -o -type d 2>/dev/null || true"
            else:
                cmd = f"ls -la {self._path} 2>/dev/null || true"
            
            result = await self._commands.run(cmd)
            if result.exit_code != 0:
                raise Exception(f"Error getting file state: {result.stderr}")

            current_state = {}
            for line in result.stdout.strip().split('\n'):
                if line.strip():
                    if self._recursive:
                        # Parse find output
                        parts = line.strip().split()
                        if len(parts) >= 1:
                            file_path = parts[0]
                            if os.path.isfile(file_path):
                                current_state[file_path] = 'file'
                            elif os.path.isdir(file_path):
                                current_state[file_path] = 'dir'
                    else:
                        # Parse ls output
                        parts = line.strip().split()
                        if len(parts) >= 8:
                            file_type = parts[0][0]
                            file_name = parts[-1]
                            if file_name not in ['.', '..']:
                                file_path = os.path.join(self._path, file_name)
                                if file_type == 'd':
                                    current_state[file_path] = 'dir'
                                else:
                                    current_state[file_path] = 'file'
            
            return current_state
        except Exception:
            return {}

    async def _detect_changes(self, old_state, new_state):
        """Detect changes between old and new file states"""
        changes = []
        
        # Check for new files
        for path, file_type in new_state.items():
            if path not in old_state:
                changes.append(FilesystemEvent(
                    name=os.path.basename(path),
                    type=file_type
                ))
        
        # Check for deleted files
        for path, file_type in old_state.items():
            if path not in new_state:
                changes.append(FilesystemEvent(
                    name=os.path.basename(path),
                    type=file_type
                ))
        
        return changes

    async def _iterate_events(self):
        """Iterate through filesystem events"""
        while self._running:
            try:
                current_state = await self._get_file_state()
                changes = await self._detect_changes(self._last_state, current_state)
                
                for change in changes:
                    yield change
                
                self._last_state = current_state
                await asyncio.sleep(1)  # Check every second
                
            except Exception as e:
                if self._on_exit:
                    cb = self._on_exit(e)
                    if inspect.isawaitable(cb):
                        await cb
                break

    async def _handle_events(self):
        """Handle filesystem events"""
        try:
            async for event in self._iterate_events():
                if not self._running:
                    break
                    
                cb = self._on_event(event)
                if inspect.isawaitable(cb):
                    await cb
        except Exception as e:
            if self._on_exit:
                cb = self._on_exit(e)
                if inspect.isawaitable(cb):
                    await cb


# Alias for backward compatibility
AsyncWatchHandle = SSHAsyncWatchHandle