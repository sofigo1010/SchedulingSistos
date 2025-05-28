import customtkinter as ctk

NAVY_BLUE     = "#001f3f"
ROYAL_BLUE    = "#4169e1"
LIGHTER_BLUE  = "#3a7bd5"
WHITE_TEXT    = "#FFFFFF"


_original_frame_configure        = ctk.CTkFrame.configure
_original_button_configure       = ctk.CTkButton.configure
_original_optionmenu_configure   = ctk.CTkOptionMenu.configure
_original_label_configure        = ctk.CTkLabel.configure
_original_entry_configure        = ctk.CTkEntry.configure
_original_checkbox_configure     = ctk.CTkCheckBox.configure


def apply_theme():

    ctk.set_appearance_mode("dark")

    ctk.set_default_color_theme("dark-blue")  

    def _frame_patch(self, **kw):
        kw.setdefault('fg_color', NAVY_BLUE)
        return _original_frame_configure(self, **kw)
    ctk.CTkFrame.configure = _frame_patch

    def _button_patch(self, **kw):
        kw.setdefault('fg_color', ROYAL_BLUE)
        kw.setdefault('hover_color', LIGHTER_BLUE)
        kw.setdefault('text_color', WHITE_TEXT)
        return _original_button_configure(self, **kw)
    ctk.CTkButton.configure = _button_patch

    def _optionmenu_patch(self, **kw):
        kw.setdefault('fg_color', ROYAL_BLUE)
        kw.setdefault('button_color', LIGHTER_BLUE)
        kw.setdefault('text_color', WHITE_TEXT)
        return _original_optionmenu_configure(self, **kw)
    ctk.CTkOptionMenu.configure = _optionmenu_patch

    def _label_patch(self, **kw):
        kw.setdefault('text_color', WHITE_TEXT)
        return _original_label_configure(self, **kw)
    ctk.CTkLabel.configure = _label_patch

    def _entry_patch(self, **kw):
        kw.setdefault('fg_color', NAVY_BLUE)
        kw.setdefault('text_color', WHITE_TEXT)
        return _original_entry_configure(self, **kw)
    ctk.CTkEntry.configure = _entry_patch

    def _checkbox_patch(self, **kw):
        kw.setdefault('fg_color', ROYAL_BLUE)
        kw.setdefault('text_color', WHITE_TEXT)
        return _original_checkbox_configure(self, **kw)
    ctk.CTkCheckBox.configure = _checkbox_patch
