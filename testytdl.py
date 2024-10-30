import yt_dlp

opts={
    "quiet":    True,
    "simulate": True,
    "forceurl": True,
    "live-from-start": True
}

with yt_dlp.YoutubeDL(opts) as ytdl:
    url=ytdl.extract_info("http://radio.garden/visit/xinzhuang-district/UjbzWC8S",download=False)
    print(url)