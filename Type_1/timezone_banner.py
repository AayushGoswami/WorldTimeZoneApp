import tkinter as tk
from PIL import Image, ImageTk
from timezonefinder import TimezoneFinder
from datetime import datetime
import pytz

class TimeZoneConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Time Zone Converter")
        
        self.load_map()
        
        self.canvas = tk.Canvas(root, width=self.map_width, height=self.map_height)
        self.canvas.pack()
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.map_img)
        
        self.canvas.bind("<Button-1>", self.on_map_click)
        
        self.timezone_finder = TimezoneFinder()
        
        self.time_label = tk.Label(root, text="", font=("Helvetica", 16))
        self.time_label.pack()

    def load_map(self):
        self.map_image = Image.open("world_map.jpg")  # Ensure this image file is in the same directory
        self.map_width, self.map_height = self.map_image.size
        self.map_img = ImageTk.PhotoImage(self.map_image)

    def on_map_click(self, event):
        x, y = event.x, event.y
        lat, lon = self.convert_xy_to_lat_lon(x, y)
        timezone = self.timezone_finder.timezone_at(lng=lon, lat=lat)
        
        if timezone:
            now = datetime.now(pytz.timezone(timezone))
            gmt_now = datetime.now(pytz.timezone('GMT'))
            gmt_offset = now.utcoffset().total_seconds() / 3600
            
            self.time_label.config(text=f"Current time in {timezone}: {now.strftime('%Y-%m-%d %H:%M:%S')}\nGMT Offset: {gmt_offset} hours")
        else:
            self.time_label.config(text="Could not determine timezone.")
    
    def convert_xy_to_lat_lon(self, x, y):
        # This is a simplified example. You need a proper conversion for real-world use.
        # This function should convert x, y coordinates on the map to latitude and longitude.
        # For the sake of example, let's assume a simple linear mapping:
        lat = 90 - (y / self.map_height) * 180
        lon = (x / self.map_width) * 360 - 180
        return lat, lon

if __name__ == "__main__":
    root = tk.Tk()
    app = TimeZoneConverterApp(root)
    root.mainloop()
