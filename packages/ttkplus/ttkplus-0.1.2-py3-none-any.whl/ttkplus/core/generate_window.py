from ttkbootstrap import Style
from ttkbootstrap import Window

from ttkplus.core.model import TkHelperModel
from ttkplus.core.render import Render

GRID_BOX_STYLE = 'grid_box.TFrame'


class GenerateWin:

    def __init__(self, model: TkHelperModel):
        self.root = None
        self.model = model

    def build(self):
        self.root = self.create_window()

        self.create_style()

        Render(self.model.layout, self.root)

        self.root.mainloop()

    def create_window(self):
        win_model = self.model.window
        root = Window(themename=win_model.theme, title=win_model.title, size=(win_model.width, win_model.height))
        root.place_window_center()
        return root

    def create_style(self):
        style = Style()
        style.configure(GRID_BOX_STYLE, bordercolor='purple', borderwidth=1, relief='solid', backgroundcolor="purple")
