import errno
import json
import logging
import os.path
import platform
import shlex
import shutil
import stat
import subprocess
import sys
from glob import glob
import os
from pathlib import Path

import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry

import album
from album.package.install_mamba import install_mamba


# Default python version for creation of an environment, in which the album-gui gets installed.
# This is the python version of the current album environment that is used to run this script.
# By doing this, we can ensure that the album-gui uses the same python version is compatible with what is currently in use.
# This allows to leave the lower bound for the album dependency in the setup.cfg as it is.
RUNTIME_PYTHON_VERSION = sys.version.split()[0]


def is_downloadable(url):
    """Shows if url is a downloadable resource."""
    with _get_session() as s:
        h = s.head(url, allow_redirects=True)
        header = h.headers
        content_type = header.get("content-type")
        if "html" in content_type.lower():
            return False
        return True


def _get_session():
    s = requests.Session()
    retry = Retry(connect=3, backoff_factor=0.5)

    adapter = HTTPAdapter(max_retries=retry)

    s.mount("http://", adapter)
    s.mount("https://", adapter)

    return s


def _request_get(url):
    """Get a response from a request to a resource url."""
    with _get_session() as s:
        r = s.get(url, allow_redirects=True, stream=True)

        if r.status_code != 200:
            raise ConnectionError("Could not connect to resource %s!" % url)

        return r


def download_resource(url, path):
    """Downloads a resource given its url."""
    path = Path(path)

    if not is_downloadable(url):
        raise AssertionError('Resource "%s" not downloadable!' % url)

    r = _request_get(url)
    with open(path, "wb") as f:
        for chunk in r:
            f.write(chunk)

    return path


def _install_missing_gui(
    album_base_path,
    mamba_base_path,
    album_env_path,
    album_gui,
    solution,
    album_dev_mode="",
):
    """Function to install album gui if only the album env is present"""
    # install album gui and if needed mamba
    print("Found album, but not album gui. Installing album gui...")
    # check for mamba
    mamba_exe = get_mamba_exe(mamba_base_path)
    if not Path(mamba_exe).is_file():
        mamba_exe = install_mamba(album_base_path, mamba_base_path)

    if check_for_installed_album(album_env_path, mamba_exe):
        if album_dev_mode:
            cmd = subprocess.run(
                [
                    mamba_exe,
                    "run -p",
                    album_env_path,
                    "install --yes",
                    "git",
                    "pip",
                    "-c",
                    "conda-forge",
                ],
                check=True,
            )
            cmd = subprocess.run(
                [
                    mamba_exe,
                    "run -p",
                    album_env_path,
                    "pip",
                    "install",
                    album_gui,
                    *shlex.split(album_dev_mode),
                ],
                capture_output=True,
            )
        else:
            cmd = subprocess.run(
                [
                    mamba_exe,
                    "install",
                    "--yes",
                    "-p",
                    album_env_path,
                    album_gui,
                    "-c",
                    "conda-forge",
                ],
                capture_output=True,
            )
        if cmd.returncode == 0:
            print("Successfully installed album gui.")
        else:
            print("There was an error installing album gui: %s" % cmd.stderr)
    else:
        _install_album_full(
            album_base_path,
            mamba_base_path,
            album_env_path,
            album_gui,
            solution,
            album_dev_mode,
        )


