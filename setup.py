#!/usr/bin/env python

from setuptools import setup, find_packages
from setuptools.command.build_ext import build_ext
import sys, os
from glob import glob
from openhrivoice.__init__ import __version__

cmd_classes = {}
try:
    from DistUtilsExtra.command import *
    cmd_classes.update({"build": build_extra.build_extra,
                        "build_i18n" :  build_i18n.build_i18n})
except ImportError:
    pass

try:
    import py2exe
    sys.path.append("openhrivoice2.10")
except ImportError:
    pass

data_files = []

if sys.platform == "win32":
    # py2exe options
    extra = {
        "console": [
                    "openhrivoice/JuliusRTC.py",
                    "openhrivoice/srgstopls.py",
                    "openhrivoice/srgstojulius.py",
                    "openhrivoice/validatesrgs.py",
                    "openhrivoice/bundlexinclude.py",
                    "openhrivoice/plstosinglewordgrammar.py",
                    "openhrivoice/OpenJTalkRTC.py",
                    "openhrivoice/FestivalRTC.py",
                    "openhrivoice/CombineResultsRTC.py",
                    "openhrivoice/XSLTRTC.py",
                    "openhrivoice/WavePlayerRTC.py",
                    "openhrivoice/srgseditor.py",
                    ],
        "options": {
            "py2exe": {
                "includes": ["xml.etree.ElementTree", "lxml._elementpath", "OpenRTM_aist", "RTC",
                             "cairo", "pango", "pangocairo",
                             "atk", "gobject", "gio", "glib", "gtk", "gtksourceview2"],
                "dll_excludes": ["USP10.dll", "NSI.dll", "MSIMG32.dll", "DNSAPI.dll", "ierutil.dll", "powrprof.dll", "msimg32.dll", "mpr.dll", "urlmon.dll", "dnsapi.dll"],
            }
        }
    }
else:
    extra = {}

setup(name='openhrivoice',
      cmdclass=cmd_classes,
      version=__version__,
      description="Voice components for OpenRTM (part of OpenHRI softwares)",
      long_description="""Voice components for OpenRTM (part of OpenHRI softwares).""",
      classifiers=[],
      keywords='',
      author='Yosuke Matsusaka',
      author_email='yosuke.matsusaka@aist.go.jp',
      url='http://openhri.net/',
      license='EPL',
      data_files = [('/usr/share/openhrivoice2.10',['util/setup_3rdparty_1204.sh',
						    'util/dictation_kit.sh','util/func_setup.sh',
						    'util/mmdagent_example.sh',
						    'util/uninstall_3rdparty.sh',
						    'util/hts_voice.sh',
					      	    'util/open_jtalk_dic_utf_8.sh']),
		    ('/usr/share/openhrivoice2.10/lice_dir',['util/lice_dir/hts_voice_copyright.txt',
							     'util/lice_dir/mmdagent_mei_copyright.txt',
							     'util/lice_dir/julius_copyright_utf8.txt',
							     'util/lice_dir/utf_8_copyright.txt'])],
      packages=find_packages(exclude=['ez_setup', 'doc', 'examples', 'tests']),
      include_package_data=True,
      package_data={'openhrivoice': ['*.dfa', '*.dict', '*.xsd']},
      zip_safe=False,
      install_requires=[
        # -*- Extra requirements: -*-
        ],
      entry_points="""
      [console_scripts]
      openjtalkrtc = openhrivoice.OpenJTalkRTC:main
      juliusrtc = openhrivoice.JuliusRTC:main
      srgstopls = openhrivoice.srgstopls:main
      srgstojulius = openhrivoice.srgstojulius:main
      validatesrgs = openhrivoice.validatesrgs:main
      bundlexinclude = openhrivoice.bundlexinclude:main
      plstosinglewordgrammar = openhrivoice.plstosinglewordgrammar:main
      juliustographviz = openhrivoice.juliustographviz:main
      maryrtc = openhrivoice.MARYRTC:main
      festivalrtc = openhrivoice.FestivalRTC:main
      combineresultsrtc = openhrivoice.CombineResultsRTC:main
      xsltrtc = openhrivoice.XSLTRTC:main
      waveplayerrtc = openhrivoice.WavePlayerRTC:main
      openhrivoicemanager = openhrivoice.OpenHRIVoiceManager:main
      srgseditor = openhrivoice.srgseditor:main
      """,
      **extra
      )
