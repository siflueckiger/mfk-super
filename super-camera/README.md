# Readme
## Install resources
### Python
Create virtual environment and activate it

    python3 -m venv env
    source env/bin/activate

install dependencies

    pip3 install Pillow
    pip3 install picamera
    pip3 install RPi.GPIO

### Samba
https://magpi.raspberrypi.org/articles/samba-file-server

    sudo apt-get install samba samba-common-bin
    sudo mkdir -m 1777 mfk-share
    sudo nano /etc/samba/smb.conf

add the following at the end:

    [mfk-super-share]
    Comment = MfK shared folder for super foto installation
    Path = /home/pi/Desktop/mfk-super/super-camera/mfk-share
    Browseable = yes
    Writeable = Yes
    only guest = no
    create mask = 0777
    directory mask = 0777
    Public = yes
    Guest ok = yes

create user and start samba

    sudo smbpasswd -a pi
    sudo /etc/init.d/samba restart
