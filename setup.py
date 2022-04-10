import setuptools
import json
import os
from pathlib import Path
from subprocess import check_call
from setuptools.command.install import install

APP_NAME = "raincoat_prowlarr"

class PostInstallCommand(install):
    """Post-installation for installation mode."""
    def run(self):
        cfg_path = f"{str(Path.home())}/.config/{APP_NAME}.json"
        if not os.path.exists(cfg_path):            
            cfg = open(cfg_path, 'x')
            j = dict(
                indexer_manager="jackett",
                jackett_apikey="",
                jackett_url="http://127.0.0.1:9117",
                jackett_indexer="all",
                prowlarr_apikey="",
                prowlarr_url="http://127.0.0.1:9117",
                prowlarr_indexer="",
                description_length=100,
                exclude="",
                results_limit=20,
                client_url="",
                display="grid",
                torrent_client="transmission",
                torrent_client_username="",
                torrent_client_password="",
                download_dir="",
                nzbget_url= "http://127.0.0.1",
                nzbget_username= "",
                nzbget_password= "",
                nzbget_port= 6789
            )
            json.dump(j, cfg, indent=4)
        install.run(self)

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="raincoat-prowlarr",
    version="0.2.1",
    author="crvideoVR",
    author_email="crvideoVR@outlook.com",
    description="Raincoat-prowlarr is a tool to search torrents using jackett and search torrents and nzb files using prowlarr and send them to your client.",
    keywords="transmission qbittorrent deluge jackett torrent nzbget",
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires=">=3.6",
    packages=setuptools.find_packages(),
    entry_points = {
        "console_scripts": ['raincoat_prowlarr = raincoat_prowlarr.raincoat_prowlarr:main']
        },
    url="https://github.com/crvideo/raincoat_prowlarr.git",
    classifiers=[
        "Programming Language :: Python :: 3 :: Only",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Unix",
        "Topic :: Communications :: File Sharing",
    ],
    install_requires=["requests>=2.23.0", "justlog", "colorama==0.4.3", "tabulate==0.8.7", "transmission-clutch==6.0.2", "deluge-client==1.8.0", "python-qbittorrent==0.4.2"],
    cmdclass={
        'install': PostInstallCommand
    },

)
