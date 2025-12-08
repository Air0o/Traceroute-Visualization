import arcade
from screeninfo import get_monitors

WINDOW_WIDTH = 1440
WINDOW_HEIGHT = 720
for m in get_monitors():
    WINDOW_WIDTH = m.width
    WINDOW_HEIGHT = WINDOW_WIDTH // 2

WINDOW_TITLE = "Traceroute Visualization"

def latlon_to_xy(lat, lon, width, height):
    lat = float(lat)
    lon = float(lon)
    x = (lon + 180) * (width / 360)
    y = (90 - lat) * (height / 180)
    return round(x), round(height - y)


class GameView(arcade.View):
    def __init__(self, hops):
        super().__init__()

        self.background = arcade.load_texture("resources/background.jpg")
        self.background_color = arcade.color.BLACK
        self.hops = hops

        # Zoom and pan
        self.zoom = 1.0
        self.pan_x = 0
        self.pan_y = 0

        # Dragging state
        self.dragging = False

    def on_draw(self):
        self.clear()

        # Background with pan + zoom
        arcade.draw_texture_rect(
            self.background,
            arcade.LBWH(
                self.pan_x, self.pan_y,
                WINDOW_WIDTH * self.zoom,
                WINDOW_HEIGHT * self.zoom
            ),
        )

        self.draw_coordinates()

    def draw_coordinates(self):
        POINT_SIZE = 10
        LINE_WIDTH = 4
        COLOR_POINT = arcade.color.RED
        COLOR_LINE = arcade.color.BLUE
        COLOR_START = arcade.color.GREEN
        COLOR_END = arcade.color.YELLOW

        coords = [
            latlon_to_xy(float(lat), float(lon), WINDOW_WIDTH, WINDOW_HEIGHT)
            for lat, lon in self.hops
        ]

        # Apply zoom + pan
        coords = [(x * self.zoom + self.pan_x, y * self.zoom + self.pan_y) for x, y in coords]

        # Draw lines
        for (x1, y1), (x2, y2) in zip(coords[:-1], coords[1:]):
            arcade.draw_line(x1, y1, x2, y2, COLOR_LINE, LINE_WIDTH)

        # Track how many labels already placed at each coordinate
        label_offsets = {}

        # Draw points + numbers
        for i, (x, y) in enumerate(coords):
            if i == 0:
                color = COLOR_START
            elif i == len(coords) - 1:
                color = COLOR_END
            else:
                color = COLOR_POINT

            arcade.draw_point(x, y, color, POINT_SIZE)

            # If multiple hops share the same position, stagger labels
            count = label_offsets.get((x, y), 0)
            label_offsets[(x, y)] = count + 1

            # Offset each subsequent label by 14 pixels vertically
            offset_y = 6 + count * 14
            arcade.draw_text(
                str(i + 1),
                x + 12, y + offset_y,
                arcade.color.WHITE,
                12,
                anchor_x="left",
                anchor_y="center"
            )



    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.ESCAPE:
            self.window.close()

    # Mouse wheel zoom centered on cursor
    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        old_zoom = self.zoom
        if scroll_y > 0:
            self.zoom *= 1.1
        elif scroll_y < 0:
            self.zoom /= 1.1

        # Adjust pan so that the point under the cursor stays fixed
        scale = self.zoom / old_zoom
        self.pan_x = x - scale * (x - self.pan_x)
        self.pan_y = y - scale * (y - self.pan_y)

    # Mouse dragging for panning
    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.dragging = True
            self.last_mouse_x = x
            self.last_mouse_y = y

    def on_mouse_release(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.dragging = False

    def on_mouse_motion(self, x, y, dx, dy):
        if self.dragging:
            self.pan_x += dx
            self.pan_y += dy


def start_window(hops):
    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE, resizable=True)
    game = GameView(hops)
    window.show_view(game)
    arcade.run()
