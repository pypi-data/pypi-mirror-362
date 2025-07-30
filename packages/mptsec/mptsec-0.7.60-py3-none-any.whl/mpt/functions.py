import os
import random
import re
import string
import time

import subprocess
import sys
import shutil

import requests
from git import Repo
from simple_term_menu import TerminalMenu

from tabulate import tabulate
from colorama import Fore, Back, Style
from urllib.parse import urlparse

import mpt
from mpt import settings
from mpt import logger
from mpt.config import Config

log = logger.getLogger()


def yes_no(message):
    options = ["Yes", "No"]
    terminal_menu = TerminalMenu(options, title=message)
    menu_entry_index = terminal_menu.show()

    if menu_entry_index == 0:
        return True
    else:
        return False


def check_command(command_name):
    if not shutil.which(command_name):
        log.error("Couldn't find {}".format(command_name))
        sys.exit(1)


def print_device_table():
    devices = run_command(command='adb devices -l | grep -w device')

    # You can see all available properties with this command:
    # adb shell getprop
    os_version = 'Android ' + str(run_command(command='adb shell getprop ro.build.version.release')[0]).replace("\n", '')
    api = str(run_command(command='adb shell getprop ro.build.version.sdk')[0]).replace("\n", '')

    devs = []
    for device in ''.join(devices).split('\n'):
        info = device.split()
        model = "unknown"
        if len(info) > 0:
            for i in info:
                if i.find('product:') >= 0:
                    product = i.split(':')[1]
                if i.find('model:') >= 0:
                    model = i.split(':')[1]

            devs.append([info[0], product, model, os_version, api])
    log.info('ADB attached devices:')
    print(tabulate(devs, headers=['ID', 'Product', 'Model', 'OS', 'API Level']))


def check_adb_device():
    check_command(command_name='adb')
    devices = run_command(command='adb devices -l | grep -w device')

    if not devices:
        log.warn('Trying to restart adb service')
        restart_adb_server()

        devices = run_command(command='adb devices -l | grep -w device')
        if not devices:
            log.error('No connected devices found')
            sys.exit()

    devices_string = ''.join(devices)
    # fix adb no permissions issue
    if devices_string.find('no permissions') >= 0:
        log.warn('adb does not have permissions to communicate with device')
        run_command(command='adb devices -l | grep -w device', print_output=True)
        log.warn('Restarting adb')
        restart_adb_server()
        devices = run_command(command='adb devices -l | grep -w device')

    if len(devices) > 1:
        log.error('Currently only single attached device is supported. Number of connected devices: {}'.format(len(devices)))
        log.debug('Connected devices:')
        log.debug(devices_string)
        sys.exit(1)

    print_device_table()


def restart_adb_server():
    run_as(user='user')

    return_code = run_command('adb --version | grep -i version', returncode=True)

    if return_code != 0:
        conf = Config()
        install_dir = conf.load_config('install-dir')
        log.error('adb is not installed. Please install package android-sdk-platform-tools '
                  'or add {} to your $PATH variable'.format(os.path.join(install_dir, "platform-tools")))
        sys.exit(return_code)

    adb_bin = settings.ANDROID_TOOLS['adb']['bin']

    log.info(f'Executing: {adb_bin} start-server')
    run_command(f'sudo {adb_bin} kill-server', return_output=True)
    run_command('sudo killall adb')
    run_command(f'sudo {adb_bin} start-server')
    output = run_command(f"{adb_bin} devices -l", return_output=True)

    if not (''.join(output)).find('product') > 0:
        log.error('Restarting adb server failed')
        log.error(f"Run the following commands manually: sudo {adb_bin} kill-server; sudo killall adb; sudo {adb_bin} start-server")


def run_command(command, shell=True, return_output=True, print_output=False, universal_newlines=True,
                returncode=False):
    output = error = []
    try:
        log.debug(f'Executing command: {command}')
        process = subprocess.Popen(command, shell=shell, stdout=subprocess.PIPE,
                                   universal_newlines=universal_newlines)

        while True:
            nextline = process.stdout.readline()
            if nextline == '' and process.poll() is not None:
                break
            if print_output:
                sys.stdout.write(nextline)
            output.append(nextline)
            sys.stdout.flush()

        if returncode:
            return process.returncode

        if output and return_output:
            return output

    except Exception as e:
        log.exception(str(e))
        if error:
            log.error(error)
        sys.exit(1)


