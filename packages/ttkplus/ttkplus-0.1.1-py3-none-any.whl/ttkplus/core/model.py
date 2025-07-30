from typing import Dict, List, Optional

from pydantic import BaseModel


class GridConfigItem(BaseModel):
    size: int  # 宽高
    weight: int  # 权重


class GridConfig(BaseModel):
    colItems: List[GridConfigItem]  # 列配置项
    rowItems: List[GridConfigItem]  # 行配置项


class TabItem(BaseModel):
    index: int
    name: str


class WidgetProps(BaseModel):
    width: Optional[int] = None
    height: Optional[int] = None
    fullWidth: Optional[bool] = None
    fullHeight: Optional[bool] = None
    bootStyle: Optional[str] = None
    state: Optional[str] = None
    widgetStyle: Optional[str] = None  # 组件样式(与bootStyle合并，用短横线隔开)


class TkLayout(WidgetProps):
    gridConfig: Optional[GridConfig] = None
    elements: Dict[str, "TkLayout"] = {}  # 自引用类型
    type: str
    key: str
    text: Optional[str] = None
    sticky_list: List[str] = []
    margin: List[int] = []  # 使用List更符合TS定义
    padding: List[int] = []  # 使用List更符合TS定义
    bootWidgetType: Optional[str] = None  # 新增字段
    tabs: List[TabItem] = []


class TkWindow(BaseModel):
    title: str
    width: int
    height: int
    minWidth: int = 0  # 默认值
    minHeight: int = 0  # 默认值
    theme: str
    isChildWindow: bool = False


class HelperInfo(BaseModel):
    version: str
    website: str
    qqGroup: str
    author: str


class TkHelperModel(BaseModel):
    layout: TkLayout
    window: TkWindow
    helperInfo: HelperInfo


# 解决前向引用问题
TkLayout.model_rebuild()