def _install_album_full(
    album_base_path,
    mamba_base_path,
    album_env_path,
    album_gui,
    solution,
    album_dev_mode="",
):
    """
    Function to install album, album gui, a solution if passed and micromamba if it is not already installed
    """
    if (solution == "None") and Path(album_env_path).is_dir():
        print("Removing old album environment...")
        force_remove(album_env_path)

    # install album and album gui and if needed micromamba
    if not Path(album_base_path).is_dir():
        Path(album_base_path).mkdir()

    mamba_exe = get_mamba_exe(mamba_base_path)
    if not Path(mamba_exe).is_file():
        print(
            "Mamba command not available. Installing Micromamba into %s..."
            % str(mamba_base_path)
        )
        if not Path(mamba_base_path).is_dir():
            Path(mamba_base_path).mkdir()

        install_mamba(album_base_path, mamba_base_path)

    print("Installing environment into %s..." % album_env_path)

    if album_dev_mode:
        album_env_install_call = [
            mamba_exe,
            "create",
            "--yes",
            "-p",
            album_env_path,
            "git", # for the pip constraints to use git urls with declared branches
            f"python={RUNTIME_PYTHON_VERSION}",
            "-c",
            "conda-forge",
        ]
    else:
        album_env_install_call = [
            mamba_exe,
            "create",
            "--yes",
            "-p",
            album_env_path,
            f"python={RUNTIME_PYTHON_VERSION}",
            "-c",
            "conda-forge",
        ]

    print("installing album via %s.." % " ".join(album_env_install_call))
    album_install_output = subprocess.run(album_env_install_call, check=True)

    # install album gui
    print("Installing album gui...")

    # Dev mode uses pip install with constraints, normal: mamba install
    if album_dev_mode:
        # on windows, we need to split the dev mode string for non-posix paths, so it does not eat up the '\\' in the path
        if platform.system() == "Windows":
            album_gui_install_call = [
                mamba_exe,
                "run",
                "-p",
                album_env_path,
                "pip",
                "install",
                album_gui,
                *shlex.split(album_dev_mode, posix=False),
            ]
        else:
            album_gui_install_call = [
                mamba_exe,
                "run",
                "-p",
                album_env_path,
                "pip",
                "install",
                album_gui,
                *shlex.split(album_dev_mode),
            ]
    else:
        album_gui_install_call = [
            mamba_exe,
            "install",
            "--yes",
            "-p",
            album_env_path,
            "-c",
            "conda-forge",
            album_gui,
        ]

    gui_install_output = subprocess.run(album_gui_install_call, check=True)

    if album_install_output.returncode == 0 and gui_install_output.returncode == 0:
        print("Successfully installed album.")
        if solution != "None":
            print("Installing the solution...")
            install_solution(mamba_exe, album_env_path, solution)
    else:
        print("An error occurred installing album: %s" % album_install_output.stderr)
        sys.exit()
    return True


def check_for_installed_album(album_env_path, mamba_exe):
    """Function to check if there is already an album environment in a specific directory"""
    try:
        cmd = subprocess.run(
            [mamba_exe, "run", "-p", album_env_path, "album", "index"],
            capture_output=True,
        )
        if cmd.stderr == "":
            return True
        else:
            return False
    except Exception as e:
        if Path(album_env_path).is_dir():
            answer = input(
                "There seems to be a broken album environment at %s. "
                "Do you want to delete it to be able to install a new album environment? (y/n)"
                % album_env_path
            )
            while True:
                if answer == "y" or answer == "yes":
                    print("Deleting broken album environment...")
                    shutil.rmtree(album_env_path)
                    break
                elif answer == "n" or answer == "no":
                    break
                else:
                    answer = input("Invalid choice please enter y/yes or n/no.")
        return False


def check_for_installed_gui(album_env_path, mamba_exe):
    """check if album gui is installed in the album environment"""
    try:
        cmd = subprocess.run(
            [mamba_exe, "run", "-p", album_env_path, "album", "gui", "-h"],
            capture_output=True,
        )
        if cmd.stderr == "":
            return True
        else:
            return False
    except Exception:
        return False


def install_solution(mamba_exe, album_env_path, solution):
    """Function to install an album solution"""
    try:
        cmd = subprocess.run(
            [mamba_exe, "run", "-p", album_env_path, "album", "install", str(solution)],
            capture_output=True,
        )
        if cmd.returncode == 1:
            print(
                "Installing the solution %s raised a problem: %s"
                % (solution, cmd.stderr.decode())
            )
    except Exception as e:
        raise RuntimeError("An error occurred installing the solution") from e


def check_for_solution(mamba_exe, album_env_path, coordinates):
    """Function to check if the passed solution is installed in the album collection"""
    try:
        cmd = subprocess.run(
            [mamba_exe, "run", "-p", album_env_path, "album", "index", "--json"],
            capture_output=True,
        )
        return check_solutions_dict(get_solution_list_json(cmd.stdout), coordinates)
    except Exception:
        return False


def get_solution_list_json(json_str):
    """Function extracts a list of solution dictionaries from the output of an album index --json call"""
    json_str = json.loads(json_str.decode())
    # list
    catalog_list = json_str["catalogs"]
    # list of catalogs_list of solution_dicts
    catalog_list_of_solution_lists = []
    # list of dict containing dicts as values
    solution_dicts_list = []

    if isinstance(catalog_list, list):
        for cat_dict in catalog_list:
            catalog_list_of_solution_lists.append(cat_dict["solutions"])
    for solution_list in catalog_list_of_solution_lists:
        for solution in solution_list:
            solution_dicts_list.append(solution)

    return solution_dicts_list


def check_solutions_dict(solution_dicts, coordinates):
    """Checks for a specific solution if it is installed, via the output of album index --json"""
    group = coordinates.split(":")[0]
    name = coordinates.split(":")[1]
    version = coordinates.split(":")[2]

    # Go through the list of dictionaries and checking there setup method for the coordinates and then check the internal
    # string for the installation status
    for solution in solution_dicts:
        internal = solution["internal"]
        setup = solution["setup"]
        installed = internal["installed"]
        tmp_group = setup["group"]
        tmp_name = setup["name"]
        tmp_version = setup["version"]
        if (group == tmp_group) and (name == tmp_name) and (version == tmp_version):
            if installed == 1:
                print("solution already installed")
                return True
            else:
                print(
                    "solution %s:%s:%s not installed, but found in the collection."
                    % (tmp_group, tmp_name, tmp_version)
                )
                return False

    return False


