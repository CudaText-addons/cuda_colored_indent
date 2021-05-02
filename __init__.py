import os
from cudatext import *
from . import opt

from time import time as t

fn_config = os.path.join(app_path(APP_DIR_SETTINGS), 'cuda_colored_indent.ini')
MARKTAG = app_proc(PROC_GET_UNIQUE_TAG, '')

def bool_to_str(v): return '1' if v else '0'
def str_to_bool(s): return s=='1'

_theme = app_proc(PROC_THEME_SYNTAX_DICT_GET, '')

def _theme_item(name):
    if name in _theme:
        return _theme[name]['color_back']
    else:
        return 0x808080

def get_indent(s):
    for i in range(len(s)):
        if s[i] not in (' ', '\t'):
            return s[:i]
    return ''

class Command:

    def __init__(self):

        self.load_settings()
        self.update_colors()

        app_proc(PROC_SET_EVENTS, ';'.join([
            'cuda_colored_indent',
            'on_open,on_change_slow,on_state',
            opt.lexers
            ]))

    def config(self):

        self.save_settings()
        file_open(fn_config)

    def toggle(self):

        opt.active = not opt.active

        self.save_settings()
        self.apply_settings()

        msg_status('Colored Indent: '+('on' if opt.active else 'off'))

    def reload_config(self):

        self.load_settings()
        self.apply_settings()

    def on_start(self, ed_self):

        pass

    def on_open(self, ed_self):

        callback = lambda *args,**vargs: self.work(ed_self)
        timer_proc(TIMER_START_ONE, callback, 1000)
        #self.work(ed_self)

    def on_change_slow(self, ed_self):

        self.work(ed_self)

    def on_state(self, ed_self, state):

        global _theme

        if state==APPSTATE_THEME_SYNTAX:
            _theme = app_proc(PROC_THEME_SYNTAX_DICT_GET, '')
            self.update_colors()
            self.apply_settings()

    def load_settings(self):

        opt.color_error = ini_read(fn_config, 'op', 'color_error', opt.DEF_ERROR)
        opt.color_set = ini_read(fn_config, 'op', 'color_set', opt.DEF_SET)
        opt.lexers = ini_read(fn_config, 'op', 'lexers', opt.DEF_LEXERS)
        opt.max_lines = int(ini_read(fn_config, 'op', 'max_lines', '2000'))
        opt.active = str_to_bool(ini_read(fn_config, 'op', 'active', opt.DEF_ACTIVE))

    def save_settings(self):
        ini_write(fn_config, 'op', 'lexers', opt.lexers)
        ini_write(fn_config, 'op', 'color_error', opt.color_error)
        ini_write(fn_config, 'op', 'color_set', opt.color_set)
        ini_write(fn_config, 'op', 'max_lines', str(opt.max_lines))
        ini_write(fn_config, 'op', 'active', bool_to_str(opt.active))

    def apply_settings(self):
        for h in ed_handles():
            e = Editor(h)
            if opt.active:
                if self.lexer_ok(e):
                    self.work(e)
            else:
                e.attr(MARKERS_DELETE_BY_TAG, tag=MARKTAG)

    def lexer_ok(self, ed):

        lex = ed.get_prop(PROP_LEXER_FILE)
        return lex and (','+lex+',' in ','+opt.lexers+',')

    def get_color(self, n):

        return self.color_set[n%len(self.color_set)]

    def update_colors(self):

        self.color_error = _theme_item(opt.color_error)
        self.color_set = [_theme_item(i) for i in opt.color_set.split(',')]

    def work(self, ed):

        if not opt.active:
            return

        if ed.get_line_count()>opt.max_lines:
            return

        tab_size = ed.get_prop(PROP_TAB_SIZE)
        tab_spaces = ed.get_prop(PROP_TAB_SPACES)

        ed.attr(MARKERS_DELETE_BY_TAG, tag=MARKTAG)

        lines = ed.get_text_all().splitlines()

        atrs = [] # (x,y,len, bg)

        for (index, s) in enumerate(lines):
            indent = get_indent(s)
            if not indent:
                continue

            level = -1
            x = 0

            while indent:
                level += 1
                if indent[0]=='\t':
                    atrs.append((x, index, 1, self.get_color(level)))
                    indent = indent[1:]
                    x += 1
                elif indent[:tab_size]==' '*tab_size:
                    atrs.append((x, index, tab_size, self.get_color(level)))
                    indent = indent[tab_size:]
                    x += tab_size
                else:
                    atrs.append((x, index, len(indent), self.color_error))
                    break
        #end for

        colors = {item[3] for item in atrs}

        for bg in colors:
            col_items = (item for item in atrs  if item[3] == bg)
            xs,ys,lens,_cols = zip(*col_items)

            ed.attr(MARKERS_ADD_MANY,
                x=xs,
                y=ys,
                len=lens,
                tag=MARKTAG,
                color_font=0,

                color_bg=bg,
                )

