#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''OpenJTalk speech synthesis component

Copyright (C) 2010
    Yosuke Matsusaka
    Intelligent Systems Research Institute,
    National Institute of Advanced Industrial Science and Technology (AIST),
    Japan
    All rights reserved.
Licensed under the Eclipse Public License -v 1.0 (EPL)
http://www.opensource.org/licenses/eclipse-1.0.txt
'''

import os
import sys
import time
import subprocess
import signal
import tempfile
import traceback
import platform
import codecs
import locale
import optparse
import wave
import socket
import OpenRTM_aist
import RTC
from openhrivoice.__init__ import __version__
from openhrivoice import utils
from openhrivoice.config import config
from openhrivoice.parseopenjtalk import parseopenjtalk
from openhrivoice.VoiceSynthComponentBase import *
try:
    import gettext
    _ = gettext.translation(domain='openhrivoice', localedir=os.path.dirname(__file__)+'/../share/locale').ugettext
except:
    _ = lambda s: s

__doc__ = _('Japanese speech synthesis component.')

class mysocket(socket.socket):
    def getline(self):
        s = ""
        buf = self.recv(1)
        while buf and buf[0] != "\n":
            s += buf[0]
            buf = self.recv(1)
            if not buf:
                break
        return s

class OpenJTalkWrap(VoiceSynthBase):
    def __init__(self):
        VoiceSynthBase.__init__(self)
        self._conf = config()
        self._args = ()
# harumi 2014.12.04 Change with a change voice form of open_jtalk ver 1.07.
#        self._args = (("td", "tree-dur.inf"),
#                      ("tf", "tree-lf0.inf"),
#                      ("tm", "tree-mgc.inf"),
#                      ("md", "dur.pdf"),
#                      ("mf", "lf0.pdf"),
#                      ("mm", "mgc.pdf"),
#                      ("df", "lf0.win1"),
#                      ("df", "lf0.win2"),
#                      ("df", "lf0.win3"),
#                      ("dm", "mgc.win1"),
#                      ("dm", "mgc.win2"),
#                      ("dm", "mgc.win3"),
#                      ("ef", "tree-gv-lf0.inf"),
#                      ("em", "tree-gv-mgc.inf"),
#                      ("cf", "gv-lf0.pdf"),
#                      ("cm", "gv-mgc.pdf"),
#                      ("k", "gv-switch.inf"))
        cmdarg = []
        cmdarg.append(self._conf._openjtalk_bin)
        (stdoutstr, stderrstr) = subprocess.Popen(cmdarg, stdout = subprocess.PIPE, stderr = subprocess.PIPE).communicate()
        self._copyrights = []
        for l in stderrstr.replace('\r', '').split('\n\n'):
            if l.count('All rights reserved.') > 0:
                self._copyrights.append(l)
        self._copyrights.append('''The Nitech Japanese Speech Database "NIT ATR503 M001"
