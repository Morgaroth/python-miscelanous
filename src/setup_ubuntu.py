#!/usr/bin/env python

from os import environ as env
from os import mkdir
from os import system as cmd
from os.path import abspath
from shutil import rmtree
from subprocess import check_output
from urllib import request


def home(rest):
    return abspath(rest)


def pwd(rest):
    return abspath('~/setup_ubuntu.d/%s' % rest)


def wget(link, output):
    def a(blocknum, bs, size):
        print('Fetch {}: {} {} {}'.format(output, blocknum, bs, size))

    request.urlretrieve(link, pwd(output), reporthook=a)


SUBLIME_VER = '3126'
SLACK_VER = '2.1.2'
NVIDIA_VER = '370'
DROPBOX_VERSION = '2015.10.28'

try:
    rmtree(home('setup_ubuntu.d'))
except:
    pass

mkdir(home('setup_ubuntu.d'))


def java():
    cmd('echo debconf shared/accepted-oracle-license-v1-1 select true | sudo debconf-set-selections')
    cmd('echo debconf shared/accepted-oracle-license-v1-1 seen true | sudo debconf-set-selections')
    cmd('sudo add-apt-repository ppa:webupd8team/java -y')
    return 'oracle-java8-installer'


def sbt():
    with open('/etc/apt/sources.list.d/sbt.list', 'w') as f:
        f.write('deb https://dl.bintray.com/sbt/debian /')
    cmd('sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 2EE0EA64E40A89B84B2DF73499E82A75642AC823')
    return 'sbt'


def virtualbox():
    with open('/etc/apt/sources.list.d/virtualbox.list', 'w') as f:
        f.write('deb http://download.virtualbox.org/virtualbox/debian xenial contrib')
    cmd('wget -q https://www.virtualbox.org/download/oracle_vbox_2016.asc -O- | sudo apt-key add -')
    return 'virtualbox-5.1'


def postgres():
    with open('/etc/apt/sources.list.d/pgdg.list', 'w') as f:
        a = check_output('lsb_release -cs'.split(' ')).strip().decode('UTF-8')
        f.write('deb http://apt.postgresql.org/pub/repos/apt/ {}-pgdg main'.format(a))
    cmd('wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -')
    return 'pgadmin3'


def spotify():
    with open('/etc/apt/sources.list.d/spotify.list') as f:
        f.write('deb http://repository.spotify.com stable non-free')
    cmd('sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 \
            --recv-keys BBEBDCB318AD50EC6865090613B00F1FD2C19886')
    return 'spotify-client'


def couchbase():
    wget('http://packages.couchbase.com/releases/couchbase-release/couchbase-release-1.0-2-amd64.deb', 'couchbase.deb')
    cmd('sudo dpkg -i couchbase-release-1.0-2-amd64.deb')
    return 'libcouchbase-dev'


def flux():
    cmd('sudo add-apt-repository ppa:nathan-renniewaldock/flux -y')
    return 'fluxgui'


def common():
    return 'git zsh guake indicator-multiload compizconfig-settings-manager terminator keepassx exfat-utils'


def vagrant():
    VAGRANT_VER = '1.8.6'
    wget('https://releases.hashicorp.com/vagrant/$VAGRANT_VER/vagrant_${VAGRANT_VER}_x86_64.deb', 'vagrant.deb')
    cmd('sudo dpkg -i {}'.format(pwd('vagrant.deb')))
    cmd('sudo pip install git+https://github.com/candidtim/vagrant-appindicator.git')
    return ''


def python3():
    return 'build-essential python-dev python-pip python3-dev python3-pip '


def locale():
    return 'mythes-pl thunderbird-locale-pl hunspell-pl \
     language-pack-pl language-pack-gnome-pl wpolish libreoffice-l10n-pl libreoffice-help-pl hyphen-pl \
     firefox-locale-pl fonts-ancient-scripts ttf-ancient-fonts'


def docker():
    cmd('sudo curl -sSL https://get.docker.com/ | sh')
    cmd('sudo usermod -aG docker {}'.format(env['USER']))
    return ''


cmd('sudo apt --force-yes dist-upgrade -y')
cmd('sudo apt --force-yes autoremove -y')
cmd('sudo apt --allow purge notification-daemon -y')
cmd('sudo apt --force-yes install --reinstall notify-osd -y')
cmd('sudo ln -s /usr/share/applications/guake.desktop /etc/xdg/autostart/')

wget('https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb', 'google-chrome.deb')
wget('https://download.sublimetext.com/sublime-text_build-${SUBLIME_VER}_amd64.deb', 'sublime.deb')
wget('https://downloads.slack-edge.com/linux_releases/slack-desktop-$SLACK_VER-amd64.deb', 'slack.deb')
wget('https://linux.dropbox.com/packages/ubuntu/dropbox_${DROPBOX_VERSION}_amd64.deb', 'dropbox.deb')

cmd('sudo dpkg -i {}'.format(pwd('google-chrome.deb')))
cmd('sudo dpkg -i {}'.format(pwd('sublime.deb')))
cmd('sudo dpkg -i {}'.format(pwd('slack.deb')))
cmd('sudo dpkg -i {}'.format(pwd('dropbox.deb')))
cmd('sudo apt install -f -y --force-yes')
cmd('sudo dpkg -i {}'.format(pwd('google-chromee.deb')))

cmd('sudo add-apt-repository ppa:graphics-drivers/ppa -y')
cmd('sudo apt update')
cmd('sudo apt --force-yes install prime-indicator -y')
cmd('sudo apt --force-yes install nvidia-prime -y')
cmd('sudo apt --force-yes install ubuntu-drivers-common -y')
cmd('sudo apt purge bumblebee* primus libvdpau-va-gl1  -y')
cmd('sudo apt purge primus libvdpau-va-gl1 -y')
cmd('sudo apt install nvidia-$NVIDIA_VER nvidia-prime mesa-utils -y')

# # sudo apt install VDPAU-va-driver -y
#
# gsettings set org.gnome.desktop.a11y.mouse secondary-click-enabled "true"



cmd('chsh -s /usr/bin/zsh')
cmd('sh -c "$(wget https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh -O -)"')
cmd('pip3 install configparser')
cmd('pip3 install gitpython')

rmtree(home('setup_ubuntu.d'))

cmd('reboot')
