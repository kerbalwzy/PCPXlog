"""
Save self-defined tools in this file
"""
import os


def create_conf_py_file():
    """
    This function is for package console scripts
    Copy the config demo file to work dir.
    """
    config_demo_py_path = os.path.dirname(os.path.abspath(__file__)) + '/configDemo.py'

    with open(config_demo_py_path, "rb") as f:
        data = f.read()

    with open('./cpxLogConfig.py', 'wb') as f:
        f.write(data)


#############################################
class EmailSender:
    # TODO create a e-mail sender class
    pass
