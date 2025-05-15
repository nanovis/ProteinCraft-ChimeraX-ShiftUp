from chimerax.core.commands import CmdDesc, register, NoArg
from chimerax.cmd_line.tool import _HistoryDialog

def hello(session):
    """Print hello world message"""
    session.logger.info("Hello from ShiftUp plugin!")

hello_desc = CmdDesc(
    synopsis='Print hello world message'
) 

def shiftUp(self, shifted):
    """Monkey patch for _HistoryDialog.up to implement shift-up functionality"""
    sels = self.listbox.selectedIndexes()
    if len(sels) != 1:
        self._search_cache = (False, None)
        return
    sel = sels[0].row()
    orig_text = self.controller.text.currentText()
    match_against = None
    if shifted:
        was_searching, prev_search = self._search_cache
        if was_searching:
            match_against = prev_search
        else:
            text = orig_text.strip()
            if text:
                match_against = text
                self._search_cache = (True, match_against)
            else:
                self._search_cache = (False, None)
    else:
        self._search_cache = (False, None)
    if match_against:
        while sel > 0:
            if self.listbox.item(sel - 1).text().startswith(match_against):
                break
            sel -= 1
    if sel == 0:
        return
    self.listbox.clearSelection()
    self.listbox.setCurrentRow(sel - 1)
    new_text = self.listbox.item(sel - 1).text()
    self.controller.cmd_replace(new_text)
    if orig_text == new_text:
        self.up(shifted)

def shiftDown(self, shifted):
    sels = self.listbox.selectedIndexes()
    if len(sels) != 1:
        self._search_cache = (False, None)
        return
    sel = sels[0].row()
    orig_text = self.controller.text.currentText()
    match_against = None
    if shifted:
        was_searching, prev_search = self._search_cache
        if was_searching:
            match_against = prev_search
        else:
            text = orig_text.strip()
            if text:
                match_against = text
                self._search_cache = (True, match_against)
            else:
                self._search_cache = (False, None)
    else:
        self._search_cache = (False, None)
    if match_against:
        last = self.listbox.count() - 1
        while sel < last:
            if self.listbox.item(sel + 1).text().startswith(match_against):
                break
            sel += 1
    if sel == self.listbox.count() - 1:
        return
    self.listbox.clearSelection()
    self.listbox.setCurrentRow(sel + 1)
    new_text = self.listbox.item(sel + 1).text()
    self.controller.cmd_replace(new_text)
    if orig_text == new_text:
        self.down(shifted)