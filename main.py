import app
from app_components import TextDialog, clear_background
from events.input import BUTTON_TYPES, Buttons


class NameBadge(app.App):
    bg_color = (0, 0, 0)
    fg_color = (255, 255, 255)
    header_bg_color = (255, 0, 0)
    header_fg_color = (255, 255, 255)

    def __init__(self):
        super().__init__()
        self.load_name()
        self.button_states = Buttons(self)

    def load_name(self):
        try:
            with open("name", "r") as f:
                self.name = f.read()
        except:
            self.name = None

    def save_name(self):
        with open("name", "w") as f:
            f.write(self.name)

    async def run(self, render_update):
        if self.name is None:
            dialog = TextDialog("What is your name?", self)
            self.overlays = [dialog]

            if await dialog.run(render_update):
                self.name = dialog.text
                self.save_name()
            else:
                self.minimise()

            self.overlays = []

        await render_update()

    def update(self, delta):
        if self.button_states.get(BUTTON_TYPES["CANCEL"]):
            self.minimise()

    def draw(self, ctx):
        clear_background(ctx)

        ctx.save()
        ctx.text_align = "center"

        # draw backgrounds
        ctx.rgb(*self.bg_color).rectangle(-120, -120, 240, 240).fill()
        ctx.rgb(*self.header_bg_color).rectangle(-120, -120, 240, 100).fill()

        ctx.font_size = 56
        ctx.font = "Arimo Bold"
        ctx.rgb(*self.header_fg_color).move_to(0, -60).text("Hello")
        if self.name is not None:
            ctx.rgb(*self.fg_color).move_to(0, 60).text(self.name)

        ctx.font_size = 28
        ctx.font = "Arimo Bold"
        ctx.rgb(*self.header_fg_color).move_to(0, -30).text("my name is")

        ctx.restore()

        self.draw_overlays(ctx)