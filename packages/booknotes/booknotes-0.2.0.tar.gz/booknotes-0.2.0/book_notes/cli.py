# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
#
# © 2025 Eren Öğrül - termapp@pm.me
import curses
import json
import os
import textwrap
DATA_FILE = "books.json"
FOCUS_BOOKS = 0
FOCUS_TAGS = 1
SORT_ALPHABETICAL = 0
SORT_LAST_EDITED = 1
import time
def load_data():
    if not os.path.exists(DATA_FILE):
        return {"books": {}}
    with open(DATA_FILE, "r") as f:
        data = json.load(f)
    for title, value in list(data.get("books", {}).items()):
        if isinstance(value, str):
            data["books"][title] = {"tags": [], "notes": value}
    return data
def save_data(data):
    for book in data["books"].values():
        if "_last_edited" not in book:
            book["_last_edited"] = time.time()
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)
def get_all_tags(data):
    tags = set()
    for b in data["books"].values():
        tags.update(b.get("tags", []))
    return sorted(tags)
def book_selector(stdscr, data):
    stdscr.timeout(50)
    for book in data["books"].values():
        if "_last_edited" not in book:
            book["_last_edited"] = time.time()
    curses.curs_set(0)
    selected_book = 0
    selected_tag_idx = 0
    search_query = ""
    is_searching = False
    focus = FOCUS_BOOKS
    active_tag_filter = None
    sort_method = SORT_LAST_EDITED  # Default to last edited sort
    while True:
        stdscr.clear()
        max_y, max_x = stdscr.getmaxyx()
        mid_x = max_x // 2
        # Get all book titles
        all_books = list(data["books"].keys())
        # Apply search query filter
        if search_query.strip():
            all_books = [b for b in all_books if search_query.lower() in b.lower() or
                         any(search_query.lower() in tag.lower() for tag in data["books"][b].get("tags", []))]
        # Apply tag filter
        if active_tag_filter:
            all_books = [b for b in all_books if active_tag_filter in data["books"][b].get("tags", [])]
        # Sort the filtered books based on the current sort method
        if sort_method == SORT_ALPHABETICAL:
            books = sorted(all_books, key=lambda title: title.lower())
        else:  # SORT_LAST_EDITED
            books = sorted(all_books,
                           key=lambda title: data["books"][title].get("_last_edited", 0),
                           reverse=True)
        tags = get_all_tags(data)
        # Header
        stdscr.addstr(0, 0, "Book Note Repository".center(max_x), curses.A_BOLD)
        # Update help line to include sorting toggle
        help_line = "[n] New  [Enter] Open  [d] Delete  [e] Edit Tags  [/] Search  [r] Reset  [s] Sort  [Tab] Switch  [q] Quit"
        stdscr.addstr(1, 0, help_line.center(max_x))
        # Book list header with current sort method
        if sort_method == SORT_ALPHABETICAL:
            sort_label = "A-Z"
        else:
            sort_label = "Last Edited"
        stdscr.addstr(2, 2, f"Books ({sort_label}):", curses.A_UNDERLINE)
        for idx, book in enumerate(books):
            if 3 + idx >= max_y - 4:
                break
            attr = curses.A_REVERSE if focus == FOCUS_BOOKS and idx == selected_book else curses.A_NORMAL
            stdscr.addstr(3 + idx, 2, book[:mid_x - 4], attr)
        # Tag line (horizontal)
        stdscr.addstr(max_y - 3, 2, "Tags:", curses.A_UNDERLINE)
        tag_line = ""
        positions = []
        x_cursor = 8
        for idx, tag in enumerate(tags):
            tag_display = f"[{tag}] "
            attr = curses.A_REVERSE if focus == FOCUS_TAGS and idx == selected_tag_idx else curses.A_NORMAL
            stdscr.addstr(max_y - 2, x_cursor, tag_display.strip(), attr)
            positions.append((x_cursor, len(tag_display.strip())))
            x_cursor += len(tag_display)
        # Footer
        footer = f"{len(books)} book(s)"
        if search_query:
            footer = f"Search: {search_query} | {footer}"
        if active_tag_filter:
            footer += f" | Tag: {active_tag_filter}"
        stdscr.addstr(max_y - 1, 0, footer[:max_x - 1], curses.A_DIM)
        stdscr.refresh()
        k = stdscr.getch()
        if is_searching:
            if k in (10, 13):
                is_searching = False
            elif k in (27,):
                is_searching = False
                search_query = ""
            elif k in (8, 127):
                search_query = search_query[:-1]
            elif 0 <= k < 256:
                search_query += chr(k)
            continue
        if k == ord('\t'):
            focus = FOCUS_TAGS if focus == FOCUS_BOOKS else FOCUS_BOOKS
        elif k in [curses.KEY_UP, ord('k')]:
            if focus == FOCUS_BOOKS:
                selected_book = max(0, selected_book - 1)
        elif k in [curses.KEY_DOWN, ord('j')]:
            if focus == FOCUS_BOOKS:
                selected_book = min(len(books) - 1, selected_book + 1)
        elif k in [curses.KEY_LEFT]:
            if focus == FOCUS_TAGS:
                selected_tag_idx = max(0, selected_tag_idx - 1)
        elif k in [curses.KEY_RIGHT]:
            if focus == FOCUS_TAGS:
                selected_tag_idx = min(len(tags) - 1, selected_tag_idx + 1)
        elif k == ord('n'):
            new_book(stdscr, data)
        elif k == ord('d') and books:
            delete_book(stdscr, data, books[selected_book])
            selected_book = max(0, selected_book - 1)
        elif k == ord('e') and books:
            edit_tags(stdscr, data, books[selected_book])
        elif k == ord('s'):  # Toggle sorting method
            sort_method = SORT_ALPHABETICAL if sort_method == SORT_LAST_EDITED else SORT_LAST_EDITED
            selected_book = 0  # Reset selection to top after sort change
        elif k == ord('/'):
            is_searching = True
            search_query = ""
            active_tag_filter = None
            selected_book = 0
        elif k == ord('r'):
            active_tag_filter = None
            search_query = ""
            selected_book = 0
        elif k == 10:
            if focus == FOCUS_BOOKS and books:
                note_editor(stdscr, data, books[selected_book])
            elif focus == FOCUS_TAGS and tags:
                active_tag_filter = tags[selected_tag_idx]
                selected_book = 0
        elif k == ord('q'):
            break
