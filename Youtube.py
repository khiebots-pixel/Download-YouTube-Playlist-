import os
import re
from yt_dlp import YoutubeDL

def download_playlist_to_phone_storage(playlist_url):
    
    ydl_info_opts = {
        'extract_flat': 'in_playlist',
        'ignoreerrors': True,
    }
    
    print("جاري فحص رابط قائمة التشغيل وجلب الاسم...")
    
    playlist_title = "Youtube_Playlist"
    try:
        with YoutubeDL(ydl_info_opts) as ydl:
            info_dict = ydl.extract_info(playlist_url, download=False)
            if info_dict and 'title' in info_dict:
                playlist_title = info_dict['title']
    except Exception as e:
        print(f"تنبيه: لم نتمكن من جلب اسم القائمة تلقائياً: {e}")

    
    clean_title = re.sub(r'[\\/*?:"<>|]', "", playlist_title).strip()
    

    phone_download_path = os.path.expanduser('~/storage/shared/Download')
    
    
    target_folder = os.path.join(phone_download_path, clean_title)


    if not os.path.exists(target_folder):
        os.makedirs(target_folder)
        print(f"تم إنشاء مجلد في ذاكرة الجهاز باسم: [{clean_title}]")
    else:
        print(f"المجلد موجود مسبقاً في الذاكرة، سيتم الحفظ داخله.")

    
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320', 
        }],
        
        'outtmpl': os.path.join(target_folder, '%(playlist_index)s - %(title)s.%(ext)s'),
        'ignoreerrors': True,

        'download_archive': os.path.join(target_folder, 'downloaded_tracks.txt'),
    }

    print(f"جاري بدء تحميل الـ MP3 في ذاكرة الهاتف بمجلد (Downloads/{clean_title})...")
    
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([playlist_url])
        
    print(f"\nتهانينا! اكتمل التحميل وتجد المجلد الآن في وحدة تخزين الهاتف -> Download -> {clean_title}")

if __name__ == "__main__":
    # ضع رابط قائمة تشغيل يوتيوب هنا
    PLAYLIST_LINK = "https://youtube.com/playlist?list=PLo9oOtkX4xIxKPpbmNPIxuBtVZ_K2pc8C"
    
    download_playlist_to_phone_storage(PLAYLIST_LINK)