def run_interactive_command(command):
    log.debug('Executing interactive command: {}'.format(command))

    cmd = command.split()
    code = os.spawnvpe(os.P_WAIT, cmd[0], cmd, os.environ)
    if code == 127:
        log.error('{0}: command not found'.format(cmd[0]))


def app_installed(app_name):
    app_found = run_command(
        command="""adb shell 'pm list packages -f' | sed -e 's/.*=//' | sort | grep {}""".format(app_name))
    if not app_found:
        log.error('Application \"{}\" is not installed on the device'.format(app_name))
        sys.exit()


def run_as(user):
    if user == 'user':
        if os.getuid() == 0:
            log.error('Run {} as user'.format(__name__))
            sys.exit(1)
    if user == 'root':
        if os.getuid() != 0:
            log.error('Run {} as root'.format(__name__))
            sys.exit(1)


# install tools via command line from OS
# local tool installation using language specific package managers (python pip or nodejs npm)
# commands will be executed from post variable
def install_local(package):

    # check if dir variable is set
    if 'dir' not in settings.ANDROID_TOOLS[package].keys():
        log.error("variable \'dir\' for tool {} is not set".format(package))
        sys.exit(1)

    conf = Config()
    install_dir = conf.load_config('install-dir')
    tool_dir = os.path.join(install_dir, settings.ANDROID_TOOLS[package]['dir'])

    # supports only installation via post command
    if settings.ANDROID_TOOLS[package]['install'] == 'local':

        if not os.path.exists(tool_dir):
            run_command(command='mkdir {}'.format(tool_dir), print_output=True)

            # execute post instructions
            if 'post' in settings.ANDROID_TOOLS[package]:
                run_command(f'cd {install_dir}; {settings.ANDROID_TOOLS[package]['post']}', print_output=True)
                log.info('{} successfully installed'.format(package))
        else:
            log.warn('Binary {} already exists. Skip installation.'.format(tool_dir))


def install_git(package):

    # supports only git clone
    if settings.ANDROID_TOOLS[package]['install'] == 'git':
        git_repo = settings.ANDROID_TOOLS[package]['url']
        conf = Config()
        install_dir = conf.load_config('install-dir')

        clone_path = os.path.join(install_dir, settings.ANDROID_TOOLS[package]['dir'])

        if os.path.exists(clone_path):
            log.warn('Folder {} already exists. Skip installation.'.format(clone_path))
        else:

            # execute pre instructions
            if 'pre' in settings.ANDROID_TOOLS[package]:
                run_command(
                    command='cd {0}; {1}'.format(install_dir, settings.ANDROID_TOOLS[package]['pre']), print_output=True)
            log.info('Cloning repo: {}'.format(git_repo))
            Repo.clone_from(url=git_repo, to_path=clone_path)
            time.sleep(3)

            # execute post instructions
            if 'post' in settings.ANDROID_TOOLS[package]:
                run_command(command='cd {0}; {1}'.format(install_dir, settings.ANDROID_TOOLS[package]['post']), print_output=True)

            log.info('{} successfully installed'.format(package))


# download files via HTTP
def install_http(package):

    # check if dir variable is set
    if 'dir' not in settings.ANDROID_TOOLS[package].keys():
        log.error("variable \'dir\' for tool {} is not set".format(package))
        sys.exit(1)

    conf = Config()
    install_dir = conf.load_config('install-dir')
    tool_path = settings.ANDROID_TOOLS[package]['bin']
    tool_url = settings.ANDROID_TOOLS[package]['url']
    tool_dir = os.path.join(install_dir, settings.ANDROID_TOOLS[package]['dir'])

    if tool_url.endswith('zip') or tool_url.endswith('tar.xz') or tool_url.endswith('tar.gz'):
        install_http_archive(package)
    else:

        # supports only download single files via direct http link
        if settings.ANDROID_TOOLS[package]['install'] == 'http':

            if not os.path.exists(tool_dir):

                # execute pre instructions
                if 'pre' in settings.ANDROID_TOOLS[package]:
                    run_command(
                        command='cd {0}; {1}'.format(install_dir, settings.ANDROID_TOOLS[package]['pre']),
                        print_output=True)

                run_command(command='mkdir {}'.format(tool_dir), print_output=True)
                log.info('Downloading {} from {} '.format(package, tool_url))
                run_command(command='wget {} -O {} -q'.format(tool_url, tool_path), print_output=True)

                # execute post instructions
                if 'post' in settings.ANDROID_TOOLS[package]:
                    run_command(
                        command='cd {0}; {1}'.format(install_dir, settings.ANDROID_TOOLS[package]['post']), print_output=True)
                log.info('{} successfully installed'.format(package))
            else:
                log.warn('Binary {} already exists. Skip installation.'.format(tool_dir))


