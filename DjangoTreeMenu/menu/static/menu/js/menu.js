let menu_item_blocks = document.querySelectorAll(".menu_item_block");


const BASE_MENU_URL = location.origin + "/menu/"; 
const INDENT_PADDING_LEFT = 20;

let prev_menu_level = 0;
let current_url = "";
menu_item_blocks.forEach((menu_item_block) => {
    let menu_level = parseInt(menu_item_block.getAttribute("data-menu-level"));
    let menu_url = encodeURIComponent(menu_item_block.getAttribute("data-menu-url"));
    menu_item_block.querySelector(".menu_item_indent").textContent = "--".repeat(menu_level * 2) + " ";

    // Skip form
    console.log(menu_url);
    if (menu_url !== "null") {
        if (menu_level > prev_menu_level) {
            current_url += menu_url;
        } else {
            splitted_url = current_url.split("/").filter(segment => segment !== "");
            let current_menu_url = menu_url;
            let before_menu_url = splitted_url.slice(0, splitted_url.length - (prev_menu_level - menu_level + 1)).join("/");

            if (before_menu_url !== "")
                before_menu_url += "/"

            current_url = before_menu_url + current_menu_url;
        }

        if (current_url !== "")
            current_url += "/"

        menu_item_url = BASE_MENU_URL + current_url;

        if (encodeURIComponent(menu_item_url) == encodeURIComponent(location.href))
            menu_item_block.classList.add("active_menu_block");

        menu_item_block.querySelector(".menu_item_title").href = menu_item_url;
        prev_menu_level = menu_level;
    }
})
