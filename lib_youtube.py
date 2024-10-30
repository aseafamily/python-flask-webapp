from pytube import Channel

channel_url = "https://www.youtube.com/c/ProgrammingKnowledge"
channel = Channel(channel_url)

video_ids = [video.video_id for video in channel.videos]
print(video_ids)