from youtube_transcript_api import YouTubeTranscriptApi

# https://www.youtube.com/feeds/videos.xml?channel_id=UCk6ONJlPzjw3DohAeMSgsng
# https://github.com/foorilla/allainews_sources


def generate_transcript(id):
    transcript = YouTubeTranscriptApi.get_transcript(id)
    script = ""

    for text in transcript:
        t = text["text"]
        if t != "[Music]":
            script += t + " "

    return script, len(script.split())


id = "Y8Tko2YC5hA"
transcript, no_of_words = generate_transcript(id)
print(transcript)
