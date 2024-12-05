from time import time
from fastapi import FastAPI, __version__
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from app.routers import main

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(main.router)

html = f"""
<!DOCTYPE html>
<html>
    <head>
        <title>FastAPI on Vercel</title>
        <link rel="icon" href="/static/favicon.ico" type="image/x-icon" />
    </head>
    <body>
        <div class="bg-gray-200 p-4 rounded-lg shadow-lg">
            <h1>Hello from FastAPI@{__version__}</h1>
            <ul>
                <li><a href="/docs">/docs</a></li>
                <li><a href="/redoc">/redoc</a></li>
            </ul>
            <p>Powered by <a href="https://vercel.com" target="_blank">Vercel</a></p>
        </div>
    </body>
</html>
"""

@app.get("/")
async def root():
    return HTMLResponse(html)

@app.get('/ping')
async def hello():
    return {'res': 'pong', 'version': __version__, "time": time()}


from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
import yt_dlp
import os


class VideoURL(BaseModel):
    url: str

def download_facebook_video(url: str):
    ydl_opts = {
        'outtmpl': '%(id)s.%(ext)s',  # Use the video ID for the file name
        'format': 'best',  # Download the best available format
        'noplaylist': True,  # Ensure it's downloading only the video, not a playlist
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)  # Download the video
            video_id = info_dict.get('id', None)
            video_ext = info_dict.get('ext', 'mp4')
            video_file = f"{video_id}.{video_ext}"  # Construct file name

            if os.path.exists(video_file):
                return video_file  # Return the path to the downloaded file
            else:
                raise HTTPException(status_code=500, detail="Video file not found after download.")
    except yt_dlp.utils.DownloadError as e:
        raise HTTPException(status_code=500, detail=f"Download failed: {e}")
    except yt_dlp.utils.ExtractorError as e:
        raise HTTPException(status_code=500, detail=f"Extractor error: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")

@app.post("/download")
async def download_video(video: VideoURL):
    video_file = download_facebook_video(video.url)
    
    # Return the video file as a response
    return FileResponse(video_file, media_type="video/mp4", filename=os.path.basename(video_file))

@app.get("/")
async def root():
    return {"message": "Hello, World!"}
