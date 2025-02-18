import os
import subprocess

from resistorkit.util.logging import Colors


class CommandHelper:
    def __init__(self, root_path=os.getcwd(), ssh_credentials=None, logger=None):
        self.root_path = root_path
        self.ssh_credentials = ssh_credentials
        self.logger = logger

    def cmd(self, cmd: str, remote=False, verbose=False) -> bool:
        """
        Run a command in the shell, optionally on a remote machine. Returns True if the command was successful.
        """
        try:
            if remote and self.ssh_credentials:
                cmd = f"ssh {self.ssh_credentials} '{cmd}'"

            if self.logger:
                self.logger.custom(f"[CMD] {cmd}", Colors.HEADER)

            process = subprocess.Popen(
                cmd,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
                universal_newlines=True,
            )

            while True:
                stdout_line = process.stdout.readline()
                stderr_line = process.stderr.readline()

                if (
                    stdout_line == ""
                    and stderr_line == ""
                    and process.poll() is not None
                ):
                    break
                if stdout_line and verbose and self.logger:
                    self.logger.custom(stdout_line.rstrip(), Colors.SUCCESS)
                if stderr_line and verbose and self.logger:
                    self.logger.custom(stderr_line.rstrip(), Colors.WARNING)

            process.stdout.close()
            process.stderr.close()
            return_code = process.wait()

            return return_code == 0

        except KeyboardInterrupt:
            if self.logger:
                self.logger.warning("Interrupt...")
            return True
        except Exception as e:
            if self.logger:
                self.logger.error(f"Command failed: {str(e)}")
            return False
