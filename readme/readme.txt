plugin for CudaText.
gives highlighting of indentation levels. by default, highlights only 4 indentation 
levels in different background colors, next levels are colored in loop.

detects indentation level from editor setting "tab_size".
if some indentation is incorrect (e.g. 5-7 chars with "tab_size":4), then 
it's highlighted in special color.

plugin has config file, to open it: "Options / Settings-plugins / Colored Indent / Config".
- "lexers": ","-separated lexers, for which plugin is active.
- "color_set": ","-separated list of syntax-theme elements, from which background colors are taken.
- "color_error": syntax-theme element, from which error color is taken.
- "max_lines": maximal count of lines in document, when plugin is active.

plugin works on events: after file opened; after text is changed and short pause is passed.

author: Alexey Torgashin (CudaText)
license: MIT
