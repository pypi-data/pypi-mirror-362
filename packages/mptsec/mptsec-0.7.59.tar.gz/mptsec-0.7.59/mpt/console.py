#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import os
import re
import shutil
import sys
from datetime import datetime

import netifaces
from colorama import Fore, Back, Style
from simple_term_menu import TerminalMenu

from mpt import functions
from mpt import settings, logger
from mpt.config import Config


def create_default_pentest_folder_structure(pentest_dir):
    os.makedirs(os.path.join(pentest_dir, settings.APP_FOLDER))
    os.makedirs(os.path.join(pentest_dir, settings.BACKUP_FOLDER))
    os.makedirs(os.path.join(pentest_dir, settings.SCREENSHOT_FOLDER))
    os.makedirs(os.path.join(pentest_dir, settings.SOURCE_FOLDER))
    os.makedirs(os.path.join(pentest_dir, settings.BURP_FOLDER))

def create_pentest_folder_with_absolute_path():
    pentest_path = input("Please put absolute path to pentest project folder: ")

    if not pentest_path.startswith("/"):
        log.warn("that is not absolute path, select another folder. Setup canceled")
        sys.exit()

    use_tool_dir = functions.yes_no('Would you like to use this directory \"{}\" ? '.format(pentest_path))
    if use_tool_dir:
        create_default_pentest_folder_structure(pentest_path)
        return pentest_path
    else:
        log.warn("Setup canceled")
        sys.exit()


def setup_pentest(apk):
    functions.run_as(user='user')

    apk_file = ''.join(apk)
    if os.path.isfile(apk_file):
        if not (apk_file.endswith('.apk') or apk_file.endswith('.APK')):
            log.error('File does not have required extension: apk')
            sys.exit()

        pentest_path = os.path.join(os.getcwd(), settings.PENTEST_FOLDER)

        # remove pentest folder, if exists
        if os.path.isdir(pentest_path):
            log.warn("Pentest folder {} already exists.".format(pentest_path))

            options = ["Delete folder content", "select another path", "Skip setup"]
            terminal_menu = TerminalMenu(options, title="Please select an option:")
            menu_entry_index = terminal_menu.show()

            if menu_entry_index == 0:
                shutil.rmtree(pentest_path)
                log.debug(f"Folder {pentest_path} recreated")
                create_default_pentest_folder_structure(pentest_path)
            if menu_entry_index == 1:
                pentest_path = create_pentest_folder_with_absolute_path()
            if menu_entry_index == 2:
                log.warn("Folder {} already exists. Skip setup".format(settings.PENTEST_FOLDER))
                sys.exit()

        else:

            # create a new pentest project
            option1 = "use folder \"{}\"".format(pentest_path)
            options = [option1, "select another path", "skip setup"]
            terminal_menu = TerminalMenu(options, title="Start new pentest project ...")
            menu_entry_index = terminal_menu.show()

            if menu_entry_index == 0:
                # create default folder structure
                create_default_pentest_folder_structure(pentest_path)
            if menu_entry_index == 1:
                pentest_path = create_pentest_folder_with_absolute_path()
            # Skip setup
            if menu_entry_index == 2:
                log.warn("Skip setup".format(settings.PENTEST_FOLDER))
                sys.exit()

        if not os.path.isdir(pentest_path):
            log.error("Error: folder {} could not be created".format(pentest_path))
            sys.exit()

        log.info("Folder for security assessment {} created".format(Fore.CYAN + settings.PENTEST_FOLDER + Style.RESET_ALL))

        # Replace masked characters with "", fix errors with special chars in shell
        new_apk_filename = functions.sanitize_path(apk_file)

        if apk_file != new_apk_filename:
            log.warn(f"APK file renamed to {new_apk_filename}")
        app_pentest_file_location = os.path.join(settings.APP_FOLDER, os.path.basename(new_apk_filename))
        app_pentest_file = os.path.join(pentest_path, app_pentest_file_location)
        shutil.copy(apk_file, app_pentest_file)

        # update apk information

        # get package name and application label
        # aapt dump badging <path-to-apk> | grep package
        # aapt dump badging <path-to-apk> | grep -w "application-label:"
        aapt_bin = settings.ANDROID_TOOLS['aapt']['bin']
        output = functions.run_command(f"{aapt_bin} dump badging {app_pentest_file}")
        output = "".join(output)

        package_match = re.search(r"package: name='(.*?)'", output)
        application_label_match = re.search(r"application-label:'(.*?)'", output)

        package = package_match.group(1) if package_match else None
        application_label = application_label_match.group(1) if application_label_match else None

        # update configuration
        conf = Config()
        conf.update('pentest-dir', pentest_path)
        conf.update('app', app_pentest_file_location)
        conf.update('package-name', package)
        conf.update('application-label', application_label)
        conf.print()

        # app install
        install_app = functions.yes_no('Would you like to install application \"{}\" on device? '.format(package))

        if install_app:
            functions.check_adb_device()
            log.info('Installing apk file: {}'.format(apk_file))
            functions.run_command('adb install "{}"'.format(apk_file))

    else:
        log.error('File {} does not exist'.format(apk_file))


