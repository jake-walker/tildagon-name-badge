import app
from events.input import BUTTON_TYPES, Buttons


class NameBadge(app.App):
    def __init__(self):
        try:
            with open("name", "r") as f:
                self.name = f.read()
        except:
            self.name = None
        self.button_states = Buttons(self)

    def update(self, delta):
        if self.button_states.get(BUTTON_TYPES["CANCEL"]):
            self.minimise()

    def draw(self, ctx):
        ctx.save()
        ctx.text_align = "center"
        ctx.gray(0).rectangle(-120, -120, 240, 240).fill()
        ctx.rgb(1, 0, 0).rectangle(-120, -120, 240, 100).fill()
        ctx.font_size = 56
        ctx.font = "Arimo Bold"
        ctx.gray(1).move_to(0, -60).text("Hello")
        if self.name is not None:
            ctx.gray(1).move_to(0, 60).text("Jake")

        ctx.font_size = 28
        ctx.font = "Arimo Bold"
        ctx.gray(1).move_to(0, -30).text("my name is")

        if self.name is None:
            ctx.font_size = 20
            ctx.gray(1).move_to(0, 0).text(
                "Set your name by making\n"
                "a file called 'name' in the\n"
                "root of the badge drive"
            )

        ctx.restore()
