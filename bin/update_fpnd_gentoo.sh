#!/bin/bash
#
# this rebuilds all (gentoo) fpnd packages that are currently installed
#

# set -x

failures=0
trap 'failures=$((failures+1))' ERR

HOST=$1
UNAME_N=$(uname -n)
TEMP_LIST="fpnd-pkgs.txt"
INSTALLED="fpnd-pkgs_current.txt"

USE_FLAGS="examples test-infra polkit sched"
if [[ $HOST = 'infra-01' || $HOST = 'infra-02' ]]; then
    echo "Found infra host $UNAME_N $HOST"
    USE_FLAGS="test-infra polkit server"
fi

#PKGS="net-misc/fpnd-9999"
PKGS="nanomsg-python-1.0.2_p4 datrie-0.8.2_p1 nanoservice-0.7.2_p3 net-misc/fpnd-9999"
#PKGS="net-misc/stunnel-5.56-r1 net-misc/fpnd-9999"
#PKGS="net-misc/stunnel-5.56-r1 net-misc/fpnd-9999 app-admin/freepn-gtk3-tray-9999"

update_pkgs() {
    ret=$?
    CHK_DM=$(qlist -ICv gdm sddm lightdm slim)
    if [[ -n $CHK_DM ]]; then
        PKGS="${PKGS} app-admin/freepn-gtk3-tray-9999"
    fi
}

if ! [[ $HOST = 'infra-01' || $HOST = 'infra-02' ]]; then
    update_pkgs
fi

sudo rc-service -N zerotier start
NODE_ID=$(sudo zerotier-cli info | awk '{print $3}')

#find /etc/ -name ._cfg\*stunnel -o -name ._cfg\*fpnd | sudo xargs rm -f

echo "setting fpnd use flags to ${USE_FLAGS} on ${UNAME_N}"
sudo /bin/bash -c "echo 'net-misc/fpnd ${USE_FLAGS}' > /etc/portage/package.use/fpnd"

CHK_SVC=$(sudo rc-service -N nfsclient start)
if [[ -n $CHK_SVC ]]; then
    sudo rc-service netmount restart
else
    sudo rc-service -N netmount start
fi

equery list -o $PKGS | cut -d" " -f2|grep -v ^\*$ > $TEMP_LIST

for pkg in $(cat $TEMP_LIST) ; do
    echo "rebuilding  =${pkg} for ${NODE_ID}"
    sudo emerge -q "=$pkg" ;
done

#sudo sed -i -e "s|net_timeout = 75|net_timeout = 90|" /etc/fpnd/fpnd.ini
#sudo chown stunnel: /var/log/stunnel-fpnd.log
#sudo rc-service -N stunnel.fpnd restart

sudo sed -i -e "s|do_check=\"true\"|do_check=\"no\"|" /etc/conf.d/fpnd

equery list $PKGS |cut -d" " -f2|grep -v ^\*$ > $INSTALLED

rm $TEMP_LIST

if ((failures == 0)); then
    echo "Success"
else
    echo "Failure"
    exit 1
fi
