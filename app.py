import time

import app
import settings
from app_components import TextDialog, clear_background
from events.input import BUTTON_TYPES, Buttons
from perf_timer import PerfTimer


class NameBadge(app.App):
    name = None

    # colors used for the main name part
    bg_color = (0, 0, 0)
    fg_color = (255, 255, 255)

    # colors used for the 'hello my name is' part
    header_bg_color = (255, 0, 0)
    header_fg_color = (255, 255, 255)

    def __init__(self):
        super().__init__()
        self.button_states = Buttons(self)
        self.name = settings.get("name")

    async def run(self, render_update):
        last_time = time.ticks_ms()
        while True:
            cur_time = time.ticks_ms()
            delta_ticks = time.ticks_diff(cur_time, last_time)
            with PerfTimer(f"Updating {self}"):
                self.update(delta_ticks)
            await render_update()
            last_time = cur_time

            if self.name is None:
                dialog = TextDialog("What is your name?", self)
                self.overlays = [dialog]

                if await dialog.run(render_update):
                    self.name = dialog.text
                    settings.set("name", dialog.text)

                    try:
                        settings.save()
                    except Exception as ex:
                        print("failed to save settings", ex)
                else:
                    self.minimise()

                self.overlays = []

    def update(self, delta):
        if self.button_states.get(BUTTON_TYPES["CANCEL"]):
            # quit the app
            self.minimise()
            self.button_states.clear()
        if self.button_states.get(BUTTON_TYPES["LEFT"]):
            settings.set("name", None)

    def draw(self, ctx):
        clear_background(ctx)

        ctx.text_align = ctx.CENTER

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

        if self.name is None:
            ctx.font = "Arimo Italic"
            ctx.rgb(*self.fg_color).move_to(0, 20).text(
                "Set your name in\nthe settings app!"
            )

        self.draw_overlays(ctx)


__app_export__ = NameBadge
