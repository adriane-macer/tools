# from pytube import YouTube
#
# # where to save
# SAVE_PATH = "./"  # to_do
#
# # link of the video to be downloaded
# link = "https://www.youtube.com/watch?v=DSstuqVAi84&list=RDDSstuqVAi84&start_radio=1"
#
# try:
#     # object creation using YouTube
#     yt = YouTube(link)
# except:
#     # to handle exception
#     print("Connection Error")
#
# # Get all streams and filter for mp4 files
# mp4_streams = yt.streams.filter(file_extension='mp4').all()
#
# # get the video with the highest resolution
# d_video = mp4_streams[-1]
#
# try:
#     # downloading the video
#     d_video.download(output_path=SAVE_PATH)
#     print('Video downloaded successfully!')
# except:
#     print("Some Error!")


from pytubefix import YouTube

# change your desire link
link = "https://www.youtube.com/watch?v=DSstuqVAi84&list=RDDSstuqVAi84&start_radio=1"

yt = YouTube(link)

# change your desired path
output_path = "D:\\Github\\tools\\"

try:
    yt.streams.filter(progressive=True,
                      file_extension="mp4").order_by('resolution').desc().last().download(output_path=output_path,
                                                                                          filename="converted.mp4")
except Exception as e:
    print(e)
    print("Some Error!")
print('Task Completed!')
