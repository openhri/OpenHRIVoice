#!/bin/sh

target_name="hts-voice-nitech-jp-atr503-m001"
target_copyright="./lice_dir/hts_voice_copyright.txt"
target_url="http://downloads.sourceforge.net/open-jtalk/hts_voice_nitech_jp_atr503_m001-1.05.tar.gz"
target_installPath="/usr/local/share"

. ./func_setup.sh

func_main(){

# Show copyrigth.
cat $target_copyright |more
read ANS

# Accept licence and download software.
func_DL $target_name $target_url

# Set archive name in target_file .
target_file=`fun_getBasename $target_url`

# Extrac archive.
func_extracFile $target_file $target_installPath

# Set to Symbolic link.
/usr/bin/sudo /bin/ln -s /usr/local/share/hts_voice_nitech_jp_atr503_m001-1.05 /usr/local/share/hts-voiceccept licence and download software.


}

func_main
