from tkinter.ttk import Notebook

from ttkbootstrap import Frame

from ttkplus.core.generate_widgets import GenerateWidgets
from ttkplus.logger import log
from ttkplus.core.model import TkLayout, TabItem, GridConfig


def parse_pos(pos):
    try:
        tab_index = None
        # 检查是否含 '|'，并解析 tab_index
        if '|' in pos:
            tab_part, pos = pos.split('|', 1)  # 只分割第一个 '|'
            tab_index = int(tab_part.strip())

        # 分割坐标部分
        parts = pos.split('x')
        if len(parts) != 2:
            raise ValueError(f"坐标格式不正确，应为 '横坐标x纵坐标'，但输入是 '{pos}'")

        x = int(parts[0].strip())
        y = int(parts[1].strip())

        return tab_index, x, y

    except ValueError as e:
        log.error(f"解析坐标 '{pos}' 失败: {e}")
        raise


class Render:
    def __init__(self, layout_model: TkLayout, parent):
        self.layout_model = layout_model
        self.parent = parent
        self.children = dict()

        self.create_frame(self.layout_model, self.parent)

    def create_frame(self, layout_model: TkLayout, parent):
        frame = Frame(parent)
        frame.pack(fill='both', expand=True)

        row = len(layout_model.gridConfig.rowItems)
        col = len(layout_model.gridConfig.colItems)
        row_items = layout_model.gridConfig.rowItems
        col_items = layout_model.gridConfig.colItems

        # frame.columnconfigure(1, weight=1)
        #
        # frame.rowconfigure(1, weight=1)
        # frame.rowconfigure(2, weight=1)
        # frame.rowconfigure(3, weight=1)

        # 设置所有行的权重
        for row_index in range(1, row + 1):
            log.info(f"设置第{row_index}行的权重")
            frame.rowconfigure(row_index, weight=1)
        # 设置所有列的权重
        for col_index in range(1, col + 1):
            log.info(f"设置第{col_index}列的权重")
            frame.columnconfigure(col_index, weight=1)

        # 生成边框支撑
        for ri in range(0, row + 1):
            for ci in range(0, col + 1):
                if ci == 0 and ri == 0:
                    log.info('0x0')
                elif ri == 0:
                    grid_item = col_items[ci - 1]
                    item = Frame(frame, height=0, width=grid_item.size)
                    item.grid(column=ci, row=0)
                    log.info(f"设置第{ci}列宽度:  {grid_item.size}")
                elif ci == 0:
                    grid_item = row_items[ri - 1]
                    item = Frame(frame, height=grid_item.size, width=0)
                    item.grid(column=0, row=ri)
                    log.info(f"设置第{ri}行高度:  {grid_item.size}")
                else:
                    continue

        # 创建合并

        # 生成包裹元素的格子
        for _key, item in layout_model.elements.items():
            # 检查key 是否缓存
            if _key not in self.children:
                # 组件的宽高设置在 Frame 上，内部元素pack到Frame
                child = Frame(frame, style='grid_box.TFrame', width=item.width, height=item.height)
                self.children[_key] = child
                _, row, col = parse_pos(_key)
                child.grid(row=row, column=col)
                # 根据配置朝向设置
                if item.sticky_list:
                    sticky = "".join(item.sticky_list)
                    if sticky:
                        child.grid(sticky=sticky)
            else:
                child = self.children[_key]

            gw = GenerateWidgets(child, item)
            log.info(f"make: {item.type}")
            widget = gw.make()
            widget.pack(fill='both', anchor='nw', expand=True)

            frame_list = ['ttk-frame', 'ttk-label-frame', 'ttk-notebook']

            # 处理每个格子中的元素
            if item.type in frame_list:
                log.info(f'渲染容器：{item.type}')
                if len(item.tabs) > 0:
                    RenderTabs(item, widget)
                else:
                    Render(item, widget)


class RenderTabs(Render):
    def __init__(self, layout_model: TkLayout, parent):
        self.tab_count = len(layout_model.tabs)
        super().__init__(layout_model, parent)

    def __get_tab_items(self, index):
        tab_items = {}
        for key, val in self.layout_model.elements.items():
            if key.startswith(f"{index}|"):
                tab_items[key] = val

        return tab_items

    def __sort(self, _item: TabItem):
        return _item.index

    def create_frame(self, layout_model: TkLayout, parent):
        self.layout_model.tabs.sort(key=self.__sort)
        for index in range(self.tab_count):
            tab_items = self.__get_tab_items(index)
            tab_frame = Frame(self.parent)
            if isinstance(self.parent, Notebook):
                self.parent.add(tab_frame, text=self.layout_model.tabs[index].name)

            tab_frame_model = TkLayout(key='tab' + str(index), type='ttk-frame', elements=tab_items,
                                       gridConfig=GridConfig(rowItems=[], colItems=[]))
            Render(tab_frame_model, tab_frame)
