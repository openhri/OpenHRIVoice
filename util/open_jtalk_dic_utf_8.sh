#!/bin/sh

target_name="open-jtalk-dic-utf-8"
target_copyright="./lice_dir/utf_8_copyright.txt"
target_url="http://downloads.sourceforge.net/open-jtalk/open_jtalk_dic_utf_8-1.08.tar.gz"
target_installPath="/usr/local/share"

. ./func_setup.sh

func_main(){

# Show copyligth.
cat $target_copyright |more
read ANS

# Accept licence and download software.
func_DL $target_name $target_url

# Set archive name in target_file .
target_file=`fun_getBasename $target_url`

# Extrac archive.
func_extracFile $target_file $target_installPath

# Set to Symbolic link.
/usr/bin/sudo /bin/mkdir -p /usr/local/share/open_jtalk/dic
/usr/bin/sudo /bin/ln -s /usr/local/share/open_jtalk_dic_utf_8-1.08/ /usr/local/share/open_jtalk/dic/utf-8


}

func_main
