import json
import typer


app = typer.Typer()

@app.command()
def info():
	from .env import debug

	print('Liminal\'s ShellSync is powered by atuin: https://atuin.sh/')
	print(json.dumps(debug(), indent='\t'))


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
	cp .local/share/atuin/history.db ./
	## remove all
	rm -rf .atuin/ .local/share/atuin/ .config/atuin ; rm -rf .liminal-tools/ ; rm lminstall.py
	## remove so can run from `.liminal-tools/venv/bin/python -m liminal.cli install`
	rm -rf .atuin/ .local/share/atuin/ .config/atuin 

	# if installed atuin without us previously, remove the sourceing of atuin



export LIMINAL_INSTALLER_SKIP_ATUIN_IMPORT=True && export LIMINAL_INSTALLER_PAUSE_AT=installed_atuin && export LIMINAL_INSTALLER_SKIP_CLEANUP=yes

curl -f https://shellsync.liminalbios.com/api/v1/install > ~/lminstall.py && python3 ~/lminstall.py

rm ~/.local/share/atuin/history.db* && cp 2025-07_dane-atuin-history.db ~/.local/share/atuin/history.db

	"""
	pass


if __name__ == '__main__':
	app()
