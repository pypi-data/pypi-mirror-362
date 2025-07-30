import httpx, os
from io import IOBase
from typing import Iterator, List, Literal, Optional, Union, overload
from agentbox.sandbox.filesystem.filesystem import WriteEntry, EntryInfo, map_file_type, FileType
from agentbox.connection_config import ConnectionConfig, Username, KEEPALIVE_PING_HEADER, KEEPALIVE_PING_INTERVAL_SEC
from agentbox.envd.api import ENVD_API_FILES_ROUTE, handle_envd_api_exception
from agentbox.envd.filesystem import filesystem_connect, filesystem_pb2
from agentbox.envd.rpc import authentication_header, handle_rpc_exception
from agentbox.exceptions import SandboxException, TemplateException, InvalidArgumentException
from agentbox.envd.versions import ENVD_VERSION_RECURSIVE_WATCH
from packaging.version import Version
import agentbox_connect as connect
from agentbox.sandbox_sync.commands_ssh.command_ssh import SSHCommands
from agentbox.sandbox_sync.filesystem_ssh.watch_handle_ssh import SSHSyncWatchHandle

class SSHSyncFilesystem:
    """
    Module for interacting with the filesystem in the sandbox (sync version).
    """

    def __init__(
        self,
        ssh_host: str,
        ssh_port: int,
        ssh_username: str,
        ssh_password: str,
        connection_config: ConnectionConfig,
        commands: SSHCommands,
        watch_commands: SSHCommands,
    ) -> None:
        self._ssh_host = ssh_host
        self._ssh_port = ssh_port
        self._ssh_username = ssh_username
        self._ssh_password = ssh_password
        self._connection_config = connection_config
        self._commands = commands
        self._watch_commands = watch_commands

    @overload
    def read(self, path: str, format: Literal["text"] = "text", user: Username = "user", request_timeout: Optional[float] = None) -> str: ...
    @overload
    def read(self, path: str, format: Literal["bytes"], user: Username = "user", request_timeout: Optional[float] = None) -> bytearray: ...
    @overload
    def read(self, path: str, format: Literal["stream"], user: Username = "user", request_timeout: Optional[float] = None) -> Iterator[bytes]: ...

    def read(self, path, format="text", user="user", request_timeout=None):
        cmd = f"cat {path}"
        result = self._commands.run(cmd)
        return result.stdout

    @overload
    def write(self, path: str, data: Union[str, bytes, IOBase], user: Username = "user", request_timeout: Optional[float] = None) -> EntryInfo: ...
    @overload
    def write(self, files: List[WriteEntry], user: Optional[Username] = "user", request_timeout: Optional[float] = None) -> List[EntryInfo]: ...

    def write(self, path_or_files, data_or_user="user", user_or_request_timeout=None, request_timeout_or_none=None):
        path, write_files, user, request_timeout = None, [], "user", None
        if isinstance(path_or_files, str):
            if isinstance(data_or_user, list):
                raise Exception("Cannot specify both path and list of files")
            path = path_or_files
            write_files = [{"path": path_or_files, "data": data_or_user}]
            user = user_or_request_timeout or "user"
            request_timeout = request_timeout_or_none
        else:
            write_files = path_or_files
            user = data_or_user
            request_timeout = user_or_request_timeout

        results = []
        for file in write_files:
            file_path, file_data = file["path"], file["data"]
            # Ensure directory exists
            dir_path = os.path.dirname(file_path)
            if dir_path:
                self.make_dir(dir_path, user, request_timeout)

            # Convert data to string or bytes
            if isinstance(file_data, str):
                data_str = file_data
            elif isinstance(file_data, bytes):
                data_str = file_data.decode('utf-8', 'replace')
            elif isinstance(file_data, IOBase):
                data_str = file_data.read()
                if isinstance(data_str, bytes):
                    data_str = data_str.decode('utf-8', 'replace')
            else:
                raise ValueError(f"Unsupported data type for file {file_path}")
            
            # Write file using echo and redirection
            # Escape the data to handle special characters
            escaped_data = data_str.replace("'", "'\"'\"'")
            cmd = f"echo '{escaped_data}' > '{file_path}'"
            runRet = self._commands.run(cmd)
            if runRet.exit_code != 0:
                raise Exception(f"Failed to write file {file_path}")
            
            # Get file info
            file_info = self._get_file_info(file_path)
            results.append(file_info)

        if len(results) == 1 and path:
            return results[0]
        else:
            return results

    def list(self, path, depth=1, user="user", request_timeout=None) -> List[EntryInfo]:
        """
        List entries in a directory.

        :param path: Path to the directory
        :param depth: Depth of the directory to list
        :param user: Run the operation as this user
        :param request_timeout: Timeout for the request in **seconds**

        :return: List of entries in the directory
        """
        if depth is not None and depth < 1:
            raise InvalidArgumentException("depth should be at least 1")
        
        # Use ls command to list directory contents
        if depth == 1:
            cmd = f"ls -la '{path}' 2>/dev/null || true"
        else:
            # For deeper listing, use find with maxdepth
            cmd = f"find '{path}' -maxdepth {depth} -type f -o -type d 2>/dev/null || true"

        result = self._commands.run(cmd)
        if result.exit_code != 0:
            raise Exception(f"Failed to list directory {path}")
        
        entries = []
        for line in result.stdout.strip().split('\n'):
            if line.strip():
                if depth == 1:
                    # Parse ls output
                    parts = line.strip().split()
                    if len(parts) >= 8:
                        file_type = parts[0][0]
                        file_name = parts[-1]
                        if file_name not in ['.', '..']:
                            file_path = os.path.join(path, file_name)
                            if file_type == 'd':
                                entries.append(EntryInfo(
                                    name=file_name,
                                    type=FileType.DIR,
                                    path=file_path
                                ))
                            else:
                                entries.append(EntryInfo(
                                    name=file_name,
                                    type=FileType.FILE,
                                    path=file_path
                                ))
                else:
                    # Parse find output
                    parts = line.strip().split()
                    if len(parts) >= 1:
                        file_path = parts[0]
                        file_name = os.path.basename(file_path)
                        if os.path.isdir(file_path):
                            entries.append(EntryInfo(
                                name=file_name,
                                type=FileType.DIR,
                                path=file_path
                            ))
                        else:
                            entries.append(EntryInfo(
                                name=file_name,
                                type=FileType.FILE,
                                path=file_path
                            ))
        
        return entries

    def exists(self, path, user="user", request_timeout=None) -> bool:
        """
        Check if a file or a directory exists.

        :param path: Path to a file or a directory
        :param user: Run the operation as this user
        :param request_timeout: Timeout for the request in **seconds**

        :return: `True` if the file or directory exists, `False` otherwise
        """
        result = self._commands.run(f"test -e '{path}' && echo 'exists' || echo 'not_exists'")
        if 'not_exists' in result.stdout.strip():
            return False
        elif 'exists' in result.stdout.strip():
            return True
        else:
            raise Exception(f"Failed to check existence of {path}")

    def remove(self, path, user="user", request_timeout=None):
        """
        Remove a file or a directory.

        :param path: Path to a file or a directory
        :param user: Run the operation as this user
        :param request_timeout: Timeout for the request in **seconds**
        """
        result = self._commands.run(f"rm -rf '{path}'")
        if result.exit_code != 0:
            raise Exception(f"Failed to remove {path}")

    def rename(self, old_path, new_path, user="user", request_timeout=None) -> EntryInfo:
        """
        Rename a file or directory.

        :param old_path: Path to the file or directory to rename
        :param new_path: New path to the file or directory
        :param user: Run the operation as this user
        :param request_timeout: Timeout for the request in **seconds**

        :return: Information about the renamed file or directory
        """
        result = self._commands.run(f"mv '{old_path}' '{new_path}'")
        if result.exit_code != 0:
            raise Exception(f"Failed to rename {old_path} to {new_path}")
        
        return self._get_file_info(new_path)

    def make_dir(
        self,
        path: str,
        user: Username = "user",
        request_timeout: Optional[float] = None,
    ) -> bool:
        """
        Create a new directory and all directories along the way if needed on the specified path.

        :param path: Path to a new directory. For example '/dirA/dirB' when creating 'dirB'.
        :param user: Run the operation as this user
        :param request_timeout: Timeout for the request in **seconds**

        :return: `True` if the directory was created, `False` if the directory already exists
        """
        # Check if directory already exists
        if self.exists(path, user, request_timeout):
            return False

        self._commands.run(f"mkdir -p '{path}'")
        return True

    def watch_dir(self, path, on_event, on_exit=None, user="user", request_timeout=None, timeout=60, recursive=False):
        """
        Watch directory for filesystem events.

        :param path: Path to a directory to watch
        :param on_event: Callback to call on each event in the directory
        :param on_exit: Callback to call when the watching ends
        :param user: Run the operation as this user
        :param request_timeout: Timeout for the request in **seconds**
        :param timeout: Timeout for the watch operation in **seconds**. Using `0` will not limit the watch time
        :param recursive: Watch directory recursively

        :return: `SSHWatchHandle` object for stopping watching directory
        """
        return SSHSyncWatchHandle(
            commands=self._watch_commands,
            path=path,
            on_event=on_event,
            on_exit=on_exit,
            recursive=recursive,
        )

        # 返回同步 WatchHandle，需要你写
        from agentbox.sandbox.filesystem.watch_handle import WatchHandle
        return WatchHandle(events=events, on_event=on_event, on_exit=on_exit)

    def _get_file_info(self, path: str) -> EntryInfo:
            """Get file information"""
            result = self._commands.run(f"ls -ld '{path}' 2>/dev/null || true")
            if result.exit_code != 0:
                raise Exception(f"File {path} not found")

            parts = result.stdout.strip().split()
            if len(parts) >= 8:
                file_type = parts[0][0]
                file_name = os.path.basename(path)
                
                if file_type == 'd':
                    return EntryInfo(
                        name=file_name,
                        type=FileType.DIR,
                        path=path
                    )
                else:
                    return EntryInfo(
                        name=file_name,
                        type=FileType.FILE,
                        path=path
                    )
            else:
                raise Exception(f"Could not parse file info for {path}")
