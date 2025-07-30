import logging
import os
import platform
import re
from pathlib import Path

import PyInstaller.__main__
from importlib.resources import open_text, files

from album.api import Album
from album.runner.album_logging import get_active_logger
from album.package.install_all import force_remove

# remove all handlers from root logger. Necessary because PyInstaller changes root logger configuration.
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)
    handler.close()


def fill_placeholder(output_path, solution_path, coordinates):
    """Fills the path and the coordinates of the passed solution into a cache file which gets copied into the executable
    so the information is availabe in the executable without destroying pyinstallers import structure"""
    with open_text('album.package', 'solution_info.txt') as file:
        template_str = file.read()

    # make windowspaths readable by escaping backslashes
    tmp = re.sub(r"\\", r"\\\\", solution_path)

    template_str = re.sub("<solution_placeholder>", tmp, template_str)
    template_str = re.sub(r"\\", r"\\\\", template_str)
    with open(Path(output_path).joinpath('solution_info.txt'), 'w') as file:
        file.write(template_str)
        file.write("\n")
        file.write(coordinates)


def create_pyinstaller_params(args, name_param):
    """creates the parameter for the pyinstaller call"""
    work_dir = Path(args.output_path).joinpath('build')
    workpath_param = '--workpath=%s' % str(work_dir)
    exe_path_param = '--distpath=%s' % str(args.output_path)
    spec_path = Path(args.output_path)
    spec_path_param = '--specpath=%s' % str(args.output_path)
    log_level_param = '--log-level=ERROR'
    script_path = str(files('album.package').joinpath('install_all.py'))
    install_mamba_script = files('album.package').joinpath('install_mamba.py')
    install_mamba_param = '--add-data=%s%s%s' % (install_mamba_script, os.pathsep, '.')
    solution_info_path = str(Path(args.output_path).joinpath('solution_info.txt'))
    solution_info_param = '--add-data=%s%s%s' % (solution_info_path, os.pathsep, '.')

    pyinstaller_params = [script_path, '--onefile', name_param, exe_path_param, install_mamba_param,
                          solution_info_param, workpath_param, spec_path_param, log_level_param]

    hidden_imports = ["pkg_resources"]
    for hidden_import in hidden_imports:
        pyinstaller_params.append("--hidden-import=%s" % hidden_import)

    return pyinstaller_params


def clean_up(output_path, name):
    force_remove(Path(output_path).joinpath('build'))
    force_remove(Path(output_path).joinpath('solution_info.txt'))
    force_remove(Path(output_path).joinpath('%s.spec' % name))


def run(album_instance: Album, args):
    """Build an executable which installs Album and the solution (in case provided)."""
    try:
        name = ""
        if not Path(args.output_path).is_dir():
            Path(args.output_path).mkdir()

        if args.solution is None:
            get_active_logger().info("Build an executable which installs album.")
        if (args.solution is not None) and (not (Path(args.solution).exists())):
            args.solution = album_instance.resolve(str(args.solution)).path()
        if args.solution is not None:
            get_active_logger().info("Build an executable which installs the solution.")
            coordinates = album_instance.resolve(str(args.solution)).coordinates()
            if coordinates is None:
                raise RuntimeError("The provided solution %s does not contain valid coordinates." % args.solution)
            get_active_logger().info(
                "solution: %s at %s" % (coordinates, args.solution))
            if platform.system() == "Darwin":
                name = "%s_%s_%s_installer.app" % (coordinates.group(), coordinates.name(),
                                                   str(coordinates.version()).replace('.', '_'))
                name_param = "--name=%s_%s_%s_installer.app" % (
                    coordinates.group(), coordinates.name(), str(coordinates.version()).replace('.', '_'))
            else:
                name = "%s_%s_%s_installer" % (coordinates.group(), coordinates.name(),
                                               str(coordinates.version()).replace('.', '_'))
                name_param = "--name=%s_%s_%s_installer" % (
                    coordinates.group(), coordinates.name(), str(coordinates.version()).replace('.', '_'))
            fill_placeholder(str(args.output_path), str(args.solution), coordinates.__str__())
        else:
            if platform.system() == "Darwin":
                name = "album_installer.app"
                name_param = "--name=album_installer.app"
            else:
                name = "album_installer"
                name_param = "--name=album_installer"
            fill_placeholder(str(args.output_path), str(args.solution), "None")

        get_active_logger().info("--output_path: %s" % args.output_path)

        pyinstaller_params = create_pyinstaller_params(args, name_param)

    except Exception as e:
        clean_up(args.output_path, name)
        raise RuntimeError("Unexpected Error when preparing the executable build %s." % e) from e

    try:
        PyInstaller.__main__.run(pyinstaller_params)
    except Exception as e:
        raise RuntimeError("PyInstaller exited with an unexpected error! %s" % e) from e
    finally:
        clean_up(args.output_path, name)


