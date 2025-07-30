"""
gets us set up on a server so the users shell history is synced


TODO:
- retry endpoints

future - 
share to shared spot on server
liminal CLI - generate report, get help

errror messages and handling is a little spaghetti



"""

from dataclasses import dataclass
import http
import json
import os
import re
import subprocess
import sys
import time
import traceback
from uuid import uuid4
import uuid

import requests

from liminal import atuin, __version__
from liminal.config import Config
from liminal.env import LAST_SUCCESS_INSTALL_FLAG_PATH, datetime_utcnow, debug, get_os_distro_info
from liminal.standalone_install_wrapper import EMAIL_CONTACT, LIMINAL_BIN, LIMINAL_DIR, LOGGER
from liminal.command_runner import run_command, run_login_command
from liminal.shell import Shell, path_replace_home_with_var


LIMINAL_PACKAGE_VERSION = __version__

LIMINAL_SHELL_EXTENSION = LIMINAL_DIR / 'shell-extension.sh'

STANDALONE_SHELLSYNC_APP_URL = 'https://shellsync.liminalbios.com'
USER_INSTALL_KEY_URL = f'{STANDALONE_SHELLSYNC_APP_URL}/docs/install'
USER_INPUTED_INSTALL_TOKEN = os.environ.get('LIMINAL_INSTALL_TOKEN')
MAIN_LIMINAL_URL = 'https://liminalbios.com/'
INSTALL_SESSION = None

PROGRESS_TRACKER = {
	# Store progress throughout the script, so we can include in our logs
	# TODO: could replace with a filtered install log
}


def set_progress(checkpoint_name: str, value):
	global PROGRESS_TRACKER
	LOGGER.debug(f'progress_tracker: {checkpoint_name}={value}')
	PROGRESS_TRACKER[checkpoint_name] = value
	if Config.LIMINAL_INSTALLER_PAUSE_AT == checkpoint_name:
		LOGGER.debug('checkpoint paused')
		input(f'\n\nPausing at {checkpoint_name=}....Press any key to continue:')



class DependencyError(Exception):
	pass

class ExpiredToken(Exception):
	pass

class UserMessagableError(Exception):
	# for errors were we only need to show the user a message
	pass


@dataclass
class InstallationSession:
	liminal_user_id: str
	install_id: str
	# api_token: str

	# atuin_host_id: str


	# def __init__(self):
	# 	self.write_api_key()
	
	# def write_api_key(self):
	# 	(LIMINAL_DIR / 'api_token').write_text(self.api_token)

class Server: # SyncAPI
	API_ADDRESS = Config.API_ADDRESS
	SYNC_ADDRESS = Config.SYNC_ADDRESS

	def verify_sync(self, expected_details):
		LOGGER.debug(f'{expected_details=}')
		payload = {
			'expected_history': expected_details,
			'liminal_user_uuid': INSTALL_SESSION.liminal_user_id
		}
		resp = requests.post(f'{self.API_ADDRESS}/install/verify-command', json=payload, timeout=10, headers=get_headers())
		self.assert_response_ok(resp)


	def test_connection(self):
		try:
			resp = requests.get(f'{self.API_ADDRESS}/health', timeout=5)
			self.assert_response_ok(resp)
		except Exception as e:
			raise AssertionError(f'Issue connecting to server {self.API_ADDRESS}') from e
		

	def authenticate_user_provided_key(self, install_token: str) -> InstallationSession:
		LOGGER.debug(f'going to verify install token {install_token}')
		headers = {'Authorization': f'Bearer {USER_INPUTED_INSTALL_TOKEN}'}
		resp = requests.get(f'{self.API_ADDRESS}/user/validate', timeout=10, headers=headers)
		if resp.status_code == http.HTTPStatus.FORBIDDEN and resp.json()['description'] == 'Token is expired':
			raise ExpiredToken()

		if resp.status_code == http.HTTPStatus.UNAUTHORIZED and resp.json()['description'].endswith('User is not registered on Liminal.'):
			raise UserMessagableError("\nStopping install...\nYou are not a registered user of Liminal :'( Please sign up in order to finish installation.")
		
		# if resp.status_code == http.HTTPStatus.FORBIDDEN and resp.json()['description'].startswith('User has already completed an install'):
		# 	old_install_id = resp.json()['install_id']
		# 	raise UserMessagableError(f'\nStopping install...\nPreviously completed installation {old_install_id}.\nContact support.')
		


		self.assert_response_ok(resp, error_suffix=f' Invalid token {install_token}')
		set_progress('user_is_verified', True)
		user_id = resp.json()['liminal_user_uuid']
		install_id = resp.json()['install_id']
		LOGGER.debug(f'Validated the user id as liminal user {user_id} {install_id=}')
		return InstallationSession(liminal_user_id=user_id, install_id=install_id)


	@classmethod
	def assert_response_ok(cls, response: requests.Response, error_suffix: str = ''):
		assert response.ok, f'Bad Response: {response.url}: {response.status_code} {response.reason}: {response.text}' + error_suffix


