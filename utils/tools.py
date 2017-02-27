import logging
import numpy as np


# Math Tools
# -----------------------------------

def lcr_series_equ(f, z, phi):
    r_s = z * np.cos(phi)
    x_s = z * np.sin(phi)
    c_s = -1 / (2 * np.pi * f * x_s)
    l_s = x_s / (2 * np.pi * f)
    D = r_s/x_s
    
    return r_s, c_s, l_s, D


def lcr_parallel_equ(f, z, phi):
    y = 1/z
    g_p = y * np.cos(phi)
    b_p = y * np.sin(phi)
    r_p = 1/g_p
    c_p = -b_p / (2 * np.pi * f)
    l_p = 1 / (2 * np.pi * f * b_p)  * (-1)
    D = g_p/b_p 

    return r_p, c_p, l_p, D


def lcr_open_cor(c_x, c_open):
	"""
	Returns the open corrected DUT impedance z_dut.

	Z_x 	... measured DUT impedance
	z_open 	... measured open impedance
	z_s
	"""

	return c_x - c_open


def lcr_open_short_cor(z_x, z_open, z_short):
	"""
	Returns the open and short corrected DUT impedance z_dut.

	Z_x 	... measured DUT impedance
	z_open 	... measured open impedance
	z_short ... measured short impedance
	"""

	return (z_x-z_short) / (1 - (z_x-z_short) * (1/z_open))


def lcr_open_short_load_cor(z_x, z_open, z_short, z_load, z_std):
	"""
	Returns the open, short and load corrected DUT impedance z_dut.

	Z_x 	... measured DUT impedance
	z_open 	... measured open impedance
	z_short ... measured short impedance
	z_load 	... measured impedance of the load device 
	z_std   ... true value of the load device
	"""

	return z_std * ((z_short-z_x) * (z_load-z_open)) / ((z_x-z_open) * (z_short-z_load))


def extract_depletion_voltage(v, c):
	x = v
	y = 1/c**2

	vdep = 1
	return v_dep


def lcr_error_cp(f, z, z_err, phi, phi_err):
    y = 1/z
    b_p = y * np.sin(phi)
    c_p = -b_p / (2 * np.pi * f)

    y_err = z_err / z**2
    bp_err = np.sqrt((y_err * np.sin(phi))**2 + (phi_err * y * np.cos(phi))**2)
    cp_err = bp_err / (2 * np.pi * f)

    return cp_err




# Misc Tools
# -----------------------------------

def add_coloring_to_emit_windows(fn):
    def _out_handle(self):
        import ctypes
        return ctypes.windll.kernel32.GetStdHandle(self.STD_OUTPUT_HANDLE)
    out_handle = property(_out_handle)

    def _set_color(self, code):
        import ctypes
        # Constants from the Windows API
        self.STD_OUTPUT_HANDLE = -11
        hdl = ctypes.windll.kernel32.GetStdHandle(self.STD_OUTPUT_HANDLE)
        ctypes.windll.kernel32.SetConsoleTextAttribute(hdl, code)

    setattr(logging.StreamHandler, '_set_color', _set_color)

    def new(*args):
        FOREGROUND_BLUE      = 0x0001 # text color contains blue.
        FOREGROUND_GREEN     = 0x0002 # text color contains green.
        FOREGROUND_RED       = 0x0004 # text color contains red.
        FOREGROUND_INTENSITY = 0x0008 # text color is intensified.
        FOREGROUND_WHITE     = FOREGROUND_BLUE | FOREGROUND_GREEN | FOREGROUND_RED
        
        # winbase.h
        STD_INPUT_HANDLE     = -10
        STD_OUTPUT_HANDLE    = -11
        STD_ERROR_HANDLE     = -12

        # wincon.h
        FOREGROUND_BLACK     = 0x0000
        FOREGROUND_BLUE      = 0x0001
        FOREGROUND_GREEN     = 0x0002
        FOREGROUND_CYAN      = 0x0003
        FOREGROUND_RED       = 0x0004
        FOREGROUND_MAGENTA   = 0x0005
        FOREGROUND_YELLOW    = 0x0006
        FOREGROUND_GREY      = 0x0007
        FOREGROUND_INTENSITY = 0x0008 # foreground color is intensified.

        BACKGROUND_BLACK     = 0x0000
        BACKGROUND_BLUE      = 0x0010
        BACKGROUND_GREEN     = 0x0020
        BACKGROUND_CYAN      = 0x0030
        BACKGROUND_RED       = 0x0040
        BACKGROUND_MAGENTA   = 0x0050
        BACKGROUND_YELLOW    = 0x0060
        BACKGROUND_GREY      = 0x0070
        BACKGROUND_INTENSITY = 0x0080 # background color is intensified.     

        levelno = args[1].levelno
        if(levelno >= 50):
            color = BACKGROUND_YELLOW | FOREGROUND_RED | FOREGROUND_INTENSITY | BACKGROUND_INTENSITY 
        elif(levelno >= 40):
            color = FOREGROUND_RED | FOREGROUND_INTENSITY
        elif(levelno >= 30):
            color = FOREGROUND_YELLOW | FOREGROUND_INTENSITY
        elif(levelno >= 20):
            color = FOREGROUND_GREEN
        elif(levelno >= 10):
            color = FOREGROUND_MAGENTA
        else:
            color = FOREGROUND_WHITE
        args[0]._set_color(color)

        ret = fn(*args)
        args[0]._set_color( FOREGROUND_WHITE )

        return ret

    return new



def add_coloring_to_emit_ansi(fn):
    # add methods we need to the class
    def new(*args):
        levelno = args[1].levelno
        
        if(levelno >= 50):
            color = '\x1b[31m' # red
        elif(levelno >= 40):
            color = '\x1b[31m' # red
        elif(levelno >= 30):
            color = '\x1b[33m' # yellow
        elif(levelno >= 20):
            color = '\x1b[0m' # green 
        elif(levelno >= 10):
            color = '\x1b[35m' # pink
        else:
            color = '\x1b[0m' # normal
        args[1].msg = color + args[1].msg +  '\x1b[0m' 

        return fn(*args)
    
    return new