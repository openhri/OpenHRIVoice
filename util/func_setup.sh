#!/bin/sh

func_DL(){

echo "Do you accept the terms of the agreement? Input [y|yes] install."
read KEY

while  [ "$KEY" = "" ]
do
	echo "Do you accept the terms of the agreement? Input [y|yes] to install."
	read KEY
done

if [ $KEY = 'y' -o $KEY = 'yes' ]; then
	echo "start to download and to setting files"

	/usr/bin/wget "${2}" "${3}" "${4}"

else
	echo "abord to setup $1 ...."
	exit 0

fi
}

fun_getBasename(){

basename $1

}


func_extracFile(){

if echo $1 |grep -q '.tar.gz'; then

        echo "Extracing $1------"

	/usr/bin/sudo /bin/tar zxvf $1 -C $2

elif echo $1 |grep -q '.tgz'; then

        echo "Extracing $1------"
	/usr/bin/sudo /bin/tar zxvf $1 -C $2

elif echo $1 |grep -q '.zip'; then

        echo "Extracing $1------"
	/usr/bin/sudo /usr/bin/unzip $1 -d $2

else

	echo "Can't extrac this archive... $1" 

fi
}

