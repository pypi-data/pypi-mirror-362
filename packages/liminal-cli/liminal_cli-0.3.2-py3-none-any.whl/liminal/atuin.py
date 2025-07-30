import logging
import os
from pathlib import Path
import shutil
import sqlite3
import subprocess

from liminal.command_runner import run_command
from liminal.config import Config
from liminal.shell import Shell
from liminal.filesystem import path_metadata

import sqlite3
from liminal.standalone_install_wrapper import LOGGER
import tomlkit

ATUIN_VERSION = 'v18.6.1'

class Paths:
	CONFIG_DIR = Path.home() / '.config/atuin'
	ATUIN_DIR = Path.home() / '.atuin/'
	EXECUTABLE = Path.home() / '.atuin/bin/atuin' # since PATH for env/shell wont be updated
	SHARE = Path.home() / '.local/share/atuin/'
	SQLITE_DB = SHARE / 'history.db'
	CLIENT_CONFIG = CONFIG_DIR / 'config.toml'
	KEY_FILE = SHARE / 'key'

_INSTALLER_SCRIPT = Path(__file__).parent / 'atuin-installer.sh'

def dict_factory(cursor, row):
	fields = [column[0] for column in cursor.description]
	return {key: value for key, value in zip(fields, row)}


def local_history_count() -> int:
	connection = sqlite3.connect(Paths.SQLITE_DB.as_posix())
	cursor = connection.cursor()

	count = cursor.execute('SELECT count(id) FROM history').fetchone()
	return count[0]


def local_history_row(command_to_query: str):
	connection = sqlite3.connect(Paths.SQLITE_DB.as_posix())
	connection.row_factory = dict_factory
	cursor = connection.cursor()
	cursor.execute('SELECT * FROM history WHERE command=?', (command_to_query,))
	return cursor.fetchone()


def backup(outdir: Path):
	shutil.copy(Paths.SQLITE_DB, outdir)

def uninstall_atuin():
	shutil.rmtree(Path.home() / '.atuin')
	shutil.rmtree(Path.home() / '.local/share/atuin')


def get_config() -> dict:
	# atuin's config file isnt created until atuin is ran for the first time
	if not Paths.CLIENT_CONFIG.exists():
		shell_executable = Shell().exec_path
		run_command([shell_executable, '-c', f'{Paths.EXECUTABLE} info'], env=os.environ.copy(), output_level=logging.INFO)
	return tomlkit.parse(Paths.CLIENT_CONFIG.read_text())



def set_config(config: dict):
	Paths.CLIENT_CONFIG.write_text(tomlkit.dumps(config))

def install_atuin(shell_exec: Path | str):
	LOGGER.info('Installing atuin')


	# resp = requests.get(f'https://github.com/atuinsh/atuin/releases/download/{ATUIN_VERSION}/atuin-installer.sh', timeout=10)
	# installer_script = Path('/tmp/atuin-installer.sh')
	# installer_script.write_bytes(resp.content)
	env_copy = os.environ.copy()
	env_copy['ATUIN_NO_MODIFY_PATH'] = '1' # dont update users' PATH, we will do that ourselves
	run_command([shell_exec, _INSTALLER_SCRIPT.as_posix(), '--verbose'], env=env_copy, output_level=logging.INFO)
	

def configure_atuin(sync_address: str):
	if Config.LIMINAL_INSTALLER_SKIP_ATUIN_IMPORT_HISTORY:
		# quick hack to at least allow transition for current atuin users 
		# (they can back up their history.db before install, then copy it back and `atuin sync`)
		pass
	else:
		run_command([Paths.EXECUTABLE, 'import', 'auto'])

	LOGGER.debug('updating atuin sync config')

	atuin_config = get_config()
	atuin_config['sync_address'] =  sync_address
	atuin_config['sync_frequency'] = '0'
	atuin_config['update_check'] = False # we will manage updates ourselves
	set_config(atuin_config)



def is_atuin_installed() -> bool:
	atuin_is_installed_in_path = False
	try:
		subprocess.run(['atuin', '--help'], check=True)
		atuin_is_installed_in_path = True
	except (subprocess.CalledProcessError, FileNotFoundError):
		pass

	atuin_is_installed_in_home = Paths.EXECUTABLE.exists()
	return atuin_is_installed_in_home or atuin_is_installed_in_path


def debug_info() -> dict:
	atuin_is_installed_in_path = False
	try:
		subprocess.run(['atuin', '--help'], check=True, capture_output=True)
		atuin_is_installed_in_path = True
	except (subprocess.CalledProcessError, FileNotFoundError):
		pass
	
	atuin_is_installed_in_home = Paths.EXECUTABLE.exists()

	atuin_doctor = None
	if atuin_is_installed_in_home:
		task = subprocess.run([Paths.EXECUTABLE, 'doctor'], capture_output=True, text=True, check=False)
		atuin_doctor = task.stdout
	
	return {
		'is_installed_in_path': atuin_is_installed_in_path,
		'is_installed_in_home': atuin_is_installed_in_home,
		'atuin_doctor_output': atuin_doctor,
		'paths': [
			path_metadata(Paths.SHARE, ),
			path_metadata(Paths.CONFIG_DIR, ),
			path_metadata(Paths.ATUIN_DIR, ),
		],
	}

