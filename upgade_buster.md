# How to upgrade to raspbian buster
# on my last approach to use apt-get update && apt-get dist-upgrade there was first the message, that the repository is not yet available, so I had to set the date manually e.g.
# Error Message: 
E: Für das Depot »http://raspbian.raspberrypi.org/raspbian buster InRelease« wurde der »Suite«-Wert von »testing« in »stable« geändert.
N: Sie müssen dies explizit bestätigen, bevor Aktualisierungen von diesem Depot angewendet werden können. Lesen Sie die apt-secure(8)-Handbuchseite, wenn Sie weitere Informationen benötigen.


$ sudo date -s "04 July 21:23:24"

# Afterwards I had to accept the repository change for buster from testing to InRelease
sudo apt update --allow-releaseinfo-change

# now there is a missing dependency for libttspico-utils in the old install.sh, so I added the debian standard repository non-free to the apt/sources.list file:
deb http://deb.debian.org/debian buster non-free

# now we need to import the new pgp keys as well

$ gpg --recv-keys 648ACFD622F3D138
$ gpg --recv-keys DCC9EFBF77E11517

# and import them
gpg -a --export 648ACFD622F3D138 | sudo apt-key add -
gpg -a --export DCC9EFBF77E11517 | sudo apt-key add -

# now update your apt sources
$ sudo apt-get update

# and install libttspico-utils
$ sudo apt-get install libttspico-utils
