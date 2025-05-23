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
import datetime
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
('language', od([('framelabel', {'text': '', 'widget_addr': None}),
                 ('button1', {'text': '', 'image': '', 'command' : '', 'state': tk.DISABLED, 'widget_addr': None}),
                 ('button2', {'text': '', 'image': '', 'command' : '', 'state': tk.DISABLED, 'widget_addr': None}),
                 ('button3', {'text': '', 'image': '', 'command' : '', 'state': tk.DISABLED, 'widget_addr': None}),
                 ])),
('clamscan_bin', od([('framelabel', {'text': '', 'widget_addr': None}),
                   ('button1', {'text': '', 'image': '', 'command' : '', 'state': tk.DISABLED, 'widget_addr': None}),
                   ])),
('history', od([('framelabel', {'text': '', 'widget_addr': None}),
                   ('button1', {'text': '', 'image': '', 'command' : '', 'state': tk.DISABLED, 'widget_addr': None}),
#                   ('button2', {'text': '', 'image': '', 'command' : '', 'state': tk.DISABLED, 'widget_addr': None}),
                   ('button3', {'text': '', 'image': '', 'command' : '', 'state': tk.DISABLED, 'widget_addr': None}),
                   ])),
('white_list', od([('framelabel', {'text': '', 'widget_addr': None}),
                   ('button1', {'text': '', 'image': '', 'command' : '', 'state': tk.DISABLED, 'widget_addr': None}),
                   ('button2', {'text': '', 'image': '', 'command' : '', 'state': tk.DISABLED, 'widget_addr': None}),
                   ])),
('analyses', od([('framelabel', {'text': '', 'widget_addr': None}),
                   ('button1', {'text': '', 'image': '', 'command' : '', 'state': tk.DISABLED, 'widget_addr': None}),
                   ('button2', {'text': '', 'image': '', 'command' : '', 'state': tk.DISABLED, 'widget_addr': None}),
                   ('virus_db_label', {'text': '', 'widget_addr': None})
                   ])),
('quit', od([('framelabel', {'text': '', 'widget_addr': None}),
                 ('button1', {'text': '', 'image': '', 'command' : '', 'state': tk.DISABLED, 'widget_addr': None}),
                 ])),
])

labels = {
'labelsFR': {'language': {'framelabel': "langage",
                          'button1': "Fr", 'button2': "Jp", 'button3': "Uk"
                         },
             'clamscan_bin': {'framelabel' : "Chemin de clamAV",
                            'button1': "Chemin de l'exécutable",
                            },
             'history': {'framelabel': "Historique",
                         'button1': 'Historique',
#                         'button2': 'Quarantaine',
                         'button3': "Chemin des logs",
                         },
             'white_list': {'framelabel': "Liste blanche",
                        'button1': "Choisir les fichiers à ne pas ananalyser",
                        'button2': "Choisir les répertoires à ne pas ananalyser",
                        },
             'analyses': {'framelabel': "Analyses",
                          'button1': "Analyse d'un fichier",
                          'button2': "Analyse d'un répertoire",
                          'virus_db_OK': "BdD virus <= 7 jours - OK",
                          'virus_db_WARN': "BdD virus > 7 jours - Faire la mise à jour",
                          },
             'quit': {'framelabel': "",
                      'button1': "Sortir"
                      }
            },
'labelsJP': {'language': {'framelabel': "言語",
                          'button1': "仏", 'button2': "日", 'button3': "英"
                          },
             'clamscan_bin': {'framelabel' : "ClamAVの道",
                            'button1': "実行ファイル道",
                            },
             'history': {'framelabel': "歴史",
                         'button1': '歴史',
#                         'button2': '隔離',
                         'button3': "ローグ道",
                         },
             'white_list': {'framelabel': "認可リスト",
                        'button1': "分析はしないファイルを選択",
                        'button2': "分析はしないティレクトリーを選択",
                        },
             'analyses': {'framelabel': "分析",
                          'button1': "ファイル分析",
                          'button2': "ティレクトリー分析",
                          'virus_db_OK': "ウイルスデータベース <= ７日 - OK",
                          'virus_db_WARN': "ウイルスデータベース > ７日 - アップデートご注意",
                          },
             'quit': {'framelabel': "",
                      'button1': "終"
                      }
             },
'labelsUK': {'language': {'framelabel': "language",
                          'button1': "Fr", 'button2': "Jp", 'button3': "Uk"
                         },
             'clamscan_bin': {'framelabel' : "ClamAV path",
                            'button1': "Executable path",
                            },
             'history': {'framelabel': "History",
                         'button1': 'History',
#                         'button2': 'Quarantine',
                         'button3': "Logs path",
                        },
             'white_list': {'framelabel': "White list",
                        'button1': "Choose file do not analysis",
                        'button2': "Choose directories do not analysis",
                        },
             'analyses': {'framelabel': "Analyses",
                          'button1': "File Analysis",
                          'button2': "Directory Analysis",
                          'virus_db_OK': "Virus DB <= 7 days - OK",
                          'virus_db_WARN': "Virus DB > 7 days - Make update",
                          },
             'quit': {'framelabel': "",
                      'button1': "Quit"
                      }
             },
}

