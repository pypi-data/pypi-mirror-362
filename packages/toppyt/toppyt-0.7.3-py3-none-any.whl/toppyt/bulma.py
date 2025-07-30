"""This module provides a set of editors based on the bulma.io css framework"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Generic, Union, Iterable, TypeVar
from html import escape

from .interactions import Editor

def bulma_page(task: str = '', session: str = '',
                url_bulma: str = 'https://cdn.jsdelivr.net/npm/bulma@1.0.2/css/bulma.min.css',
                url_fontawesome: str = 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.1.1/css/all.min.css',
                theme_vars: dict[str,str] | None = None) -> str:
    
    if theme_vars is not None:
        theme_css = ':root {' + ' '.join(f'--bulma-{var}: {value};' for var,value in theme_vars.items())+'}'
        theme_css_element = f'<style type="text/css">{theme_css}</style>'
    else:
        theme_css_element = ''
    return f'''
        <!DOCTYPE html>
        <html>
            <head>
                <meta charset="utf-8">
                <meta name="viewport" content="width=device-width, initial-scale=1">
                <title></title>
                <link rel="stylesheet" href="{url_fontawesome}" />
                <link rel="stylesheet" href="{url_bulma}" />
                {theme_css_element}
                <script src="/static/toppyt.js" defer></script>
            </head>
            <body>
            {session}
            {task}
            </body>
        </html>
        '''

def bulma_modal_dialog(title = '', body = '', footer = '', task_tag = ''):
    return f'''
    <div {task_tag} class="modal is-active">
    <div class="modal-background"></div>
        <div class="modal-card">
            <header class="modal-card-head">
                <p class="modal-card-title">{title}</p>
            </header>
            <section class="modal-card-body">
            {body}
            </section>
            <footer class="modal-card-foot">
            {footer}
            </footer>
        </div>
    </div>
    '''

T = TypeVar('T')

class BulmaInputBase(Editor[T],Generic[T]):
    label: str | None
    placeholder: str | None
    icon: str | None
    help: str | tuple[str,str] | None
    disabled: bool
    sync: bool

    _raw: str

    def __init__(self,
        label: str | None = None,
        placeholder: str | None = None,
        icon: str | None = None,
        help: str | tuple[str,str] | None = None,
        disabled: bool = False,
        sync: bool = False):

        self.label = label
        self.placeholder = placeholder
        self.icon = icon
        self.help = help
        self.disabled = disabled
        self.sync = sync

    def _generate_input(self, name: str, help_class: str, placeholder_attr: str, sync_attr: str, disabled_attr: str) -> str:
        """Generate the specific input tag for the type of input"""
        return ''

    @staticmethod
    def _to_raw(value: T) -> str:
        """Convert a new value to a string representation for editing"""
        return str(value)

    def start(self, value: T | None) -> None:
        self._raw = '' if value is None else self._to_raw(value)

    def generate_ui(self, name: str = 'v', task_tag: str = '') -> str:  
        cssclass = 'control'
        
        label_html = ''
        if self.label is not None:
            label_html = f'<label class="label">{self.label}</label>'
        
        icon_html = ''
        if self.icon is not None:
            cssclass += ' has-icons-left'
            icon_html = f'<span class="icon is-small is-left"><i class="fas fa-{self.icon}"></i></span>'

        help_html = ''
        help_class = ''
        if self.help is not None:
            if isinstance(self.help,tuple):
                help_class = f' is-{self.help[1]}'

            help_text = self.help if isinstance(self.help,str) else self.help[0]
            help_html = f'<p class="help{help_class}">{help_text}</p>'
           
        placeholder_attr = self.placeholder if self.placeholder is not None else ''
        sync_attr = 'true' if self.sync else 'false'
        disabled_attr = 'disabled' if self.disabled else ''
        
        input_html = self._generate_input(name, help_class, placeholder_attr, sync_attr, disabled_attr)
        return f'<div {task_tag} class="field">{label_html}<div class="{cssclass}">{input_html}{icon_html}</div>{help_html}</div>'

    def handle_edit(self, edit: Any) -> bool:
        if isinstance(edit,str):
            self._raw = edit
        return False
        
    def get_value(self) -> T | None:
        return None

class BulmaTextInput(BulmaInputBase[str]):
    def _generate_input(self, name: str, help_class: str, placeholder_attr: str, sync_attr: str, disabled_attr: str) -> str:
        return f'<input class="input{help_class}" type="text" name="{name}" value="{self._raw}" placeholder="{placeholder_attr}" oninput="toppyt_notify(this,{sync_attr})" {disabled_attr}>'

    def get_value(self) -> str | None:
        return self._raw

class BulmaPasswordInput(BulmaInputBase[str]):
    def _generate_input(self, name: str, help_class: str, placeholder_attr: str, sync_attr: str, disabled_attr: str) -> str:
        return f'<input class="input{help_class}" type="password" name="{name}" value="{self._raw}" placeholder="{placeholder_attr}" oninput="toppyt_notify(this,{sync_attr})" {disabled_attr}>'
    def get_value(self) -> str | None:
        return self._raw

class BulmaIntInput(BulmaInputBase[int]):
    def _generate_input(self, name: str, help_class: str, placeholder_attr: str, sync_attr: str, disabled_attr: str) -> str:
        return f'<input class="input{help_class}" type="number" name="{name}" value="{self._raw}" placeholder="{placeholder_attr}" onblur="toppyt_notify(this,{sync_attr})" {disabled_attr}>'

    def get_value(self) -> int | None:
        if self._raw is None:
            return None
        try:
            return int(self._raw)
        except ValueError:
            return None

class BulmaFloatInput(BulmaInputBase[float]):
    def _generate_input(self, name: str, help_class: str, placeholder_attr: str, sync_attr: str, disabled_attr: str) -> str:
        return f'<input class="input{help_class}" type="number" name="{name}" value="{self._raw}" placeholder="{placeholder_attr}" onblur="toppyt_notify(this,{sync_attr})" {disabled_attr}>'

    def get_value(self) -> float | None:
        if self._raw is None:
            return None
        try:
            return float(self._raw)
        except ValueError:
            return None
   
@dataclass
class BulmaFileInput(Editor[dict[str,str]]):
    upload_url: str
    label: str | None
    placeholder: str | None
    text: str | None
    icon: str | None
    help: str | tuple[str,str] | None
    disabled: bool
    sync: bool

    value: dict[str,str] | None = None

    def __init__(self,
        upload_url: str,
        label: str | None = None,
        placeholder: str | None = None,
        text: str | None = None,
        icon: str | None = None,
        help: str | tuple[str,str] | None = None,
        disabled: bool = False,
        sync: bool = True):
        
        self.upload_url = upload_url
        self.label = label
        self.placeholder = placeholder
        self.text = text
        self.icon = icon
        self.help = help
        self.disabled = disabled
        self.sync = sync

    def start(self,value: dict[str,str] | None) -> None:
        self.value = None
        if isinstance(value,dict) and 'name' in value:
            self.value = value
            
    def generate_ui(self, name: str = 'v', task_tag = '') -> str:
        value_html = ''
        if isinstance(self.value,dict) and 'name' in self.value:
            value_html = self.value['name']

        label_html = ''
        if self.label is not None:
            label_html = f'<label class="label">{self.label}</label>'
        icon_html = ''
        if self.icon is not None:
            icon_html = f'<span class="file-icon"><i class="fas fa-{self.icon}"></i></span>'
        
        text_html = ''
        if self.text is not None:
            text_html = f'<span class="file-label">{self.text}</span>'
        
        help_html = ''
        help_class = ''
        if self.help is not None:
            if isinstance(self.help,tuple):
                help_class = f' is-{self.help[1]}'

            help_text = self.help if isinstance(self.help,str) else self.help[0]
            help_html = f'<p class="help{help_class}">{help_text}</p>'

        sync_attr = 'true' if self.sync else 'false'
        disabled_attr = 'disabled' if self.disabled else ''

        return f'<div {task_tag} class="field">{label_html}<div class="file has-name is-fullwidth{help_class}"><label class="file-label"><input class="file-input" type="file" name="{name}" onchange="toppyt_notify_file(this,\'{self.upload_url}\',{sync_attr})" {disabled_attr}><span class="file-cta">{icon_html}{text_html}</span><span class="file-name">{value_html}</span></label></div>{help_html}</div>'

    def handle_edit(self, edit: Any) -> bool:
        if isinstance(edit,dict):
            self.value = edit
        return True

    def get_value(self) -> dict[str,str] | None:
        if isinstance(self.value,dict):
            return self.value
        return None

class BulmaTextArea(BulmaInputBase[str]):
    def _generate_input(self, name: str, help_class: str, placeholder_attr: str, sync_attr: str, disabled_attr: str) -> str:
        return f'<textarea class="textarea {help_class}" name="{name}" placeholder="{placeholder_attr}" onblur="toppyt_notify(this,{sync_attr})" {disabled_attr}>{self._raw}</textarea>'
    def get_value(self) -> str | None:
        return self._raw
        
class BulmaSelect(BulmaInputBase[str]):
    options: list[Union[str,tuple[str,str]]]
    label: str | None
    placeholder: str | None
    text: str | None
    icon: str | None
    help: str | tuple[str,str] | None
    disabled: bool
    sync: bool
    allow_empty: bool
    
    _raw: str

    def __init__(self,
        options: Iterable[Union[str,tuple[str,str]]],
        label: str | None = None,
        placeholder: str | None = None,
        icon: str | None = None,
        help: str | tuple[str,str] | None = None,
        disabled: bool = False,
        sync: bool = False,
        allow_empty: bool = True):
        
        self.options = list(options)
        self.label = label
        self.placeholder = placeholder
        self.icon = icon
        self.help = help
        self.disabled = disabled
        self.sync = sync
        self.allow_empty = allow_empty
    
    def _generate_input(self, name: str, help_class: str, placeholder_attr: str, sync_attr: str, disabled_attr: str) -> str:
        parts = []
        options = [v if isinstance(v,tuple) else (v,v) for v in self.options]
        placeholder = 'Select...' if self.placeholder is None else self.placeholder
        for k, v in ([(placeholder,'')]if self.allow_empty else []) + options:
            selected = 'selected' if v == self._raw else ''
            parts.append(f'<option value="{v}" {selected}>{k}</option>')
        options_html = ''.join(parts)

        return f'<div class="select is-fullwidth{help_class}"><select name="{name}" oninput="toppyt_notify(this,{sync_attr})" {disabled_attr}>{options_html}</select></div>'

    def get_value(self) -> Any:
        if self._raw == '':
            if self.allow_empty or len(self.options) == 0:
                return None
            return self.options[0][1] if isinstance(self.options[0],tuple) else self.options[0]
        return self._raw

class BulmaCheckboxField(BulmaInputBase[bool]):
    label: str | None
    placeholder: str | None
    text: str | None
    icon: str | None
    help: str | tuple[str,str] | None
    disabled: bool
    sync: bool

    _checked: bool = False
    
    def __init__(self,
        label: str | None = None,
        placeholder: str | None = None,
        text: str | None = None,
        icon: str | None = None,
        help: str | tuple[str,str] | None = None,
        disabled: bool = False,
        sync: bool = False):
        
        self.label = label
        self.placeholder = placeholder
        self.text = text
        self.icon = icon
        self.help = help
        self.disabled = disabled
        self.sync = sync

    def start(self, value: Any) -> None:
        self._checked = value if isinstance(value,bool) else False

    def _generate_input(self, name: str, help_class: str, placeholder_attr: str, sync_attr: str, disabled_attr: str) -> str:
        checked_attr = 'checked' if self._checked else ''
        text_attr = '' if self.text is None else escape(self.text)
        return f'<label class="checkbox{help_class}"><input type="checkbox" name="{name}" {checked_attr} oninput="toppyt_notify(this,{sync_attr});" {disabled_attr}> {text_attr}</label>'

    def handle_edit(self, edit: Any) -> bool:
        self._checked = edit
        return True

    def get_value(self) -> bool:
        return self._checked

class BulmaTextView(BulmaInputBase[str]):
    def _generate_input(self, name: str, help_class: str, placeholder_attr: str, sync_attr: str, disabled_attr: str) -> str:
        value_attr = '' if self._raw is None else escape(self._raw)
        return f'<p>{value_attr}</p>'
        
    def get_value(self) -> str | None:
        return self._raw

class BulmaHidden(Editor[Any]):
    value: Any | None

    def __init__(self):
        self.value = None
    def start(self, value: Any) -> None:
        self.value = value
    def generate_ui(self, name: str = 'v', task_tag: str = None) -> str:
        return ''
    def handle_edit(self, edit: Any) -> bool:
        return False
    def get_value(self) -> Any | None:
        return self.value


#The following types can be used as button specifcations
type BulmaButtonSpecLike = BulmaButtonSpec | str | tuple[str,str] | tuple[str,str,str]

@dataclass
class BulmaButtonSpec:
    value: str
    text: str | None = None
    icon: str | None = None
    is_enabled: bool = True
    is_compact: bool = False
    is_enter: bool = False
    is_escape: bool = False
    extra_cls: str | None = None

    def to_html(self, name: str, value: str | None):
         
        css_cls = 'button'
        icon_html = ''
        if not self.icon is None:
            css_cls += ' has-icon'
            icon_html = f'<span class="icon"><i class="fas fa-{self.icon}"></i></span>'
        
        label_html = '' if (self.text is None or self.is_compact) else  f'<span>{self.text}</span>'
        title_attr = '' if self.text is None else f' title="{self.text}"'
        disabled_attr = ' disabled' if not self.is_enabled else ''

        if self.value == value:
            css_cls += ' is-info'
        if self.is_enter:
            css_cls += ' toppyt-enter'
        if self.is_escape:
            css_cls += ' toppyt-escape'
        if self.extra_cls:
            css_cls += f' {self.extra_cls}'
        return f'<button class="{css_cls}" name="{name}" value="{self.value}"{title_attr}{disabled_attr} onclick="toppyt_notify(this,true)">{icon_html}{label_html}</button>'

    @classmethod
    def create(cls, spec: BulmaButtonSpecLike):
        if isinstance(spec,BulmaButtonSpec):
            return BulmaButtonSpec(spec.value,spec.text,spec.icon,spec.is_enabled,spec.is_compact,spec.is_enter,spec.is_escape,spec.extra_cls)
        elif isinstance(spec,str):
            return cls(value=spec, text=spec)
        elif isinstance(spec,tuple) and len(spec) == 2:
            return cls(value=spec[0], text=spec[1])
        elif isinstance(spec,tuple) and len(spec) == 3:
            return cls(value=spec[0], text=spec[1], icon=spec[2])
        else:
            raise ValueError(f'Incorrect button specification {spec}')

class BulmaButton(Editor[str]):
   
    spec: BulmaButtonSpec
    value: str | None

    def __init__(self, value: str,
                 text: str| None = None,
                 icon: str | None = None,
                 is_enabled: bool = True,
                 is_compact: bool = False,
                 is_enter: bool = False,
                 is_escape: bool = False,
                 extra_cls: str | None = None
                 ):
        
        self.spec = BulmaButtonSpec(value,text,icon,is_enabled,is_compact,is_enter,is_escape,extra_cls)
        self.value = None
    
    def start(self, value: str | None) -> None:
        self.value = value

    def generate_ui(self, name: str = 'v', task_tag = '') -> str:
        return f'<span {task_tag}>{self.spec.to_html(name,self.value)}</span>'
     
    def handle_edit(self, edit: Any) -> bool:
        if isinstance(edit,str):
            self.value = edit
        return False

    def get_value(self) -> str | None:
        return self.value

class BulmaButtons(Editor[str]):

    specs: list[BulmaButtonSpec]
    align: str
    has_addons: bool
    value: str | None

    def __init__(self, options: list[BulmaButtonSpecLike], align: str = 'left', has_addons: bool = False):
        
        specs = [BulmaButtonSpec.create(option) for option in options]
    
        self.specs = specs
        self.align = align
        self.has_addons = has_addons
        self.value = None

    def start(self, value: str | None) -> None:
        self.value = value

    def generate_ui(self, name: str  ='v', task_tag: str = '') -> str:
        options = ''.join([spec.to_html(name,self.value) for spec in self.specs])
        align_cls = ' is-right' if self.align == 'right' else (' is-center' if self.align == 'center' else '')
        addons_cls = ' has-addons' if self.has_addons else ''
        return f'<div {task_tag} class="buttons{align_cls}{addons_cls}">{options}</div>'

    def handle_edit(self, edit: Any) -> bool:
        if isinstance(edit,str):
            self.value = edit
        return True

    def get_value(self) -> str | None:
        return self.value


@dataclass
class BulmaTableRowSpec:
    value: str
    columns: list[str]
    buttons: list[BulmaButtonSpecLike]
    selected: bool

    @classmethod
    def create(cls, spec: BulmaTableRowSpecLike):
        if isinstance(spec,BulmaTableRowSpec):
            return BulmaTableRowSpec(spec.value,spec.columns,spec.buttons,spec.selected)
        elif isinstance(spec,tuple) and len(spec) == 2:
            return cls(value=str(spec[0]), columns = [str(col) for col in spec[1]], buttons = [], selected = False)
        elif isinstance(spec,tuple) and len(spec) == 3:
            return cls(value=str(spec[0]), columns = [str(col) for col in spec[1]], buttons = spec[2], selected = False)
        elif isinstance(spec,tuple) and len(spec) == 4:
            return cls(value=str(spec[0]), columns = [str(col) for col in spec[1]], buttons = spec[2], selected = spec[3])
        else:
            return cls(str(spec),[str(spec)],[],False)
        
type BulmaTableRowSpecLike = BulmaTableRowSpec | Any | tuple[Any,list[str]] | tuple[Any,list[str],list[BulmaButtonSpecLike]] | tuple[Any,list[str],list[BulmaButtonSpecLike],bool]
type BulmaTableResult = tuple[str] | tuple[str,str]

class BulmaTable(Editor[BulmaTableResult]):

    def __init__(self, rows: list[BulmaTableRowSpecLike], headers: list[str] | None = None, with_select: bool = True, with_buttons: bool = True):
        self.rows = [BulmaTableRowSpec.create(row) for row in rows]
        self.headers = headers
        self.with_select = with_select
        self.with_buttons = with_buttons

    def start(self, value) -> None:
        self.value = None

    def generate_ui(self, name='v', task_tag: str = ''):
        headers_html = []
        if self.with_select:
            any_selected = any(row.selected for row in self.rows)
            select_html = f'<th style="width: 1em"><input type="checkbox" {'checked' if any_selected else ''} onclick="toppyt_notify(this,true,\'{name}\',\'{'deselect_all' if any_selected else 'select_all'}\');return false;"></th>'
            headers_html.append(select_html)
        if self.headers:
            for header in self.headers:
                headers_html.append(f'<th>{escape(header)}</th>')
        if self.with_buttons:
            headers_html.append('<th>&nbsp;</th>')

        rows_html =[self.row_html(name, row) for row in self.rows]

        return f'<div {task_tag} class="field"><table class="table is-fullwidth is-striped"><thead>{"".join(headers_html)}</thead><tbody>{"".join(rows_html)}<tbody></table></div>'
    
    def row_html(self, name, row: BulmaTableRowSpec):
       
        columns_html = []
        if self.with_select:
            select_html = f'<td><input type="checkbox" {'checked' if row.selected else ''} onclick="toppyt_notify(this,true,\'{name}\',\'{'deselect' if row.selected else 'select'}:{row.value}\');return false;"></td>'
            columns_html.append(select_html)

        for column in row.columns:
            columns_html.append(self.column_html(name, column, row.value, row.selected))

        if self.with_buttons:
            buttons_html = [self.button_html(name, row.value, button_spec) for button_spec in row.buttons]
            columns_html.append(f'<td><div class="buttons is-right">{"".join(buttons_html)}</div></td>')
    
        return f'<tr {'class="is-selected"' if row.selected else ''}>{"".join(columns_html)}</tr>'

    def column_html(self, name, column, value,selected):
        if self.with_select:
            return f'<td onclick="toppyt_notify(this,true,\'{name}\',\'{'deselect' if selected else 'select'}:{value}\');return false;">{escape(column)}</td>'
        else:
            return f'<td>{escape(column)}</td>'

    def button_html(self,name,subject,spec_like):
        spec = BulmaButtonSpec.create(spec_like)
        spec.value = f'{spec.value}:{subject}'
        return spec.to_html(name,None)
        
    def get_value(self):
        return tuple(self.value.split(":")) if self.value is not None else None

    def handle_edit(self,edit):
        if isinstance(edit,str):
            self.value = edit
        return True

class BulmaPagination(Editor[int]):

    def __init__(self, num_pages: int, prev_html: str = '&laquo;', next_html: str = '&raquo;'):
        self.num_pages = num_pages
        self.cur_page = 1
        self.prev_html = prev_html
        self.next_html = next_html
        
        super().__init__()

    def start(self, value):
        self.cur_page = 1 if value is None else value

    def handle_edit(self, edit):
        if isinstance(edit, str) and edit.isdigit():
            page = int(edit)
            if page > 0 and page <= self.num_pages:
                self.cur_page = page
                return True
        return False
    
    def get_value(self):
        return self.cur_page

    def generate_ui(self, name: str = 'v', task_tag: str = ''):
        prev_button = f'<a href="#" onclick="toppyt_notify(this,true,\'{name}\',\'{self.cur_page - 1}\');return false;" class="pagination-previous{' is-disabled' if self.cur_page == 1 else ''}">{self.prev_html}</a>'
        next_button = f'<a href="#" onclick="toppyt_notify(this,true,\'{name}\',\'{self.cur_page + 1}\');return false;" class="pagination-next{' is-disabled' if self.cur_page == self.num_pages else ''}">{self.next_html}</a>'
        
        links = []
          
        if self.num_pages <= 7:
            page_nums = list(range(1,self.num_pages + 1))
        else:
            first_page = max(1,min(self.num_pages - 6, self.cur_page - 3))
            page_nums = list(range(first_page,first_page+7))
            page_nums[0] = 1
            if page_nums[1] != 2:
                page_nums[1] = None
            page_nums[-1] = self.num_pages
            if page_nums[-2] != self.num_pages -1:
                page_nums[-2] = None

        for num in page_nums:
            if num is None:
                links.append('<li><span class="pagination-ellipsis">&hellip;</span></li>')
            elif num == self.cur_page:
                links.append(f'<li><a class="pagination-link is-current">{self.cur_page}</a></li>')
            else:
                links.append(f'<li><a href="#" onclick="toppyt_notify(this,true,\'{name}\',\'{num}\');return false;"class="pagination-link">{num}</a></li>')

        return f'''
        <nav {task_tag} class="pagination is-centered" role="navigation" aria-label="pagination">
        {prev_button}{next_button}
        <ul class="pagination-list">
        {''.join(links)}
        </ul>
        </nav>'''

class BulmaTupleEditor(Editor[list[Any]]):
    parts: list[Editor[Any]]
    label: str | None

    def __init__(self, parts: list[Editor[Any]] | None, label: str | None = None):
        self.parts = parts if parts is not None else list()
        self.label = label

    def start(self, value: list[Any] | None) -> None:
        for n, part in enumerate(self.parts):
            part_value = value[n] if value is not None and n < len(value) else None
            part.start(part_value)

    def generate_ui(self, name: str = 'v', task_tag: str = '') -> str:
        parts_html = list()

        for n, part in enumerate(self.parts):
            parts_html.append(part.generate_ui(f'{name}-field{n}',''))

        if self.label is None:
            return f'<div {task_tag}>{"".join(parts_html)}</div>'

        return f'''
            <div {task_tag} class="message mt-2">
            <div class="message-header">{self.label}</div>
            <div class="message-body">{"".join(parts_html)}</div>
            </div>
            '''

    def handle_edit(self, edit: Any) -> bool:
        updated = False
        for n, part in enumerate(self.parts):
            part_name = f'field{n}'
            if part_name in edit:
                part_updated = part.handle_edit(edit[part_name])
                updated = updated or part_updated
        return updated

    def get_value(self) -> list[Any]:
        return tuple(part.get_value() for part in self.parts)

class BulmaRecordEditor(Editor[dict[str,Any]]):
    parts: list[tuple[str,Editor[Any]]]
    label: str | None

    def __init__(self, parts: list[tuple[str,Editor[Any]]] | None, label: str | None = None):
        self.parts = parts if parts is not None else list()
        self.label = label

    def start(self, value: dict[str,Any] | None) -> None:
        for (part_name,part) in self.parts:
            part_value = value[part_name] if value is not None and part_name in value else None
            part.start(part_value)

    def generate_ui(self, name: str = 'v', task_tag: str = '') -> str:
        parts_html = list()

        for (part_name,part) in self.parts:
            parts_html.append(part.generate_ui(f'{name}-{part_name}',''))

        if self.label is None:
            return f'<div {task_tag}>{"".join(parts_html)}</div>'

        return f'''
            <div {task_tag} class="message mt-2">
            <div class="message-header">{self.label}</div>
            <div class="message-body">{"".join(parts_html)}</div>
            </div>
            '''

    def handle_edit(self, edit: Any) -> bool:
        update = False
        for part_name, part in self.parts:
            if part_name in edit:
                part_update = part.handle_edit(edit[part_name])
                update = update or part_update
        return update
   
    def get_value(self) -> dict[str,Any]:
        value = dict()
        for (part_name, part) in self.parts:
            value[part_name] = part.get_value()
        return value