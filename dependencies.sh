#!/bin/bash

PYTHON_VERSION=python3.2

easy_install()
{
	P=$1	
	c=$(find /usr/local/bin -iname easy_install-3*)
	y="sudo $c $P"
	$y
}

easy_install2()
{
	P=$1	
	c=$(find /usr/local/bin -iname easy_install-2*)
	y="sudo $c $P"
	$y
}

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
	easy_install2 yolk
	sudo mv /usr/local/bin/yolk /usr/local/bin/yolk2.7
	easy_install https://bitbucket.org/prologic/yolk3/get/tip.zip	
fi


for P in mockito coverage suds
do		
	if ! yolk -l $P | grep -i $P >/dev/null 2>&1	
	then
		echo "Python package $P not found, installing..."
		if [[ $P == 'suds' ]]; then
			easy_install http://bitbucket.org/bernh/suds-python-3-patches/downloads/suds_patched.zip
		else
			easy_install $P
		fi
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

./dependencies2.x.sh