win_titles = {
'fr_FR': {'main': "clamAV Python3 TK GUI - Version faite rapidement",
          'choose_dir': "Choisir un répertoire",
          'choose_files': "Choisir un ou plusieurs fichiers",
          'output': "Sortie de terminal"},
'ja_JP': {'main': "clamAV Python3 TK GUI - 急に出たバーション",
          'choose_dir': "ディレクトリを選択",
          'choose_files': "ファイルを選択",
          'output': "端末出力"},
'C': {'main': "clamAV Python3 TK GUI - Quicky done version",
      'choose_dir': "Choose a directory",
      'choose_files': "Choose one or several file",
      'output': "Terminal output"}
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
        'linux': os.path.join(os.path.expanduser( '~' ), ".config", "clamav_pytkgui"),
        'win32': os.path.join(os.path.expanduser( '~' ), "", "clamav_pytkgui"),
        'default': os.path.join(os.path.expanduser( '~' ), "clamav_pytkgui")
        }
        self.os = sys.platform
        self.confs = configparser.ConfigParser()

        conf_dir = conf_dirs[self.os] if self.os in conf_dirs else conf_dirs["default"]
        self.conf_file = os.path.join(conf_dir, 'clamav_pytkgui.conf')
        if not os.path.exists(conf_dir):
            os.mkdir(conf_dir)
        if not os.path.exists(self.conf_file) or reset_conf == True:
            print("Reset configuration !")
            self.init_1st_conf()
            self.write_conf()
        else:
            self.read_conf()

        if self.confs['parameters']['lang'] == "auto":
            self.confs['parameters']['lang'] = locale.getlocale()[0]

        self.subproc = None

    def init_1st_conf(self):
        """
        """
        clamscan_dirs = {
        'linux': '/usr/bin/clamscan',
        'win32': 'C:\Program Files\ClamAV\clamscan.exe',
        'default': ''
        }

        default_confs = {
            'parameters': {
                'lang': 'auto',
                'clamscan_bin': clamscan_dirs[self.os],
                'clamscan_logs': clamscan_dirs[self.os]
                          },
            'whitelist': {
                'Do_no_scan_dirs': []
                         },
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

class Clamav_utils():
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

class Clamav_pytkgui(Config, Clamav_utils):
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

        Config.__init__(self, reset_conf)
        Clamav_utils.__init__(self)

        self.virus_db_is_old = False if check_virus_db() < 8 else True

        self.rootwin = tk.Tk()

        IHM['language']['button1']['image'] = tk.PhotoImage(file=os.path.join(os.getcwd(), "fr.png")).zoom(2, 2).subsample(3, 3)
        IHM['language']['button2']['image'] = tk.PhotoImage(file=os.path.join(os.getcwd(), "ja.png")).zoom(2, 2).subsample(3, 3)
        IHM['language']['button3']['image'] = tk.PhotoImage(file=os.path.join(os.getcwd(), "en.png")).zoom(2, 2).subsample(3, 3)
        IHM['language']['button1']['command'] = self.on_Fr_btn
        IHM['language']['button2']['command'] = self.on_Jp_btn
        IHM['language']['button3']['command'] = self.on_Uk_btn
        IHM['clamscan_bin']['button1']['command'] = self.on_clamscan_bin_btn
        IHM['history']['button1']['command'] = self.on_history_btn
#        IHM['history']['button2']['command'] = None
        IHM['history']['button3']['command'] = self.on_history_clamscan_logs_btn
        IHM['white_list']['button1']['command'] = None
        IHM['white_list']['button2']['command'] = None
        IHM['analyses']['button1']['command'] = self.on_analyses_file_btn
        IHM['analyses']['button2']['command'] = self.on_analyses_dir_btn
        IHM['quit']['button1']['command'] = self.terminate

        self.rootterminal = tk.Toplevel()
        self.rootterminal.title(win_titles[self.confs['parameters']['lang']]['output'])
        self.terminal = ScrolledText(self.rootterminal, width=80,  height=25)
        button_terminal = ttk.Button(self.rootterminal, text='Ok', compound=tk.RIGHT, command=self.hide_rootterminal, state=tk.NORMAL)
        self.terminal.config(fg="#F0F0F0", bg="#282C34", insertbackground="white")
        self.terminal.pack(padx = 10, pady=10,  fill=tk.BOTH, side=tk.TOP, expand=True)
        button_terminal.pack(side=tk.BOTTOM, pady=10)
        self.rootterminal.withdraw()

        self.prepare_locale(self.confs['parameters']['lang'])
        self.design()

    def hide_rootterminal(self):
        """
        """
        if self.subproc:
            self.subproc.terminate()
        self.rootterminal.withdraw()
        IHM['analyses']['button1']['widget_addr'].configure(state=tk.NORMAL)
        IHM['analyses']['button2']['widget_addr'].configure(state=tk.NORMAL)

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

        self.rootwin.title(win_titles[self.confs['parameters']['lang']]['main'])
        self.rootwin.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

        self.rootwin.bind('<Escape>', lambda e: self.terminate()) # TO REMOVE IN PROD

        for frmlbl in IHM.keys():
            for widget in IHM[frmlbl].keys():
                if widget == 'framelabel':
                    if frmlbl == 'quit':
                        lblfrm = ttk.Label(self.rootwin)
                        lblfrm.pack(expand='yes', fill=tk.BOTH, padx=10, pady=5)
                    else:
                        lblfrm = ttk.LabelFrame(self.rootwin, text=IHM[frmlbl]['framelabel']['text'])
                        lblfrm.pack(expand='yes', fill=tk.BOTH, padx=10, pady=5)
                    if IHM[frmlbl][widget]['widget_addr'] == None:
                        IHM[frmlbl][widget]['widget_addr'] = lblfrm
                elif widget.startswith('button'):
                    IHM[frmlbl][widget]['state'] = tk.NORMAL if IHM[frmlbl][widget]['command'] else tk.DISABLED
                    btn = ttk.Button(lblfrm, text=IHM[frmlbl][widget]['text'], image=IHM[frmlbl][widget]['image'], compound=tk.RIGHT, command=IHM[frmlbl][widget]['command'], state=IHM[frmlbl][widget]['state'])
                    if IHM[frmlbl][widget]['widget_addr'] == None:
                        IHM[frmlbl][widget]['widget_addr'] = btn
                    btn.pack(side=tk.LEFT, padx=20, pady=20)
            if frmlbl == "clamscan_bin":
                clamscan_bin_frame = ttk.Frame(lblfrm, borderwidth=1, relief=tk.SOLID)
                clamscan_bin_frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=20, pady=10)
                self.clamscan_bin_label = ttk.Label(clamscan_bin_frame, text=self.confs['parameters']['clamscan_bin'])
                self.clamscan_bin_label.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=10)
            if frmlbl == "history":
                history_log_frame = ttk.Frame(lblfrm, borderwidth=1, relief=tk.SOLID)
                history_log_frame.pack(side=tk.BOTTOM, expand=True, fill=tk.BOTH, padx=20, pady=10)
                self.history_log_label = ttk.Label(history_log_frame, text=self.confs['parameters']['clamscan_logs'])
                self.history_log_label.pack(side=tk.BOTTOM, expand=True, fill=tk.X, padx=10)
            if frmlbl == "analyses":
                bg_color = "orange" if self.virus_db_is_old else "green"
                virus_db_frame = tk.Frame(lblfrm, bg=bg_color, borderwidth=1, relief=tk.SOLID)
                virus_db_frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=20, pady=10)
                self.virus_db_label = tk.Label(virus_db_frame, bg=bg_color, text=IHM[frmlbl]['virus_db_label']['text'])
                self.virus_db_label.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=10)
                IHM[frmlbl]['virus_db_label']['widget_addr'] = self.virus_db_label

    def refresh_text(self, ):
        """
        """
        for frmlbl in IHM.keys():
            for widget in IHM[frmlbl].keys():
                IHM[frmlbl][widget]['widget_addr'].configure(text=IHM[frmlbl][widget]['text'])

        self.rootwin.title(win_titles[self.confs['parameters']['lang']]['main'])
        self.rootterminal.title(win_titles[self.confs['parameters']['lang']]['output'])

    def prepare_locale(self, wanted_locale):
        """
        """
        locales = {'fr_FR': 'labelsFR', 'ja_JP': 'labelsJP', 'C': 'labelsUK'}
        for frmlbl in IHM.keys():
            for widget in IHM[frmlbl].keys():
                if widget is 'virus_db_label':
                    if self.virus_db_is_old:
                        IHM[frmlbl][widget]['text'] = labels[locales[wanted_locale]]['analyses']['virus_db_WARN']
                    else:
                        IHM[frmlbl][widget]['text'] = labels[locales[wanted_locale]]['analyses']['virus_db_OK']
                else:
                    IHM[frmlbl][widget]['text'] = labels[locales[wanted_locale]][frmlbl][widget]

    def run(self):
        """
        """
        self.rootwin.mainloop()

    def terminate(self):
        """
        """
        if self.subproc:
            self.subproc.terminate()
        self.rootwin.destroy()

    def on_history_btn(self):
        """
        """
        file_choose = tk.filedialog.askopenfile(mode='r', title=win_titles[self.confs['parameters']['lang']]['choose_files'], initialdir=self.confs['parameters']['clamscan_logs'])
        if file_choose:
            self.rootterminal.deiconify()
            self.terminal.configure(state=tk.NORMAL)
            self.terminal.delete("1.0", tk.END)
            for l in file_choose:
                self.terminal.insert
                self.terminal.insert(tk.END, l)
            file_choose.close()
            self.terminal.see("end")
            self.terminal.configure(state=tk.DISABLED)

    def on_history_clamscan_logs_btn(self):
        """
        self.confs['parameters']['clamscan_logs']
        """
        IHM['history']['button3']['widget_addr'].configure(state=tk.DISABLED)
        dir_choose = tk.filedialog.askdirectory(title=win_titles[self.confs['parameters']['lang']]['choose_dir'], initialdir=self.confs['parameters']['clamscan_logs'])
        if dir_choose:
            self.confs['parameters']['clamscan_logs'] = dir_choose
            self.history_log_label['text'] = dir_choose
            self.write_conf()
        IHM['history']['button3']['widget_addr'].configure(state=tk.NORMAL)

    def on_clamscan_bin_btn(self):
        """
        self.confs['parameters']['clamscan_bin']
        """
        IHM['clamscan_bin']['button1']['widget_addr'].configure(state=tk.DISABLED)
        file_choose = tk.filedialog.askfilename(title=win_titles[self.confs['parameters']['lang']]['choose_files'], initialdir=os.path.dirname(self.confs['parameters']['clamscan_bin']))
        if file_choose:
            self.confs['parameters']['clamscan_bin'] = file_choose
            self.clamscan_bin_label['text'] = file_choose
            self.write_conf()
        IHM['clamscan_bin']['button1']['widget_addr'].configure(state=tk.NORMAL)

    def on_analyses_dir_btn(self):
        """
        """
        IHM['analyses']['button2']['widget_addr'].configure(state=tk.DISABLED)
        dir_choose = tk.filedialog.askdirectory(title=win_titles[self.confs['parameters']['lang']]['choose_dir'], initialdir=os.getcwd())
        if dir_choose:
            dir_choose = os.sep.join(dir_choose.split('/'))     # Because of Windows '\' directory separator portability.
            self.rootterminal.deiconify()
            self.terminal.configure(state=tk.NORMAL)
            self.terminal.delete("1.0", tk.END)
            self.terminal.configure(state=tk.DISABLED)
            process_thread = Thread(target=run_clamscan_dir, name='T_run_clamscan_dir', args=[self, self.confs['parameters']['clamscan_bin'], self.confs['parameters']['clamscan_logs'], dir_choose])
            process_thread.start()
        else:
            IHM['analyses']['button2']['widget_addr'].configure(state=tk.NORMAL)

    def on_analyses_file_btn(self):
        """
        """
        IHM['analyses']['button1']['widget_addr'].configure(state=tk.DISABLED)
        files_choose = tk.filedialog.askopenfilename(title=win_titles[self.confs['parameters']['lang']]['choose_files'], initialdir=os.getcwd(), multiple=True)
        if files_choose:
            files_choose = tuple([os.sep.join(file_choose.split('/')) for file_choose in files_choose])   # Because of Windows '\' directory separator portability.
            self.rootterminal.deiconify()
            self.terminal.configure(state=tk.NORMAL)
            self.terminal.delete("1.0", tk.END)
            self.terminal.configure(state=tk.DISABLED)
            process_thread = Thread(target=run_clamscan_files, name='T_run_clamscan_files', args=[self, self.confs['parameters']['clamscan_bin'], self.confs['parameters']['clamscan_logs'], files_choose])
            process_thread.start()
        else:
            IHM['analyses']['button1']['widget_addr'].configure(state=tk.NORMAL)

    def change_lang(self, lang_is):
        """
        """
        self.confs['parameters']['lang'] = lang_is
        self.prepare_locale(self.confs['parameters']['lang'])
        self.refresh_text()
        self.write_conf()

    def on_Fr_btn(self):
        """
        """
        self.change_lang('fr_FR')

    def on_Jp_btn(self):
        """
        """
        self.change_lang('ja_JP')

    def on_Uk_btn(self):
        """
        """
        self.change_lang('C')

