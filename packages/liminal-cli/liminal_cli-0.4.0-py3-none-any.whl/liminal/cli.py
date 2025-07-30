import json
import typer


app = typer.Typer()

@app.command()
def info():
	from .env import debug

	print('Liminal\'s ShellSync is powered by atuin: https://atuin.sh/')

	# last sync
	# atuin docs link

	# --status (syncing progress for large historys)
	# install status ()

	# --debug
	# print(json.dumps(debug(), indent='\t'))
	# try `atuin sync`, ping our server
	# search our logs for any issues 
	# num install attempts (determined from logs)

# or doctor?
def triage():
	# try to fix the issue for the user, and if all fails, then prints debug/info
	pass

# @app.command()
# def prompt_upgrade():
# 	input('Would you like to upgrade from Liminal v{} to v{}?')


@app.command()
def install():
	from liminal import installer
	installer.main()


@app.command()
def backup():
	"""
	# uninstall
	cp .local/share/atuin/history.db ./my-backed-up-atuin-history.db
	## remove all
	rm -rf .atuin/ .local/share/atuin/ .config/atuin ; rm -rf .liminal-tools/ ; rm lminstall.py
	## remove so can run from `.liminal-tools/venv/bin/python -m liminal.cli install`
	rm -rf .atuin/ .local/share/atuin/ .config/atuin 

	# manual: if installed atuin standalone (without us) previously, remove the sourceing of atuin in whatever rc file


	export LIMINAL_INSTALLER_SKIP_ATUIN_IMPORT=True && export LIMINAL_INSTALLER_PAUSE_AT=installed_atuin && export LIMINAL_INSTALLER_SKIP_CLEANUP=yes
	curl -f https://shellsync.liminalbios.com/api/v1/install > ~/lminstall.py && python3 ~/lminstall.py

	# the `rm` seems to be necessary, otherwise the copied db wont work
	rm ~/.local/share/atuin/history.db* && cp my-backed-up-atuin-history.db ~/.local/share/atuin/history.db

	"""
	pass


# help, --help, -h # allow `help` since might be easier to remember for those who dont know the standard flag
# --help --beginner --onboarding
# this is the liminal_cl tool, which blah blah blah
# some common things you might want to do:
# x,y,z
# if you have any further questions, reach out to us at @aemail.com



if __name__ == '__main__':
	app()
