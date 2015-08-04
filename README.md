## Description
This program will convert Minecraft player stats files from the 1.7 format (numerical block and item IDs)
to the 1.8 format (string identifiers). (Why Mojang didn't include this in the game is beyond me...)

## Requirements
You need to have Python installed. It should work at least with Python 2.7 or 3.3.

## Usage
* First of all, make a backup!!!
* Clone the repo or download both the program itself and the mappings file somewhere.
  (ie. the mc_stats_converter.py and the mappings.txt files; preferably put them in the same directory)
  * If you downloaded the mappings file into the same directory as the program itself,
    then you don't have to specify the --mappings=filename parameter.
  * If the mappings file is not in the same directory as the program (the mc_stats_converter.py file),
    or if you want to specify the mappings file to use, then you need to give the
    --mappings=/path/to/mappingsfile.txt parameter when running it, with the full path to the mappings file to use.
* Run the program via python, giving it the path to the stats directory of the world save as an argument
  (ie. the full path to the stats/ directory inside the world save directory), like so:
  ```python mc_stats_converter.py /path/to/mcserver/world/stats/```
  or, if you want to specify the mappings file:
  ```python mc_stats_converter.py --mappings=/path/to/mappingsfile.txt /path/to/mcserver/world/stats/```
  If your path or filenames have spaces in them, remember to double quote the whole path.
* Optionally you can give it the `--pretty` option and it will also output nice
  human-readable versions of both the old and the new stats files, so you can
  manually check if everything seems right:
  ```python mc_stats_converter.py --pretty /path/to/mcserver/world/stats/```
* If you run the program without arguments, it will print the help.
* The program will create backups of the stats files before converting them,
  they will be named like `<uuid>.json_backup_<timestamp>`
* After running the program and if everything seems correct, you can remove
  the backup files. For example, on Linux: `rm /path/to/mcserver/world/stats/*.json_backup_*`