def test_environment():
	"""
	assert atuin isn't already installed. exit if it is.
	
	"""
	shell = Shell()
	assert shell.is_supported()
	set_progress('shell_is_supported', True)
	
	if atuin.is_atuin_installed():
		raise RuntimeError("""Atuin is already installed. We currently cant support a custom setup""")
	set_progress('atuin_is_not_installed', True)

	missing_tools = []
	for tool in ['curl', 'sed']:
		try:
			subprocess.run([tool, '--version'], check=True, capture_output=True)
		except (subprocess.CalledProcessError, FileNotFoundError):
			missing_tools.append(tool)
	if missing_tools:
		raise DependencyError(f'Missing the following CLI tools: {missing_tools}')
	set_progress('prereq_tools_are_installed', True)

	Server().test_connection()
	set_progress('server_connection_good', True)



def preflight_tests():
	LOGGER.info('Running preflight checks')
	test_environment()




def test_correctly_setup():
	"""
	- run a command and make sure it syncs, and that the server can decrypt it
	"""
	LOGGER.info('Checking installation')

	assert atuin.Paths.SQLITE_DB.exists()
	count_before_test = atuin.local_history_count()

	command = f'logger "liminal installed {datetime_utcnow()} {uuid4()}"'

	cmd_output = run_login_command(Shell().exec_path, command)

	count_after = atuin.local_history_count()
	expected_details = None
	# some times it takes 1 second for the history to update (perhaps for larger dbs?)
	for _i in range(3):
		expected_details = atuin.local_history_row(command)
		if expected_details:
			break
		time.sleep(1)
	assert expected_details, f'Test command not found in local history. {count_before_test=} {count_after=}. {cmd_output=}'

	Server().verify_sync(expected_details)
	set_progress('correctly_setup', True)



class ShellConfig:

	def __init__(self):
		self.shell = Shell()

	def generate_extension_file(self):

		shell = Shell()
		LIMINAL_BIN.mkdir(exist_ok=True)
		content = f'#!/bin/sh\n# {LIMINAL_PACKAGE_VERSION}'
		# TODO: maybe just include with our package? would be more reliable
		if shell.is_bash():
			commit = 'e8e9024d4d101a69016169e46f5d75df3fdb7e32'
			url = f'https://raw.githubusercontent.com/rcaloras/bash-preexec/{commit}/bash-preexec.sh'
			response = requests.get(url, timeout=10)
			bash_preexec_path = LIMINAL_DIR / 'bash-preexec.sh'
			bash_preexec_path.write_bytes(response.content)
			bash_preexec_path = path_replace_home_with_var(bash_preexec_path)
			content += f'\n[[ -f {bash_preexec_path} ]] && source {bash_preexec_path}'

		content += '\n' + f"""
. "$HOME/.atuin/bin/env"
eval "$(atuin init {shell.name})"

# add liminal binaries to PATH if they aren't added yet
# affix colons on either side of $PATH to simplify matching
case ":${{PATH}}:" in
    *:"{LIMINAL_BIN}":*)
        ;;
    *)
        # Prepending path in case a system-installed binary needs to be overridden
        export PATH="{LIMINAL_BIN}:$PATH"
        ;;
esac
		""".strip() + '\n'
		LIMINAL_SHELL_EXTENSION.write_text(content)


	def add(self):
		# TODO: backup their file
		current_content = self.shell.config_file.read_text()
		extension_source_path = path_replace_home_with_var(LIMINAL_SHELL_EXTENSION)
		
		content_to_add = f"""
### Liminal tools ---
# info: Activates liminal shell extension and tools. Managed through `liminal_cl` command. Learn more at {MAIN_LIMINAL_URL}
# version {LIMINAL_PACKAGE_VERSION}. date = {datetime_utcnow()}
. "{extension_source_path}"
sourcing_exit_status=$?
if [ "$sourcing_exit_status" -ne 0 ]; then
	# Attempt to use the CLI, if it exists for a more helpful message.
	if command -v liminal_cl >/dev/null 2>&1; then
		liminal_cl doctor --check-shell-env
	else
		echo "Error: Liminal shell extension not activated from " >&2
	fi
fi
### --- Liminal tools
		""".strip()

		existing_breadcrumb_pattern = '^### Liminal tools ---.*^### --- Liminal tools'

		if re.search(existing_breadcrumb_pattern, current_content, flags=re.MULTILINE | re.DOTALL):
			updated_file_content = re.sub(existing_breadcrumb_pattern, content_to_add, current_content, flags=re.MULTILINE | re.DOTALL)
		else:
			updated_file_content = current_content + '\n\n' + content_to_add + '\n'
		self.shell.config_file.write_text(updated_file_content)