def update_mpt():
    log.info("Updating TMP from https://github.com/ByteSnipers/mobile-pentest-toolkit ...")
    output = functions.run_command('pipx install git+https://github.com/ByteSnipers/mobile-pentest-toolkit --include-deps --force', return_output=True)

    installed_version = ""
    for out in output:
        if out.find('installed package mpt') > 0:
            installed_version = out.strip()

    if installed_version:
        log.success(installed_version)
    else:
        for out in output:
            log.error(out.strip())


def list_packages(show_all_pkgs):
    functions.run_as(user='user')
    functions.check_adb_device()
    print_all = False

    if show_all_pkgs == 'all':
        print_all = True

    if print_all:
        log.info('Print all installed packages')
    else:
        log.info('Only user apps are listed. ' + Style.BRIGHT + Fore.WHITE + 'Use option \'-l all\' to display all packages.' + Style.RESET_ALL)

    packages = functions.run_command(command="""adb shell 'pm list packages -f' | cut -d ":" -f 2""",
                                     print_output=False)

    for p in sorted(packages):

        package = p.rstrip("\n\r").split(".apk=")
        package[0] = package[0] + ".apk"

        # print user packages in bold, do not show default google applications
        if package[0].find('/data/app/') >= 0 \
                and not (package[1].startswith('com.google') or package[1].startswith('com.android')):
            package[0] = Style.BRIGHT + package[0] + Style.RESET_ALL

        # print all apps including system
        if print_all:
            print(Fore.CYAN + package[1] + Style.RESET_ALL)
            print("[APP]: " + package[0])
            print("[DIR]: " + os.path.join("/data/data/", package[1]))

        # print only user apps
        else:
            # do not show default google applications
            if package[0].find('/data/app/') >= 0 \
                    and not (package[1].startswith('com.google') or package[1].startswith('com.android')):

                dumpsys_package = functions.run_command(f'adb shell dumpsys package {package[1]}', return_output=True)
                #print(dumpsys_package)
                # Find lines containing both 'pkgFlags' and 'ALLOW_BACKUP'
                # adb shell dumpsys package {package-name} | grep -i pkgFlags | grep ALLOW_BACKUP'
                backup_enabled = [line for line in dumpsys_package
                                  if 'pkgFlags' in line and 'ALLOW_BACKUP' in line]
                # adb shell dumpsys package "package-name" | grep versionName
                version = [line for line in dumpsys_package if 'versionName' in line]
                version = version[0].strip().split('=')[1]

                if backup_enabled:
                    backup_status = "[BACKUP]:    " + Fore.GREEN + "enabled" + Style.RESET_ALL
                else:
                    backup_status = "[BACKUP]:    " + Fore.YELLOW + "disabled" + Style.RESET_ALL

                if backup_enabled:
                    backup_status = Fore.GREEN + "ENABLED" + Style.RESET_ALL
                else:
                    backup_status = Fore.YELLOW + "disabled" + Style.RESET_ALL

                print(Fore.CYAN + package[1]  + f"  (version: {version})"+ Style.RESET_ALL )
                print("[APP]:       " + Style.BRIGHT + package[0] + Style.RESET_ALL)
                print("[DIR]:       " + Style.BRIGHT + os.path.join("/data/data/", package[1]) + Style.RESET_ALL)
                print("[BACKUP]:    " + backup_status)


def run_pidcat(package_name):
    functions.run_as(user='user')
    functions.check_adb_device()

    if not package_name:
        conf = Config()
        package_name = conf.load_config('package-name')

    functions.app_installed(package_name)

    tool_name = 'pidcat'
    width_left = 30
    pidcat_bin = settings.ANDROID_TOOLS[tool_name]['bin']

    functions.run_command(command='python3 -u  {} -w {} {}'.format(pidcat_bin, width_left, package_name), print_output=True,
                          universal_newlines=True)


def run_pidcat_ex(package_name):
    functions.run_as(user='user')
    functions.check_adb_device()

    if not package_name:
        conf = Config()
        package_name = conf.load_config('package-name')

    functions.app_installed(package_name)

    tool_name = 'pidcat-ex'
    width_left = 30
    pidcat_bin = settings.ANDROID_TOOLS[tool_name]['bin']

    functions.run_command(command='python3 -u {0} -w {1} {2} --hl \'{2}\\yellow|/data/data/\\blue|/data/user/\\blue|/data/app/\\blue|.so\\cyan|activity\\green|Exception\\bg_red\''
                          .format(pidcat_bin, width_left, package_name), print_output=True, universal_newlines=True)