class TerminalInfo(object):
    """

    Public attributes.
    """

    # Private attributes.


    # Public methods.
    def __init__(self, textbox):
        """
        __init__ : initiate class
        @parameters : ...
        @return : none.
        """
        self.textbox = textbox

    def write(self, text):
        """
        """
        self.textbox.configure(state=tk.NORMAL)
        self.textbox.insert(tk.END, text)
        self.textbox.see(tk.END)
        self.textbox.configure(state=tk.DISABLED)

    def flush(self):
        """
        Just need by TerminalInfo
        """
        pass

def compute_clamscan_log_full(clamscan_logs):
    """
    """
    d = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
    return os.path.join(clamscan_logs, f"clamscan-{d}.log")

def check_virus_db():
    """
    """
    cde_line = ['clamscan', '--version']
    rsl = subprocess.run(cde_line, capture_output=True)
    date_last_db_virus = rsl.stdout.decode('utf-8').split("/")[2].strip()
    date_last_db_virus = datetime.datetime.date(datetime.datetime.strptime(date_last_db_virus, '%c'))
    date_today = datetime.datetime.date(datetime.datetime.now())
    return (date_today - date_last_db_virus).days

def run_clamscan_dir(tk_app, clamscan_bin, clamscan_logs, dir_to_scan):
    """
    """
    clamscan_logs_full = compute_clamscan_log_full(clamscan_logs)
    cde_line = [clamscan_bin, '-l', clamscan_logs_full, dir_to_scan]
    terminalinfo = TerminalInfo(tk_app.terminal)
    sys.stdout = terminalinfo
    with subprocess.Popen(cde_line, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=1, universal_newlines=True) as p:
        tk_app.subproc = p
        for line in p.stdout:
            print(line, end='')
    sys.stdout = sys.__stdout__

