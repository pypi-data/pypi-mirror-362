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
import os
import re
import time
import threading

class MarkdownEditor:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.filename = None
        self.backup_filename = None
        self.content = []
        self.cursor_y = 0  # logical line index
        self.cursor_x = 0  # position within logical line
        self.search_query = ""
        self.search_matches = []
        self.search_index = 0
        self.running = True
        self.visual_lines = []  # Stores wrapped visual lines
        self.line_map = []      # Mapping from visual line to (logical line, start_pos, end_pos)

    def calculate_visual_lines(self):
        """Calculate the visual lines with wrapping based on current terminal width."""
        self.visual_lines = []
        self.line_map = []

        h, w = self.stdscr.getmaxyx()
        max_width = w if w > 0 else 80  # Default width if we can't get terminal width

        actual_width = max_width - 1  # Leave a little margin

        for logical_line_idx, logical_line in enumerate(self.content):
            start_pos = 0
            line_length = len(logical_line)

            while start_pos < line_length:
                end_pos = min(start_pos + actual_width, line_length)
                if end_pos < line_length:
                    last_space = logical_line.rfind(' ', start_pos, end_pos)
                    if last_space > start_pos:
                        end_pos = last_space

                visual_line = logical_line[start_pos:end_pos]
                self.visual_lines.append(visual_line)
                self.line_map.append((logical_line_idx, start_pos, end_pos))
                start_pos = end_pos

                if start_pos < line_length and logical_line[start_pos].isspace():
                    while start_pos < line_length and logical_line[start_pos].isspace():
                        start_pos += 1

        if not self.visual_lines and not self.content:
            self.visual_lines.append("")
            self.line_map.append((0, 0, 0))

    def logical_to_visual_pos(self, logical_line_idx, logical_pos):
        """Convert logical position to visual line and x position."""
        if not self.line_map:
            self.calculate_visual_lines()

        if logical_line_idx < 0 or logical_line_idx >= len(self.content):
            return None, None

        for visual_line_idx, (line_idx, start_pos, end_pos) in enumerate(self.line_map):
            if line_idx == logical_line_idx and start_pos <= logical_pos < end_pos:
                visual_x = logical_pos - start_pos
                return visual_line_idx, visual_x

        last_visual_line_idx = None
        for i in range(len(self.line_map)-1, -1, -1):
            line_idx, start_pos, end_pos = self.line_map[i]
            if line_idx == logical_line_idx:
                if logical_pos >= end_pos:
                    last_visual_line_idx = i
                else:
                    return i, logical_pos - start_pos

        if last_visual_line_idx is not None:
            return last_visual_line_idx, len(self.visual_lines[last_visual_line_idx])

        for visual_line_idx, (line_idx, start_pos, end_pos) in enumerate(self.line_map):
            if line_idx == logical_line_idx:
                return visual_line_idx, 0

        if self.visual_lines:
            return 0, 0
        return None, None

    def visual_to_logical_pos(self, visual_line_idx, visual_x):
        """Convert visual position to logical line and position."""
        if visual_line_idx < 0 or visual_line_idx >= len(self.line_map):
            return None, None

        line_idx, start_pos, end_pos = self.line_map[visual_line_idx]
        logical_pos = min(start_pos + visual_x, end_pos)
        return line_idx, logical_pos

    def prompt_filename(self):
        curses.echo()
        self.stdscr.addstr(0, 0, "Enter filename to create: ")
        self.filename = self.stdscr.getstr(0, 23, 60).decode("utf-8")
        curses.noecho()

        if not self.filename:
            self.filename = "untitled.md"

        self.backup_filename = f"{self.filename}.bak"
        self.content = ['']

    def open_file(self, filename=None):
        """Open a file for editing."""
        if not self.prompt_save_if_needed():
            return False

        if filename is None:
            curses.echo()
            self.stdscr.addstr(0, 0, "Enter filename to open: ")
            filename = self.stdscr.getstr(0, 22, 60).decode("utf-8")
            curses.noecho()

        if not filename:
            return False

        if os.path.exists(filename):
            try:
                with open(filename, 'r') as f:
                    content = f.read()
                    self.content = content.splitlines()
                    if not self.content:
                        self.content = ['']

                self.filename = filename
                self.backup_filename = f"{self.filename}.bak"
                self.show_flash(f"Opened: {filename}")
                return True
            except Exception as e:
                self.show_flash(f"Error opening file: {str(e)}")
                return False
        else:
            curses.echo()
            self.stdscr.addstr(0, 0, f"File '{filename}' doesn't exist. Create new? (y/n): ")
            choice = self.stdscr.getstr(0, len(f"File '{filename}' doesn't exist. Create new? (y/n): "), 1).decode("utf-8").lower()
            curses.noecho()

            if choice == 'y':
                self.filename = filename
                self.backup_filename = f"{self.filename}.bak"
                self.content = ['']
                self.show_flash(f"Created new file: {filename}")
                return True
            else:
                self.show_flash("Operation canceled")
                return False

    def prompt_save_if_needed(self):
        """Prompt to save if there are unsaved changes. Returns True if should continue, False if canceled."""
        if self.file_modified():
            h, w = self.stdscr.getmaxyx()
            self.stdscr.addstr(h//2, w//2 - 20, "File has unsaved changes. Save before continuing? (y/n/cancel): ")
            curses.echo()
            try:
                self.stdscr.move(h//2, w//2 + 40)
                choice = self.stdscr.getstr().decode("utf-8").lower()
                curses.noecho()

                if choice == 'y':
                    return self.save_file()
                elif choice == 'n':
                    return True
                else:
                    return False
            except:
                curses.noecho()
                return False
        return True

    def file_modified(self):
        """Check if the current file has unsaved changes."""
        if not self.filename:
            return len(self.content) > 1 or (len(self.content) == 1 and self.content[0] != '')

        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as f:
                    saved_content = f.read()
                    current_content = "\n".join(self.content)
                    return saved_content != current_content
            except:
                return True
        else:
            return len(self.content) > 1 or (len(self.content) == 1 and self.content[0] != '')

    def startup_prompt(self):
        """Prompt user with options at startup."""
        options = [
            "1. Create new file",
            "2. Open existing file",
            "3. Continue last file (if available)"
        ]

        last_file = None
        config_file = os.path.expanduser("~/.md_editor_config")
        try:
            if os.path.exists(config_file):
                with open(config_file, 'r') as f:
                    last_file = f.read().strip()
                    if last_file and not os.path.exists(last_file):
                        last_file = None
        except Exception:
            pass

        self.stdscr.clear()
        h, w = self.stdscr.getmaxyx()

        for i, option in enumerate(options):
            y = h//2 - 2 + i
            if i == 2 and not last_file:
                option_text = "3. Continue last file (none available)"
            else:
                option_text = option
            self.stdscr.addstr(y, w//2 - len(option_text)//2, option_text)

        self.stdscr.addstr(h//2 + 2, w//2 - 10, "Enter your choice (1-3): ")
        curses.echo()
        self.stdscr.refresh()

        try:
            self.stdscr.move(h//2 + 2, w//2 + 15)
            choice = self.stdscr.getstr().decode("utf-8")
            curses.noecho()
        except:
            curses.noecho()
            choice = ""

        if choice == '1':
            self.prompt_filename()
        elif choice == '2':
            self.open_file()
        elif choice == '3' and last_file:
            if self.open_file(last_file):
                self.show_flash(f"Continued editing: {last_file}")
            else:
                self.show_flash(f"Could not open previous file: {last_file}")
                self.prompt_filename()
        else:
            self.prompt_filename()

    def get_file_status(self):
        """Return a string indicating the file status."""
        if not self.filename:
            return "New File"

        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as f:
                    saved_content = f.read()
                    current_content = "\n".join(self.content)
                    if saved_content == current_content:
                        return os.path.basename(self.filename)
                    else:
                        return f"{os.path.basename(self.filename)} [modified]"
            except:
                return os.path.basename(self.filename) + " [error reading]"
        else:
            return os.path.basename(self.filename) + " [new]"

    def save_file(self, prompt_for_filename=True):
        """Save the current file, optionally prompting for filename if not set."""
        if not self.filename and prompt_for_filename:
            curses.echo()
            self.stdscr.addstr(0, 0, "Enter filename to save: ")
            filename = self.stdscr.getstr(0, 22, 60).decode("utf-8")
            curses.noecho()

            if not filename:
                return False

            self.filename = filename
            self.backup_filename = f"{self.filename}.bak"

        try:
            if not self.content:
                self.content = ['']

            with open(self.filename, 'w') as f:
                f.write("\n".join(self.content))

            config_file = os.path.expanduser("~/.md_editor_config")
            try:
                with open(config_file, 'w') as f:
                    f.write(self.filename)
            except Exception:
                pass

            self.show_flash(f"Saved: {self.filename}")
            return True
        except Exception as e:
            self.show_flash(f"Error saving: {str(e)}")
            return False

    def save_file_and_exit(self):
        """Save file and exit, prompting for filename if needed."""
        if not self.filename:
            if not self.save_file():
                self.running = False
                return

        if self.save_file(prompt_for_filename=False):
            self.running = False
        else:
            self.running = False

    def auto_save(self):
        while self.running:
            time.sleep(30)
            if self.backup_filename and self.filename:
                try:
                    with open(self.backup_filename, 'w') as f:
                        content_string = "\n".join(self.content)
                        f.write(content_string)
                    self.show_flash("Auto-saved")
                except Exception:
                    pass

    def prompt_search(self):
        curses.echo()
        h, w = self.stdscr.getmaxyx()
        self.stdscr.addstr(h - 2, 0, "Search: ")
        self.stdscr.clrtoeol()
        self.search_query = self.stdscr.getstr(h - 2, 8, 60).decode("utf-8").lower()
        curses.noecho()
        self.find_all_matches()
        self.jump_to_match(0)

    def find_all_matches(self):
        self.search_matches = []
        self.search_index = 0
        if not self.search_query:
            return
        for i, line in enumerate(self.content):
            lower_line = line.lower()
            start = 0
            while (pos := lower_line.find(self.search_query, start)) != -1:
                self.search_matches.append((i, pos))
                start = pos + len(self.search_query)

    def jump_to_match(self, index):
        if not self.search_matches:
            return
        self.search_index = index % len(self.search_matches)
        y, x = self.search_matches[self.search_index]
        self.cursor_y = y
        self.cursor_x = x

    def next_match(self):
        if self.search_matches:
            self.jump_to_match(self.search_index + 1)

    def prev_match(self):
        if self.search_matches:
            self.jump_to_match(self.search_index - 1)

    def run(self):
        self.startup_prompt()

        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(1, curses.COLOR_CYAN, -1)   # Markdown syntax
        curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_YELLOW)  # Search highlight
        curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_BLUE)  # Header bar

        threading.Thread(target=self.auto_save, daemon=True).start()
        self.stdscr.clear()

        while self.running:
            self.render()
            key = self.stdscr.getch()

            if key == 27:  # ESC to quit
                if self.file_modified():
                    h, w = self.stdscr.getmaxyx()
                    self.stdscr.addstr(h//2, w//2 - 20, "File has unsaved changes. Save before quitting? (y/n/cancel): ")
                    curses.echo()
                    try:
                        self.stdscr.move(h//2, w//2 + 40)
                        choice = self.stdscr.getstr().decode("utf-8").lower()
                        curses.noecho()

                        if choice == 'y':
                            self.save_file_and_exit()
                        elif choice == 'n':
                            self.running = False
                    except:
                        curses.noecho()
                        continue
                else:
                    self.running = False
            elif key == curses.KEY_BACKSPACE or key == 127:
                self.backspace()
            elif key == curses.KEY_ENTER or key in [10, 13]:
                self.newline()
            elif key == curses.KEY_UP:
                current_visual_line, current_visual_x = self.logical_to_visual_pos(self.cursor_y, self.cursor_x)
                if current_visual_line is not None:
                    new_visual_line = max(0, current_visual_line - 1)
                    if new_visual_line < current_visual_line:
                        line_idx, logical_pos = self.visual_to_logical_pos(new_visual_line, current_visual_x)
                        if line_idx is not None:
                            line_length = len(self.content[line_idx])
                            if logical_pos > line_length:
                                logical_pos = line_length
                            self.cursor_y = line_idx
                            self.cursor_x = logical_pos
            elif key == curses.KEY_DOWN:
                current_visual_line, current_visual_x = self.logical_to_visual_pos(self.cursor_y, self.cursor_x)
                if current_visual_line is not None:
                    new_visual_line = min(len(self.visual_lines) - 1, current_visual_line + 1)
                    if new_visual_line > current_visual_line:
                        line_idx, logical_pos = self.visual_to_logical_pos(new_visual_line, current_visual_x)
                        if line_idx is not None:
                            line_length = len(self.content[line_idx])
                            if logical_pos > line_length:
                                logical_pos = line_length
                            self.cursor_y = line_idx
                            self.cursor_x = logical_pos
            elif key == curses.KEY_LEFT:
                if self.cursor_x > 0:
                    self.cursor_x -= 1
                elif self.cursor_y > 0:
                    self.cursor_y -= 1
                    self.cursor_x = len(self.content[self.cursor_y])
            elif key == curses.KEY_RIGHT:
                current_line_length = len(self.content[self.cursor_y])
                if self.cursor_x < current_line_length:
                    self.cursor_x += 1
                elif self.cursor_y < len(self.content) - 1:
                    self.cursor_y += 1
                    self.cursor_x = 0
            elif key == 6:  # Ctrl+F to search
                self.prompt_search()
            elif key == 14:  # Ctrl+N for next match
                self.next_match()
            elif key == 16:  # Ctrl+P for previous match
                self.prev_match()
            elif key == 15:  # Ctrl+O to open file
                self.open_file()
                self.cursor_y = 0
                self.cursor_x = 0
            elif key == 4:  # Ctrl+D for "save and exit"
                self.save_file_and_exit()
                break
            elif 0 <= key < 256:
                self.insert_char(chr(key))

    def render(self):
        self.calculate_visual_lines()
        h, w = self.stdscr.getmaxyx()
        total_chars = sum(len(line) for line in self.content)
        self.stdscr.clear()

        # Header bar
        header_text = f" {self.get_file_status()} "
        header_display = header_text[:w - 1].ljust(w - 1)
        self.stdscr.attron(curses.color_pair(4))
        self.stdscr.addstr(0, 0, header_display)
        self.stdscr.attroff(curses.color_pair(4))

        # Display visual lines
        max_content_lines = h - 2
        for visual_line_idx in range(min(len(self.visual_lines), max_content_lines)):
            line_y = visual_line_idx + 1
            if visual_line_idx < len(self.line_map):
                logical_line_idx, start_pos, end_pos = self.line_map[visual_line_idx]
                if logical_line_idx < len(self.content):
                    full_logical_line = self.content[logical_line_idx]
                    self.render_line(line_y, full_logical_line, h, w, visual_line_idx, start_pos, end_pos)

        # Footer bar
        footer_text = f"Ctrl+O: Open    Ctrl+D: Save & Exit    Ctrl+F: Search    Ctrl+N/P: Next/Prev    Esc: Exit    ↑↓←→: Navigate    Chars: {total_chars}"
        footer_display = footer_text[:w - 1].ljust(w - 1)
        self.stdscr.attron(curses.color_pair(4))
        self.stdscr.addstr(h - 1, 0, footer_display)
        self.stdscr.attroff(curses.color_pair(4))

        visual_line_idx, visual_x = self.logical_to_visual_pos(self.cursor_y, self.cursor_x)
        if visual_line_idx is not None and 0 <= visual_line_idx < len(self.visual_lines):
            cursor_y = visual_line_idx + 1
            cursor_x = min(visual_x, w - 1) if visual_x is not None else 0
            if 0 <= cursor_y < h - 1 and 0 <= cursor_x < w:
                self.stdscr.move(cursor_y, cursor_x)

        self.stdscr.refresh()

    def render_line(self, y, full_logical_line, h, w, visual_line_idx, start_pos, end_pos):
        if visual_line_idx >= len(self.visual_lines):
            return

        visual_line = self.visual_lines[visual_line_idx]
        x = 0
        markdown_patterns = [
            r'(?:#+\s)',                # headers
            r'(?:\*\*[^*]+\*\*)',     # bold
            r'(?:\*[^*]+\*)',           # italic
            r'(?:`[^`]+`)',              # inline code
            r'(?:~~[^~]+~~)',            # strikethrough
            r'(?:\!\[.*?\]\(.*?\))', # images
            r'(?:\[.*?\]\(.*?\))',    # links
            r'(?:\s*[-*+]\s)',          # lists
        ]
        pattern = '|'.join(markdown_patterns)

        try:
            full_parts = re.split(f'({pattern})', full_logical_line) if full_logical_line else []
        except Exception as e:
            full_parts = [full_logical_line] if full_logical_line else []

        current_pos = 0
        visual_line_parts = []

        for part in full_parts:
            part_length = len(part)
            part_end_pos = current_pos + part_length

            if current_pos < end_pos and part_end_pos > start_pos:
                overlap_start = max(current_pos, start_pos)
                overlap_end = min(part_end_pos, end_pos)
                part_overlap_start = overlap_start - current_pos
                part_overlap_end = overlap_end - current_pos
                visible_part = part[part_overlap_start:part_overlap_end]
                if visible_part:
                    visual_line_parts.append((visible_part, part))

            current_pos = part_end_pos

        highlight_indices = []
        if self.search_query and full_logical_line:
            lower_line = full_logical_line.lower()
            lower_query = self.search_query.lower()
            query_len = len(self.search_query)
            start = max(0, start_pos - query_len + 1)

            while True:
                pos = lower_line.find(lower_query, start)
                if pos == -1 or pos >= end_pos:
                    break
                match_end = pos + query_len
                if pos < end_pos and match_end > start_pos:
                    visual_start = max(pos, start_pos) - start_pos
                    visual_end = min(match_end, end_pos) - start_pos
                    if visual_start < visual_end:
                        highlight_indices.append((visual_start, visual_end))
                start = match_end
                if start >= end_pos:
                    break

        current_x = x
        for visible_part, full_part in visual_line_parts:
            for i, ch in enumerate(visible_part):
                abs_x = current_x + i
                if 0 <= y < h and 0 <= abs_x < w:
                    is_highlighted = any(start <= (current_x + i) < end for start, end in highlight_indices)
                    is_markdown = re.match(pattern, full_part) is not None if full_part else False

                    attr = 0
                    if is_highlighted:
                        attr = curses.color_pair(2)
                    elif is_markdown:
                        attr = curses.color_pair(1)

                    try:
                        self.stdscr.addstr(y, abs_x, ch, attr)
                    except curses.error:
                        pass

            current_x += len(visible_part)

    def insert_char(self, char):
        line = self.content[self.cursor_y]
        self.content[self.cursor_y] = line[:self.cursor_x] + char + line[self.cursor_x:]
        self.cursor_x += 1
        self.find_all_matches()

    def backspace(self):
        if self.cursor_x > 0:
            line = self.content[self.cursor_y]
            self.content[self.cursor_y] = line[:self.cursor_x - 1] + line[self.cursor_x:]
            self.cursor_x -= 1
        elif self.cursor_y > 0:
            prev_line = self.content[self.cursor_y - 1]
            current_line = self.content[self.cursor_y]
            self.cursor_x = len(prev_line)
            self.content[self.cursor_y - 1] += current_line
            del self.content[self.cursor_y]
            self.cursor_y -= 1
        self.find_all_matches()

    def newline(self):
        line = self.content[self.cursor_y]
        self.content[self.cursor_y] = line[:self.cursor_x]
        self.content.insert(self.cursor_y + 1, line[self.cursor_x:])
        self.cursor_y += 1
        self.cursor_x = 0
        self.find_all_matches()

    def show_flash(self, message):
        h, w = self.stdscr.getmaxyx()
        x = max(0, (w - len(message)) // 2)
        self.stdscr.attron(curses.A_BOLD)
        self.stdscr.addstr(0, x, message[:w - 1])
        self.stdscr.attroff(curses.A_BOLD)
        self.stdscr.refresh()
        time.sleep(1)

def main():
    curses.wrapper(run_editor)

def run_editor(stdscr):
    editor = MarkdownEditor(stdscr)
    editor.run()