def get_backup_folder(package_name):
    """
    This method generates filename like backup<number>_<package_name>_<comment>

    :param package_name:
    :return: absolute_path to the backup folder
    """
    comment = input('Enter your comment for backup (optional): ')
    log.debug("comment: {} , len = {}".format(comment, len(comment)))

    backup_dir = ""
    # find next folder index
    for index in range(1, 100):
        if len(comment) > 0:
            dir_name = 'backup{}_{}_{}'.format(index, package_name, comment)
        else:
            dir_name = 'backup{}_{}'.format(index, package_name)
        conf = Config()
        pentest_dir = conf.load_config('pentest-dir')

        # if pentest project is set
        if pentest_dir:
            backup_dir = os.path.join(pentest_dir, settings.BACKUP_FOLDER, dir_name)
            # list directories
            dirs = ''.join(os.listdir(os.path.join(pentest_dir, settings.BACKUP_FOLDER)))

        # otherwise save backup in local folder
        else:
            backup_dir = os.path.join(os.getcwd(), dir_name)
            # list directories
            dirs = ''.join(os.listdir(os.getcwd()))

        # check if backup<index> folder does not exist
        if dirs.find("backup" + str(index)) < 0:
            # backup_dir =  backup<last_index>
            log.info('Backup folder: {}'.format(backup_dir))
            break
    return backup_dir


def dump_appdata_as_backup(backup_dir, package_name):
    """
    Pull /data/data/<package_name> folder from device to local backup_dir
    :param backup_dir:
    :param package_name:
    :return:
    """

    user_id = functions.get_shell_user_id()

    # adb shell running as root (virtual device)
    if user_id.find('uid=0(root)') >= 0:
        log.info("Running on virtual device")
        commands = ["cd {}; adb pull /data/data/{}".format(backup_dir, package_name), f'cd {backup_dir}; mv {os.path.join(package_name, "*")} {backup_dir}',
                    f'cd {backup_dir}; rmdir {package_name}']

    else:
        tmp_file = "tmp_app_78923468971.tar.gz"
        log.info("Running on physical device")

        # adb shell running as user (physical device)
        commands = [f'adb shell su -c \"tar -czf /sdcard/{tmp_file} /data/data/{package_name}\"',
                    f'cd {backup_dir}; adb pull /sdcard/{tmp_file}',
                    f'adb shell su -c \"rm /sdcard/{tmp_file}\"',
                    # tar -xzvf /sdcard/backup.tar.gz -C /tmp
                    f'cd {backup_dir}; tar -xzf {tmp_file}',
                    f'cd {backup_dir}; rm {tmp_file}',
                    f'cd {backup_dir}; mv {os.path.join("data/data/", package_name, "*")} {backup_dir}',
                    f'cd {backup_dir}; rmdir {os.path.join("data/data/" + package_name)}',
                    f'cd {backup_dir}; rmdir data/data',
                    f'cd {backup_dir}; rmdir data',
                    ]

    for cmd in commands:
        functions.run_command(cmd)


def backup_app(package_name):
    functions.run_as(user='user')
    functions.check_adb_device()
    abe_bin = settings.ANDROID_TOOLS['abe']['bin']
    app_tar = "backup.tar"
    adb_backup = "backup.ab"

    if not package_name:
        conf = Config()
        package_name = conf.load_config('package-name')

    if not package_name:
        log.error("parameter \"package_name\" is required. Use " + Style.BRIGHT + "mpt -l" + Style.NORMAL + " to list packages")
        sys.exit()

    functions.app_installed(package_name)

    # check whether backup is allowed: <application android:allowBackup="true">
    code = functions.run_command(
        'adb shell dumpsys package {} | grep -i pkgFlags | grep ALLOW_BACKUP'.format(package_name), returncode=True)

    # backup disabled
    if code:
        log.info("Application {}: android:allowBackup={}. Backup is disabled".format(
            Fore.CYAN + package_name + Style.RESET_ALL, Style.BRIGHT + Fore.WHITE + "[FALSE]" + Style.RESET_ALL))
        log.info("dump application using adb pull \"{}\"".format("/data/data/" + package_name))

        backup_dir = get_backup_folder(package_name)
        os.makedirs(backup_dir)

        # dump application using adb pull
        dump_appdata_as_backup(backup_dir, package_name)

    # backup enabled
    else:
        log.info("Application {}: android:allowBackup={}. Backup is enabled"
                 "".format(Fore.CYAN + package_name + Style.RESET_ALL, Style.BRIGHT + Fore.WHITE + "[TRUE]" + Style.RESET_ALL))

        options = ["dump application using adb pull \"{}\"".format("/data/data/" + package_name),
                   "Backup application using Android backup extractor (ABE) tool"]
        terminal_menu = TerminalMenu(options, title="Please select an option:")
        menu_entry_index = terminal_menu.show()

        # dump application using adb pull
        if menu_entry_index == 0:
            backup_dir = get_backup_folder(package_name)
            os.makedirs(backup_dir)

            print(backup_dir)

            dump_appdata_as_backup(backup_dir, package_name)

        # Backup application using ABE
        if menu_entry_index == 1:

            log.info('Backing up application using Android backup extractor (ABE) {}'.format(package_name))
            backup_dir = get_backup_folder(package_name)

            print("Please enter password 0000 on the device")
            backup_dir_tmp = backup_dir + '_tmp'
            os.makedirs(backup_dir_tmp)

            backup_file = os.path.join(backup_dir_tmp, adb_backup)
            app_tar = os.path.join(backup_dir_tmp, app_tar)
            functions.run_command('adb backup -app -f "{0}" {1}'.format(backup_file, package_name))

            log.debug("tar file: " + app_tar)
            log.info('Unpacking backup file')
            functions.run_command(command='java -jar {} unpack "{}" "{}" 0000 &> /dev/null'.format(abe_bin, backup_file, app_tar),
                                  print_output=True)

            file_list = functions.run_command(command='tar -tvf "{}"'.format(app_tar), return_output=True)

            if not file_list:
                log.error("Backup file {} is empty. Maybe the application is compiled with android:allowBackup=\"false\""
                          .format(os.path.basename(app_tar)))
                shutil.rmtree(backup_dir_tmp)
                sys.exit()

            functions.run_command(command='tar xf "{}" -C "{}"'.format(app_tar, backup_dir_tmp), print_output=True)

            # move files to backup folder
            shutil.copytree(os.path.join(backup_dir_tmp + '/apps/' + package_name + '/'), backup_dir)

            files = {'db': 'databases',
                     'f': 'files',
                     'sp': 'shared_prefs',
                     'ef': 'external_storage_files',
                     'r': 'root'}
            # rename files
            for key in files.keys():
                if os.path.isdir(os.path.join(backup_dir, key)):
                    shutil.move(os.path.join(backup_dir, key), os.path.join(backup_dir, files[key]))

            shutil.rmtree(backup_dir_tmp)

    log.success("Backup successfully created")


