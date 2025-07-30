from jarvis.install import auto_etp_install

try:
    from auto_etp.jarvis import main_new_window
except ModuleNotFoundError as ex:
    print(ex)
    auto_etp_install()
finally:
    from auto_etp.jarvis import main_new_window
from auto_etp.jarvis import main_new_window

main_new_window()