def get_headers():
	return {'Authorization': f'Bearer {USER_INPUTED_INSTALL_TOKEN}'}
	# return {'Authorization': f'Bearer {InstallationSession.api_token}'}

def copy_key_to_server(liminal_user_uuid: str):
	LOGGER.info('Copying key')
	key_file = atuin.Paths.KEY_FILE
	# for atuin.Paths.HOST_ID file to be generated by atuin, you need to do a real instantiation of atuin
	run_login_command(Shell().exec_path, 'atuin info',)
	host_id = atuin.Paths.HOST_ID.read_text()
	files = {
		'file_content': ('key', key_file.open(mode='rb'))
	}
	data = {
		'metadata': json.dumps({
			'liminal_user_uuid': liminal_user_uuid,
			'atuin_host_id': host_id,
			'install_id': INSTALL_SESSION.install_id,
		})
	}
	response = requests.post(f'{Server.API_ADDRESS}/install/key', data=data, files=files, headers=get_headers())
	Server.assert_response_ok(response)
	set_progress('key_copied_to_server', True)



def _main():
	"""
	"""
	global INSTALL_SESSION
	global USER_INPUTED_INSTALL_TOKEN
	LOGGER.debug('Starting ----------')
	print('\nWelcome!')
	print(f'If you haven\'t already, get your install token from {USER_INSTALL_KEY_URL}')
	
	preflight_tests()


	try:
		while not INSTALL_SESSION:
			if not USER_INPUTED_INSTALL_TOKEN:
				USER_INPUTED_INSTALL_TOKEN = input('\nPlease enter in your Liminal install token: ').strip()
			try:
				INSTALL_SESSION = Server().authenticate_user_provided_key(USER_INPUTED_INSTALL_TOKEN)
			except ExpiredToken:
				USER_INPUTED_INSTALL_TOKEN = None
				INSTALL_SESSION = None
				LOGGER.error(f'Your install token has expired. Please generate a new one by visiting {USER_INSTALL_KEY_URL}')
			except UserMessagableError as e:
				LOGGER.debug('expected error', stack_info=True)
				print(*e.args) # the string (or list of strings) passed to the exception
				sys.exit(2)
	except KeyboardInterrupt:
		LOGGER.debug('user quit')
		sys.exit(2)


	shellconfig = ShellConfig()
	shellconfig.generate_extension_file()
	shellconfig.add()

	atuin.install_atuin(shellconfig.shell.exec_path)
	set_progress('installed_atuin', True)
	atuin.configure_atuin(Server.SYNC_ADDRESS)

	ATUIN_REGISTRATION_PASSWORD = str(uuid.uuid4()) # can be random and forgotten since this is for logging in on other machine. if users request in future they want to sync multiple machines, a future update can reset their password
	env_copy = os.environ.copy()
	env_copy['ATUIN_REGISTRATION_PASSWORD'] = ATUIN_REGISTRATION_PASSWORD
	atuin_username = INSTALL_SESSION.liminal_user_id.replace('-', '')
	register_task = run_command([atuin.Paths.EXECUTABLE, 'register', '-u', atuin_username, '-e', f'{INSTALL_SESSION.liminal_user_id}@forward.shellsync.liminalbios.com', '-p', '$ATUIN_REGISTRATION_PASSWORD'], env=env_copy, check=False)
	if register_task.returncode != 0:

		# for now, we will do a hard reset on the user - basically delete their atuin account and redo
		# this is ok to do for a single machine, but not multiple
		# TODO: only do delete if user has not done a succesful install. it is NOT OK to do this hard reset multiple times if there wasn't an install issue. 
		# 	like imagine you run the installer again a few days later after reports are generated, 
		# 	then all the relations will be messed up
		# 
		if 'Error: username already in use' in register_task.stderr:
			run_command([atuin.Paths.EXECUTABLE, 'account', 'delete'])
			run_command([atuin.Paths.EXECUTABLE, 'register', '-u', atuin_username, '-e', f'{INSTALL_SESSION.liminal_user_id}@forward.shellsync.liminalbios.com', '-p', '$ATUIN_REGISTRATION_PASSWORD'], env=env_copy)
			# FUTURE:
			# env_copy['TODO_GET_ATUIN_ACCOUNT_PASSWORD'] = ''
			# env_copy['ATUIN_KEY'] = atuin.Paths.KEY_FILE.read_text()
			# run_command([atuin.Paths.EXECUTABLE, 'login', '-u', atuin_username, '--password', '$TODO_GET_ATUIN_ACCOUNT_PASSWORD', '--key', '$ATUIN_KEY'], env=env_copy)
			# set_progress('atuin_account_login', True)
		else:
			raise Exception(f'Issue with registration: {register_task.returncode}: {register_task.stdout=}\n{register_task.stderr=}')


	set_progress('atuin_account_registered', True)
	copy_key_to_server(INSTALL_SESSION.liminal_user_id)

	test_correctly_setup()

	LAST_SUCCESS_INSTALL_FLAG_PATH.write_text(json.dumps({'date': datetime_utcnow().isoformat(), 'version': LIMINAL_PACKAGE_VERSION}))
	LOGGER.debug('Finished sucesffuly')
	
	confirm_response = requests.post(f'{Server.API_ADDRESS}/install/confirmation', timeout=10, headers=get_headers(), json={
		'liminal_user_uuid': INSTALL_SESSION.liminal_user_id,
		'python_version': sys.version,
		'os_distribution': get_os_distro_info(),
		'liminal_version': LIMINAL_PACKAGE_VERSION,
		'history_count': atuin.local_history_count(),

		# 'atuin_host_id': InstallationSession.atuin_host_id,
		'install_id': INSTALL_SESSION.install_id,
	})
	LOGGER.debug(f'{confirm_response.status_code=}')



