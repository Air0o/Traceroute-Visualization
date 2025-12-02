import arcade
from screeninfo import get_monitors

WINDOW_WIDTH = 1440
WINDOW_HEIGHT = 720
for m in get_monitors():
    WINDOW_WIDTH = m.width
    WINDOW_HEIGHT = WINDOW_WIDTH//2

WINDOW_TITLE = "Traceroute Visualization"

def latlon_to_xy(lat, lon, width, height):
    lat = float(lat)
    lon = float(lon)
    x = (lon + 180) * (width / 360)
    y = (90 - lat) * (height / 180)
    return round(x), round(height-y)


class GameView(arcade.View):
    def __init__(self, hops):
        super().__init__()

        self.background = arcade.load_texture("resources/background.jpg")

        self.background_color = arcade.color.AMAZON
        self.hops = hops

    def on_resize(self, width, height):
        super().on_resize(width, height)

    def on_draw(self):
        self.clear()

        # Draw the background texture
        arcade.draw_texture_rect(
            self.background,
            arcade.LBWH(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT),
        )

        for i in range(len(self.hops)-1):
            hop1 = self.hops[i]
            x1, y1 = latlon_to_xy(float(hop1[0]), float(hop1[1]), WINDOW_WIDTH, WINDOW_HEIGHT)
            arcade.draw_point(x1, y1, arcade.color.RED, 10)

            hop2 = self.hops[i+1]
            x2, y2 = latlon_to_xy(float(hop2[0]), float(hop2[1]), WINDOW_WIDTH, WINDOW_HEIGHT)

            arcade.draw_line(x1,y1,x2,y2,arcade.color.BLUE,4)
        
        hop = self.hops[-1]
        x, y = latlon_to_xy(float(hop[0]), float(hop[1]), WINDOW_WIDTH, WINDOW_HEIGHT)
        arcade.draw_point(x, y, arcade.color.RED, 10)

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.ESCAPE:
            self.window.close()


def start_window(hops):
    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE, resizable=True)

    game = GameView(hops)
    window.show_view(game)

    arcade.run()

