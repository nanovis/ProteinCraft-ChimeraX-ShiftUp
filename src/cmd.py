from chimerax.core.commands import CmdDesc, register, NoArg, BoolArg
from chimerax.cmd_line.tool import _HistoryDialog

# Store original functions
_original_up = _HistoryDialog.up
_original_down = _HistoryDialog.down

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

def enable(session, enabled):
    """Enable or disable shift-up functionality"""
    if enabled:
        _HistoryDialog.up = shiftUp
        _HistoryDialog.down = shiftDown
        session.logger.info("ShiftUp functionality enabled")
    else:
        _HistoryDialog.up = _original_up
        _HistoryDialog.down = _original_down
        session.logger.info("ShiftUp functionality disabled")

enable_desc = CmdDesc(
    required=[('enabled', BoolArg)],
    synopsis='Enable or disable shift-up functionality'
)