def generate_jar_file():
    """
    :return converted jar from APP_FOLDER:
    """
    conf = Config()
    app_dir = os.path.join(conf.load_config('pentest-dir'), settings.APP_FOLDER)
    apk_file = conf.load_config('app')
    jar_file = ""
    for file in os.listdir(app_dir):
        if file.endswith('.jar'):
            jar_file = file
            log.debug(f"jar file available: {jar_file}")

    if not jar_file:
        # run command cd pentest-folder; d2j-dex2jar  test.apk
        code = functions.run_command('cd {}; {} "{}"'.format(app_dir, settings.ANDROID_TOOLS['dex2jar']['bin'],
                                                             os.path.basename(apk_file)),
                                     returncode=True, return_output=False)
        if code != 0:
            log.error('Converting dex to class files using dex2jar failed')
            exit(1)

        for file in os.listdir(app_dir):
            if file.endswith('.jar'):
                jar_file = file

        log.debug(f"jar file generated: {jar_file}")

    return jar_file


def run_decompiler(decompiler):
    functions.run_as(user='user')

    if len(decompiler) == 0:
        decompiler = settings.DECOMPILER

    if decompiler in ['jd-gui', 'jadx', 'luyten']:
        log.info("Decompiler: " + decompiler)

        conf = Config()
        if decompiler == 'jd-gui':
            app_dir = os.path.join(conf.load_config('pentest-dir'), settings.APP_FOLDER)
            jar_file = generate_jar_file()
            decompiler_bin = os.path.join(conf.load_config('install-dir'), settings.ANDROID_TOOLS['jd-gui']['bin'])
            functions.run_command('cd {}; java -jar {} "{}"'.format(app_dir, decompiler_bin, jar_file), print_output=True)

        if decompiler == 'jadx':
            apk_file = os.path.join(conf.load_config('pentest-dir'), conf.load_config('app'))
            decompiler_bin = os.path.join(conf.load_config('install-dir'), settings.ANDROID_TOOLS['jadx']['bin'])
            functions.run_command('{} "{}"'.format(decompiler_bin, apk_file), print_output=True)

        if decompiler == 'luyten':
            app_dir = os.path.join(conf.load_config('pentest-dir'), settings.APP_FOLDER)
            jar_file = generate_jar_file()
            decompiler_bin = os.path.join(conf.load_config('install-dir'), settings.ANDROID_TOOLS['luyten']['bin'])
            functions.run_command('cd {}; java -jar {} "{}"'.format(app_dir, decompiler_bin, jar_file), print_output=True)
    else:
        log.warn("Decompiler {} is unknown. Available options: jadx|jd-gui|luyten".format(decompiler))
        sys.exit(1)


# prints usage of run_tool
def print_run_tool_usage():

    print("list of available tools:")
    for package in settings.ANDROID_TOOLS:

        if 'info' in settings.ANDROID_TOOLS[package].keys():
            placeholder = ""
            if len(package) < 5:
                placeholder = "       "
            print(" * {}{} \t [ {} ]".format(package, placeholder, settings.ANDROID_TOOLS[package]['info']))
        else:
            print(" * {}".format(package))

    print("\n use: mpt -t <toolname> '<arg1> <arg2> ...' to run command")
    print("  if you pass the argument to file location please use absolute path !!!")


