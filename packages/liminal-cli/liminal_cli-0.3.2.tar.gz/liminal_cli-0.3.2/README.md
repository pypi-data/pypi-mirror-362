

Liminal tools


## Debugging

things we can't determine through python:
```
echo $0
```
if a dash appears before the shell name, it is a login shell




tip from negishi:
A very portable way to find what shell you are running is to do:
   $  my_shell=$(basename $(ps -p $$ -ocomm=)); echo $my_shell
