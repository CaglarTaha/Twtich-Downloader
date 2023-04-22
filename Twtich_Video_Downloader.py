import tkinter as tk
from twython import TwythonStreamer
import urllib.request
from tkinter import ttk



class MyStreamer(TwythonStreamer):
    
    def __init__(self, consumer_key, consumer_secret, access_token, access_token_secret):
        super().__init__(consumer_key, consumer_secret, access_token, access_token_secret)
        self.video_url = ""

    def on_success(self, data):
        if 'media' in data['entities']:
            for media in data['entities']['media']:
                if media['type'] == 'video':
                    self.video_url = media['video_info']['variants'][0]['url']
                    self.disconnect()

    def on_error(self, status_code, data):
        print(status_code, data)
        self.disconnect()

def download_video():
    url = url_entry.get()
    start_time = start_entry.get()
    end_time = end_entry.get()
    
    consumer_key = consumer_key_entry.get()
    consumer_secret =consumer_secret_entry.get()
    access_token =access_token_entry.get()
    access_token_secret=access_token_secret_entry.get()
    streamer = MyStreamer(consumer_key, consumer_secret, access_token, access_token_secret)
    streamer.statuses.filter(track=url)

    while streamer.video_url == "":
        pass


    video_file_name = f"{url.split('/')[-1]}_{start_time}-{end_time}.mp4"
    urllib.request.urlretrieve(streamer.video_url, f"downloads/{video_file_name}", 
                               data=lambda chunk, _, total: progress_bar.config(maximum=total, value=chunk))

 
    tk.messagebox.showinfo("Download Complete", f"The video has been downloaded as {video_file_name}.")


root = tk.Tk()
root.title("Twitch Video Downloader")
root.geometry("1080x720")
root.resizable(False, False)
root.config(bg="#f2f2f2")



# Create the widgets
url_label = tk.Label(root, text="Enter the Twitch video URL:", font=("Arial", 12), bg="#f2f2f2")
url_label.pack(pady=10)

url_entry = tk.Entry(root, width=50, font=("Arial", 12), bd=2, relief="groove")
url_entry.pack(pady=5)

ConsumerKey_label = tk.Label(root, text="Enter the Twitch Consumer Key:", font=("Arial", 12), bg="#f2f2f2")
ConsumerKey_label.pack(pady=10)

consumer_key_entry = tk.Entry(root, width=50, font=("Arial", 12), bd=2, relief="groove")
consumer_key_entry.pack(pady=5)

consumer_secret_entry_label = tk.Label(root, text="Enter the Twitch Consumer Secret Key:", font=("Arial", 12), bg="#f2f2f2")
consumer_secret_entry_label.pack(pady=10)

consumer_secret_entry = tk.Entry(root, width=50, font=("Arial", 12), bd=2, relief="groove")
consumer_secret_entry.pack(pady=5)

access_token_entry_label = tk.Label(root, text="Enter the Twitch Access Token:", font=("Arial", 12), bg="#f2f2f2")
access_token_entry_label.pack(pady=10)

access_token_entry = tk.Entry(root, width=50, font=("Arial", 12), bd=2, relief="groove")
access_token_entry.pack(pady=5)



access_token_secret_entry_label = tk.Label(root, text="Enter the Twitch  access_token_Secret:",font=("Arial", 12), bg="#f2f2f2")
access_token_secret_entry_label.pack()

access_token_secret_entry = tk.Entry(root,width=50,font=("Arial", 12), bd=2, relief="groove")
access_token_secret_entry.pack()



start_label = tk.Label(root, text="Enter the start time in seconds:",font=("Arial", 12), bg="#f2f2f2")
start_label.pack()

start_entry = tk.Entry(root, width=50,font=("Arial", 12), bd=2, relief="groove")
start_entry.pack()

end_label = tk.Label(root, text="Enter the end time in seconds:",font=("Arial", 12), bg="#f2f2f2")
end_label.pack()

end_entry = tk.Entry(root, width=50,font=("Arial", 12), bd=2, relief="groove")
end_entry.pack()

download_button = tk.Button(root, text="Download Video", command=download_video,font=("Arial", 12), bg="#f2f2f2")
download_button.pack()

progress_bar = ttk.Progressbar(root, orient="horizontal", length=200, mode="determinate")

progress_bar.pack()

root.mainloop()