def new_book(stdscr, data):
    curses.echo()
    stdscr.timeout(-1)  # Set to blocking mode to wait for input
    stdscr.clear()
    stdscr.addstr(0, 0, "Enter new book title: ")
    name = stdscr.getstr().decode().strip()
    stdscr.addstr(2, 0, "Enter tags (comma-separated): ")
    tags_input = stdscr.getstr().decode().strip()
    tags = [t.strip() for t in tags_input.split(",") if t.strip()]
    if name and name not in data["books"]:
        data["books"][name] = {"tags": tags, "notes": "", "_last_edited": time.time()}
        save_data(data)
        stdscr.clear()
        stdscr.refresh()
        curses.noecho()
        note_editor(stdscr, data, name)
        # note_editor sets its own timeout, so no need to restore here
    else:
        curses.noecho()
        stdscr.clear()
        stdscr.refresh()
        # Restore the timeout to 50 before returning to the main loop
        stdscr.timeout(50)
def edit_tags(stdscr, data, book_title):
    curses.echo()
    stdscr.clear()
    current_tags = data["books"][book_title].get("tags", [])
    stdscr.addstr(0, 0, f"Editing tags for '{book_title}'")
    stdscr.addstr(2, 0, f"Current tags: {', '.join(current_tags)}")
    stdscr.addstr(4, 0, "Enter new tags (comma-separated): ")
    tags_input = stdscr.getstr().decode().strip()
    new_tags = [t.strip() for t in tags_input.split(",") if t.strip()]
    data["books"][book_title]["tags"] = new_tags
    data["books"][book_title]["_last_edited"] = time.time()
    save_data(data)
    curses.noecho()
