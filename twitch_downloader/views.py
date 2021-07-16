from django.shortcuts import render, HttpResponse
from django.http import FileResponse
from .models import Game, Broadcaster
from django.conf import settings
from .utils import TwitchAPI
from .models import Game, Broadcaster


from .forms import DownloadForm

def home(request):
    context = {
        'STATIC_URL' : settings.STATIC_URL,
    }


    if request.method == 'POST':
        # Validate name ----------------------------------------------------------------
        details = request.POST

        #Check if game or channel is in database
        name = details['twitch-name']

        twitch_id = Game.objects.filter(name=name)
        id_type = 'game'

        if twitch_id.exists():
            twitch_id = twitch_id[0].game_id
        else:
            twitch_id = Broadcaster.objects.filter(name=name)
            if twitch_id.exists():
                twitch_id = twitch_id[0].broadcaster_id
                id_type = 'broadcaster'

        
        twitch = TwitchAPI()
        #If not, get id from twithAPI
        if not twitch_id:
            # Download clips -----------------------------------------------------------
            # Assume name given is valid 
            # get id regardless of game or broadcaster and add to respectul table
            twitch_id = twitch.get_game(name)

            if twitch_id:
                twitch_id = twitch_id[0]
                Game.objects.create(game_id=twitch_id, name=name)
        
            else: 
                twitch_id = twitch.get_broadcaster(name)[0]['id']
                id_type = 'broadcaster'
                Broadcaster.objects.create(broadcaster_id=twitch_id, name=name)

        file_server = ''
        if id_type == 'game':
            file_server = twitch.download_game_clips(twitch_id, details['period'], details['limit'], name)
        else:
            file_server = twitch.download_broadcaster_clips(twitch_id, details['period'], details['limit'], name)

        path = '\\'.join(file_server.split('\\')[0:-1])
        file_name = file_server.split('\\')[-1]

        # Download file
        zip_file = open(file_server, 'rb')
        return FileResponse(zip_file)
    else:
        form = DownloadForm()
        context['form'] = form,
      


    return render(request, 'twitch_downloader/index.html', context)

