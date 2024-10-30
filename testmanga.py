from enma import *

config = CloudFlareConfig(
    user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
    cf_clearance=''
)

enma = Enma()
enma.source_manager.set_source('nhentai')
enma.source_manager.source.set_config(config=config)