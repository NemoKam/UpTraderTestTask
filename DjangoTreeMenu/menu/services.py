from collections import defaultdict
from functools import lru_cache

from menu.models import MenuItem
from menu.types import LoadedMenuItem, MenuChildrenInfo, MenuItemInfo, MenuTree


class MenuService:
    """Service class for managing menu items."""

    def get_menu_items(self, path: str) -> list[MenuItem]:
        """Get the menu items for the given request."""
        menu_names: list[str] = list(path.split("/"))

        # Because menu title is non unique, we need to go through all path.
        # Example: /menu1/menu2/menu3 => menu1, menu2, menu3
        # If url might be like /1/3/2 (ids) or title might be unique, it would be easier
        raw_whereclauses = "p.depth = 0"
        if len(menu_names) > 1:
            raw_whereclauses = " OR ".join([f"p.depth = {depth} AND m.title = '{menu_name}'"
                for depth, menu_name in enumerate(menu_names[1:], start=1)])

        # STEP 1: Get menu all fathers + menu items with empty father_id
        # STEP 2: Get every selected father in step 1 children
        # STEP 3: Union all of them
        # STEP 4: GROUP BY id and ORDER BY depth DESC => first row with depth will be current menu
        get_menu_items_raw_query = f"""
            WITH RECURSIVE parents AS (
                SELECT id, title, father_id, 1 AS depth
                FROM {MenuItem._meta.db_table}
                WHERE father_id IS NULL AND title = '{menu_names[0]}'

                UNION

                SELECT m.id, m.title, m.father_id, depth + 1
                FROM {MenuItem._meta.db_table} m
                JOIN parents p ON m.father_id = p.id
                WHERE {raw_whereclauses}
            ),

            children AS (
                SELECT id, title, father_id, NULL AS depth
                FROM {MenuItem._meta.db_table}
                WHERE father_id IN (SELECT id FROM parents) OR father_id IS NULL
            )

            SELECT id, title, father_id, MAX(depth) AS depth FROM (
                SELECT * FROM parents
                UNION
                SELECT * FROM children
            )
            GROUP BY id
            ORDER BY depth DESC;
            """

        # Yeah! One reqeust to DB, but all menu items will be loaded

        menu_items: list[MenuItem] = list(MenuItem.objects.raw(get_menu_items_raw_query))

        return menu_items

    def get_menu_tree(self, path: str) -> MenuTree:
        """Get the menu tree for the given request."""
        menu_items: defaultdict[int, LoadedMenuItem] = defaultdict(LoadedMenuItem)
        current_menu_id: int | None = None
        for ind, menu_item in enumerate(self.get_menu_items(path)):
            # If there is no items or first menu_item depth is None,
            # that means current menu is default super root.
            if ind == 0 and menu_item.depth is not None:
                current_menu_id: int = menu_item.id

            menu_items[menu_item.id] = LoadedMenuItem(menu_item.id, menu_item.title,
                                                      menu_item.depth, menu_item.father_id)

        tree_menu: list[MenuItemInfo] = [MenuItemInfo(0, "", 0, is_open=False)] * len(menu_items)

        tree_children: defaultdict[int, MenuChildrenInfo] = defaultdict(MenuChildrenInfo)
        tree_roots: list[int] = []


        for menu_item in menu_items.values():
            menu_item_father: LoadedMenuItem | None = None
            menu_item_father_depth: int = 0

            if menu_item.father_id:
                menu_item_father: LoadedMenuItem = menu_items[menu_item.father_id]
            if menu_item_father is not None:
                menu_item_father_depth = menu_item_father.depth

            if menu_items[menu_item.id].depth is None:
                menu_items[menu_item.id].depth = menu_item_father_depth + 1

            if menu_item_father is not None:
                if menu_item_father.id not in tree_children:
                    tree_children[menu_item_father.id] = MenuChildrenInfo()

                tree_children[menu_item_father.id].children.append(menu_items[menu_item.id])
            else:
                tree_roots.append(menu_items[menu_item.id])

        # We will form an array size of menu items, and will form schema for tree in one array.
        # Example:
        #   * grandfather1:
        #       * father1:
        #           * son1
        #           * daughter1 <- active
        #       * father2
        #       * father3
        #   * grandfather2
        # Tree will be converted in list of [level, menu_title, all_children_include_nested_count]
        # 1) level is needed to make indents
        # 2) title is needed to name that menu
        # 3) all_children_include_nested_count is needed to rightfully insert them in tree array.
        # if grandfather1.all_children_include_nested_count = 5 =>
        # grandfather2 will be in tree_menu[1 + 5 + 1]

        # Explanation: 1 - is grandfather by himself, 5 - his children..., 1 - is for grandfather2
        # [(1, grandfather1, 5,), (2, father1, 2,), (3, son1, 0,), (3, daughter1, 0,),
        # (2, father2, 0,), (2, father3, 0), (1, grandfather2, 0)]

        # Memory complexity: ~O(N)
        for menu_item in sorted(menu_items.values(), key=lambda menu_item: -menu_item.depth):
            menu_item_extra_children_cnt = (1 + tree_children[menu_item.id].all_children_cnt)
            tree_children[menu_item.father_id].all_children_cnt += menu_item_extra_children_cnt

        # For easy reaching father index, and calculating self index
        indexes: defaultdict[int, int] = defaultdict(int)
        current_root_index = 0
        # Sorting roots by title
        for root in sorted(tree_roots, key=lambda root: root.title):
            indexes[root.id] = current_root_index
            current_root_index += tree_children[root.id].all_children_cnt + 1

        branches_ids: set[int] = {tree_root.id for tree_root in tree_roots}
        current_level = 1
        while len(branches_ids) > 0:
            next_branches_ids: set[LoadedMenuItem] = set()
            for branch_id in branches_ids:
                branch: LoadedMenuItem = menu_items[branch_id]

                is_open: bool = tree_children[branch.id].all_children_cnt > 0
                branch_index: int = indexes[branch.id]

                tree_menu[branch_index] = MenuItemInfo(branch.id, branch.title,
                                                       current_level, is_open)

                # Sorting MenuItem by title
                for branch_child in sorted(tree_children[branch.id].children,
                                           key=lambda child: child.title):
                    branch_index += 1 # child is next index
                    indexes[branch_child.id] = branch_index
                    # Save space for all nested chidlren
                    branch_index += tree_children[branch_child.id].all_children_cnt

                    next_branches_ids.add(branch_child.id)

            current_level += 1 # Level increases from root to leaves

            branches_ids, next_branches_ids = next_branches_ids, branches_ids

        return MenuTree(current_menu_id, tree_menu)


@lru_cache
def get_menu_service():
    return MenuService()
