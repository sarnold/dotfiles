#!/usr/bin/env bash

set -euxo pipefail

THIS=${1:-100}
THAT=${2:-100}

if [ "${THIS}" -gt "${THAT}" ]
then
	echo "THIS is great"
elif [ "${THIS}" -lt "${THAT}" ]
then
	echo "THAT is great"
fi

CHG=$(( THIS - THAT ))
echo "change was $CHG"
CHG="${CHG/-/}"
echo "now change is $CHG"

if ! [ "${CHG}" = "0" ]
then
	echo "This is not 0!"
else
	echo "That is $CHG"
fi

CHG="00000"
if [[ "${CHG}" == 0* ]]
then
	echo "This is big $CHG"
else
	echo "This is bad $CHG :/"
fi
