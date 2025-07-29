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
import shutil
import sys
import stat
import time

LOG_FILE = "deleted_files.log"
PROTECTED_PATHS = ['/', '/root', '/etc', '/boot', '/bin', '/sbin', '/usr']

def is_root():
    return os.geteuid() == 0

def log_deletion(path, simulated=False):
    with open(LOG_FILE, 'a') as log:
        action = "SIMULATED" if simulated else "DELETED"
        log.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {action}: {path}\n")

def format_permissions(mode):
    is_dir = 'd' if stat.S_ISDIR(mode) else '-'
    perms = ''
    for who in ['USR', 'GRP', 'OTH']:
        for what in ['R', 'W', 'X']:
            perms += what.lower() if mode & getattr(stat, f'S_I{what}{who}') else '-'
    return is_dir + perms

def human_size(bytes):
    for unit in ['B','KB','MB','GB','TB']:
        if bytes < 1024:
            return f"{bytes:.1f}{unit}"
        bytes /= 1024
    return f"{bytes:.1f}PB"

def overwrite_file(file_path, passes=3, simulated=False):
    if simulated:
        log_deletion(file_path, simulated=True)
        return
    try:
        with open(file_path, 'r+b') as f:
            length = os.path.getsize(file_path)
            for _ in range(passes):
                f.seek(0)
                f.write(os.urandom(length))
        os.remove(file_path)
        log_deletion(file_path)
    except:
        pass

def secure_delete(path, stdscr=None, simulated=False):
    messages = []

    if path in PROTECTED_PATHS and not is_root():
        msg = f"[PROTECTED] Skipped protected system folder: {path}"
        messages.append(msg)
        if simulated and stdscr:
            show_output(stdscr, [msg])
        return messages

    if os.path.isfile(path):
        if simulated:
            messages.append(f"[SIMULATED] Would delete: {path}")
            log_deletion(path, simulated=True)
        else:
            overwrite_file(path)
        return messages

    try:
        total = sum(len(files) for _, _, files in os.walk(path))
    except Exception as e:
        messages.append(f"[ERROR] Could not scan directory: {path} - {str(e)}")
        return messages

    processed = 0

    for root, dirs, files in os.walk(path, topdown=False):
        for f in files:
            fpath = os.path.join(root, f)
            try:
                if simulated:
                    messages.append(f"[SIMULATED] Would delete: {fpath}")
                    log_deletion(fpath, simulated=True)
                else:
                    overwrite_file(fpath)
                processed += 1
                if stdscr and not simulated:
                    draw_progress(stdscr, processed, total, fpath)
            except Exception as e:
                messages.append(f"[ERROR] Could not delete file: {fpath} - {str(e)}")

        for d in dirs:
            dpath = os.path.join(root, d)
            try:
                if simulated:
                    messages.append(f"[SIMULATED] Would remove directory: {dpath}")
                    log_deletion(dpath, simulated=True)
                else:
                    os.rmdir(dpath)
                    log_deletion(dpath)
            except Exception as e:
                messages.append(f"[ERROR] Could not remove directory: {dpath} - {str(e)}")

    try:
        if simulated:
            messages.append(f"[SIMULATED] Would remove root: {path}")
            log_deletion(path, simulated=True)
        else:
            os.rmdir(path)
            log_deletion(path)
    except Exception as e:
        messages.append(f"[ERROR] Could not remove root directory: {path} - {str(e)}")

    return messages

def draw_progress(stdscr, processed, total, current):
    h, w = stdscr.getmaxyx()
    bar_w = w - 20
    percent = processed / total if total > 0 else 1
    filled = int(bar_w * percent)
    bar = '[' + '#' * filled + '-' * (bar_w - filled) + ']'

    stdscr.addstr(h - 4, 0, f"Processing: {current[:w-1]}")
    stdscr.addstr(h - 3, 0, f"Progress:   {bar} {processed}/{total}")
    stdscr.refresh()

def show_output(stdscr, lines):
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    max_lines = h - 2
    offset = 0

    while True:
        stdscr.clear()
        for i in range(min(max_lines, len(lines) - offset)):
            stdscr.addstr(i, 0, lines[offset + i][:w-1])
        stdscr.addstr(h - 1, 0, "[UP/DOWN] Scroll | [q] Quit")

        key = stdscr.getch()
        if key == curses.KEY_DOWN and offset < len(lines) - max_lines:
            offset += 1
        elif key == curses.KEY_UP and offset > 0:
            offset -= 1
        elif key == ord('q'):
            break

