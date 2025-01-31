import requests
from clutch import Client as tClient
from deluge_client import DelugeRPCClient
from qbittorrent import Client as qClient
from .helpers import fetch_torrent_url, convert_to_torrent
import subprocess

class torrent:
    def __init__(self, id, description, media_type, seeders, leechers, download, size, age, protocol,cn):
        self.id = id
        self.media_type = media_type
        self.description = description
        self.seeders = seeders
        self.leechers = leechers
        self.download = download
        self.age = -age ## smaller is better
        self.protocol = protocol
        self.cn = cn
        if(leechers > 0):
            self.ratio = self.seeders / self.leechers
        else:
            self.ratio = self.seeders
        self.size = size / 1000

def filter_out(title, exclusions):
    exclusions = exclusions.split()
    for exclude in exclusions:
        if exclude in title.lower():
            return True
    return False

def deluge(torrent, CLIENT_URL, TOR_CLIENT_USER, TOR_CLIENT_PW, logger):
    TOR_CLIENT = "Deluge"
    print(f"Sending {torrent.description} to {TOR_CLIENT}")
    url = fetch_torrent_url(torrent)
    try:
        logger.debug("Connecting to torrent client...")
        # Connection
        logger.debug(f"{TOR_CLIENT} connection info: {CLIENT_URL.split(':')[0]}, {int(CLIENT_URL.split(':')[1])}, {TOR_CLIENT_USER}")
        client = DelugeRPCClient(CLIENT_URL.split(':')[0], int(CLIENT_URL.split(':')[1]), TOR_CLIENT_USER, TOR_CLIENT_PW)
        client.connect()
        logger.debug(f"Connected to {TOR_CLIENT}") 
                                       
        # Add torrent
        logger.debug(f"Adding {torrent.description} with url: {url}")
        client.call("download_torrent_from_url", url)
        print("Torrent sent!")
    except Exception as e:
        print(f"Unable to send to {TOR_CLIENT}. Check the logs for more information.")
        logger.error(f"Error sending to {TOR_CLIENT}. {str(e)}")
        exit()

def transmission(torrent, CLIENT_URL, TOR_CLIENT_USER, TOR_CLIENT_PW, logger):
    TOR_CLIENT = "Transmission"
    print(f"Sending {torrent.description} to {TOR_CLIENT}")
    url = fetch_torrent_url(torrent)
    try:
        logger.debug("Connecting to torrent client...")
        # Connection
        if TOR_CLIENT_PW != "":
            logger.debug(f"{TOR_CLIENT} connection info: {CLIENT_URL}, {TOR_CLIENT_USER}")
            client = tClient(address=CLIENT_URL, username=TOR_CLIENT_USER, password=TOR_CLIENT_PW)
        else:
            logger.debug(f"{TOR_CLIENT} connection info: {CLIENT_URL}")
            client = tClient(address=CLIENT_URL)
            logger.debug(f"Connected to {TOR_CLIENT}")    
                                       
        # Add torrent
        logger.debug(f"Adding {torrent.description} with url: {url}")
        client.torrent.add({"filename": url})
        print("Torrent sent!")
    except Exception as e:
        print(f"Unable to send to {TOR_CLIENT}. Check the logs for more information.")
        logger.error(f"Error sending to {TOR_CLIENT}. {str(e)}")
        exit()

def qbittorrent(torrent, CLIENT_URL, TOR_CLIENT_USER, TOR_CLIENT_PW, logger):
    TOR_CLIENT = "qBittorrent"
    print(f"Sending {torrent.description} to {TOR_CLIENT}")
    url = fetch_torrent_url(torrent)
    try:
        logger.debug("Connecting to torrent client...")
        # Connection
        logger.debug(f"{TOR_CLIENT} connection info: {CLIENT_URL}, {TOR_CLIENT_USER}")
        client = qClient(CLIENT_URL)
        client.login(TOR_CLIENT_USER, TOR_CLIENT_PW)
  
                                       
        # Add torrent
        logger.debug(f"Adding {torrent.description} with url: {url}")
        client.download_from_link(url)
        print("Torrent sent!")
    except Exception as e:
        print(f"Unable to send to {TOR_CLIENT}. Check the logs for more information.")
        logger.error(f"Error sending to {TOR_CLIENT}. {str(e)}")
        exit()

def local(torrent, download_dir, logger):
    TOR_CLIENT = "local download"
    print(f"Sending {torrent.description} to {TOR_CLIENT}")
    url = fetch_torrent_url(torrent)
    try:
        if url.startswith("magnet:?"):
            
            print(f"{torrent.description} appears to be a magnet link.")
            logger.info(f"Adding {torrent.description} with url: {url}")
            logger.info(f"Using local download method...")   
            convert_to_torrent(url, download_dir)
        else:
            logger.info(f"Using local download method...")   
            r = requests.get(url, allow_redirects=True)
            open(f"{download_dir}{torrent.description}.torrent", 'wb').write(r.content)
            print(f"Torrent downloaded! -> {download_dir}{torrent.description}.torrent")
            logger.info(f"Torrent downloaded! -> {download_dir}{torrent.description}.torrent")
    except Exception as e:
        print(f"Unable to send to {TOR_CLIENT}. Check the logs for more information.")
        logger.error(f"Error sending to {TOR_CLIENT}. {str(e)}")
        exit()


def nzbget(torrent, NZBGET_URL, NZBGET_USER, NZBGET_PW, NZBGET_PORT,logger):
    TOR_CLIENT = "nzbget"
    print(f"Sending {torrent.description} to {TOR_CLIENT}")
    url = torrent.download
    #print(url)
    try:
        logger.debug("Connecting to nzbget client...")
        # Connection
        logger.debug(f"{TOR_CLIENT} connection info: {NZBGET_URL}, {NZBGET_USER}")
                                       
        # Add torrent
        logger.debug(f"Adding {torrent.description} with url: {url}")
        cmd = 'nzbget -n -o ControlIP='+ str(NZBGET_URL) + ' -o ControlUsername=' + str(NZBGET_USER) + ' -o ControlPassword=' + str(NZBGET_PW)+ ' -o ControlPort=' + str(NZBGET_PORT) + ' -A T N ' + "\"" + str(torrent.description) + "\" \"" + url +"\""
        #print(cmd)
        logger.debug(f"Running {cmd}")
        res = subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell = True)
        #print(res.stdout.decode("utf8"))
        print("Torrent sent!")
    except Exception as e:
        print(f"Unable to send to {TOR_CLIENT}. Check the logs for more information.")
        logger.error(f"Error sending to {TOR_CLIENT}. {str(e)}")
        exit()
