import logging
import subprocess
import sys
import pexpect
import uuid
from liminal.standalone_install_wrapper import LOGGER

def run_login_command(shell_exec_path: str, cmd: str):
	"""
	this seems to be the only way to run a command from python and have atuin record it

	since someone's PS1 can contain anything and/or be dynamic (like mine), we temporarily set PS1 as a uuid we generate
	so we can match between them to get the exact command output
	
	subprocess.run(['bash', '-ic', 'mycommand; exit']) doesnt work
		# resp = subprocess.run(['bash', '-ic', f'logger "liminal installed {datetime_utcnow()} {uuid4()}"'])
		resp = subprocess.run(['bash', '-ic', f'eval "$(atuin init bash)"; echo pleaseeee; true; exit 0'], cwd=Path(__file__).parent.parent, env=None)
	"""
	shell_command = f"{shell_exec_path} -l"
	uniquePS1 = f'--{uuid.uuid4()}$: '
	LOGGER.info(f"{uniquePS1=} {shell_exec_path} -l '{cmd}'")
	child = pexpect.spawn(shell_command, encoding='utf-8', timeout=11)
	export_command = f"export PS1='{uniquePS1}'  "
	child.sendline(export_command)
	
	# child.logfile = sys.stdout # use sys.stdout to more easily debug (see output as it is occuring)

	try:
		child.expect_exact(export_command, timeout=5) 
		# ^ eat up the match of running the export command
		# now we can match our newly set prompt
		child.expect_exact(uniquePS1, timeout=3)
		child.sendline(cmd)
		child.expect_exact(uniquePS1, timeout=3)
		raw_cmd_output = child.before
		return raw_cmd_output
	finally:
		child.terminate()
		child.close()  


def run_command(cmd: list, cmd_output_log_level=logging.DEBUG, logger=LOGGER, check=True, **kwargs) -> subprocess.CompletedProcess[str]:
	logger.debug(f'Running command: {cmd}')
	try:
		task = subprocess.run(cmd, capture_output=True, text=True, check=check, **kwargs)
	except subprocess.CalledProcessError as e:
		logger.error(f'Error running command: {cmd}')
		logger.info(e.stdout)
		logger.info(e.stderr)
		raise e

	logger.log(cmd_output_log_level, task.stdout)
	logger.log(cmd_output_log_level, task.stderr)


	if task.returncode != 0:
		msg = f'Error running command: {task.returncode}: {cmd}'
		log_level = logging.WARNING
		if not check:
			log_level = logging.DEBUG
		logger.log(log_level, msg)
		logger.debug(e.stdout)
		logger.debug(e.stderr)
	else:
		logger.debug(f'Finished command: {cmd}')

	return task


if __name__ == '__main__':
	import uuid 
	# run_in_pty_shell('/bin/bash', f'logger "ok {uuid.uuid4()}"')
	run_login_command('/bin/bash', f'logger "ok {uuid.uuid4()}"')
