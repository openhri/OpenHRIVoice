#!/bin/sh


echo "--------------------------------------------------------------"
echo "-       Welcome to the OpenHRIVoice 2.10 setup script.       -"
echo "--------------------------------------------------------------"
echo ""
echo "This script will guide you through the installation of 3rdparty"
echo "software and voice data for OpenHRIVoice 2.10."
echo ""
echo "It is recommended that you dose all other applications bofore"
echo "starting Setup."
echo ""
echo "This will make it possible to update relevant system files"
echo "without having to reboot your computer."
echo ""
echo "Please review the license terms bofore installing  3rdparty"
echo "software."
echo "Press Page Down to see the rest of the agreement."
echo ""

#cat ./lice_dir/startup.txt | more
read ANS

./dictation_kit.sh
./mmdagent_example.sh
./hts_voice.sh
./open_jtalk_dic_utf_8.sh

