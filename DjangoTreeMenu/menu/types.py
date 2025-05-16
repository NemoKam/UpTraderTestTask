from dataclasses import dataclass, field


@dataclass
class MenuItemInfo:
    id: int
    title: str
    level: int
    is_open: bool = False


@dataclass
class LoadedMenuItem:
    id: int
    title: str
    depth: int
    father_id: int | None


@dataclass
class MenuChildrenInfo:
    children: list[LoadedMenuItem] = field(default_factory=list)
    all_children_cnt: int = 0


@dataclass
class MenuTree:
    current_menu_id: int | None
    tree_menu_items: list[LoadedMenuItem] = field(default_factory=list)


