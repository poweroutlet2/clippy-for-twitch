from django import forms
from .utils import TwitchAPI

class DownloadForm(forms.Form):
    name = forms.CharField(label='',  
                            widget=forms.TextInput(attrs={
                                'id': 'name', 
                                'required': True, 
                                'placeholder': 'Streamer or Game'                
                            })
            )

    period_choices = [
        ('Daily', 'Daily'),
        ('Weekly', 'Weekly'),
        ('Monthly', 'Monthly'),
        ('Yearly', 'Yearly')
    ]
    period = forms.ChoiceField(label='', choices=period_choices, widget=forms.Select(attrs={ 'id': 'period', 'required': True, }))

    limit = forms.IntegerField(label='', 
                                widget=forms.NumberInput(attrs= {
                                    'name': "limit",
                                    'id': "limit", 
                                    'min': "1", 
                                    'max': "100", 
                                    'placeholder':"# of clips",
                                }
    ))

    def clean(self):
        cleaned_data = super(DownloadForm, self).clean()

        # #validate name
        # name = cleaned_data.get('twith-name')
        # twitch = TwitchAPI()
        # print(name)
        # if twitch.get_broadcaster(name)['broadcaster_type'] != 'partner':
            
        #     self.add_error('name', 'Invalid broadcaster')
        # print(twitch.get_broadcaster(name)['broadcaster_type'] != 'partner')
            
        



        
