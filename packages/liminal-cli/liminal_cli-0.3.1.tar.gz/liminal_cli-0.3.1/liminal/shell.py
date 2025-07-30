
import os
from pathlib import Path
import pwd
import subprocess
import psutil



class Shell:


	def __init__(self):
		self.exec_path = self.get_default_shell_path()
		self.name = self.exec_path.name
		self.config_file = Path.home() / '.bashrc' if self.is_bash() else Path.home() / '.zshrc'

		# {
		# 	'bash': ['.bashrc', '.bash_profile', '.bash_login', '.profile'],
		# 	'zsh': ['.zshrc', '.zshenv', '.zprofile', '.zlogin']
		# }


	def dict(self):
		return {
			'name': self.exec_path.name,
			'exec_path': self.exec_path.as_posix(),
			'version': subprocess.run([self.exec_path, '--version'], check=False, capture_output=True, text=True, timeout=1).stdout,
			'envvar_SHLVL': os.environ.get('SHLVL'),
			'envvar_TERM': os.environ.get('TERM'),
			'envvar_PS1': os.environ.get('PS1'), # certain PS1 might not match for our command testing (hack.run_logingcommand pexpect.)
		}

	def is_supported(self):
		return self.exec_path.name in ['bash', 'zsh']
	
	def is_bash(self):
		return self.exec_path.name == 'bash'

	def get_default_shell_path(self) -> Path:
		"""Gets the default shell for the current user."""
		user_id = os.getuid()
		user_info = pwd.getpwuid(user_id)
		return Path(user_info.pw_shell)
		
	def this_process_shell_path(self) -> Path:
		parent_pid = os.getppid()
		parent_process = psutil.Process(parent_pid)
		# .exe() gives the full path, .name() just the command name (e.g., 'bash')
		# We prefer .exe() for uniqueness
		shell_exe = parent_process.exe()
		return Path(shell_exe)
