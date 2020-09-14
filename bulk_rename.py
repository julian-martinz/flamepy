# :coding: utf-8

''' 
Rename multiple clips using tokens and/or find/replace. Works on Desktop and Library.
Tested on flame version 2020.0+

Copyright (c) 2019 Julian Martinz (martinz.julian@gmail.com)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *
import datetime
import string

__version__ = '0.2'

# GLOBALS
now = datetime.datetime.now()
date = now.strftime("%Y%m%d")
time = now.strftime("%Hh%M")
date_time = now.strftime("%Y%m%d_%Hh%M")


class RenameWindow(QDialog):
    def __init__(self, selected_clips, parent=None):
        super(RenameWindow, self).__init__(parent)

        self.selected_clips = selected_clips
        self.preview_clip = self.selected_clips[0]
        self.setMinimumSize(600, 300)
        self.setWindowTitle('Rename Shots')
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_DeleteOnClose)

        # Labels and Buttons
        self.rename_label = QLabel('Template:')
        self.token_input = QLineEdit('<name>')
        tooltip = '''
        Available tokens:
        <name> : original name
        <date> : current date YYYYMMDD
        <time> : current time formatted 12h00
        <date_time> : date and time 
        <count> : Index of each clip when selecting multiple clips. <count##> will pad with zeroes
        '''
        self.rename_label.setToolTip(tooltip)
        self.token_input.setToolTip(tooltip)
        self.find_label = QLabel('Find String:')
        self.find_input = QLineEdit()

        self.replace_label = QLabel('Replace String:')
        self.replace_input = QLineEdit()
        self.previewLabel = QLabel('Preview:')
        self.preview = QLabel('preview ..')

        self.cancel_btn = QPushButton('Cancel')
        self.rename_btn = QPushButton('Rename')

        # Layout
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.rename_label)
        mainLayout.addWidget(self.token_input)
        mainLayout.addWidget(self.find_label)
        mainLayout.addWidget(self.find_input)
        mainLayout.addWidget(self.replace_label)
        mainLayout.addWidget(self.replace_input)
        mainLayout.addWidget(self.previewLabel)
        mainLayout.addWidget(self.preview)
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.cancel_btn)
        button_layout.addWidget(self.rename_btn)
        mainLayout.addLayout(button_layout)

        # Core
        self.cancel_btn.clicked.connect(self.cancel_button)
        self.rename_btn.clicked.connect(self.rename_button)
        self.token_input.textChanged.connect(self.update_preview)
        self.find_input.textChanged.connect(self.update_preview)
        self.replace_input.textChanged.connect(self.update_preview)
        self.update_preview()
        self.setLayout(mainLayout)

    def update_preview(self):
        preview_name = self.return_new_name(self.preview_clip)
        self.preview.setText(preview_name)
        return

    def cancel_button(self):
        self.close()

    def rename_button(self):
        count = 0
        for clip in self.selected_clips:
            count += 1
            new_name = self.return_new_name(clip, count)
            clip.name = new_name
        self.close()

    def return_new_name(self, clip, count=1):
        '''process clipname and return new name'''
        template = self.token_input.text()
        find_string = self.find_input.text()
        replace_string = self.replace_input.text()

        if '<count' in template:
            index_count = [
                i for i in range(len(template))
                if template.startswith('<count', i)
                ][0]
            tail = template[index_count + 6:]
            hash_count = len(tail.split('>')[0])
            template = string.replace(
                template, '<count' + hash_count * '#' + '>', '<count>')
        else:
            hash_count = 0

        current_name = str(clip.name)[1:-1]
        new_name = string.replace(template, '<name>', current_name)
        new_name = string.replace(
            new_name, '<count>', str(count).zfill(hash_count))
        new_name = string.replace(
            new_name, find_string, replace_string)
        new_name = string.replace(new_name, '<date>', date)
        new_name = string.replace(new_name, '<time>', time)
        new_name = string.replace(new_name, '<date_time>', date_time)
        return str(new_name)


def show_ui(selected_clips):    
    window = RenameWindow(selected_clips)
    window.show()
    return window


def get_media_panel_custom_ui_actions():
    """Return custom actions to execute on Media Panel objects."""
    return [
        {
            "name": "Bulk rename ..",
            "actions": [
                {
                    "name": "bulk rename",
                    "execute": show_ui,
                    "minimumVersion": "2020.0"
                }
            ]
        },
    ]
