"""
YouTube ভিডিও ডাউনলোডার টুল
- Creative Commons ভিডিও ডাউনলোড করুন
- বিভিন্ন কোয়ালিটি সাপোর্ট
- কপিরাইট সতর্কতা
"""

import yt_dlp
import os
from typing import Optional, Dict
from datetime import datetime

class YouTubeDownloader:
    def __init__(self):
        self.output_dir = "downloads/youtube"
        self.copyright_status = "COPYRIGHTED"
        os.makedirs(self.output_dir, exist_ok=True)
    
    def download_video(
        self,
        url: str,
        quality: str = "best",
        audio_only: bool = False
    ) -> Dict:
        """
        YouTube ভিডিও ডাউনলোড করুন
        
        Args:
            url: YouTube ভিডিও URL
            quality: "best", "1080p", "720p", "480p", "360p"
            audio_only: শুধু অডিও ডাউনলোড করবেন কি
        
        Returns:
            ডাউনলোড স্ট্যাটাস এবং ফাইল তথ্য
        """
        
        ydl_opts = {
            'format': 'bestaudio' if audio_only else 'best',
            'outtmpl': os.path.join(self.output_dir, '%(title)s.%(ext)s'),
            'quiet': False,
            'no_warnings': False,
            'progress_hooks': [self._progress_hook],
        }
        
        # কোয়ালিটি সেট করুন
        if not audio_only and quality != "best":
            ydl_opts['format'] = f'bestvideo[height<={quality[:-1]}]+bestaudio/best'
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                
                return {
                    "status": "success",
                    "copyright_warning": "⚠️ এই ভিডিও সাধারণত কপিরাইটেড। শুধুমাত্র Creative Commons লাইসেন্সযুক্ত ভিডিও ব্যবহার করুন।",
                    "title": info.get('title'),
                    "duration": info.get('duration'),
                    "file_name": f"{info.get('title')}.{info.get('ext')}",
                    "file_path": os.path.join(self.output_dir, f"{info.get('title')}.{info.get('ext')}"),
                    "uploader": info.get('uploader'),
                    "upload_date": info.get('upload_date'),
                    "view_count": info.get('view_count'),
                    "like_count": info.get('like_count'),
                    "description": info.get('description'),
                    "metadata": {
                        "format": info.get('ext'),
                        "quality": quality,
                        "audio_only": audio_only,
                        "downloaded_at": datetime.now().isoformat()
                    }
                }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
                "copyright_warning": "⚠️ ডাউনলোড ব্যর্থ - সম্ভবত কপিরাইট সুরক্ষা বা ভৌগোলিক সীমাবদ্ধতা"
            }
    
    def get_video_info(self, url: str) -> Dict:
        """ভিডিও তথ্য পান (ডাউনলোড ছাড়াই)"""
        ydl_opts = {'quiet': True, 'no_warnings': True}
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                
                return {
                    "status": "success",
                    "copyright_status": "COPYRIGHTED",
                    "title": info.get('title'),
                    "duration": info.get('duration'),
                    "uploader": info.get('uploader'),
                    "upload_date": info.get('upload_date'),
                    "view_count": info.get('view_count'),
                    "like_count": info.get('like_count'),
                    "description": info.get('description'),
                    "available_formats": self._get_available_formats(info)
                }
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def _get_available_formats(self, info: Dict) -> list:
        """উপলব্ধ ফরম্যাট পান"""
        formats = []
        if info.get('formats'):
            for fmt in info['formats']:
                if fmt.get('height'):
                    formats.append(f"{fmt['height']}p - {fmt.get('ext')}")
        return list(set(formats))
    
    def _progress_hook(self, d: Dict):
        """ডাউনলোড অগ্রগতি ট্র্যাক করুন"""
        if d['status'] == 'downloading':
            percent = d['_percent_str']
            speed = d['_speed_str']
            print(f"📥 ডাউনলোড করছি: {percent} at {speed}")
        elif d['status'] == 'finished':
            print(f"✅ ডাউনলোড সম্পন্ন!")


# টুল ব্যবহার করুন
if __name__ == "__main__":
    downloader = YouTubeDownloader()
    
    # উদাহরণ
    url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    
    # ভিডিও তথ্য পান
    info = downloader.get_video_info(url)
    print("ভিডিও তথ্য:", info)
    
    # ভিডিও ডাউনলোড করুন
    result = downloader.download_video(url, quality="720p")
    print("ডাউনলোড ফলাফল:", result)