def run_tool_objection():
    functions.run_as(user='user')
    functions.check_adb_device()
    functions.check_frida_is_running()

    log.info("Execute the followings steps")
    log.info(f"1) Please run 'frida-ps -U' to find the app name")
    log.info(f"2) start objection with the following command: 'objection --gadget \"<APP-NAME>\" explore'")

    conf = Config()
    package = conf.load_config('package-name')
    application_label = conf.load_config('application-label')
    command = settings.ANDROID_TOOLS['objection']['bin']

    if len(application_label) > 0:

        app = f"\"{application_label}\" ({package})"
        options = [f"run objection for app {app}", "run objection"]
        terminal_menu = TerminalMenu(options, title="Please select an option:")
        menu_entry_index = terminal_menu.show()

        if menu_entry_index == 0:
            objection_command = f"objection --gadget \\\"{application_label}\\\" explore"
            command = command.rsplit(";", 1)[0] + f"; {objection_command}; exec $SHELL"
            log_info = f"Running command in {Style.BRIGHT + Fore.CYAN}kitty terminal{Style.RESET_ALL} {objection_command.replace('\\', '')}"
        if menu_entry_index == 1:
            # replace last objection mit exec $SHELL
            command = command.rsplit(";", 1)[0] + "; objection --help; exec $SHELL"
            log_info = f"Running command in {Style.BRIGHT + Fore.CYAN}kitty terminal{Style.RESET_ALL} ..."
    else:
        command = command.rsplit(";", 1)[0] + "; objection --help; exec $SHELL"
        log_info = f"Running command in {Style.BRIGHT + Fore.CYAN}kitty terminal{Style.RESET_ALL} ..."

    terminal_with_command = f"{settings.ANDROID_TOOLS['kitty']['bin']} -- bash -c \"{command}\""
    log.info(log_info)
    functions.run_command(terminal_with_command, return_output=False)


def run_tool(tool_with_args):
    """
    Accepts only two parameters tool + <arg>
    <args> multiple parameters are accepted
    :param tool_with_args:
    :return:
    """
    functions.run_as(user='user')

    if not tool_with_args:
        print_run_tool_usage()
        sys.exit()

    tool = tool_with_args[0]
    tool_args = ""
    if len(tool_with_args) > 1:
        tool_args = ' '.join(tool_with_args[1:len(tool_with_args)])

    if tool == 'list' or tool not in settings.ANDROID_TOOLS.keys():
        print_run_tool_usage()
        sys.exit()

    if tool in settings.ANDROID_TOOLS.keys():

        # check if dir variable is set
        if 'dir' not in settings.ANDROID_TOOLS[tool].keys():
            log.error("variable \'dir\' for tool {} is not set".format(tool))
            sys.exit()

        log.info("Running tool {} ...".format(Style.BRIGHT + tool + Style.RESET_ALL))
        conf = Config()
        tool_dir = os.path.join(conf.load_config('install-dir'), settings.ANDROID_TOOLS[tool]['dir'])
        if os.path.exists(tool_dir):

            try:
                log.info("Press Ctrl+C to interrupt running command")

                if 'bin_info' in settings.ANDROID_TOOLS[tool]:
                    log.info(settings.ANDROID_TOOLS[tool]['bin_info'])

                command = settings.ANDROID_TOOLS[tool]['bin']
                if command.endswith(".jar"):
                    command = 'java -jar ' + command

                # run tool + <args> (all parameters will be processed)
                if tool_args:
                    command = command + " " + tool_args

                if tool == 'objection':
                    run_tool_objection()

                # default case
                else:
                    log.debug("Command: {}".format(Style.BRIGHT + command + Style.RESET_ALL))
                    functions.run_command(command=command, return_output=True, shell=True, print_output=True)

            except KeyboardInterrupt:
                log.warn('Command execution canceled by user')
        else:
            log.error("{} not found".format(settings.ANDROID_TOOLS[tool]['bin']))
    else:
        log.error(f"{tool} tool not found")
        print_run_tool_usage()


def run_inspeckage():
    functions.run_as(user='user')
    functions.check_adb_device()
    functions.app_installed('mobi.acpm.inspeckage')

    url = 'http://127.0.0.1:8008'
    functions.run_command(command='adb forward tcp:8008 tcp:8008', print_output=True)

    # check if drozer server is running
    returncode = functions.run_command(command='curl -I -s {}'.format(url), returncode=True)

    if returncode != 0:
        log.error('Could not connect to the Inspeckage server. Please start inspeckage app on your mobile phone and chouse target application')
        sys.exit(returncode)

    functions.run_command(command=' {} {}'.format(settings.BROWSER, url), returncode=True)


def run_frida_script(package_name, frida_script):
    """
    :param package_name: Android package name
    :param frida_script: frida script file location
    :return: None
    """

    functions.run_as(user='user')
    functions.check_adb_device()

    log.debug('pwd: ' + settings.MPT_PATH)
    frida_script = os.path.join(settings.MPT_PATH, frida_script)

    if not package_name:
        conf = Config()
        package_name = conf.load_config('package-name')

    functions.app_installed(package_name)
    functions.check_frida_is_running()

    if os.path.isfile(frida_script):

        log.info("Frida script {} loaded\n".format(os.path.basename(frida_script)))
        functions.run_interactive_command(command='frida -R -f {} -l {}'.format(package_name, frida_script))
    else:
        log.error('File not found: {}'.format(frida_script))