def delete_book(stdscr, data, book_title):
    stdscr.clear()
    stdscr.addstr(0, 0, f"Delete '{book_title}'? (y/n): ")
    # Set timeout to -1 to make getch() blocking
    stdscr.timeout(-1)
    key = stdscr.getch()
    if key in [ord('y'), ord('Y')]:
        del data["books"][book_title]
        save_data(data)
    # Restore the timeout to 50
    stdscr.timeout(50)
def note_editor(stdscr, data, book_title):
    stdscr.timeout(50)  # Note: This was already present
    curses.curs_set(1)
    note = data["books"][book_title].get("notes", "")
    lines = note.split("\n") if note else [""]
    row = len(lines) - 1
    col = len(lines[-1])
    saved_msg_timer = 0
    while True:
        stdscr.clear()
        max_y, max_x = stdscr.getmaxyx()
        stdscr.addstr(0, 0, f"Notes for: {book_title}".center(max_x), curses.A_BOLD)
        stdscr.addstr(1, 0, "[Ctrl+S] Save  [q] Back".center(max_x))
        display_lines = []
        for line in lines:
            wrapped = textwrap.wrap(line, width=max_x - 4) or [""]
            display_lines.extend(wrapped)
        for idx, dline in enumerate(display_lines):
            if idx + 3 < max_y - 2:
                stdscr.addstr(idx + 3, 2, dline)
        if saved_msg_timer > 0:
            stdscr.addstr(max_y - 1, 0, "[Saved]".center(max_x - 1), curses.A_DIM)
            saved_msg_timer -= 1
        else:
            stdscr.addstr(max_y - 1, 0, " " * (max_x - 1))
        cursor_y, cursor_x = 0, 0
        count = 0
        for i in range(row):
            count += len(textwrap.wrap(lines[i], width=max_x - 4) or [""])
        sub_line_wrap = textwrap.wrap(lines[row][:col], width=max_x - 4) or [""]
        cursor_y = 3 + count + len(sub_line_wrap) - 1
        cursor_x = len(sub_line_wrap[-1]) + 2
        if cursor_y < max_y - 1:
            stdscr.move(cursor_y, min(cursor_x, max_x - 1))
        stdscr.refresh()
        ch = stdscr.getch()
        if ch in (3, 113):
            break
        elif ch == 19:
            data["books"][book_title]["notes"] = "\n".join(lines)
            data["books"][book_title]["_last_edited"] = time.time()
            save_data(data)
            saved_msg_timer = 30
        elif ch in (10, 13):
            lines.insert(row + 1, "")
            row += 1
            col = 0
        elif ch in (8, 127, curses.KEY_BACKSPACE):
            if col > 0:
                lines[row] = lines[row][:col - 1] + lines[row][col:]
                col -= 1
            elif row > 0:
                col = len(lines[row - 1])
                lines[row - 1] += lines[row]
                del lines[row]
                row -= 1
        elif ch == curses.KEY_UP:
            if row > 0:
                row -= 1
                col = min(col, len(lines[row]))
        elif ch == curses.KEY_DOWN:
            if row < len(lines) - 1:
                row += 1
                col = min(col, len(lines[row]))
        elif ch == curses.KEY_LEFT:
            if col > 0:
                col -= 1
            elif row > 0:
                row -= 1
                col = len(lines[row])
        elif ch == curses.KEY_RIGHT:
            if col < len(lines[row]):
                col += 1
            elif row < len(lines) - 1:
                row += 1
                col = 0
        elif 0 <= ch < 256:
            lines[row] = lines[row][:col] + chr(ch) + lines[row][col:]
            col += 1
def main(stdscr):
    data = load_data()
    book_selector(stdscr, data)
def run():
    curses.wrapper(main)
if __name__ == "__main__":
    run()