def run_clamscan_files(tk_app, clamscan_bin, clamscan_logs, files_to_scan):
    """
    """
    clamscan_logs_full = compute_clamscan_log_full(clamscan_logs)
    cde_line = [clamscan_bin, '-l', clamscan_logs_full]
    cde_line += files_to_scan
    terminalinfo = TerminalInfo(tk_app.terminal)
    sys.stdout = terminalinfo
    with subprocess.Popen(cde_line, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=1, universal_newlines=True) as p:
        tk_app.subproc = p
        for line in p.stdout:
            print(line, end='')
    sys.stdout = sys.__stdout__

def main(args):
    """
    Main function.
    @parameters : some arguments, in case of use.
    @return : 0 = all was good.
              ... = some problem occures.
    """
    reset = True if len(args) != 0 and args[0] == '--reset' else False

#    try:
#        app = TKapp(conf)
    app = Clamav_pytkgui(reset)

    print(app.os, flush=True)          # Because of Windows terminal.
    print(app.conf_file)
    print(app.confs['parameters']['lang'])

    app.run()
#    except BaseException as e:
#        print(sys.exc_info()[2].tb_lineno)
#        print(e)
#        return 1

    return 0

######################

if __name__ == "__main__":
    rc = main(sys.argv[1:])      # Keep only the argus after the script name.
    sys.exit(rc)