def disable_ssl_pinning(package_name):

    log.info("Disabling SSL Pinning: " + Fore.CYAN + package_name + Style.RESET_ALL)
    frida_script = "scripts/frida/frida-sslpinning-disable.js"
    frida_script = os.path.join(settings.MPT_PATH, frida_script)

    run_frida_script(package_name, frida_script)


def disable_root_detection(package_name):

    log.info("Disabling Root Detection: " + Fore.CYAN + package_name + Style.RESET_ALL)
    frida_script = "scripts/frida/frida-bypass-root-detection.js"
    frida_script = os.path.join(settings.MPT_PATH, frida_script)

    run_frida_script(package_name, frida_script)

def take_screenshot():

    conf = Config()
    pentest_dir = conf.load_config('pentest-dir')

    # if pentest project is set
    if pentest_dir:

        screenshot_dir = os.path.join(pentest_dir, settings.SCREENSHOT_FOLDER)
        if not os.path.isdir(screenshot_dir):
            os.makedirs(screenshot_dir)

        date = datetime.today().strftime('%Y-%m-%d_%H-%M-%S')
        screenshot_file = os.path.join(screenshot_dir, f"screenshot-{date}.png")

        # adb shell screencap -p /sdcard/Download/screencap.png && adb pull /sdcard/Download/screencap.png screenshot-$(date +%Y-%m-%d_%H-%M-%S).png
        functions.run_command(command=f'adb shell screencap -p /sdcard/Download/screencap.png && adb pull /sdcard/Download/screencap.png {screenshot_file}', returncode=True)
        log.success(f"Screenshot {os.path.basename(screenshot_file)} saved to pentest folder")
    else:
        log.error("Pentest directory is not set. Run mpt --setup to create a pentest environment")



def run_fridump():
    functions.run_as(user='user')
    functions.check_adb_device()
    functions.check_frida_is_running()

    conf = Config()
    package_name = conf.load_config('package-name')
    application_label = conf.load_config('application-label')
    functions.app_installed(package_name)
    fridump_bin = settings.ANDROID_TOOLS['fridump']['bin']

    log.info(f'Dumping application memory "{application_label}" ({package_name}) ...')

    # python ~/fridump/fridump.py -U -s Chrome
    dump_output_dir = os.path.join(conf.load_config('pentest-dir'), 'dump')

    # create dump folder
    if not os.path.isdir(dump_output_dir):
        os.makedirs(dump_output_dir)
    else:
        log.warn(f"Folder {dump_output_dir} already exists")

        options = ["Yes", "No"]
        terminal_menu = TerminalMenu(options, title="Would you like to overwrite the folder")
        menu_entry_index = terminal_menu.show()

        if menu_entry_index == 0:
            shutil.rmtree(dump_output_dir)
            os.makedirs(dump_output_dir)
        if menu_entry_index == 1:
            log.info("Memory dumping skipped ..... ")
            sys.exit(0)

    functions.run_command(command=f'{fridump_bin} -u -s \'{application_label}\' -o {dump_output_dir}',
                          print_output=True,
                          universal_newlines=True)
    log.success("Application memory dump finished")
    log.info(f"Check file: {os.path.join(dump_output_dir, "strings.txt")}")

# Proxy Options
def proxy_status():
    functions.run_as(user='user')
    functions.check_adb_device()

    proxy_check = functions.run_command(command='adb shell settings get global http_proxy')[0].replace('\n', '')

    match = re.findall(r'[0-9]+(?:\.[0-9]+){3}:[0-9]+', proxy_check)
    if match:
        log.success('Proxy status: ENABLED - {}'.format(proxy_check))
    else:
        log.success('Proxy status: DISABLED')


def proxy_enable(proxy):
    functions.run_as(user='user')
    functions.check_adb_device()
    conf = Config()

    if proxy:
        match = re.findall(r'[0-9]+(?:\.[0-9]+){3}:[0-9]+', proxy)
        if not match:
            log.error(f'Required parameter for proxy missing host:port: {proxy}')
            sys.exit(1)

        proxy_host = proxy.split(':')[0]
        proxy_port = proxy.split(':')[1]
        conf.update('proxy', {'host': proxy_host, 'port': proxy_port})

    else:
        proxy_host = conf.load_config('proxy')['host']
        proxy_port = conf.load_config('proxy')['port']
        log.info(f"Load proxy configuration from settings: {proxy_host}:{proxy_port}")

    functions.run_command(command=f'adb shell settings put global http_proxy {proxy_host}:{proxy_port}', return_output=True)
    proxy_current = functions.run_command(command='adb shell settings get global http_proxy', return_output=True)[0].replace('\n', '')
    log.success('Proxy enabled: {}'.format(proxy_current))


def proxy_disable():
    functions.run_as(user='user')
    functions.check_adb_device()

    functions.run_command(command='adb shell settings put global http_proxy :0')
    log.success('Proxy status: DISABLED')


