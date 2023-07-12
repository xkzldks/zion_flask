from pytube import YouTube, Playlist
import glob
import os.path

def info(a):
    url = a
    yt = YouTube(url)
    # print("title : ", yt.title)
    # print("length : ", yt.length)
    # print("author : ", yt.author)
    # print("publish_date : ", yt.publish_date)
    # print("views : ", yt.views)
    # print("keywords : ", yt.keywords)
    # print("description : ", yt.description)
    # print("thumbnail_url : ", yt.thumbnail_url)
    stream = yt.streams.get_highest_resolution()
    stream.download(DOWNLOAD_FOLDER)

    # return yt


def cvt(a, mp):
    DOWNLOAD_FOLDER = "/download"
    li = []
    try:
        #플레이리스트일경우
        p = Playlist(a)
        print(p)
        print("다수곡 mp", mp)
        for video in p.videos:
            video.streams.filter(only_audio=True).all()
            video.streams.filter(only_audio=True).first().download(DOWNLOAD_FOLDER)
            if int(mp) == 3:
                files = glob.glob("/download/*.mp4")
                for _ in files:
                    if not os.path.isdir(_):
                        filename = os.path.splitext(_)
                        try:
                            os.rename(_, filename[0] + '.mp3')
                        except:
                            pass
            li.append(str(video.title)+".mp"+str(mp))
        return li
    except:
        #한곡일경우
        print("한곡 mp", mp)
        yt = YouTube(a)
        yt.streams.filter(only_audio=True).all()
        yt.streams.filter(only_audio=True).first().download(DOWNLOAD_FOLDER)
        if int(mp) == 3:
            print('mp', mp)
            files = glob.glob("/download/*.mp4")
            for _ in files:
                if not os.path.isdir(_):
                    filename = os.path.splitext(_)
                    try:
                        os.rename(_, filename[0] + '.mp3')
                    except:
                        pass
        return str(yt.title)+".mp"+str(mp)