def draw_menu(stdscr, path):
    curses.curs_set(0)
    current_dir = path
    selected = 0
    offset = 0
    selected_items = set()
    show_hidden = True

    while True:
        stdscr.clear()
        h, w = stdscr.getmaxyx()
        max_display = h - 6

        stdscr.addstr(0, 0, f"Browsing: {current_dir} (hidden: {'ON' if show_hidden else 'OFF'})")
        try:
            all_entries = os.listdir(current_dir)
            entries = [e for e in all_entries if show_hidden or not e.startswith('.')]
        except:
            entries = []

        entries.sort()
        if current_dir != '/':
            entries.insert(0, '..')

        visible_entries = entries[offset:offset + max_display]

        for idx, entry in enumerate(visible_entries):
            abs_path = os.path.join(current_dir, entry)
            try:
                stats = os.lstat(abs_path)
                perms = format_permissions(stats.st_mode)
                size = human_size(stats.st_size)
                ftype = 'DIR' if stat.S_ISDIR(stats.st_mode) else (
                        'LNK' if stat.S_ISLNK(stats.st_mode) else 'FILE')
            except:
                perms, size, ftype = '?????????', '?', '?'

            is_protected = abs_path in PROTECTED_PATHS
            is_selected = abs_path in selected_items

            display = f"{entry:<30.30} {ftype:<5} {perms:<10} {size:>7}"
            y = 2 + idx

            if idx + offset == selected:
                stdscr.attron(curses.color_pair(1))
                stdscr.addstr(y, 0, display[:w - 1])
                stdscr.attroff(curses.color_pair(1))
            elif is_selected:
                stdscr.attron(curses.color_pair(3))
                stdscr.addstr(y, 0, display[:w - 1])
                stdscr.attroff(curses.color_pair(3))
            elif is_protected:
                stdscr.attron(curses.color_pair(2))
                stdscr.addstr(y, 0, display[:w - 1])
                stdscr.attroff(curses.color_pair(2))
            else:
                stdscr.addstr(y, 0, display[:w - 1])

        stdscr.addstr(h - 2, 0, "[↑↓] Navigate | [SPACE] Select | [ENTER] Open | [d] Delete | [h] Show/Hide dotfiles | [q] Quit")

        key = stdscr.getch()

        if key == curses.KEY_UP and selected > 0:
            selected -= 1
            if selected < offset:
                offset -= 1
        elif key == curses.KEY_DOWN and selected < len(entries) - 1:
            selected += 1
            if selected >= offset + max_display:
                offset += 1
        elif key == ord('q'):
            break
        elif key == ord('h'):
            show_hidden = not show_hidden
            selected = offset = 0
        elif key == ord('\n'):
            chosen = entries[selected]
            new_path = os.path.join(current_dir, chosen)
            if chosen == '..':
                current_dir = os.path.dirname(current_dir)
                selected = offset = 0
                selected_items.clear()
            elif os.path.isdir(new_path):
                current_dir = new_path
                selected = offset = 0
                selected_items.clear()
        elif key == ord(' '):
            target = os.path.join(current_dir, entries[selected])
            if target in selected_items:
                selected_items.remove(target)
            else:
                selected_items.add(target)
        elif key == ord('d'):
            if not selected_items:
                stdscr.addstr(h - 5, 0, "No items selected. Press any key.")
                stdscr.getch()
                continue

            for item in selected_items:
                if item in PROTECTED_PATHS and not is_root():
                    stdscr.addstr(h - 5, 0, f"Root required to delete {item}. Press any key.")
                    stdscr.getch()
                    break
            else:
                stdscr.addstr(h - 5, 0, "Run as simulation only? (y/n): ")
                simulate = stdscr.getch() == ord('y')

                all_messages = []
                for i, target in enumerate(selected_items):
                    messages = secure_delete(target, stdscr, simulated=simulate)
                    all_messages.extend(messages)

                if simulate:
                    show_output(stdscr, all_messages)
                else:
                    stdscr.addstr(h - 2, 0, "Finished. Press any key.")
                    stdscr.getch()
                    selected_items.clear()

def main():
    import curses
    curses.wrapper(_main)

def _main(stdscr):
    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_CYAN)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_GREEN)
    home = os.path.expanduser("~")
    draw_menu(stdscr, home)
