"""Button class for Tkinter applications."""
import tkinter as tk
from tkinter import ttk
from pathlib import Path
from PIL import Image, ImageTk

from .constants import PAD, Pad
from .widgets import enter_widget, clickable_widget, HAND

import psiutils.text as text


class IconButton(ttk.Frame):
    def __init__(
            self,
            master,
            text,
            icon,
            command=None,
            sticky: str = '',
            dimmable: bool = False,
            icon_path: str = '',
            **kwargs):
        super().__init__(master, borderwidth=1, relief="raised", **kwargs)
        self.command = command
        self._state = 'normal'

        # Icon and text
        if not icon_path:
            icon_path = f'{Path(__file__).parent}/icons/'
        image = Image.open(f'{icon_path}{icon}.png').resize((16, 16))
        photo_image = ImageTk.PhotoImage(image)

        self.button_label = ttk.Label(
            self, text=text, image=photo_image, compound=tk.LEFT)
        self.button_label.image = photo_image  # Prevent garbage collection
        self.button_label.pack(padx=(3, 5), pady=5)
        self.widget = self.button_label

        # Make the whole frame clickable
        self.bind_widgets()

        self.sticky = sticky
        self.dimmable = dimmable

    def state(self) -> dict:
        return self._state

    def enable(self, enable: bool = True) -> None:
        state = tk.NORMAL if enable else tk.DISABLED
        self.button_label.configure(state=state)
        self._state = state

    def disable(self, disable: bool = True) -> None:
        state = tk.DISABLED if disable else tk.NORMAL
        self.button_label.configure(state=state)
        self._state = state

    def bind_widgets(self):
        for widget in (self, self.button_label):
            widget.bind("<Button-1>", self._on_click)
            widget.bind("<Enter>", self._enter_button)
            widget.bind("<Leave>", lambda e: self.config(relief="raised"))

    def _enter_button(self, event) -> None:
        if self._state == tk.DISABLED:
            return
        self.config(relief="sunken")
        event.widget.winfo_toplevel().config(cursor=HAND)

    def _on_click(self, *args):
        if self.command:
            self.command()


class Button(ttk.Button):
    def __init__(
            self,
            *args,
            sticky: str = '',
            dimmable: bool = False,
            **kwargs: dict,
            ) -> None:
        super().__init__(*args, **kwargs)

        self.sticky = sticky
        self.dimmable = dimmable

    def enable(self, enable: bool = True) -> None:
        state = tk.NORMAL if enable else tk.DISABLED
        self['state'] = state

    def disable(self, disable: bool = True) -> None:
        state = tk.DISABLED if disable else tk.NORMAL
        self['state'] = state


class ButtonFrame(ttk.Frame):
    def __init__(
            self,
            master: tk.Frame,
            orientation: str = tk.HORIZONTAL,
            **kwargs: dict) -> None:
        super().__init__(master, **kwargs)
        self._buttons = []
        self._enabled = False
        self.orientation = orientation

        if 'enabled' in kwargs:
            self._enabled = kwargs['enabled']

        self.icon_buttons = {
            'build': IconButton(self, text.BUILD, 'build'),
            'close': IconButton(self, text.CLOSE, 'cancel'),
            'compare': IconButton(self, text.COMPARE, 'compare'),
            'copy_docs': IconButton(self, text.COPY, 'copy_docs'),
            'copy_clipboard': IconButton(self, text.COPY, 'copy_clipboard'),
            'delete': IconButton(self, text.DELETE, 'delete'),
            'diff': IconButton(self, text.DIFF, 'diff'),
            'done': IconButton(self, text.DONE, 'done'),
            'edit': IconButton(self, text.EDIT, 'edit'),
            'exit': IconButton(self, text.EXIT, 'cancel'),
            'new': IconButton(self, text.NEW, 'new'),
            'next': IconButton(self, text.NEXT, 'next'),
            'open': IconButton(self, text.OPEN, 'open'),
            'previous': IconButton(self, text.PREVIOUS, 'previous'),
            'refresh': IconButton(self, text.REFRESH, 'refresh'),
            'report': IconButton(self, text.REPORT, 'report'),
            'save': IconButton(self, text.SAVE, 'save'),
            'send': IconButton(self, text.SEND, 'send'),
            'use': IconButton(self, text.USE, 'done'),
        }

    def icon_button(
            self, id: str, dimmable: bool = False, command=None) -> IconButton:
        button = self.icon_buttons[id]
        button.dimmable = dimmable
        button.command = command
        return button

    @property
    def buttons(self) -> list[Button]:
        return self._buttons

    @buttons.setter
    def buttons(self, value: list[Button]) -> None:
        self._buttons = value

        if self.orientation == tk.VERTICAL:
            self._vertical_buttons()
        elif self.orientation == tk.HORIZONTAL:
            self._horizontal_buttons()

    @property
    def enabled(self) -> bool:
        return self._enabled

    @enabled.setter
    def enabled(self, value: bool) -> None:
        self._enabled = value
        state = tk.NORMAL if value else tk.DISABLED
        for button in self. buttons:
            button.widget['state'] = state

    def enable(self, enable: bool = True) -> None:
        self._enabled = enable
        self._enable_buttons(self.buttons, enable)

    def disable(self) -> None:
        self._enabled = False
        self._enable_buttons(self.buttons, False)

    def _vertical_buttons(self) -> None:
        self.rowconfigure(len(self.buttons)-1, weight=1)
        for row, button in enumerate(self.buttons):
            pady = PAD
            if row == 0:
                pady = Pad.S
            if row == len(self.buttons) - 1:
                self.rowconfigure(row, weight=1)
                row += 1
                pady = Pad.N

            button.grid(row=row, column=0, sticky=tk.EW, pady=pady)
            clickable_widget(button)

    def _horizontal_buttons(self) -> None:
        self.columnconfigure(len(self.buttons)-1, weight=1)
        for col, button in enumerate(self.buttons):
            padx = PAD
            if col == 0:
                padx = Pad.W
            if col == len(self.buttons) - 1:
                self.columnconfigure(col, weight=1)
                col += 1
            # if not button.sticky:
            #     button.sticky = tk.W
            button.grid(row=0, column=col, sticky=button.sticky, padx=padx)
            clickable_widget(button)

    @staticmethod
    def _enable_buttons(buttons: list[Button], enable: bool = True):
        state = tk.NORMAL if enable else tk.DISABLED
        for button in buttons:
            if button.dimmable:
                if isinstance(button, Button):
                    button['state'] = state
                    button.bind('<Enter>', enter_widget)
                elif isinstance(button, IconButton):
                    if enable:
                        button.enable()
                    else:
                        button.disable()



def enable_buttons(buttons: list[Button], enable: bool = True):
    state = tk.NORMAL if enable else tk.DISABLED
    for button in buttons:
        if button.dimmable:
            button['state'] = state
            button.bind('<Enter>', enter_widget)
