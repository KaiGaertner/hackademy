# Vorlesegerät

Bei diesem Projekt handelt es sich um ein DIY-Projekt als Hilfmittel für Menschen mit Sehbehinderung. Das Ziel ist es eine kostengünstige Lösung zu entwickeln, mit deren Hilfe gedruckte Texte in gesprochene Sprache umgewandelt werden. Als Grundlage dafür dient der Raspberry Pi 3B+ mit einer 5MP-Kamera. Als Software kommen tesseract-ocr und PicoTTS zum Einsatz. Darüber hinaus finden sich in diesem Repo 3D-Dateien für ein selbst entwickeltes Gehäuse, das z.B. mit Hilfe eines LaserCutters ausgeschnitten und zusammengebaut werden kann.

## Installation manual
### Download Buster image and copy to microSD-Card
You can download the latest image for the *raspberry* here: https://www.raspberrypi.org/downloads/raspbian/

> $ sudo dd bs=4M if=2019-07-10-raspbian-buster-lite.img of=/dev/XXX conv=fsync

Replace XXX with the path to your device (could be different depending on your operation system.

### Install the system and set it up properly
You can login to your new installed Raspberry using the credentials *pi* as username and *raspberry* as password (default keyboard setting is set to British, so you have to use z instead of y on a German keyboard).

#### [optional] change keyboard layout
If you're like me and want to use a German keyboard because of the special characters for passwords and terminal commands, changing the keyboard layout would be one of the things you would like to do at first. Unfortunatelly their have been some changes in the raspi-config since the Buster release, which made this change more difficult. Therefore I use the following workaround and adjust the */etc/default/keyboard* file by hand:

> sudo nano /etc/default/keyboard

Now change the following lines as follows:

> XKBLAYOUT=”de”

> XKBVARIANT=”nodeadkeys”

And restart the system:

> sudo reboot 0

Now you can start the configuration using *raspi-config*:

> sudo raspi-config

* First you can *change your password for the pi*. Therefore this manual doesn't include a description how to run the device with an encrypted microSD card and is also using auto-login for the user *pi* there is no real improvement by changing the password anyway, but it's always a good habit.
* You will need an internet connection for the installation, so you will have to set up the *Network options*, if you're not using the ethernet connection, which should be connected automatically at boot. If you want to access the *raspberry* with SSH, you should be in the same network (most standard guest networks from routers will not allow connections between devices). Set up the country Code (two letters like GB or DE), the SSID and the passwort, which will be active after reboot.
* *Setup login configuration* which should be set to *Console Autologin*.
* Now you can setup the *Localization Options*. I sometimes considered the problem, that even if I set the timezone correctly, the system time was not set propperly, so there is another step later. 
* Now we have to set up some *Interface options*. First of all you have to activate the *camera*. If you want to use *SSH* and *Remote GPIO* (serial control pins), you can do this as well. At this menu you can also set a differnt name for the *raspberry* (for example if you have multiple one at your disposal or knew this https://xkcd.com/910/)
* Usually the file system is expanded at first boot. But to ensure this process you could do it manually again from the *raspi-config* menue.
* Now you can finish the *raspi-config* and reboot

After the reboot you can try to *update* the *raspi-config* tool and see if your network settings are correct.

#### [optional] set time and date
If for any reason the *raspberry* can not set the current system time, you will not be able to update. What you can do is setting the date manually:

> $ sudo date -s "30 July 2019 14:00:00 CEST"

#### update the system
Now it's time to look if there have been some updates between the Buster image was created and your installation:

> $ sudo apt-get update && sudo apt-get dist-upgrade

You can also remove old packages afterwards:

> $ sudo apt-get autoremove

Last step, you have to install git to get everything necessary vor the vorleser-syste:

> $ sudo apt-get install git

### Install the Vorleser-System
At first you have to checkout the repository (usually the home folder of the *pi* user would be a good place */home/pi/*):

> $ git clone https://github.com/KaiGaertner/hackademy.git

Now move to the new directory *hakcademy*:

> $ cd hackademy

Now you have to run the install script with root privileges:

> $ sudo sh install.sh

#### [optional] Expanding the available sources
It could happen, that the script *install.sh* can not finish, because some packages couldn't be found. What I had experienced was, that some packages haven't been available for Raspberry Buster yet, but already are for the standard Debian Buster. Therefor the sources must have to been added. Open the */etc/apt/sources.list* file with root privilege:

> $ sudo nano /etc/apt/sources.list

Add the following lines or some other mirror for Debian Buster:

> deb http://ftp.de.debian.org/debian/ buster main contrib non-free

After saving and closing, you will have to get the keys for this repository, before you can use them. If you run:

> $ sudo apt-get update

You will see the keys you have to import and if they haven't changed you can use the following command to import and accept them:

> $ sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 04EE7237B7D453EC 648ACFD622F3D138 EF0F382A1A7B6500 DCC9EFBF77E11517

The last part of the *install.sh* script installs the software for the *audio hat* (https://www.raspiaudio.com) and will ask you to reboot the system. 