# download and extract zip and tar.xz files
def install_http_archive(package):

    conf = Config()
    install_dir = conf.load_config('install-dir')
    tool_url = settings.ANDROID_TOOLS[package]['url']
    tool_dir = os.path.join(install_dir, settings.ANDROID_TOOLS[package]['dir'])
    temp_archive_filename = ""
    download_dir = install_dir

    if os.path.exists(tool_dir):
        log.warn('Folder {} already exists. Skip installation.'.format(tool_dir))

    else:
        if 'download_dir' in settings.ANDROID_TOOLS[package]:
            download_dir = os.path.join(install_dir, settings.ANDROID_TOOLS[package]['download_dir'])

        # execute pre instructions
        if 'pre' in settings.ANDROID_TOOLS[package]:
            run_command(
                command='cd {0}; {1}'.format(install_dir, settings.ANDROID_TOOLS[package]['pre']), print_output=True)

        # handle zip files
        if tool_url.endswith('zip'):
            temp_archive_filename = 'download-tmp.zip'
            run_command(command='cd {0}; wget -q {1} -O {2}; unzip -q {2};'
                        .format(download_dir, tool_url, temp_archive_filename, ), print_output=True)

        # handle tar.xz files
        if tool_url.endswith('tar.xz'):
            temp_archive_filename = 'download-tmp.tar.xz'
            run_command(command=f'cd {download_dir}; wget -q {tool_url} -O {temp_archive_filename}; tar -xf {temp_archive_filename};',
                        print_output=True)

        # handle tar.gz files
        if tool_url.endswith('tar.gz'):
            temp_archive_filename = 'download-tmp.tar.gz'
            run_command(command=f'cd {download_dir}; wget -q {tool_url} -O {temp_archive_filename}; tar -xzf {temp_archive_filename};',
                        print_output=True)

        # execute post instructions
        if 'post' in settings.ANDROID_TOOLS[package]:
            run_command(
                command='cd {0}; {1}'.format(install_dir, settings.ANDROID_TOOLS[package]['post']), print_output=True)

        # remove downloaded file
        if os.path.exists(os.path.join(install_dir, temp_archive_filename)):
            run_command(command=f'cd {install_dir}; rm {temp_archive_filename}', print_output=True)

        log.info('{} successfully installed'.format(package))


# not used anymore
"""
def install_app(app):

    log.info('Installing {0} app'.format(Fore.CYAN + app + Style.RESET_ALL))

    pkg = settings.ANDROID_APKS[app]['pkg']
    apk_file = os.path.join(settings.MPT_PATH,settings.ANDROID_APKS[app]['apk'])

    if not os.path.isfile(apk_file):
        log.error('File {} not found. Installation canceled.'.format(apk_file))
        sys.exit()

    app_found = run_command(command="adb shell 'pm list packages -f' | grep {}".format(pkg))

    if not app_found:
        run_command(
            command="adb install {}".format(apk_file))
    else:
        log.warn('Package {} already installed. Skip installation.'.format(pkg))
"""


def check_requirements(package):
    # check tool requirements
    if 'requirement_checks' in settings.ANDROID_TOOLS[package].keys():
        counter = len(settings.ANDROID_TOOLS[package]['requirement_checks'].split(";"))
        installed = 0

        for requirement in settings.ANDROID_TOOLS[package]['requirement_checks'].split(";"):

            if not run_command(command=requirement, return_output=True):
                log.error(f"Missing dependency: please install the dependency to be able to run the following command: {requirement}")

                terminal_menu = TerminalMenu(["Yes", "No"], title=f"Would you like to skip installation for {package}")
                menu_entry_index = terminal_menu.show()
                if menu_entry_index == 0:
                    # skip tool installation
                    return False
                else:
                    log.info("Tools installation canceled by user")
                    sys.exit()
            else:
                installed += 1

        if installed == counter:
            return True

    else:
        # continue tool installation
        return True


