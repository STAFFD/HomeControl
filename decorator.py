import pyautogui as pag


def reset_mouse(method):
    def reset(*args, **kw):
        method(*args, **kw)
        pag.moveTo(pag.size()[0], pag.size()[1]/2)
    return reset
