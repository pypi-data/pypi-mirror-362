import io
import platform
import subprocess
import sys
import threading
import time
import traceback
import warnings

from cryptography.utils import CryptographyDeprecationWarning

with warnings.catch_warnings():
    warnings.simplefilter("ignore", CryptographyDeprecationWarning)
    import paramiko
    import paramiko.ssh_exception

from .utils import AuthenticationFailed, Singleton, SSHException, UnableToConnect


class SSHClient(metaclass=Singleton):
    TIMEOUT = 360

    def __init__(self, hostname, username, password=None, port=22, key_file=None):
        self.hostname = hostname
        self.port = port
        self.username = username
        self.password = password
        self.key_file = key_file
        self.client = None

    @classmethod
    def change_default_timeout(cls, new_timeout):
        cls.TIMEOUT = new_timeout

    def login(self):
        """Establish an SSH connection to the server."""
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            if self.key_file:
                key = paramiko.RSAKey.from_private_key_file(self.key_file)
                self.client.connect(
                    self.hostname, port=self.port, username=self.username, pkey=key
                )
            else:
                self.client.connect(
                    self.hostname,
                    port=self.port,
                    username=self.username,
                    password=self.password,
                )
            print("Connected successfully.")
        except paramiko.AuthenticationException:
            print("Authentication failed.")
            raise AuthenticationFailed(
                "Authentication failed. Please check credentials."
            )
        except paramiko.SSHException as sshException:
            print(f"Unable to establish SSH connection: {sshException}")
            raise SSHException(f"Unable to establish SSH connection: {sshException}")
        except Exception as e:
            print(f"Exception in connecting: {e}")
            raise UnableToConnect(
                f"Unable to connect {self.hostname}. Please check correct details"
            )

    def run_command(self, command, timeout=TIMEOUT, verbose=True):
        """Run a command on the remote server with timeout and live output."""
        if self.client:
            try:
                if verbose:
                    sys.stdout = sys.__stdout__
                else:
                    sys.stdout = io.StringIO()

                def target():
                    nonlocal output, errors
                    try:
                        print(f"\nRun_Command: {command}")
                        stdin, stdout, stderr = self.client.exec_command(command)
                        start_time = time.time()
                        while not stdout.channel.exit_status_ready():
                            if time.time() - start_time > timeout:
                                # Timeout occurred, kill the command
                                stdout.channel.close()  # Send termination signal
                                print(
                                    f"\nCommand timed out after {timeout} seconds and has been terminated."
                                )
                                break
                            if stdout.channel.recv_ready():
                                sys.stdout.write(stdout.channel.recv(1024).decode())
                                sys.stdout.flush()
                            if stderr.channel.recv_ready():
                                sys.stderr.write(stderr.channel.recv(1024).decode())
                                sys.stderr.flush()
                            time.sleep(0.5)
                        output = stdout.read().decode()
                        errors = stderr.read().decode()
                    except Exception as e:
                        errors = str(e)

                output = ""
                errors = ""
                thread = threading.Thread(target=target)
                thread.start()

                start_time = time.time()
                while thread.is_alive():
                    if time.time() - start_time > timeout:
                        # Timeout has occurred
                        thread.join(timeout=0)  # Ensure the thread terminates
                        break
                    time.sleep(0.5)

                thread.join()  # Wait for the thread to finish

                if output:
                    print("\nOutput:")
                    print(output)
                if errors:
                    print("Errors:")
                    print(errors)

                return output, errors
            except Exception as why:
                print("Got exception while running cmd: ")
                print(f"Exception: {why}")
            finally:
                sys.stdout = sys.__stdout__
        else:
            print("Connection not established. Call login() first.")

    def get_remote_os(self):
        """Detect the remote OS and return as a dict: {'os': 'windows'} or {'os': 'linux'}"""
        if not self.client:
            print("Connection not established. Call login() first.")
            return {"os": None}
        try:
            # Try Windows command
            out, err = self.run_command("ver", verbose=False)
            if out and "Microsoft" in out:
                return {"os": "windows"}
            # Try Linux command
            out, err = self.run_command("uname", verbose=False)
            if out and "Linux" in out:
                return {"os": "linux"}
        except Exception as e:
            print(f"Error detecting remote OS: {e}")
        return {"os": None}

    def send_File(self, file, path=None):
        import os

        if self.client:
            try:
                if not os.path.isfile(file):
                    print(f"Local file does not exist: {file}")
                    return None
                print(f"Sending {file} to remote machine")
                sftp = self.client.open_sftp()
                remote_os = self.get_remote_os().get("os")
                print(f"Detected remote OS: {remote_os}")
                if path:
                    if remote_os == "windows":
                        self.run_command(f"mkdir {path}", verbose=False)
                        remote_script_path = f"{path}\\{os.path.basename(file)}"
                    else:
                        self.run_command(f"mkdir -p {path}", verbose=False)
                        remote_script_path = f"{path}/{os.path.basename(file)}"
                    sftp.put(file, remote_script_path)
                else:
                    if remote_os and remote_os.lower() == "windows":
                        temp_path = "C:\\temp"
                        self.run_command(f"mkdir {temp_path}", verbose=False)
                        remote_script_path = f"{temp_path}\\{os.path.basename(file)}"
                    elif remote_os and remote_os.lower() == "linux":
                        # Create temp directory and get its absolute path
                        out, err = self.run_command("mktemp -d", verbose=False)
                        temp_path = out.strip()
                        if not temp_path:
                            print("Failed to create temp directory on remote Linux.")
                            return None
                        remote_script_path = f"{temp_path}/{os.path.basename(file)}"
                        print(f"Remote script path: {remote_script_path}")
                    else:
                        print("Unknown remote OS. Cannot determine temp path.")
                        return None
                    sftp.put(file, remote_script_path)
                print(f"Sent file : {remote_script_path}")
                return remote_script_path
            except Exception as e:
                print(f"Failed to send file: {e}")
                return None
            finally:
                try:
                    sftp.close()
                except Exception:
                    pass
        else:
            print("Connection not established. Call login() first.")
            return None

    def receive_File(self, remote_path, local_path):
        """Receive a file from the remote machine to the local machine."""
        if self.client:
            try:
                print(f"Receiving {remote_path} from remote machine")
                sftp = self.client.open_sftp()

                # Retrieve the file from the remote machine
                sftp.get(remote_path, local_path)

                print(f"Received file and saved as: {local_path}")
                return True
            except Exception as e:
                print(f"Failed to receive file: {e}")
                return False
            finally:
                sftp.close()
        else:
            print("Connection not established. Call login() first.")
            return None

    def run_python_file(self, script_file, timeout=TIMEOUT):
        """Run a Python script file on the remote server, using python3 for Linux and python for Windows."""

        if self.client:
            try:
                remote_script_path = self.send_File(script_file)
                print(f"Running remote script: {remote_script_path}")
                if not remote_script_path:
                    print("Failed to send script file to remote machine.")
                    return False

                remote_os = self.get_remote_os().get("os")
                if remote_os == "linux":
                    remote_command = f"python3 {remote_script_path}"
                elif remote_os == "windows":
                    remote_command = f"python {remote_script_path}"
                else:
                    print("Unknown remote OS. Cannot determine Python interpreter.")
                    return False

                output, errors = self.run_command(remote_command, timeout=timeout)
                if errors:
                    print("Errors while executing remote function:")
                    print(errors)
                return True

            except Exception as e:
                print(f"Failed to execute remote function: {e}")
                return False
        else:
            print("Connection not established. Call login() first.")
            return None

    def run_powershell_command(self, command, timeout=360):
        """Run a PowerShell command on the remote server."""
        if not self.client:
            print("Connection not established. Call login() first.")
            return None

        remote_os = self.get_remote_os().get("os")
        try:
            if remote_os == "windows":
                ps_command = f'powershell -Command "{command}"'
                return self.run_command(ps_command, timeout)
            elif remote_os == "linux":
                # Check if pwsh is available
                out, err = self.run_command("which pwsh", verbose=False)
                if out.strip():
                    ps_command = f'pwsh -Command "{command}"'
                    return self.run_command(ps_command, timeout)
                else:
                    print(
                        "PowerShell (pwsh) is not installed on the remote Linux machine. Please install the PowerShell package."
                    )
                    return None
            else:
                print("Unknown remote OS. Cannot run PowerShell command.")
                return None
        except Exception as e:
            print(f"Failed to execute remote PowerShell command: {e}")
            return None

    def run_ansible_playbook(
        self,
        playbook_or_command,
        extra_vars=None,
        inventory_file=None,
        out=None,
        display=True,
    ):
        """
        Runs an Ansible playbook or an ad-hoc command targeting the remote host.
        Ansible must be installed on the machine running this script.
        This method only runs on a Linux host.

        Args:
            playbook_or_command (str): Path to playbook file or ad-hoc command.
            extra_vars (str, optional): Extra variables for Ansible.
            inventory_file (str, optional): Path to inventory file. If None, a temporary inventory is created.
        """
        if platform.system().lower() != "linux":
            print("Error: This function can only be run on a Linux system.")
            return False

        import os
        import shutil
        import subprocess
        import tempfile

        is_playbook = os.path.isfile(playbook_or_command)
        executable = "ansible-playbook" if is_playbook else "ansible"

        if not shutil.which(executable):
            print(f"Error: {executable} command not found. Please install Ansible.")
            return False

        if is_playbook and not os.path.isfile(playbook_or_command):
            print(f"Error: Playbook file not found at {playbook_or_command}")
            return False

        temp_inventory_path = None
        if inventory_file is None:
            inventory_content = f"{self.hostname} ansible_port={self.port} ansible_user={self.username} ansible_connection=paramiko\n"
            with tempfile.NamedTemporaryFile(
                mode="w", delete=False, suffix=".ini"
            ) as inv_file:
                temp_inventory_path = inv_file.name
                inv_file.write(inventory_content)
            inventory_path = temp_inventory_path
        else:
            inventory_path = inventory_file

        try:
            if is_playbook:
                command = [executable, "-i", inventory_path, playbook_or_command]
            else:
                # Ad-hoc command
                if inventory_file is None:
                    command = [
                        executable,
                        self.hostname,
                        "-i",
                        inventory_path,
                        "-m",
                        "shell",
                        "-a",
                        playbook_or_command,
                    ]
                else:
                    command = [
                        executable,
                        "all",
                        "-i",
                        inventory_path,
                        "-m",
                        "shell",
                        "-a",
                        playbook_or_command,
                    ]

            extra_vars_list = []
            if self.password:
                extra_vars_list.append(
                    "ansible_password=****** ansible_become_password=******"
                )
            if extra_vars:
                extra_vars_list.append(extra_vars)
            if extra_vars_list:
                command_to_print = command + ["--extra-vars", " ".join(extra_vars_list)]
            else:
                command_to_print = command.copy()
            if self.key_file:
                command_to_print.extend(["--private-key", self.key_file])

            # Build the real command (with real password) for execution
            real_extra_vars_list = []
            if self.password:
                real_extra_vars_list.append(
                    f"ansible_password={self.password} ansible_become_password={self.password}"
                )
            if extra_vars:
                real_extra_vars_list.append(extra_vars)
            real_command = command.copy()
            if real_extra_vars_list:
                real_command.extend(["--extra-vars", " ".join(real_extra_vars_list)])
            if self.key_file:
                real_command.extend(["--private-key", self.key_file])

            print(f"Running Ansible: {' '.join(command_to_print)}")

            # Set environment for Ansible to use UTF-8 and disable host key checking
            ansible_env = os.environ.copy()
            ansible_env["PYTHONIOENCODING"] = "utf-8"
            ansible_env["ANSIBLE_HOST_KEY_CHECKING"] = "False"

            # Open output file if specified
            file_handle = None
            if out is not None:
                file_handle = open(out, "w", encoding="utf-8")

            try:
                process = subprocess.Popen(
                    real_command,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    env=ansible_env,
                    bufsize=1,
                )

                if display:
                    print("--- Ansible Output ---")

                while True:
                    output = process.stdout.readline()
                    if output == "" and process.poll() is not None:
                        break
                    if output:
                        if display:
                            print(output, end="")
                        if file_handle:
                            file_handle.write(output)

                stderr_output = process.stderr.read()
                if stderr_output:
                    if display:
                        print("--- Ansible Errors ---")
                        print(stderr_output)
                    if file_handle:
                        file_handle.write("--- Ansible Errors ---\n")
                        file_handle.write(stderr_output)

                result = process.wait()
                return result == 0
            finally:
                if file_handle:
                    file_handle.close()

        except Exception as e:
            print(f"An error occurred while running Ansible: {e}")
            return False
        finally:
            if temp_inventory_path and os.path.exists(temp_inventory_path):
                os.remove(temp_inventory_path)

    def ping(self):
        """Check the connectivity to the remote server by running the ping command locally."""

        count_flag = "-n" if platform.system().lower() == "windows" else "-c"
        try:
            result = subprocess.run(
                ["ping", count_flag, "5", self.hostname],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=30,
            )
            print(result.stdout)
            if result.returncode == 0:
                return True
            else:
                print(result.stderr)
                return False
        except Exception as e:
            print(f"Ping failed: {e}")
            return False

    def reboot(self, wait_until=300):
        """Reboot remote machine immediately, using appropriate command for Windows or Linux (no sudo)."""
        print("Rebooting remote machine")
        try:
            remote_os = self.get_remote_os().get("os")
            if remote_os == "windows":
                # Use 'shutdown /r /t 0' for Windows, which does not require sudo
                reboot_cmd = "shutdown /r /t 0"
            elif remote_os == "linux":
                # Try 'reboot' first, which does not require sudo on most systems
                reboot_cmd = f"echo {self.password} | sudo -S  reboot"
            else:
                print("Unknown remote OS. Cannot determine reboot command.")
                return False

            out, err = self.run_command(reboot_cmd, verbose=False)
            time.sleep(20)
            self.wait(timeout=wait_until)
            return not err
        except Exception as e:
            print(f"Unexpected error: {e}")
            print(traceback.format_exc())
        return False

    def wait(self, timeout=300, interval=10):
        """Wait until the remote machine is back online after a reboot.

        Args:
            timeout (int): Maximum time to wait in seconds.
            interval (int): Interval between connection attempts in seconds.
        """
        print("Waiting for the remote machine...")
        start_time = time.time()

        while (time.time() - start_time) < timeout:
            try:
                # Attempt to establish a new SSH connection
                self.client = paramiko.SSHClient()
                self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                self.client.connect(
                    hostname=self.hostname,
                    port=self.port,
                    username=self.username,
                    password=self.password,
                    timeout=10,
                )
                print("Remote machine is back online.")
                return True
            except (
                TimeoutError,
                paramiko.ssh_exception.SSHException,
                paramiko.ssh_exception.NoValidConnectionsError,
            ) as e:
                # If connection failed, wait for the interval period before retrying
                print(
                    f"Machine is not reachable yet (Error: {e}). Retrying in {interval} seconds..."
                )
                time.sleep(interval)
            except Exception as e:
                print(f"Unexpected error: {e}")
                print(traceback.format_exc())
                break

        print("Timeout reached. The remote machine did not come back online.")
        return False

    def close(self):
        """Close the SSH connection."""
        if self.client:
            self.client.close()
            print("Connection closed.")
        else:
            print("Connection was not established.")

    def __del__(self):
        """Ensure the SSH connection is closed when the object is deleted."""
        self.close()