def configure_access_point():
    conf = Config()

    # read interfaces
    wifi_interfaces = functions.run_command(command='iw dev | grep -i interface | grep -vi "unnamed"', return_output=True)
    internet_interface = functions.run_command(command="route | grep '^default' | grep -o '[^ ]*$'", return_output=True)
    internet_interface = internet_interface[0].strip()

    # get default gateway
    if internet_interface:
        log.info(f"Default Gateway (internet connection): {internet_interface}")
    else:
        interface_list = netifaces.interfaces()
        interface_list.remove('lo')

        terminal_menu = TerminalMenu(interface_list, title="Please select default gateway interface (internet connection)?")
        menu_index = terminal_menu.show()
        internet_interface = interface_list[menu_index]

    # get access point interface
    available_interfaces = []
    for i in wifi_interfaces:
        available_interfaces.append(i.strip().split(' ')[1])

    terminal_menu = TerminalMenu(available_interfaces, title="Please select an interface, which can be used as access point")
    menu_index = terminal_menu.show()
    ap_interface = available_interfaces[menu_index]

    ap_name = functions.generate_funny_wifi_name()
    ap_password = functions.generate_wifi_password()
    ap_ip = conf.get_default_access_point_ip()

    conf.update('access-point', {'internet-interface': internet_interface, 'ap-interface': ap_interface, 'ap-ip': ap_ip, 'name': ap_name, 'password': ap_password})
    log.info(f"* WiFi SSID: {ap_name}")
    log.info(f"* AP Interface: {ap_interface}")
    log.info(f"* Default Gateway: {internet_interface}")
    log.info(f"* IP: {ap_ip}")
    log.warn(f"Configure Burp to set a proxy listener on the IP: {ap_ip}")
    log.success('Access point configured')


def access_point():

    conf = Config()
    access_point_conf = conf.load_config('access-point')
    
    if access_point_conf:
        log.info(f"Loaded access point (AP) configuration from settings file")
        log.warn("Root privileges required to start access point (AP)")

        linux_router_bin = settings.ANDROID_TOOLS['linux-router']['bin']
        # sudo ./lnxrouter -o <WiFi-Internet> --ap <AP-WiFi> <SSID> -p <Password> --qr
        log.warn("sudo ./lnxrouter -o <WiFi-Internet> --ap <AP-WiFi> <SSID> -p <Password> --qr")
        log.info(f"AP WiFi SSID: {access_point_conf['name']}")
        log.info(f"Connect your device to {access_point_conf['name']} with password {access_point_conf['password']}")
        log.warn(f"Configure Burp to set a proxy listener on the IP: {Fore.CYAN}{access_point_conf['ap-ip']}{Style.RESET_ALL}")
        try:
            log.info("Press Ctrl+C to interrupt this script.")
            functions.run_command(command=
                                  f"{linux_router_bin} -g {access_point_conf['ap-ip']} -o {access_point_conf['internet-interface']} "
                                  f"--ap {access_point_conf['ap-interface']} {access_point_conf['name']} -p {access_point_conf['password']} --qr",
                                  print_output=True)

        except KeyboardInterrupt:
            log.warn('Canceled by user')
            log.warn('Access point deactivated')

    else:
        configure_access_point()


def print_banner():
    banner = """{}                        __    _ __                         __            __     __              ____   _ __ 
       ____ ___   ___  / /_  (_) /__     ____  ___  ____  / /____  _____/ /_   / /_____  ____  / / /__(_) /_
      / __ \`__ \/__ \/ __ \/ / / _ \   / __ \/ _ \/ __ \/ __/ _ \/ ___/ __/  / __/ __ \/ __ \/ / //_/ / __/
     / / / / / / /_/ / /_/ / / /  __/  / /_/ /  __/ / / / /_/  __(__  ) /_/  / /_/ /_/ / /_/ / / ,< / / /_  
    /_/ /_/ /_/\____/_.___/_/_/\___/  / .___/\___/_/ /_/\__/\___/____/\__/   \__/\____/\____/_/_/|_/_/\__/  
                                     /_/                 
    {}
    @bytesnipers https://bytesnipers.com
    Written by @coreb1t (Alexander Subbotin) 
    Version: {}
    """.format(Fore.GREEN, Style.RESET_ALL, settings.__version__)
    print(banner)


