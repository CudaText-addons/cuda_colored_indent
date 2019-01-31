import os
from cudatext import *

fn_config = os.path.join(app_path(APP_DIR_SETTINGS), 'cuda_colored_indent.ini')
MARKTAG = 103 #uniq value for all ed.attr() plugins

def bool_to_str(v): return '1' if v else '0'
def str_to_bool(s): return s=='1'

_theme = app_proc(PROC_THEME_SYNTAX_DATA_GET, '')

def _theme_item(name):
    for i in _theme:
        if i['name']==name:
            return i['color_back']
    return 0x808080

COLOR_SET = 'SectionBG1,SectionBG2,SectionBG3,SectionBG4'
COLOR_ERROR = 'IncludeBG1'
            
def get_indent(s):
    for i in range(len(s)):
        if s[i] not in (' ', '\t'):
            return s[:i]
    return ''
            
class Command:
    
    def __init__(self):

        self.color_error = _theme_item(COLOR_ERROR)            
        self.color_set = [_theme_item(s) for s in COLOR_SET.split(',')]

    def get_color(self, n):
        return self.color_set[n%len(self.color_set)]

    def config(self):

        pass
        
    def on_change_slow(self, ed_self):
        
        self.work(ed_self)
        
    def on_open(self, ed_self):
    
        self.work(ed_self)
        
    def work(self, ed):
   
        tab_size = ed.get_prop(PROP_TAB_SIZE)
        tab_spaces = ed.get_prop(PROP_TAB_SPACES)
    
        ed.attr(MARKERS_DELETE_BY_TAG, tag=MARKTAG)
    
        lines = ed.get_text_all().splitlines()
        for (index, s) in enumerate(lines):
            indent = get_indent(s)
            if not indent:
                continue
            
            level = -1
            x = 0
            
            while indent:
                level += 1
                if indent[0]=='\t':
                    ed.attr(MARKERS_ADD, 
                        x=x, 
                        y=index, 
                        len=1, 
                        tag=MARKTAG, 
                        color_font=0,
                        color_bg=self.get_color(level),
                        )
                    indent = indent[1:]
                    x += 1
                elif indent[:tab_size]==' '*tab_size:
                    ed.attr(MARKERS_ADD, 
                        x=x, 
                        y=index, 
                        len=tab_size, 
                        tag=MARKTAG, 
                        color_font=0,
                        color_bg=self.get_color(level),
                        )
                    indent = indent[tab_size:]
                    x += tab_size
                else:
                    ed.attr(MARKERS_ADD, 
                        x=x, 
                        y=index, 
                        len=len(indent), 
                        tag=MARKTAG, 
                        color_font=0,
                        color_bg=self.color_error,
                        )
                    break
