## MacroW

MacroW is a simple unix (X11) Keyboard Macro Recorder / player for Keyboard with dedicated macro keys.

### Features:
  - Records on the fly.
  - Play macro on the fly
  - Macros are erased on reboot.

### Keyboard support
 - Razer Blackwidow Chroma
   - Supported macro keys:  M1 / M2 / M3 / M4 / M5

### Tested with
 - UBUNTU 14.04 + https://github.com/pez2001/razer_chroma_drivers ( Enables macro keys + colors profile)

If you have a different keyboard and want to help. Enter in contact  https://github.com/igorbb/MacroW/labels/help%20wanted

---
## Usage:

###Recording:
   - Press F9 to start recording
   - Select the Macro Caller by pressing a macro key.
   - Type the desired keyboard inputs 
     - If ESC is pressed recorded is canceled and selected macro MX is cleared
     - Press any of the macro keys  to confirm.

###Playing:
   - Press a macro key with a recording.
  
---

## Installation:
### Dependencies:
   - python-xlib
   -  libnotify  or python-notify
   -  python-gobject

### Running:
Just run macrow.py or put it on your distribution autostart. :)
