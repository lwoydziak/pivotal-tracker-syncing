#!/bin/bash

PYTHON_VERSION=python3.2

for P in wget ant $PYTHON_VERSION "${PYTHON_VERSION}-dev"
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


if ! find /usr/local/bin -iname easy_install-3* | grep easy_install >/dev/null 2>&1
then
	echo "Python package easy_install not found, installing..."
	sudo wget http://python-distribute.org/distribute_setup.py
	sudo $PYTHON_VERSION distribute_setup.py
	sudo rm -f distribute_setup.py
	sudo rm -f distribute*.gz
	sudo rm -rf build
fi

install()
{
	cd $1
	sudo $PYTHON_VERSION setup.py install
	cd ..
}

# manual install
if ! $PYTHON_VERSION find_package.py --package suds
then
	echo "Python package suds not found, installing..."
	sudo wget http://bitbucket.org/bernh/suds-python-3-patches/downloads/suds_patched.zip
	sudo unzip suds_patched.zip
	install suds_patched
	sudo rm -rf suds_*
fi

for P in mockito coverage
do
	if ! $PYTHON_VERSION find_package.py --package $P
	then
		echo "Python package $P not found, installing..."
		c=$(find /usr/local/bin -iname easy_install-3*)
		y="sudo $c $P"
		$y
	fi
done

#for P in pylint
#do
#        if ! $PYTHON_VERSION find_package.py --package $P
#        then
#		P="pylint==0.24"
#                echo "Python package $P not found, installing..."
#                c=$(find /usr/local/bin -iname easy_install-3*)
#                y="sudo $c $P"
#                $y
#        fi
#done


