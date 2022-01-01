import requests 
from requests.utils import quote #percent encoding
import os
from datetime import datetime, timedelta, date
from .downloadandzip import download_file, zipdir, delete_files_in_dir
import zipfile
import pathlib
from pathlib import Path
import shutil

class TwitchAPI():
    client_id = os.environ['TWITCH_CLIENTID']
    twitch_secret = os.environ['TWITCH_SECRET']
    bearer_token = ''
    bearer_token_expiration = ''

    def refreshBearerToken(self):
        """
        Fetches new bearer token from Twitch. Bearer tokens last up to 60 days
        """
        url = f"https://id.twitch.tv/oauth2/token?client_id={self.client_id}&client_secret={self.twitch_secret}&grant_type=client_credentials"
        status_code =  requests.post(url)
        self.bearer_token = 'Bearer ' + status_code.json()['access_token']
        return self.bearer_token

    def get_game(self, name):
        url = 'https://api.twitch.tv/helix/games?name=' + quote(name)
        headers = {'Client-Id': self.client_id, 'Authorization' : self.bearer_token}
        return requests.get(url, headers=headers).json()['data']

    def get_game_id(self, name):
        return self.get_game(name)['0']


    def get_broadcaster(self, login):
        """
        Returns the Twitch broadcaster id of the provided login username 
        Example return format:
        {
            "id": "23161357",
            "login": "lirik",
            "display_name": "LIRIK",
            "type": "",
            "broadcaster_type": "partner",
            "description": "We like to play everything, relax, and have a good time. ",
            "profile_image_url": "https://static-cdn.jtvnw.net/jtv_user_pictures/27fdad08-a2c2-4e0b-8983-448c39519643-profile_image-300x300.png",
            "offline_image_url": "https://static-cdn.jtvnw.net/jtv_user_pictures/f3b9dc80-8f92-4b62-99e8-cf510d836417-channel_offline_image-1920x1080.jpeg",
            "view_count": 393985569,
            "created_at": "2011-06-27T18:34:45.119555Z"
        }
        """
        url = 'https://api.twitch.tv/helix/users?login=' + quote(login)
        headers = {'Client-Id': self.client_id, 'Authorization' : self.bearer_token}
        
        return requests.get(url, headers=headers).json()['data']
    
    def get_broadcaster_id(self, login):
        return self.get_broadcaster(login)['id']

    def getTopClips(self, broadcaster_id=None, game_id=None, period='daily', first='50'):
        """
        Returns json format with top clips of given broadcaster or game ordered by viewcount

        Parameters
        period: daily, weekly, monthly, or yearly
        first: number of clips to return
        """
        #TODO: Process period started_at and ended_at (defaults to week)
        d = datetime.utcnow() # <-- get time in UTC
        period = period.lower()
        if period == 'daily':
            d = d.replace(hour=4, minute=0, second=00, microsecond=00)
            x = d + timedelta(days = -1)
            d = d.isoformat("T") + "Z"
            x = x.isoformat("T") + "Z"
        elif period == 'weekly':
            d = d.replace(hour=4, minute=0, second=00)
            x = d + timedelta(days = -7)
            d = d.isoformat("T") + "Z"
            x = x.isoformat("T") + "Z"       
        elif period == 'monthly':
            d = d.replace(hour=4, minute=0, second=00)
            x = d + timedelta(days = -30)
            d = d.isoformat("T") + "Z"
            x = x.isoformat("T") + "Z"
        elif period == 'yearly':
            d = d.replace(hour=4, minute=0, second=00)
            x = d + timedelta(days = -365)
            d = d.isoformat("T") + "Z"
            x = x.isoformat("T") + "Z"

        url = 'https://api.twitch.tv/helix/clips?'
        if broadcaster_id != None:
            url = url + 'broadcaster_id=' + quote(broadcaster_id) + '&'
        elif game_id != None:
            url = url + 'game_id=' + quote(game_id) + '&'
        if period != None:
            url = url + 'started_at={}&ended_at={}&'.format(x, d)
        if first != None:
            url = url + f'first={first}'

        headers = {'Client-Id': self.client_id, 'Authorization' : self.bearer_token}
        top_clips = requests.get(url, headers=headers).json()['data']
        return top_clips
    
    def get_slug_clip(self, slug):
        url = 'https://api.twitch.tv/helix/clips?id=' + slug
        headers = {'Client-Id': self.client_id, 'Authorization' : self.bearer_token}
        print(url)
        
        return requests.get(url, headers=headers).json()['data']

    def download_clips_directory(self, clips, dirname='', max='5', language='en'):
        media_dir = str(Path('{}/media'.format(os.getcwd())))
        
        # Delete previous downloaded files
        if os.path.exists(media_dir):
            delete_files_in_dir(media_dir)

        clips_path = str(Path('{}/{}_{}'.format(media_dir, dirname, date.today().strftime('%B %d %Y'))))
        if not os.path.exists(clips_path):
            os.mkdir(clips_path)
        i = 1
        for clip in clips:
            if clip['language'] == language:
                keepcharacters = (' ','.', '_') #special chars to be kept in filename
                description = str(Path(clips_path + '/description.txt'))
                with open(description, 'a', encoding="utf-8") as file:
                    file.write('Clip #{}\n'.format(i))
                    file.write('Streamer: {}\n'.format(clip['broadcaster_name']))
                    file.write('Clip Title: {}\n'.format(clip['title']))
                    file.write('Clipped by: {}\n'.format(clip['creator_name']))
                    file.write('Views: {}\n'.format(clip['view_count']))
                    file.write('Duration: {}\n'.format(clip['duration']))
                    file.write('Timestamp: {}\n'.format(clip['created_at']))
                    file.write('URL: {}\n'.format(clip['url']))
                    file.write('\n')
                    vid_url = clip['thumbnail_url'].split('-preview')[0] + '.mp4'

                    #remove special chars from filename
                    video_filename = f'{i}. ' + clip['broadcaster_name'] + '_' + clip['title']
                    video_filename = "".join(c for c in video_filename if c.isalnum() or c in keepcharacters).rstrip()
                    filename = str(Path(clips_path + '/' + video_filename))
                    file.close()
                download_file(vid_url, filename=filename)
                clip['filepath'] = filename
                i += 1
                if i > int(max):
                    break

        #zip directory
        zipf = zipfile.ZipFile(clips_path + '.zip', 'w', zipfile.ZIP_DEFLATED)
        zipdir(clips_path, zipf)
        zipf.close()  

        #delete original directory
        dir_path = clips_path.split('.')[0]


        if os.path.exists(dir_path):
            shutil.rmtree(dir_path)

        return clips_path + '.zip'

    def download_slug_clip(self, slug):
        clip = self.get_slug_clip(slug)
        print(clip)
        return self.download_clips_directory(clips=clip, dirname=slug)
        

    def download_game_clips(self, id, period, limit, name):
        clips = self.getTopClips(game_id=id)
        video_title = self.download_clips_directory(clips, dirname='{}_{}_Clips - '.format(name, period), max=limit)
        return video_title
    
    
    def download_broadcaster_clips(self, id, period, limit, name):
        clips = self.getTopClips(broadcaster_id=id)
        video_title = self.download_clips_directory(clips, dirname='{}_{}_Clips - '.format(name, period), max=limit)
        return video_title
        
    def __init__(self):
        self.bearer_token = self.refreshBearerToken()
        self.bearer_token_expiration = ''

