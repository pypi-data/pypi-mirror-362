![python](https://img.shields.io/pypi/pyversions/Django.svg)
![size](https://img.shields.io/github/repo-size/ByteSnipers%2Fmobile-pentest-toolkit)
![lastcommit](https://img.shields.io/github/last-commit/ByteSnipers/mobile-pentest-toolkit.svg)
![follow](https://img.shields.io/github/followers/ByteSnipers.svg?label=Follow&style=social)

# MPT (Mobile Pentest Toolkit)

The MPT (Mobile Pentest Toolkit) is a must-have solution for your android penetration testing workflows. This tool allow you to automate security tasks and focus on security assessment without to know, where the tools are located and with parameters are required.

Features:

- Automation of your security checks
- Perform project based security assessments
- TMP provides a full set of required tools on any linux distribution
  - local installation of required tools, you can easy extend missing tools
  - installation of required APKs on your devices  
- ADB is included
- Switch WI-FI proxy on your device (e.g. Burp Proxy)
- Show colored logcat output with special highlighting
- Install and run frida server on your device
- Dump application memory
- Analyse source code using several decompilers
- Backup and dump you application data from device. Even if backup is disabled.
- Disable SSL pinning
- Disable root detection
- Start security tools from one place

list of available tools:
 * MobSF         [ Mobile Security Framework (MobSF) ]
 * RMS           [ Runtime Mobile Security (RMS) ]
 * objection     [ Runtime Mobile Exploration Toolkit ]
 * spotbugs      [ Static code analysis for vulnerabilities and bugs ]
 * jadx          [ Dex to Java decompiler ]
 * jd-gui        [ Java Decompiler, dex2jar required ]
 * luyten        [ Java Decompiler Gui for Procyon ]
 * sqlitestudio  [ Multi-platform SQLite database manager ]
 * pidcat        [ excellent logcat color script ]
 * pidcat-ex     [ PID Cat (extended version) ]
 * adus          [ Bash script to dump, build and sign apk ]
 * fridump       [ Memory dumping tool uring frida ]
 * adb           [ Android Debug Bridge (adb) ]
 * aapt          [ Android Asset Packaging Tool ]
 * abe           [ Android backup extractor, android:allowBackup="true" required ]
 * signapk       [ sign an apk with the Android test certificate ]
 * apktool       [ A tool for reverse engineering Android apk files ]
 * dex2jar       [ Convert the Dalvik Executable (.dex) file to jar ]
 * janus         [ scans an APK and an Android device for CVE-2017–13156 ]
 * linux-router 	 [ Set Linux as router in one command. Able to provide Internet, or create WiFi hotspot ]
 * scrcpy 	 [ Application mirrors Android devices (video and audio) connected via USB ]



The mobile pentest toolkit (MPT) was presented on conference OWASP Bucharest AppSec 2018.

* [Tales of Practical Android Penetration Testing
(Mobile Pentest Toolkit)](https://www.owasp.org/images/4/4b/OWASP-Tales-of-practical-penetration-testing.pdf)

# Installation

## Installation using PIPX (preferred installation method)
```
pipx install mptsec

# alternative way install from a public repository
pipx install git+https://github.com/ByteSnipers/mobile-pentest-toolkit --include-deps
```

### 1. if required install pipx
```
# Python (pip)
python3 -m pip install --user pipx

# Debian/Ubuntu/Kali
sudo apt update
sudo apt install python-pipx

# Fedora/Red Hat
sudo dnf install pipx

# Arch Linux/Black Arch
sudo pacman -S python-pipx

# openSUSE
sudo zypper install python-pipx
```
### 2. ensure pipx path is set correctly 
The pipx ensurepath command is used to ensure that the directory containing pipx's installed binaries is included in your system's `PATH` environment variable. 
```
pipx ensurepath
```

## Installation using PIP
```
pip install mptsec
```
If `pip install mptsec` fails, you can isolate the installation using a virtual environment (venv) to avoid system-level conflicts.
```
python3 -m venv venv
source venv/bin/activate
pip install mptsec
```

# Update

### Update using PIPX
```
pipx install git+https://github.com/ByteSnipers/mobile-pentest-toolkit --include-deps --force
```
### Update using MPT
```
mpt --update
```

# Uninstallation
### Uninstall using PIPX
```
pipx uninstall mptsec
```

### Uninstall using PIP
```
pip uninstall mptsec
```


# Configuration

### Alias pentest-dir

You can set this alias to quickly and easily navigate to your project directory based on the configuration in the `settings.json` file. Here’s how you can do it:

#### Adding the Alias to `.bashrc` or `.zshrc`
Run the following command to add the alias to your `.bashrc` file:

```
echo '\n# mpt alias\nalias pentest-dir="cd $(cat /home/$USER/.mpt/settings.json | grep pentest-dir | awk -F'\''\\"'\'' '\''{print $4}'\'') && ls -l"' >> ~/.bashrc

```
You can also add a new alias manually to your `.bashrc` file:
 

```
alias pentest-dir="cd $(cat /home/$USER/.mpt/settings.json | grep pentest-dir | awk -F'\"' '{print $4}') && ls -l"

```

#### Activating the Alias:
After adding the alias, reload your .bashrc file to make it immediately available or open a new terminal window

```
source ~/.bashrc
```

### Install zsh plugin (autocomplete support) - Outdated 

:warning: You need to install [Oh My ZSH](https://github.com/robbyrussell/oh-my-zsh)

:warning: The command line options has not been updated for a while and does not match with the latest version. PRs are welcome

```
cp -r mpt/mpt-zsh-plugin/ ~/.oh-my-zsh/plugins/mpt

```
Enable MPT plugin in `.zshrc` by adding the fooling line `plugins=(mpt)`


# Start New Project

1) Setup pentest environment and install required tools

```
mpt --install-tools
```

2) Setup a new pentest project

```
mpt --setup <apk-file>
```


# Usage
```
mpt.py <command> [options]

options:
  -h, --help            show this help message and exit
  --update              Update MPT to the latest version

Pentest:
  Configure and manage current pentest

  --setup [APK]         Setup pentest environment
  --config              Show current pentest config

Frida:
  Run frida server and execute frida scripts

  -f, --frida           Run frida server on the device
  -fs, --frida-select-version
                        Run frida server on the device (select frida version)

  -s [package-name], --ssl-pinning [package-name]
                        Disable SSL Pinning (<package name> optional)
  -r [package-name], --root-detection [package-name]
                        Disable Root Detection (<package name> optional)

Application:
  Perform app related tasks

  -l [all], --list-packages [all]
                        Show all installed packages (use option 'all' to display system apps)
  -p [package-name], --pidcat [package-name]
                        Show colored logcat for a specific application (<package name> optional)
  -st, --screenshot     Take a screenshot from device screen
  -sc, --screen-copy    Mirrors Android device screen connected via USB to host (scrcpy)
  -D, --fridump         Dump application memory
  -b [package-name], --backup [package-name]
                        Backup an android application (<package name> optional)
  -d [decompiler], --decompile [decompiler]
                        Start java decompiler for source code analysis (<decompiler> optional): jadx(default), jd-gui, luyten

Tools:
  Install and run pentest tools on your host

  -tl, --tool-list      Show all supported tools
  -t tool [tool ...], --tool tool [tool ...]
                        Run selected tool with <arguments> (use option 'list' to display all tools)
  -i, --install-tools   Install pentesting tools on local system in a separate environment
  -a, --adb-run         Start adb server with root to avoid a lot of issues using adb

Proxy and WiFi:
  Manage proxy on device and WiFi settings locally

  -ps, --proxy-status   Check WiFi proxy status
  -pe [host:port], --proxy-enable [host:port]
                        Set proxy for WiFi connection on your device (optional <host:port>), if not set loads proxy settings from configuration file
  -pd, --proxy-disable  Disable WiFi proxy
  -ap, --access-point   Create an Hotspot which connected to internet and can be used for Burp proxy

```

## License
[GNU GPL v3](LICENSE) ©[@bytesnipers](https://bytesnipers.com)