def cli():

    parser = argparse.ArgumentParser(description=print_banner())

    global log
    log = logger.getLogger()
    conf = Config()

    parser.add_argument('--update', help='Update MPT to the latest version', action='store_true')

    tools = parser.add_argument_group("Tools", "Install and run pentest tools on your host")
    tools.add_argument('-tl', '--tool-list', action='store_true', help='Show all supported tools')
    tools.add_argument('-t', '--tool', metavar='tool', nargs='+',
                       help='Run selected tool with <arguments> (use option \'list\' to display all tools)')
    tools.add_argument('-i', '--install-tools', action='store_true',
                       help='Install pentesting tools on local system in a separate environment')
    tools.add_argument('-a', '--adb-run', help='Start adb server with root to avoid a lot of issues using adb', action='store_true')

    pentest = parser.add_argument_group("Pentest", "Configure and manage current pentest")
    pentest.add_argument('--setup', metavar='[APK]', nargs=1, type=str, help='Setup pentest environment')
    pentest.add_argument('--config', help='Show current pentest config', action='store_true')

    frida = parser.add_argument_group("Frida", "Run frida server and execute frida scripts")
    frida.add_argument('-f', '--frida', help='Run frida server on the device (latest version)', action='store_true')
    frida.add_argument('-fs', '--frida-select-version', help='Run frida server on the device (select frida version)', action='store_true')
    frida.add_argument('-s', '--ssl-pinning', metavar='package-name', nargs='?', type=str, const='',
                       help='Disable SSL Pinning (<package name> optional)')
    frida.add_argument('-r', '--root-detection', metavar='package-name', nargs='?', type=str, const='',
                       help='Disable Root Detection (<package name> optional)')

    app = parser.add_argument_group("Application", "Perform app related tasks")
    app.add_argument('-l', '--list-packages', metavar='all', nargs='?', type=str, const='',
                     help='Show all installed packages (use option \'all\' to display system apps)')

    app.add_argument('-p', '--pidcat', metavar='package-name', nargs='?', type=str, const='',
                     help='Show colored logcat for a specific application (<package name> optional)')
    app.add_argument('-st', '--screenshot', help='Take a screenshot from device screen', action='store_true')
    app.add_argument('-sc', '--screen-copy', help='Mirrors Android device screen connected via USB to host (scrcpy)', action='store_true')
    app.add_argument('-D', '--fridump', help='Dump application memory', action='store_true')
    app.add_argument('-b', '--backup', metavar='package-name', nargs='?', type=str, const='',
                     help='Backup an android application \n (<package name> optional)')
    app.add_argument('-d', '--decompile', metavar='decompiler', nargs='?', type=str, const='',
                     help='Start java decompiler for source code analysis (<decompiler> optional): jadx(default), jd-gui, luyten')

    proxy_wifi = parser.add_argument_group("Proxy and WiFi", "Manage proxy on device and WiFi settings locally")
    proxy_wifi.add_argument('-ps', '--proxy-status', help='Check WiFi proxy status', action='store_true')
    proxy_wifi.add_argument('-pe', '--proxy-enable', metavar='host:port', nargs='?', type=str, const='',
                            help='Set proxy for WiFi connection on your device (optional <host:port>), if not set loads proxy settings from configuration file')
    proxy_wifi.add_argument('-pd', '--proxy-disable', help='Disable WiFi proxy', action='store_true')
    proxy_wifi.add_argument('-ap', '--access-point', help='Create an Hotspot which connected to internet and can be used for Burp proxy', action='store_true')
    # obsolete options
    # parser.add_argument('-e', '--inspeckage', help='Open Inspeckage web interface', action='store_true')
    # nargs='+' accept multiple parameters like -t janus path/to/apk

    # parser.add_argument('-t', '--tool', metavar='toolname <args>', default='list', nargs='+',
    # help='Run selected tool (use option \'list\' to display all tools)')
    # parser.add_argument('-d', '--drozer', help='Run drozer application', action='store_true')

    if len(sys.argv) == 1:
        parser.print_usage()
        sys.exit()

    args = parser.parse_args()

    if args.update:
        update_mpt()

    # Tool Options
    if args.tool_list:
        print_run_tool_usage()
    if args.tool:
        run_tool(tool_with_args=args.tool)
    if args.install_tools or type(args.install_tools) is str:
        functions.install_tools()
    if args.adb_run:
        functions.restart_adb_server()

    # Pentest Options
    if args.setup or type(args.setup) is str:
        setup_pentest(apk=args.setup)  # done
    if args.config:
        conf.print()

    # Frida options
    if args.frida:
        functions.run_frida()
    if args.frida_select_version:
        functions.run_frida(select_version=True)
    if args.ssl_pinning or type(args.ssl_pinning) is str:
        disable_ssl_pinning(package_name=args.ssl_pinning)
    if args.root_detection or type(args.root_detection) is str:
        disable_root_detection(package_name=args.root_detection)

    # Application Options
    if args.list_packages or type(args.list_packages) is str:
        list_packages(show_all_pkgs=args.list_packages)
    if args.pidcat or type(args.pidcat) is str:
        # replaced pidcat mit pidcat-extended  run_pidcat(package_name=args.pidcat)
        run_pidcat_ex(package_name=args.pidcat)
    if args.screenshot:
        take_screenshot()
    if args.screen_copy:
        run_tool(["scrcpy"])
    if args.fridump:
        run_fridump()
    if args.backup or type(args.backup) is str:
        backup_app(package_name=args.backup)
    if args.decompile or type(args.decompile) is str:
        run_decompiler(decompiler=args.decompile)

    # Proxy Options
    if args.proxy_status:
        proxy_status()
    if args.proxy_enable or type(args.proxy_enable) is str:
        proxy_enable(proxy=args.proxy_enable)
    if args.proxy_disable:
        proxy_disable()
    if args.access_point:
        access_point()

    # if args.inspeckage:
    #    run_inspeckage()
    # if args.drozer:
    #    run_drozer()
    # if args.start_appmon or type(args.start_appmon) is str:
    #    start_appmon(package_name=args.start_appmon)