# set symbolic links if package provides binaries, which should be available gloobally
# binary folder is settings.MPT_BIN
def set_symbolic_links(package):

    if 'bin_global' in settings.ANDROID_TOOLS[package].keys():

        if not os.path.isdir(settings.MPT_BIN):
            log.info(f'Creating MPT bin folder "{settings.MPT_BIN}" ...')
            os.makedirs(settings.MPT_BIN)

        installation_required = False
        # check if sym links already exists
        for link in settings.ANDROID_TOOLS[package]['bin_global'].keys():
            if os.path.islink(os.path.join(settings.MPT_BIN,link)):
                log.debug(f"link exists {link}")
            else:
                installation_required = True
                break

        if (installation_required):
            log.info(f"Linking binaries to {settings.MPT_BIN}")
            for link_name, bin_location in settings.ANDROID_TOOLS[package]['bin_global'].items():
                bin = os.path.join(mpt.settings.DEFAULT_MOBILE_FOLDER, settings.ANDROID_TOOLS[package]['dir'], bin_location)

                if os.path.isfile(bin):
                    # create a symbolic link to biniry
                    #   cd tools/mobile/bin
                    #   e.q. => ln -s /home/$USER/tools/MOBILE/jadx/bin/jadx jadx
                    log.info(f"Found binary: {link_name}")
                    run_command(f'cd {settings.MPT_BIN}; ln -s {bin} {link_name}', return_output=True)


def install_tools():

    conf = Config()
    install_dir = conf.load_config('install-dir')

    for package in settings.ANDROID_TOOLS:
        log.info('Installing {0} into directory: {1}'.format(Fore.CYAN + package + Style.RESET_ALL, install_dir))

        # install package, if requirements are met
        if check_requirements(package):
            if settings.ANDROID_TOOLS[package]['install'] == 'git':
                install_git(package)
            if settings.ANDROID_TOOLS[package]['install'] == 'http':
                install_http(package)
            if settings.ANDROID_TOOLS[package]['install'] == 'local':
                install_local(package)

        set_symbolic_links(package)





def check_frida_is_running():
    frida_running = run_command(command='adb shell "ps" | grep {}'.format(settings.FRIDA_BIN), return_output=True)

    if not frida_running:
        log.error('Frida server is not running. Please start server before running the script (-f option)')
        sys.exit()

    # TODO replace ps with ps -A for Android 8.0
    # sometimes the app crashes and a new frida-helper starts.
    # If multiple helpers are running at the same time, frida does not work properly.
    pids = run_command(command='adb shell "ps" | grep frida-helper', return_output=True)
    if pids and len(pids) > 1:
        log.warn("Multiple frida-helper processes running, restarting frida")
        run_frida()


