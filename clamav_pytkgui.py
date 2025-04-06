#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
THANKS TO :
https://docs.python.org/
https://www.pythontutorial.net/tkinter/
https://www.geeksforgeeks.org/python-tkinter-tutorial/
https://stackoverflow.com/questions/68198575/how-can-i-displaymy-console-output-in-tkinter
https://www.tutorialspoint.com/run-process-with-realtime-output-to-a-tkinter-gui
"""

# Standard library import.
import sys
import os
import locale
import configparser
import subprocess
from threading import Thread
from collections import OrderedDict as od

# Third-part library import.
import tkinter as tk
import tkinter.filedialog
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText

# Project library import.

######################

IHM = od([
('language', od([('label', {'text': ""}),
                 ('button1', {'text': '', 'image': '', 'command' : '', 'state': tk.NORMAL, 'class_addr': None}),
                 ('button2', {'text': '', 'image': '', 'command' : '', 'state': tk.NORMAL, 'class_addr': None}),
                 ('button3', {'text': '', 'image': '', 'command' : '', 'state': tk.NORMAL, 'class_addr': None}),
                 ])),
('parameters', od([('label', {'text': ""}),
                   ('button1', {'text': '', 'image': '', 'command' : '', 'state': tk.DISABLED, 'class_addr': None}),
                   ('button2', {'text': '', 'image': '', 'command' : '', 'state': tk.DISABLED, 'class_addr': None}),
                   ('button3', {'text': '', 'image': '', 'command' : '', 'state': tk.DISABLED, 'class_addr': None}),
                   ('button4', {'text': '', 'image': '', 'command' : '', 'state': tk.DISABLED, 'class_addr': None}),
                   ])),
('history', od([('label', {'text': ""}),
                   ('button1', {'text': '', 'image': '', 'command' : '', 'state': tk.DISABLED, 'class_addr': None}),
                   ('button2', {'text': '', 'image': '', 'command' : '', 'state': tk.DISABLED, 'class_addr': None}),
                   ])),
('update', od([('label', {'text': ""}),
                   ('button1', {'text': '', 'image': '', 'command' : '', 'state': tk.DISABLED, 'class_addr': None}),
                   ('button2', {'text': '', 'image': '', 'command' : '', 'state': tk.DISABLED, 'class_addr': None}),
                   ])),
('analyses', od([('label', {'text': ""}),
                   ('button1', {'text': '', 'image': '', 'command' : '', 'state': tk.DISABLED, 'class_addr': None}),
                   ('button2', {'text': '', 'image': '', 'command' : '', 'state': tk.NORMAL, 'class_addr': None}),
                   ('button3', {'text': '', 'image': '', 'command' : '', 'state': tk.DISABLED, 'class_addr': None}),
                   ])),
('quit', od([('label', {'text': ""}),
                 ('button1', {'text': '', 'image': '', 'command' : '', 'state': tk.NORMAL, 'class_addr': None}),
                 ])),
])

labels = {
'labelsFR': {'language': {'label': "langage",
                          'button1': "Fr", 'button2': "Jp", 'button3': "Uk"
                         },
             'parameters': {'label' : "Paramètres",
                            'button1': "Paramètres",
                            'button2': "Liste blanche",
                            'button3': "Réseau",
                            'button4': "Planificateur"
                            },
             'history': {'label': "Historique",
                         'button1': 'Historique',
                         'button2': 'Quarantaine'
                         },
             'update': {'label': "Mise à jour",
                        'button1': "Mise à jour",
                        'button2': "Assistant de mise jour"
                        },
             'analyses': {'label': "Analyses",
                          'button1': "Analyse d'un fichier",
                          'button2': "Analyse d'un répertoire",
                          'button3': "Analyses"
                          },
             'quit': {'label': "",
                      'button1': "Sortir"
                      }
            },
'labelsJP': {'language': {'label': "言語",
                          'button1': "仏", 'button2': "日", 'button3': "英"
                          },
             'parameters': {'label' : "パラメーター",
                            'button1': "パラメーター",
                            'button2': "認可リスト",
                            'button3': "ネットワーク",
                            'button4': "プランナー"
                            },
             'history': {'label': "歴史",
                         'button1': '歴史',
                         'button2': '隔離'
                         },
             'update': {'label': "アプデート",
                        'button1': "アプデート",
                        'button2': "アプデート補佐"
                        },
             'analyses': {'label': "分析",
                          'button1': "ファイル分析",
                          'button2': "ティレクトリー分析",
                          'button3': "分析"
                          },
             'quit': {'label': "",
                      'button1': "終"
                      }
             },
'labelsUK': {'language': {'label': "language",
                          'button1': "Fr", 'button2': "Jp", 'button3': "Uk"
                         },
             'parameters': {'label' : "Parameters",
                            'button1': "Paramèters",
                            'button2': "White list",
                            'button3': "Network",
                            'button4': "Scheduller"
                            },
             'history': {'label': "History",
                         'button1': 'History',
                         'button2': 'Quarantine'
                        },
             'update': {'label': "Update",
                        'button1': "Update",
                        'button2': "Update assistant"
                        },
             'analyses': {'label': "Analyses",
                          'button1': "File Analysis",
                          'button2': "Directory Analysis",
                          'button3': "Analyses"
                          },
             'quit': {'label': "",
                      'button1': "Quit"
                      }
             },
}

######################

class Config():
    """

    Public attributes.
    """

    # Private attributes.


    # Public methods.
    def __init__(self, reset_conf=False):
        """
        __init__ : initiate class
        @parameters : ...
        @return : none.
        """
        conf_dirs = {
        'linux': os.path.join(os.path.expanduser( '~' ), ".config", "clamAV_pygui"),
        'win32': os.path.join(os.path.expanduser( '~' ), "", "clamAV_pygui"),
        'default': os.path.join(os.path.expanduser( '~' ), "clamAV_pygui")
        }
        self.os = sys.platform
        self.confs = configparser.ConfigParser()

        conf_dir = conf_dirs[self.os] if self.os in conf_dirs else conf_dirs["default"]
        self.conf_file = os.path.join(conf_dir, 'clamAV_pygui.conf')
        if not os.path.exists(conf_dir):
            os.mkdir(conf_dir)
        if not os.path.exists(self.conf_file) or reset_conf == True:
            print("Reset configuration !")
            self.init_1st_conf()
            self.write_conf()
        else:
            self.read_conf()

    def init_1st_conf(self):
        """
        """
        default_confs = {
            'parameters': {
                'lang': 'auto',
                'clamscan_bin': 'clamscan'
                          },
            'whitelist': {
                'Do_no_scan_dirs': []
                         },
            'network': {
                'proxy': 'None',
                'IP_host': '',
                'port': 8080
                       },
            'scheduler': {
                'analysis_hour': 00,
                'analysis_min': 00,
                'update_sign_hour': 00,
                'update_sign_min': 00,
                         }
                }

        for c, v in default_confs.items():
            self.confs[c] = v

    def read_conf(self):
        """
        """
        self.confs.read(self.conf_file)

    def write_conf(self):
        """
        """
        with open(self.conf_file, 'w') as conf_file_fd:
            self.confs.write(conf_file_fd)

class TKapp():
    """

    Public attributes.
    """

    # Private attributes.


    # Public methods.
    def __init__(self, conf):
        """
        __init__ : initiate class
        @parameters : ...
        @return : none.
        """
        self.conf = conf
        self.lang = self.conf.confs['parameters']['lang'] if self.conf.confs['parameters']['lang'] != "auto" else locale.getdefaultlocale()[0]
        print(self.lang)
        self.rootwin = tk.Tk()
        IHM['language']['button1']['image'] = tk.PhotoImage(file=os.path.join(os.getcwd(), "fr.png")).zoom(2, 2).subsample(3, 3)
        IHM['language']['button2']['image'] = tk.PhotoImage(file=os.path.join(os.getcwd(), "ja.png")).zoom(2, 2).subsample(3, 3)
        IHM['language']['button3']['image'] = tk.PhotoImage(file=os.path.join(os.getcwd(), "en.png")).zoom(2, 2).subsample(3, 3)
        self.precise_command()
        self.prepare_locale(self.lang)
        self.design()

        self.rootterminal = tk.Toplevel()
        self.rootterminal.title("Output")
        self.terminal = ScrolledText(self.rootterminal, width=80,  height=25)
        button_temrinal = ttk.Button(self.rootterminal, text='Ok', compound=tk.RIGHT, command=self.rootterminal.withdraw, state=tk.NORMAL)
        self.terminal.config(fg="#F0F0F0", bg="#282C34", insertbackground="white")
        self.terminal.pack(padx = 10, pady=10,  fill=tk.BOTH, side=tk.TOP, expand=True)
        button_temrinal.pack(side=tk.BOTTOM, pady=10)
        self.rootterminal.withdraw()

    def precise_command(self):
        """
        """
        IHM['language']['button1']['command'] = self.on_Fr_btn
        IHM['language']['button2']['command'] = self.on_Jp_btn
        IHM['language']['button3']['command'] = self.on_Uk_btn
        IHM['parameters']['button1']['command'] = None
        IHM['parameters']['button2']['command'] = None
        IHM['parameters']['button3']['command'] = None
        IHM['parameters']['button4']['command'] = None
        IHM['history']['button1']['command'] = None
        IHM['history']['button2']['command'] = None
        IHM['update']['button1']['command'] = None
        IHM['update']['button2']['command'] = None
        IHM['analyses']['button1']['command'] = None
        IHM['analyses']['button2']['command'] = self.on_Analyses_dir_btn
        IHM['analyses']['button3']['command'] = None
        IHM['quit']['button1']['command'] = self.rootwin.destroy

    def design(self):
        """
        """
        window_width = 800
        window_height = 600
        screen_width = self.rootwin.winfo_screenwidth()
        screen_height = self.rootwin.winfo_screenheight()
        center_x = int(screen_width/2 - window_width / 2)
        center_y = int(screen_height/2 - window_height / 2)
        self.rootwin.minsize(window_width, window_height)

        self.rootwin.title("clamAV Python3 TK GUI - Quicky done version")
        self.rootwin.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

        self.refresh()

        self.rootwin.bind('<Escape>', lambda e: self.rootwin.destroy()) # TO REMOVE IN PROD

    def refresh(self):
        """
        """
        try:
            for widget in self.widgets_text:
                widget.destroy()
            self.widgets_text = []
        except:
            self.widgets_text = []

        for k0 in IHM.keys():
            for k1 in IHM[k0].keys():
                if k1 == 'label':
                    if k0 == 'quit':
                        lblfrm = ttk.Label(self.rootwin)
                        self.widgets_text.append(lblfrm)
                        lblfrm.pack(expand='yes', fill=tk.BOTH, padx=10, pady=5)
                    else:
                        lblfrm = ttk.LabelFrame(self.rootwin, text=IHM[k0]['label']['text'])
                        self.widgets_text.append(lblfrm)
                        lblfrm.pack(expand='yes', fill=tk.BOTH, padx=10, pady=5)
                elif k1.startswith('button'):
                    btn = ttk.Button(lblfrm, text=IHM[k0][k1]['text'], image=IHM[k0][k1]['image'], compound=tk.RIGHT, command=IHM[k0][k1]['command'], state=IHM[k0][k1]['state'])
                    self.widgets_text.append(btn)
                    if IHM[k0][k1]['class_addr'] == None:
                        IHM[k0][k1]['class_addr'] = btn
                    btn.pack(side=tk.LEFT, padx=20, pady=20)

    def prepare_locale(self, wanted_locale):
        locales = {'fr_FR': 'labelsFR', 'C': 'labelsUK', 'ja_JP': 'labelsJP'}
        for k0 in IHM.keys():
            for k1 in IHM[k0].keys():
                IHM[k0][k1]['text'] = labels[locales[wanted_locale]][k0][k1]

    def run(self):
        """
        """
        self.rootwin.mainloop()

    def on_Analyses_dir_btn(self):
        """
        """
        dir_choose = tk.filedialog.askdirectory(title='Choose a directory', initialdir=os.getcwd())
        IHM['analyses']['button2']['class_addr'].configure(state=tk.DISABLED)
        self.rootterminal.deiconify()
        self.terminal.configure(state=tk.NORMAL)
        self.terminal.delete("1.0", "end")
        self.terminal.configure(state=tk.DISABLED)
        process_thread = Thread(target=run_clamscan, name='T_run_clamscan', args=[self, self.conf, dir_choose, 'button2'])
        process_thread.start()

    def on_Fr_btn(self):
        """
        """
        self.lang = 'fr_FR'
        self.prepare_locale(self.lang)
        self.refresh()

    def on_Jp_btn(self):
        """
        """
        self.lang = 'ja_JP'
        self.prepare_locale(self.lang)
        self.refresh()

    def on_Uk_btn(self):
        """
        """
        self.lang = 'C'
        self.prepare_locale(self.lang)
        self.refresh()

class TerminalInfo(object):
    """

    Public attributes.
    """

    # Private attributes.


    # Public methods.
    def __init__(self, textbox):
        self.textbox = textbox

    def write(self, text):
        self.textbox.configure(state=tk.NORMAL)
        self.textbox.insert("end", text)
        self.textbox.see("end")
        self.textbox.configure(state=tk.DISABLED)

    def flush(self):
        pass


def run_clamscan(tk_app, conf, dir_to_scan, calling_btn):
    """
    """
    cde_line = [conf.confs['parameters']['clamscan_bin'], dir_to_scan]

    terminalinfo = TerminalInfo(tk_app.terminal)
    sys.stdout = terminalinfo
    print("Scan from :", dir_to_scan)
    with subprocess.Popen(cde_line, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=1, universal_newlines=True) as p:
        for line in p.stdout:
            print(line, end='')
    sys.stdout = sys.__stdout__

    IHM['analyses'][calling_btn]['class_addr'].configure(state=tk.NORMAL)

def main(args):
    """
    Main function.
    @parameters : some arguments, in case of use.
    @return : 0 = all was good.
              ... = some problem occures.
    """
    reset = True if len(args) != 0 and args[0] == '--reset' else False

    try:
        conf = Config(reset)
    except BaseException as e:
        print(e)
        return 1
    print(conf.os)
    print(conf.conf_file)

    try:
        app = TKapp(conf)
        app.run()
    except BaseException as e:
        print(sys.exc_info()[2].tb_lineno)
        print(e)
        return 2

    return 0

######################

if __name__ == "__main__":
    rc = main(sys.argv[1:])      # Keep only the argus after the script name.
    sys.exit(rc)