def cleanup():
	"""Cleanup any mess made by _main(), and make subsequent install attempts possible
	"""
	if Config.LIMINAL_INSTALLER_SKIP_CLEANUP == 'yes':
		LOGGER.debug('skipping cleanup')
		return
	if PROGRESS_TRACKER.get('installed_atuin'):
		try:
			atuin.uninstall_atuin()
		except Exception:
			LOGGER.debug('issue with cleanup', exc_info=True)
	
	# TODO: if registered_user_to_atuin, unregister them or handle in some way so they can run installer again


def print_user_stats():
	env_copy = os.environ.copy()
	env_copy['ATUIN_SESSION'] = (atuin.Paths.SHARE / 'session').read_text()
	stats = run_command([atuin.Paths.EXECUTABLE, 'stats'], env=env_copy, check=False)
	# check=false so we dont log anything to user if error
	if stats.returncode == 0:
		print('\nYour top 10 most ran commands:')
		print(stats.stdout)


def main():
	try:
		_main()
	except Exception:
		report_install_issue()
		cleanup()
		exit(1)
	
	print('\n\n######################')
	print('Woohoo! Almost ready to go!')
	print('######################\n')
	print('Liminal\'s `liminal_cl` tool has been installed!!\n')
	print(f'Your command history will now be continuously synced to {STANDALONE_SHELLSYNC_APP_URL} (powered by `atuin`)')
	print('If you run into any issues or want to learn more, run `liminal_cl --help`')
	print_user_stats()
	print('\nFor everything to work properly, please exit this terminal and start a new one')

	# https://docs.atuin.sh/guide/basic-usage/

	# TODO:
	# if atuin.local_history_count() > 2000:
	# 	print('command history might take 1-3 minutes to sync')
	# 	# `atuin sync` # run it so it works even if shell exits. forget how to do that phup or something


def _report_install_issue():
	debug_info = debug()

	traceback_str = traceback.format_exc()
	payload = {
		'traceback': traceback_str,
		'PROGRESS_TRACKER': PROGRESS_TRACKER,
		'debug_info': debug_info,
		'liminal_user_uuid': INSTALL_SESSION.liminal_user_id  if INSTALL_SESSION else None,
		'install_token': INSTALL_SESSION.install_id if INSTALL_SESSION else None,
		'package_version': LIMINAL_PACKAGE_VERSION,
	}
	try:
		print('## JSON Output')
		print(json.dumps(payload) + '\n##\n')
	except Exception as e:
		print('Error dumping debug info', e)

	LOGGER.exception('Unexpected error during install')
	LOGGER.debug(f'sending report issue to server: {payload}')
	# TODO: with retries
	requests.post(f'{Server.API_ADDRESS}/install/issue', json=payload)


def report_install_issue():
	try:
		_report_install_issue()
	except Exception:
		LOGGER.exception('Exception when trying to report install issue')
		traceback.print_exc()
	print(f'\n\nThere was an error during installation. Please let us know at {EMAIL_CONTACT} and provide ALL the output from running the command')
	# print('') # TODO: universal clipboard copy command? nope. `cat liminal_logfile | pbcopy`


if __name__ == '__main__':
	main()
