## Description
This program will convert Minecraft player stats files from the 1.7 format (numerical block and item IDs)
to the 1.8 format (string identifiers). (Why Mojang didn't include this in the game is beyond me...)

## Usage
* First of all, make a backup!!!
* Clone the repo or download both the program itself and the mappings file somewhere.
* If you downloaded the mappings file into the same directory as the program itself,
  then you don't have to specify the --mappings=filename parameter.
* Run the program, giving it the path to the Minecraft world/stats/ directory as an argument:
  ```python mc_stats_converter.py /path/to/mcserver/world/stats/```
* Optionally you can give it the `--pretty` option and it will also output nice
  human-readable versions of both the old and the new stats files, so you can
  manually check if everything seems right.
* The program will create backups of the stats files before converting them,
  they will be named like `<uuid>.json_backup_timestamp`
* After running the program and if everything seems correct, you can remove
  the backup files, for example on Linux: `rm /path/to/mcserver/world/stats/*.json_backup_*`