def run_frida(select_version=False):
    run_as(user='user')
    check_adb_device()

    if not os.path.exists(settings.TEMP_DIR):
        os.makedirs(settings.TEMP_DIR)
        log.info("TMP folder created: " + settings.TEMP_DIR)

    frida_bin = os.path.join(settings.TEMP_DIR + settings.FRIDA_BIN)

    # determine architecture for available frida-server binary
    bin_arch = ''
    if os.path.exists(frida_bin):
        if run_command(command='file {} | grep -i arm | grep 64'.format(frida_bin)):
            bin_arch = 'arm64'
        elif run_command(command='file {} | grep -i arm | grep 32'.format(frida_bin)):
            bin_arch = 'arm'
        elif run_command(command='file {} | grep -i elf | grep 64'.format(frida_bin)):
            bin_arch = 'x86_64'
        elif run_command(command='file {} | grep -i elf | grep 32'.format(frida_bin)):
            bin_arch = 'x86'

    arch = get_device_architecture()

    if not select_version:
        # remove frida binary if it is not match on arch
        if arch != bin_arch and bin_arch and os.path.isfile(frida_bin):
            os.remove(frida_bin)
            log.info("Wrong architecture, {} removed".format(frida_bin))
    else:
        os.remove(frida_bin)

    # download frida-server binary
    if not os.path.exists(frida_bin):
        download_frida(arch, select_version)
    else:
        log.info('File {} [{}] exists, skip downloading'.format(frida_bin, arch))

    user_id = get_shell_user_id()
    log.info('adb shell is running as {}'.format(user_id))

    kill_process_by_name('frida-helper')
    kill_process_by_name('frida-server')

    # run frida
    run_command(command='adb forward tcp:27042 tcp:27042', print_output=True)
    run_command(command=f'adb push {frida_bin} /data/local/tmp/', print_output=False)
    run_command(command=f'adb shell "chmod 755 /data/local/tmp/{settings.FRIDA_BIN}"', print_output=True)
    rversion = run_command(command=f'adb shell "/data/local/tmp/{settings.FRIDA_BIN} --version"',
                           print_output=False)[0].replace('\n', '')
    lversion = run_command('frida-ps --version')[0].replace('\n', '')

    log.info('Frida version running on Android:   {}'.format(rversion))
    log.info('Frida version installed on Desktop: {}'.format(lversion))
    if rversion != lversion:
        log.warn('Frida versions do not match')

    # kill frida processes on the device TODO
    # ps -ef | grep frida | grep -v 'grep' | awk '{print $2}' | xargs kill -9 $1

    # adb shell running as root (virtual device)
    if user_id.find('uid=0(root)') >= 0:
        command = """adb shell \"/data/local/tmp/{}\" &""".format(settings.FRIDA_BIN)
    else:
        # adb shell running as user (physical device)
        command = """adb shell "su -c \"/data/local/tmp/{}\"\" &""".format(settings.FRIDA_BIN)

    log.info(
        'Executing {}adb shell /data/local/tmp/{}'.format(
                    Style.BRIGHT, settings.FRIDA_BIN + Style.RESET_ALL))
    log.debug('Run frida command: ' + command)
    subprocess.Popen(command, shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)
    check_frida_is_running()


def kill_process_by_name(process_name):

    # TODO replace ps with ps -A for Android 8.0
    pids = run_command(command='adb shell "ps" | grep {}'.format(process_name), return_output=True)

    if pids:
        for pid in pids:
            pid = pid.split()[1]
            log.debug('Killing process {} [pid:{}]'.format(process_name, pid))
            # adb shell running as root (virtual device)
            user_id = get_shell_user_id()
            if user_id.find('uid=0(root)') >= 0:
                run_command(command="adb shell \"kill -9 {}\"".format(pid))
            # adb shell running as user (physical device)
            else:
                run_command(command="adb shell \"su -c kill -9 {}\"".format(pid))


def get_shell_user_id():

    user_id = run_command(command="adb shell id")
    user_id = ''.join(user_id).strip('\n').split(' ')[0]

    # start adbd as root for android emulator
    if user_id.find('uid=0(root)') < 0:
        log.debug("Trying to restart adbd as root")
        run_command(command="adb root")
        user_id = run_command(command="adb shell id")
        user_id = ''.join(user_id).strip('\n').split(' ')[0]

    return user_id


def get_frida_selected_version():
    # GitHub API URL for Frida releases
    url = 'https://api.github.com/repos/frida/frida/releases'

    # Send a GET request to the GitHub API
    response = requests.get(url)
    response.raise_for_status()  # Raise an error for bad status codes

    # Parse the JSON response
    releases = response.json()

    # Extract the tag names of the releases
    release_versions = [release['tag_name'] for release in releases]

    terminal_menu = TerminalMenu(release_versions, title=f"Select frida version you want to run on device")
    menu_entry_index = terminal_menu.show()

    return release_versions[menu_entry_index]


