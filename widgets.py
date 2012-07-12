##############################################################################
# Copyright (c) 2012 Piotr Skamruk.
# All Rights Reserved.
#
# This software is subject to the provisions of the BSD-like license at
# https://github.com/jellonek/urwidext/blob/master/LICENSE. A copy of the
# license should accompany this distribution. THIS SOFTWARE IS PROVIDED
# "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED WARRANTIES ARE DISCLAIMED,
# INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF TITLE,
# MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS FOR A PARTICULAR PURPOSE

from urwid.widget import Edit, LEFT, SPACE


class ExtendedEdit(Edit):
    def __init__(self, prompt=u'', edit_text=u'',
                 align=LEFT, wrap=SPACE, allow_tab=False,
                 edit_pos=None):
        if not isinstance(prompt, unicode):
            prompt = unicode(prompt)
        self.__super.__init__(prompt, edit_text, False, align, wrap,
                              allow_tab, edit_pos, None, None)

    def keypress(self, size, key):
        if key == 'ctrl w':
            p = self.edit_pos
            while self.edit_pos and self.edit_text[self.edit_pos - 1] == ' ':
                self.edit_pos -= 1
            try:
                self.edit_pos = self.edit_text[:self.edit_pos].rindex(' ') + 1
                self.set_edit_text(
                    self.edit_text[:self.edit_pos] + self.edit_text[p:])
            except ValueError:
                self.set_edit_text(self.edit_text[p:])
                self.set_edit_pos(0)

        elif key == 'ctrl left':
            while self.edit_pos and self.edit_text[self.edit_pos - 1] == ' ':
                self.edit_pos -= 1
            try:
                self.edit_pos = self.edit_text[:self.edit_pos].rindex(' ') + 1
            except ValueError:
                self.set_edit_pos(0)

        elif key == 'ctrl right':
            try:
                while self.edit_pos < len(self.edit_text) and \
                      self.edit_text[self.edit_pos] == ' ':
                    self.edit_pos += 1
                self.edit_pos = self.edit_text.index(' ', self.edit_pos)
                while self.edit_pos < len(self.edit_text) and \
                      self.edit_text[self.edit_pos] == ' ':
                    self.edit_pos += 1
                self._invalidate()
            except ValueError:
                self.set_edit_pos(self.edit_text)

        elif key == 'ctrl k':
            self.set_edit_text(u'')

        else:
            return self.__super.keypress(size, key)
        return True


class CompletingEdit(ExtendedEdit):
    def __init__(self, prompt=u'', edit_text=u'',
                 align=LEFT, wrap=SPACE, allow_tab=False,
                 edit_pos=None, completing_dict=None):
        if not isinstance(completing_dict, dict):
            # it has to be dictionary with specified values
            raise ValueError()

        self.completing_dict = completing_dict
        self.in_multiple_completion = False

        self.__super.__init__(prompt, edit_text, align, wrap,
                              allow_tab, edit_pos)

    def keypress(self, size, key):
        if key == 'tab':
            if self.edit_text[:self.edit_pos].find(' ') == -1:
                command = self._complete_command()
                if command:
                    t = [command]
                    if not len(self.edit_text) + 1 > self.edit_pos:
                        t.append(' ')
                    t.append(self.edit_text[self.edit_pos:])
                    self.set_edit_text(''.join(t))
                    self.set_edit_pos(len(command))
            else:
                return self._complete_arguments()
            return
        else:
            self.in_multiple_completion = False
            return self.__super.keypress(size, key)
        return True

    def _complete_command(self):
        command = self.edit_text[:self.edit_pos]
        matches = []
        for el in self.completing_dict.keys():
            if el.startswith(command):
                matches.append(el)

        if not matches:
            return
        if len(matches) == 1:
            return matches[0]
        else:
            newstart = command
            while True:
                try:
                    newstart += matches[0][len(command)]
                except IndexError:
                    return command

                for el in matches:
                    if not el.startswith(newstart):
                        self.in_multiple_completion = True
                        return command

                command = newstart


    def _complete_arguments(self):
        # TODO: check which parameter is to be completed and call
        # completing function for command at the begining of edit_text
        # with command, param_nr, text to complete, position in this text
        return True
