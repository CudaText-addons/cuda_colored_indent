import os
from cudatext import *

fn_config = os.path.join(app_path(APP_DIR_SETTINGS), 'cuda_colored_indent.ini')
MARKTAG = 103 #uniq value for all ed.attr() plugins

option_colors = (0xa000, 0xa0a0, 0xa04000, 0xa000a0)
option_color_error = 0xa0a0ff

def bool_to_str(v): return '1' if v else '0'
def str_to_bool(s): return s=='1'

def get_indent(s):
    for i in range(len(s)):
        if s[i] not in (' ', '\t'):
            return s[:i]
    return ''
            
def get_color(n):
    return option_colors[n%len(option_colors)]

class Command:
    
    def __init__(self):

        pass
        #global option_int
        #global option_bool
        #option_int = int(ini_read(fn_config, 'op', 'option_int', str(option_int)))
        #option_bool = str_to_bool(ini_read(fn_config, 'op', 'option_bool', bool_to_str(option_bool)))

    def config(self):

        pass
        #ini_write(fn_config, 'op', 'option_int', str(option_int))
        #ini_write(fn_config, 'op', 'option_bool', bool_to_str(option_bool))
        #file_open(fn_config)
        
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
            indent_str = get_indent(s)
            if not indent_str:
                continue
            
            level = -1
            x = 0
            
            while indent_str:
                level += 1
                if indent_str[0]=='\t':
                    ed.attr(MARKERS_ADD, 
                        x=x, 
                        y=index, 
                        len=1, 
                        tag=MARKTAG, 
                        color_font=0,
                        color_bg=get_color(level),
                        )
                    indent_str = indent_str[1:]
                    x += 1
                elif indent_str[:tab_size]==' '*tab_size:
                    ed.attr(MARKERS_ADD, 
                        x=x, 
                        y=index, 
                        len=tab_size, 
                        tag=MARKTAG, 
                        color_font=0,
                        color_bg=get_color(level),
                        )
                    indent_str = indent_str[tab_size:]
                    x += tab_size
                else:
                    ed.attr(MARKERS_ADD, 
                        x=x, 
                        y=index, 
                        len=len(indent_str), 
                        tag=MARKTAG, 
                        color_font=0,
                        color_bg=option_color_error,
                        )
                    break
