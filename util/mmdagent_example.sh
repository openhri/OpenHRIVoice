#!/bin/sh

target_name="MMDAgent-Example"
target_copyright="./lice_dir/mmdagent_mei_copyright.txt"
target_url="http://sourceforge.net/projects/mmdagent/files/MMDAgent_Example/MMDAgent_Example-1.4/MMDAgent_Example-1.4.zip"
target_installPath="/usr/local/share"

. ./func_setup.sh

func_main(){

# Show copyligth.
cat $target_copyright |more
read ANS

# Accept licence and download software.
func_DL $target_name $target_url

# Accept licence and download software.
target_file=`fun_getBasename $target_url`

# Extrac archive.
func_extracFile $target_file $target_installPath

# Set to Symbolic link.
/usr/bin/sudo /bin/mkdir /usr/local/share/mmdagent
/usr/bin/sudo /bin/ln -s /usr/local/share/MMDAgent_Example-1.4/Voice /usr/local/share/mmdagent/voice

}

func_main
