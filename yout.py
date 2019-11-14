from pytube import YouTube
import os.path

downloaded_links_filename = ''
links_to_be_downloaded = ''

def decor(func):
    def wrap(url):
        print('=' * 30)
        func(url)
    return wrap


@decor
def download_video(url):
    if len(url) < 1:
        return

    downloaded_links = []
    try:
        with open(downloaded_links_filename, 'r') as f:
            for l in f.readlines():
                downloaded_links.append(l.replace('\n', ''))
    except Exception as e:
        print(e)
        print('Cannot open', downloaded_links_filename)
        return

    # creating YouTube object
    if url not in downloaded_links:
        try:
            print('checking ', url, 'YouTube link')
            yt = YouTube(url)
        except Exception as e:
            print(e)
            print(url, 'is not valid YouTube site!!!')
            return
        else:
            # accessing video stream of YouTube obj.(first one, more available)
            stream = yt.streams.first()
            print('downloading video from', url)
            print(yt.title)
            # download into working directory
            print('checking file existence' + './' + yt.title + '.mp4')
            # if os.path.isfile('./'+yt.title+'.mp4'):
            #     print('./'+yt.title+'.mp4')
            #     print('File already exist')
            #     return
            stream.download()
            print('Downloaded video')
            try:
                with open(downloaded_links_filename, 'a+') as f:
                    f.write('\n'+url)
                    print('Added', url, 'link to', downloaded_links_filename)
            except Exception:
                print('Cannot open', downloaded_links_filename)
                return
    else:
        print(url, 'is downloaded already.')


if __name__ == "__main__":

    downloaded_links_filename = input("Filename where the list of youtube links resides.\n"
                                      "e.g. C:\\\\Users\\Username\\youtube_downloadLinks.txt\n")

    links_to_be_downloaded = input("Filename where the list of youtube links already downloaded.\n"
                                   "e.g.  C:\\\\Users\\Username\\youtube_downloadedLinks.txt\n")


    tobe_downloaded = []
    with open(links_to_be_downloaded, 'r') as f:
        lines = f.readlines()
        total = len(lines)
        count = 1
        for line in lines:
            print(count,'of',total)
            download_video(line.replace('\n',''))
            count += 1
    print('*' * 30)
    print('Done!')
