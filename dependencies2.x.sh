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


if ! find /usr/local/bin -iname easy_install-2* | grep easy_install >/dev/null 2>&1
then
	echo "Python package easy_install not found, installing..."
	sudo wget http://python-distribute.org/distribute_setup.py
	sudo $PYTHON_VERSION distribute_setup.py
	sudo rm -f distribute_setup.py
	sudo rm -f distribute*.gz
	sudo rm -rf build
fi

for P in clonedigger
do
	if ! $PYTHON_VERSION find_package.py --package $P
	then
		echo "Python package $P not found, installing..."
		c=$(find /usr/local/bin -iname easy_install-2*)
		y="sudo $c $P"
		$y
	fi
done



