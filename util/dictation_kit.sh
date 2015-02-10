#!/bin/sh

target_name="julius-runkit_with_dictation-kit"
target_copyright="./lice_dir/julius_copyright_utf8.txt"
target_url="http://sourceforge.jp/frs/redir.php?m=jaist&f=%2Fjulius%2F59050%2Fdictation-kit-v4.2.3.tar.gz"
target_option1="-O"
target_option2="dictation-kit-v4.2.3.tar.gz"
target_installPath="/usr/local/share"

. ./func_setup.sh

func_main(){

# Show Copyright.
cat $target_copyright |more
read ANS

# Accept licence and download software.
echo "${target_url}"

func_DL $target_name "${target_url}" "${target_option1}" "${target_option2}" 

# Set archive name in target_file .
target_file="dictation-kit-v4.2.3.tar.gz"

# Extrac archive.
#func_extracFile $target_file $target_installPath

# Set to Symbolic link.
#/usr/bin/sudo /bin/ln -s /usr/local/share/dictation-kit-v4.2.3 /usr/local/share/julius-runkit

}

func_main
