#! /usr/bin/env python3
#
# Remove the quarantine extended file attribute so brew installed apps will open w/out
# the confirming dialog box.
#
# https://stackoverflow.com/questions/15304934/how-to-get-the-list-of-error-numbers-errno-for-an-exception-type-in-python
# https://gist.github.com/roskakori/4572921 - errno.errorcode.keys()
#
# Build as an exe:
#   python3 -m nuitka --follow-imports --show-progress --python-flag=no_site --remove-output brew-app-rmquar.py --standalone
#
# May need to use  --file-reference-choice=FILE_REFERENCE_MODE
#


from grp import getgrnam
import json
from os import getlogin, stat
from os.path import abspath, dirname, exists, isfile, join
from pwd import getpwnam, getpwuid
from subprocess import run
from shlex import shlex
from stat import ST_UID
from sys import exit

try:
    import xattr
except ImportError as e:
    print("  {} was not found. Might want to 'pip install {}'".format(e.name, e.name))
    exit(1)


def rm_quar(app_file, app_root="/Applications/"):
    # If a requested attribute doesn't exist, the error is always
    # "[Errno 93] Attribute not found" independent of the method called.
    # Test cases:
    #   OSError: [Errno 93] Attribute not found:
    #   PermissionError: [Errno 13] Permission denied:
    quar_attr = "com.apple.quarantine"
    f = app_root + app_file
    try:
        xattr.xattr(f).remove(quar_attr)
    except FileNotFoundError:
        print("    Not found: {}".format(f))
    except PermissionError as e:
        # Same as error 13
        # Some apps get installed w/the owner as root and others w/the login account
        # or script is run from non-admin account.
        owner_uid = stat(f)[stat.ST_UID]
        if getpwnam(getlogin()).pw_uid != owner_uid:
            print("    Owned by {}: Skipping {}".format(getpwuid(owner_uid)[0], f))
    except OSError as e:
        if e.errno != 93:
            print("    Unexpected: {}.format(e)")


def is_admin():
    """Check to see if the user belongs to the 'admin' group.
    "SUDO_USER" in os.environ() doesn't work.


    :return: boolean
    """
    return getlogin() in getgrnam("admin").gr_mem


def main():

    if not is_admin():
        # sys.exit("** Need admin privs to run **")
        print(
            "**** {} is not an admin.  Quarantine setting will not be removed ****".format(
                getlogin()
            )
        )

<<<<<<< HEAD:scripts/brew-app-rmquar.command
# os.path.dirname(os.path.abspath(sys.argv[0])) add to call from directory script lives in!
    mapping_file = abspath("cask_to_app_mapping.json")
||||||| merged common ancestors:scripts/brew-app-rmquar.command
    mapping_file = abspath("cask_to_app_mapping.json")
=======
    # figure out how to handle app names w/spaces in them. Garmin Express isn't being processed...
    mapping_file = join(dirname(abspath(__file__)), "cask_to_app_mapping.json")
    print("....Mapping file: {}".format(mapping_file))
>>>>>>> 8c27efc38c0d0453e5166918214b5696a877c86c:scripts/brew-app-rmquar/brew-app-rmquar.py
    if isfile(mapping_file):
        try:
            file = open(mapping_file, "r")  # read existing mapping file,
            cask_mapping = json.load(file)
        except Exception:
            cask_mapping = {}
        finally:
            file.close()
    else:
        cask_mapping = {}

    cmd = "brew cask list"
    installed_casks = run(
        shlex(cmd), capture_output=True, universal_newlines=True
    ).stdout.splitlines()
    atypical_casks = ["adobe-air", "java8"]
    new_mapping = {}
    for cask in installed_casks:
        if cask in cask_mapping:
            rm_quar(cask_mapping[cask])
        elif cask not in atypical_casks:
            app_file = input("Please enter file name for {}: ".format(cask))
            if exists(join("/Applications", app_file)):
                new_mapping[cask] = app_file
                rm_quar(app_file)
            else:
                print("  Skipping {} - file not found".format(app_file))

    if new_mapping:
        try:
            file = open(mapping_file, "w")
            dump({**cask_mapping, **new_mapping}, file, indent=4)
        finally:
            file.close()
            print("  Updated {}".format(file.name))


if __name__ == "__main__":
    main()
else:
    print("** Did not plan on being imported **")