released by HTS Working Group (http://hts.sp.nitech.ac.jp/)
Copyright (C) 2003-2011  Nagoya Institute of Technology
Some rights reserved.
''')
        self._copyrights.append('''HTS Voice "Mei (Normal)"
released by MMDAgent Project Team (http://www.mmdagent.jp/)
Copyright (C) 2009-2011  Nagoya Institute of Technology
Some rights reserved.
''')

    def synthreal(self, data, samplerate, character):
        textfile = self.gettempname()
        wavfile = self.gettempname()
        logfile = self.gettempname()
        # text file which specifies synthesized string
        fp = codecs.open(textfile, 'w', 'utf-8')
        fp.write(u"%s\n" % (data,))
        fp.close()
        # command line for OpenJTalk
        cmdarg = []
        cmdarg.append(self._conf._openjtalk_bin)
        # harumi 2014.12.04 Change to comment out with a change voice form of open_jtalk ver 1.07.
        #for o, v in self._args:
        #    cmdarg.append("-"+o)
        #    if character == "female":
        #        cmdarg.append(os.path.join(self._conf._openjtalk_phonemodel_female_ja, v))
        #    else:
        #        cmdarg.append(os.path.join(self._conf._openjtalk_phonemodel_male_ja, v))
        if character == "female":
            cmdarg.append("-m")
            cmdarg.append(self._conf._openjtalk_phonemodel_female_ja)
        else:
            cmdarg.append("-m")
            cmdarg.append(self._conf._openjtalk_phonemodel_male_ja)

        cmdarg.append("-z")
        cmdarg.append("2000")
#        cmdarg.append("-s")
#        cmdarg.append("16000")
#        cmdarg.append("-p")
#        cmdarg.append("160")
        cmdarg.append("-x")
        cmdarg.append(self._conf._openjtalk_dicfile_ja)
        cmdarg.append("-ow")
        cmdarg.append(wavfile)
        cmdarg.append("-ot")
        cmdarg.append(logfile)
        cmdarg.append(textfile)
        # run OpenJTalk
        p = subprocess.Popen(cmdarg)
        p.wait()
        # convert samplerate
        if samplerate != 32000:
            wavfile2 = self.gettempname()
            cmdarg = [self._conf._sox_bin, "-t", "wav", wavfile, "-r", str(samplerate), "-t", "wav", wavfile2]
            p = subprocess.Popen(cmdarg)
            p.wait()
            os.remove(wavfile)
            wavfile = wavfile2
        # read duration data
        d = parseopenjtalk()
        d.parse(logfile)
        durationdata = d.toseg().encode("utf-8")
        os.remove(textfile)
        os.remove(logfile)
        return (durationdata, wavfile)
    
    def terminate(self):
        pass

OpenJTalkRTC_spec = ["implementation_id", "OpenJTalkRTC",
                     "type_name",         "OpenJTalkRTC",
                     "description",       __doc__.encode('UTF-8'),
                     "version",           __version__,
                     "vendor",            "AIST",
                     "category",          "communication",
                     "activity_type",     "DataFlowComponent",
                     "max_instance",      "5",
                     "language",          "Python",
                     "lang_type",         "script",
                     "conf.default.format", "int16",
                     "conf.__widget__.format", "radio",
                     "conf.__constraints__.format", "(int16)",
                     "conf.__description__.format", _("Format of output audio (fixed to 16bit).").encode('UTF-8'),
                     "conf.default.rate", "16000",
                     "conf.__widget__.rate", "spin",
                     "conf.__constraints__.rate", "16000",
                     "conf.__description__.rate", _("Sampling frequency of output audio (fixed to 16kHz).").encode('UTF-8'),
                     "conf.default.character", "male",
                     "conf.__widget__.character", "radio",
                     "conf.__constraints__.character", "(male, female)",
                     "conf.__description__.character", _("Character of the voice.").encode('UTF-8'),
                     ""]

class OpenJTalkRTC(VoiceSynthComponentBase):
    def __init__(self, manager):
        VoiceSynthComponentBase.__init__(self, manager)

    def onInitialize(self):
        VoiceSynthComponentBase.onInitialize(self)
        self._wrap = OpenJTalkWrap()
        self._logger.RTC_INFO("This component depends on following softwares and datas:")
        self._logger.RTC_INFO('')
        for c in self._wrap._copyrights:
            for l in c.strip('\n').split('\n'):
                self._logger.RTC_INFO('  '+l)
            self._logger.RTC_INFO('')
        return RTC.RTC_OK
    
class OpenJTalkRTCManager:
    def __init__(self):
        encoding = locale.getpreferredencoding()
        sys.stdout = codecs.getwriter(encoding)(sys.stdout, errors = "replace")
        sys.stderr = codecs.getwriter(encoding)(sys.stderr, errors = "replace")

        parser = utils.MyParser(version=__version__, description=__doc__)
        utils.addmanageropts(parser)
        try:
            opts, args = parser.parse_args()
        except optparse.OptionError, e:
            print >>sys.stderr, 'OptionError:', e
            sys.exit(1)
        self._comp = None
        self._manager = OpenRTM_aist.Manager.init(utils.genmanagerargs(opts))
        self._manager.setModuleInitProc(self.moduleInit)
        self._manager.activateManager()

    def start(self):
        self._manager.runManager(False)

    def moduleInit(self, manager):
        profile=OpenRTM_aist.Properties(defaults_str=OpenJTalkRTC_spec)
        manager.registerFactory(profile, OpenJTalkRTC, OpenRTM_aist.Delete)
        self._comp = manager.createComponent("OpenJTalkRTC")

def main():
    manager = OpenJTalkRTCManager()
    manager.start()

if __name__=='__main__':
    main()
