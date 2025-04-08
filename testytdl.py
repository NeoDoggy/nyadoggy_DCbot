import yt_dlp

opts={
    "quiet":    True,
    "simulate": True,
    "forceurl": True,
    "live-from-start": True,
}

with yt_dlp.YoutubeDL(opts) as ytdl:
    url=ytdl.extract_info("https://youtu.be/yAZOws_I55k?si=8Fz2OZMzi_Tw5OSb",download=False)
    print(url)