import tkinter as tk
from PIL import Image, ImageTk
from timezonefinder import TimezoneFinder
from datetime import datetime
import pytz
from geopy.geocoders import Nominatim

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
        self.geolocator = Nominatim(user_agent="timezone_converter_app")

    def load_map(self):
        self.map_image = Image.open("world_map.jpg")  # Ensure this image file is in the same directory
        self.map_width, self.map_height = self.map_image.size
        self.map_img = ImageTk.PhotoImage(self.map_image)

    def on_map_click(self, event):
        x, y = event.x, event.y
        lat, lon = self.convert_xy_to_lat_lon(x, y)
        timezone = self.timezone_finder.timezone_at(lng=lon, lat=lat)
        location = self.geolocator.reverse((lat, lon), exactly_one=True, language="en")
        country = location.raw['address'].get('country', 'Unknown country')

        if timezone:
            now = datetime.now(pytz.timezone(timezone))
            gmt_offset = now.utcoffset().total_seconds() / 3600
            time_info = f"Country: {country}\nTime: {now.strftime('%Y-%m-%d %H:%M:%S')}\nGMT Offset: {gmt_offset} hours"

            self.canvas.delete("time_bubble")
            self.show_time_bubble(x, y, time_info)
            self.highlight_country_boundary(x, y)
        else:
            self.canvas.delete("time_bubble")
            self.canvas.delete("country_boundary")

    def show_time_bubble(self, x, y, text):
        bubble_width = 250
        bubble_height = 70
        bubble_x = x
        bubble_y = y - bubble_height - 10  # Show above the clicked point

        # Draw speech bubble
        self.canvas.create_rectangle(
            bubble_x, bubble_y, bubble_x + bubble_width, bubble_y + bubble_height,
            fill="white", outline="black", tags="time_bubble"
        )
        self.canvas.create_text(
            bubble_x + 10, bubble_y + 10, anchor="nw",
            text=text, tags="time_bubble"
        )

    def highlight_country_boundary(self, x, y):
        # For simplicity, we will draw a fixed-size rectangle around the clicked point
        boundary_margin = 10
        self.canvas.delete("country_boundary")
        self.canvas.create_rectangle(
            x - boundary_margin, y - boundary_margin, x + boundary_margin, y + boundary_margin,
            outline="red", width=2, tags="country_boundary"
        )

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
