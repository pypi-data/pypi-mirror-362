from abc import ABC, abstractmethod

from ttkbootstrap import Frame, Notebook

from ttkplus.core.create_widget import CreateWidget
from ttkplus.core.model import TkLayout, TabItem, GridConfig
from ttkplus.logger import log


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


class RenderAbc(ABC):
    @abstractmethod
    def recursion_create(self, layout_model: TkLayout, parent) -> dict:
        pass


class Render(RenderAbc):
    def __init__(self):
        self.children = dict()

    def recursion_create(self, layout_model: TkLayout, parent) -> dict:
        widgets = dict()
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

            gw = CreateWidget(child, item)
            log.info(f"make: {item.type}")
            widget = gw.make()
            widget.pack(fill='both', anchor='nw', expand=True)

            widgets[item.key] = widget

            frame_list = ['ttk-frame', 'ttk-label-frame', 'ttk-notebook']

            # 处理每个格子中的元素
            if item.type in frame_list:
                log.info(f'渲染容器：{item.type}')
                if len(item.tabs) > 0:
                    render = RenderTabs()
                else:
                    render = Render()
                _widgets = render.recursion_create(item, widget)
                widgets.update(_widgets)
        return widgets


def get_tab_items(elements, index):
    tab_items = {}
    for key, val in elements.items():
        if key.startswith(f"{index}|"):
            tab_items[key] = val

    return tab_items


def sort(item: TabItem):
    return item.index


class RenderTabs(Render):
    def __init__(self):
        super().__init__()

    def recursion_create(self, layout_model: TkLayout, parent) -> dict:
        widgets = dict()
        layout_model.tabs.sort(key=sort)
        tab_count = len(layout_model.tabs)
        for index in range(tab_count):
            tab_items = get_tab_items(layout_model.elements, index)
            tab_frame = Frame(parent)
            if isinstance(parent, Notebook):
                parent.add(tab_frame, text=layout_model.tabs[index].name)

            tab_frame_model = TkLayout(key='tab' + str(index), type='ttk-frame', elements=tab_items,
                                       gridConfig=GridConfig(rowItems=[], colItems=[]))

            render = Render()
            _widgets = render.recursion_create(tab_frame_model, tab_frame)
            widgets.update(_widgets)
        return widgets
