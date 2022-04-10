# Raincoat

Raincoat_prowlarr is a CLI tool to search torrents using [Jackett](https://github.com/Jackett/Jackett)'s indexers or [Prowlarr](https://github.com/Prowlarr/Prowlarrand) and send them directly to your client. Prowlarr supports NZB indexer.

### Installation

`pip install raincoat-prowlarr

### Requirements

- Python 3.6+
- Jackett and configured indexers
- Or Prowlarr and configure indexers
- qBittorrent, Transmission or Deluge (or use local download option)
- nzbget, downloader for nzb files
- libtorrent if you use local downloader and magnet links.
  - Arch: `pacman -S libtorrent-rasterbar`
  - Ubuntu: `apt-get install python-libtorrent -y`
  - Fedora: `dnf install rb_libtorrent-python2`

### Usage

`raincoat_prowlarr "Terms to search"`

#### Parameters

- --indexer_manager
  - specify the indexer manager to search; prowlarr or jackett
- --jackett_ key
  - Specify a Jackett API key
- --prowlarr_ key
  - Specify a Prowlarr API key
- -l, --length
  - Max number of characters displayed in the "Description" column.
- -L, --limit
  - Limits the number of results displayed.
- -c, --config
  - Specifies a different config path.
- -s, --sort
  - Change the sorting criteria. Valid choices are: 'cn','protocol','seeders', 'leechers', 'ratio', 'size' and 'description'. Default/not specified is 'cn/size'. cn is chinese subtitle.  protocol is usenet/torrent, if not specified, torrent has high priority or vice versa.
- --jackett_indexer
  - Change the indexer for Jackett used for your search, in cases where you want to only search one site. Default is "all".
- --prowlarr_indexer
  - Change the indexer for prowlarr used for your search, in cases where you want to only search one site. Default is "". "" for all; -1 for all usenet; -2 for all torrents. look at https://wiki.servarr.com/prowlarr/search
- -d, --download x
  - Grab the first x resultd and send to the client immediately. Defaults to 1.
- -K, --insecure
  - Don't verify certificates  
- --local
  - Force use of "local" file download.
- --list
  - Specify a file to load search terms from. One term per line.
- --verbose
  - Extra verbose logging sent to log file.

#### Configuration file

Upon installation, a config file is created in your home directory. Before you can use Raincoat, you will need to modify it.

```json
{
    "indexer_manager": "prowlarr",
	"jackett_apikey": "",
	"jackett_url": "http://your_base_jackett_url:port",
	"jackett_indexer": "all",
	"prowlarr_apikey": "",
	"prowlarr_url": "http://you_base_prowlarr_url:port",
    "prowlarr_indexer": "",
	"description_length": 100,
	"exclude": "words to exclude",
	"results_limit": 20,
	"client_url": "http://your_torrent_client_api",
	"display": "grid",
	"torrent_client": "qbittorrent",
	"torrent_client_username": "admin",
	"torrent_client_password": "admin",
	"download_dir": "/some/directory/",
	"nzbget_url": "http://your_nzb_server_url",
    "nzbget_username**: "***",
    "nzbget_password**: "***",
    "nzbget_port": 6789

}
```
- indexer_manager (string)
  - indexer manager to search. jackett or prowlarr
- jackett_apikey (string)
  - The api key provided by Jackett, found on the dashboard.
- jackett_url (string)
  - The base url for your jackett instance. (default: http://127.0.0.1:9117)
- jackett_indexer (string)
  - The jackett indexer you wish to use for searches.
- prowlarr_apikey (string)
  - The api key provided by Prowlarr, found on the dashboard.
- prowlarr_url (string)
  - The base url for your prowlarr instance. (default: not sure)
- prowlarr_indexer (string)
  - The prowlarr indexer you wish to use for searches.
- description_length (int)
  - The default description length
- exclude (string)
  - Words to exclude from your results seperated by a space.
- results_limit (int)
  - Max number of lines to show.
- client_url (string)
  - The url to your torrent client's API
- display (string)
  - The display style of the results table. You can view available choices [here](https://pypi.org/project/tabulate/)
- torrent_client (string)
  - Your torrent client. Valid options are: local, qbittorrent, transmission and deluge.
- torrent_client_username (string)
  - Your torrent client's login username.
- torrent_client_password
  - Your torrent client's login password. Note: Only Transmission accepts empty passwords.
- download_dir
  - Where to save the torrent files when using "local" downloader.
- nzbget_url (string)
  - url for nzbget server
- nzbget_username (string)
  - nzbget username
- nzbget_password (string)
  - nzbget pasword
- nzbget_port (int)
  - nzbget port


# Built with

- requests
- justlog
- colorama
- tabulate
- transmission-clutch
- deluge-client
- python-qbittorrent

All available on Pypi.

# License

This project is licensed under the MIT License