def download_frida(arch, select_version):
    # download frida-server binary

    frida_bin = os.path.join(settings.TEMP_DIR + settings.FRIDA_BIN)

    if not os.path.exists(frida_bin):

        if(select_version):
            frida_version = get_frida_selected_version()
            frida_link = f"https://api.github.com/repos/frida/frida/releases/tags/{frida_version}"
        else:
            frida_link = "https://api.github.com/repos/frida/frida/releases/latest"

        # get download link
        # curl -s  https://api.github.com/repos/frida/frida/releases/latest | grep browser | grep server | grep android
        down_link = run_command(command=f'curl -s {frida_link} | grep browser | grep server | grep android')
        if not down_link:
            log.error('Download frida from github failed')
            sys.exit()

        down_link = [x.split(':', 1) for x in down_link]
        # get second item and delete newline, quotes and trailing spaces
        down_link = [x[1].replace('\n', '').replace('"', '').strip() for x in down_link]
        for link in down_link:
            if '{}.'.format(arch) in link:
                down_link = link
                break

        # download file
        filename = os.path.basename(urlparse(down_link).path)
        log.info('Downloading frida {}'.format(down_link))
        run_command(command='cd {}; wget -q {} -O {}'.format(settings.TEMP_DIR, down_link, filename), print_output=True)
        run_command(command='cd {}; unxz {}'.format(settings.TEMP_DIR, filename), print_output=True)

        filename = os.path.join(settings.TEMP_DIR + os.path.splitext(filename)[0])
        log.info('Frida filename: {}'.format(filename))
        if os.path.isfile(filename):
            run_command(command='mv {} {}'.format(filename, frida_bin))
            log.info('Frida server file (renamed): {}'.format(frida_bin))
            if os.path.isfile('{}.xz'.format(filename)):
                os.remove('{}.xz'.format(filename))
        else:
            log.error('{} file not found'.format(filename))
    else:
        log.info('File {} [{}] exists, skip downloading'.format(settings.FRIDA_BIN, arch))


def get_device_architecture():
    """
    :return: ['arm64', 'arm', 'x86_64', 'x86'] or exit
    """
    arch = run_command(command="adb shell getprop | grep -w 'cpu.abi'")
    arch = arch[0].split(' ')[1].strip('\n')
    arch = arch.replace('[', '').replace(']', '')
    log.info("Detected device architecture {}".format(Style.BRIGHT + arch + Style.RESET_ALL))

    # check architecture for physical devices
    available_arch = ['arm64', 'arm', 'x86_64', 'x86']
    if arch not in available_arch:

        if arch.find('arm64') >= 0:
            arch = 'arm64'
            log.warn('Architecture changed to {}'.format(arch))
        else:
            if arch.find('arm') >= 0:
                arch = 'arm'
                log.warn('Architecture changed to {}'.format(arch))

    if not arch:
        log.error('Frida server for architecture {} not found. Download frida manually'.format(arch))
        sys.exit()
    else:
        return arch


# sanitize path – replace unsafe characters in file name only
def sanitize_path(path):
    dir_name = os.path.dirname(path)
    base_name = os.path.basename(path)

    # Replace disallowed characters and whitespace with underscores
    # Includes: < > : " / \ | ? * control chars, whitespace, (), []
    safe_base = re.sub(r'[<>"\/\\|?*\[\]\(\)\x00-\x1F\s]', '_', base_name)

    return os.path.join(dir_name, safe_base)



# data for wifi username and password generation
adjectives = [
    "Silly", "Wobbly", "Sneaky", "Clumsy", "Jolly", "Grumpy", "Nifty", "Goofy", "Zany", "Loopy",
    "Bouncy", "Giggly", "Nerdy", "Cheeky", "Witty", "Dizzy", "Funky", "Sassy", "Quirky", "Chirpy"
]
animals = [
    "Penguin", "Monkey", "Panda", "Dolphin", "Sloth", "Llama", "Otter", "Meerkat", "Ferret", "Frog",
    "Kangaroo", "Squirrel", "Hedgehog", "Turtle", "Giraffe", "Elephant", "Duck", "Fox", "Bear", "Moose"
]


def generate_funny_wifi_name():

    adj = random.choice(adjectives)
    animal = random.choice(animals)
    number = random.randint(1, 99)
    return f"{adj}{animal}{number}"


def generate_wifi_password():
    words = random.choice(adjectives) + random.choice(animals)
    symbols = random.choices(string.punctuation, k=2)
    digits = random.choices(string.digits, k=4)
    all_chars = list(words) + symbols + digits
    random.shuffle(all_chars)
    return ''.join(all_chars[:16])