def force_remove(path, warning=True):
    """Function to force remove a specific file/directory"""
    path = Path(path)
    if path.exists():
        try:
            if path.is_file():
                try:
                    path.unlink()
                except PermissionError:
                    handle_remove_readonly(os.unlink, path, sys.exc_info())
            else:
                shutil.rmtree(
                    str(path), ignore_errors=False, onerror=handle_remove_readonly
                )
        except PermissionError as e:
            logging.warning("Cannot delete %s." % str(path))
            if not warning:
                raise e


def handle_remove_readonly(func, path, exc):
    """Changes readonly flag of a given path."""
    excvalue = exc[1]
    if func in (os.rmdir, os.remove, os.unlink) and excvalue.errno == errno.EACCES:
        os.chmod(path, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)  # 0777
        func(path)
    else:
        raise


def create_shortcut(mamba_exe, album_env_path):
    """Creates a shortcut for the album gui on the users desktop"""
    subprocess.run(
        [mamba_exe, "run", "-p", album_env_path, "album", "add-shortcut"], check=True
    )


def get_album_base_path():
    """returns the base directory of the album collection"""
    return Path.home().joinpath(".album")


def get_album_env_path(album_base_path):
    """returns the path to the album environment"""
    return Path(album_base_path).joinpath("envs", "album")


def get_mamba_exe(mamba_base_path):
    """returns the path to the micromamba executable"""
    if platform.system() == "Windows":
        return str(Path(mamba_base_path).joinpath("Library", "bin", "micromamba.exe"))
    else:
        return str(Path(mamba_base_path).joinpath("bin", "micromamba"))


def read_solution_info():
    """Function to read the information of the solution which should be installed.
    Returns path to the solution and it's coordinates. solution_info.txt is used to pass the information about
    the solution into the executable without destroying the import structure ob pyinstaller
    """
    with open(
        Path(os.path.realpath(__file__)).parent.joinpath("solution_info.txt"), "r"
    ) as file:
        sol_info = file.read()
    return sol_info.split("\n")


def main():
    album_base_path = str(get_album_base_path())
    mamba_base_path = str(Path(album_base_path).joinpath("micromamba"))
    mamba_exe = get_mamba_exe(mamba_base_path)
    album_env_path = str(get_album_env_path(album_base_path))
    album_gui = "album-gui"
    solution_info = read_solution_info()
    solution_path = solution_info[0]
    coordinates = solution_info[1]
    full_install = False

    # NOTE: Development environment:
    # This is used to replace the mamba installation of album-gui
    # and album itself with a pip constraints file to overwrite
    # the source to the dev-branches of the repositories
    # Let's use the contraints directly in a pip install call when ALBUM_DEV_ONLY is set in the CI/CD environment.
    ALBUM_DEV_ONLY_CONSTRAINTS = os.environ.get("ALBUM_DEV_ONLY_CONSTRAINTS", "")

    if not Path(album_base_path).is_dir():
        Path(album_base_path).mkdir()

    print("Checking for micromamba installation...")
    if not Path(mamba_exe).is_file():
        print(
            "Mamba command not available. Installing micromamba into %s..."
            % mamba_base_path
        )
        install_mamba(album_base_path, mamba_base_path)

    if not check_for_installed_album(album_env_path, mamba_exe) or (
        solution_path == "None"
    ):
        full_install = _install_album_full(
            album_base_path,
            mamba_base_path,
            album_env_path,
            album_gui,
            solution_path,
            album_dev_mode=ALBUM_DEV_ONLY_CONSTRAINTS,
        )

    if not full_install:
        print("Checking for album gui installation...")
        if not check_for_installed_gui(album_env_path, mamba_exe):
            _install_missing_gui(
                album_base_path,
                mamba_base_path,
                album_env_path,
                album_gui,
                solution_path,
                ALBUM_DEV_ONLY_CONSTRAINTS,
            )

        if solution_path != "None":
            print("Checking if the solution is installed...")
            if not check_for_solution(mamba_exe, album_env_path, coordinates):
                print("Installing the solution...")
                install_solution(mamba_exe, album_env_path, solution_path)

    print("Creating shortcut..")
    create_shortcut(mamba_exe, album_env_path)

    print("Installation successfully finished.")


if __name__ == "__main__":
    main()
