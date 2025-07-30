# Album plugin for packaging solutions into executables

This plugin is used to create installation executables for Album and Album solutions, so Album and a solution can be
installed with a simple double click. The executable creates a shortcut for running Albums UI on the desktop of the
user. The executables can be distributed to a different system running the same operating system. To create executables
for different operating systems, run this plugin on a system running the target operating system. If the the target
system runs Windows or MacOS it doesn't need to have anything preinstalled, the executable will install every needed
component (Micromamba and album) into the ~/.album directory if they are not already installed in this location. Linux users
need to have the binutils package installed.

## Installation:

1. [Install Album](https://docs.album.solutions/en/latest/installation-instructions.html#)
2. Activate the album environment:

```
conda activate album
```

3. Install the album package plugin:

```
pip install album-package
```

4. If you are using a linux system, make sure the source and the target system got the binutils package installed. For
   example on ubuntu it can be installed with the following command:

```
apt-get update && apt-get install binutils
```

## Usage:

To create an executable which installs Album run following command:

```
album package --output_path /your/output/path
```

To create an executable which installs Album and a solution in one go run following command:

```
album package --solution /path/to/your/solution.py --output_path /your/output/path
```


### Input parameter:

- solution: The album solution.py file which should be packed into an executable.
  If you provide the path to a directory containing a solution.py all files in the directory will be packaged into the
  solution executable. If you provide the direct path to a solution.py only the solution will packaged. If your solution
  contains local imports, make sure all imported files lie in the same directory as the solution and you provide the
  path containing the solution.py. If this parameter is not set, the resulting executable will only install Album without
  a solution. 
- output_path: The path where the executable should be saved
