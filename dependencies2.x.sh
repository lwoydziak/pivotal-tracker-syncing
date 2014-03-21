#!/bin/bash

PYTHON_VERSION=python2.7

for P in $PYTHON_VERSION "${PYTHON_VERSION}-dev"
do
	if ! dpkg-query -s $P | grep ok.installed >/dev/null 2>&1
	then
		echo "package $P not found; installing..."
		sudo apt-get install $P
		if ["$P" == "$PYTHON_VERSION"]; then
			sudo update-alternatives --install /usr/bin/python python /usr/bin/$PYTHON_VERSION 10
		fi			
	fi
done


pip freeze > .pipPackageList

for P in clonedigger
do
	$PYTHON_VERSION find_package.py --package $P .pipPackageList
	case $? in
	1)
		echo "Python package $P not found, installing..."
        y="pip install $P"
        $y	
		;;
	2)
		echo "Python package $P needs upgrade, upgrading..."
        y="pip install --upgrade $P"
        $y
		;;
	esac
done

rm -f .pipPackageList



