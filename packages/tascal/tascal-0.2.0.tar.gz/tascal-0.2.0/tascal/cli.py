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
import calendar
from datetime import datetime
import textwrap
import json
import os

NOTES_FILE = "notes.json"

def load_notes():
    if os.path.exists(NOTES_FILE):
        with open(NOTES_FILE, "r") as f:
            return json.load(f)
    return {}

def save_notes(notes):
    with open(NOTES_FILE, "w") as f:
        json.dump(notes, f)

def get_date_string(year, month, day):
    return f"{year:04d}-{month:02d}-{day:02d}"

def prompt_input(stdscr, prompt_text):
    curses.echo()
    stdscr.move(curses.LINES - 2, 0)
    stdscr.clrtoeol()
    stdscr.addstr(curses.LINES - 2, 0, prompt_text)
    input_str = stdscr.getstr(curses.LINES - 2, len(prompt_text)).decode("utf-8")
    curses.noecho()
    return input_str

def prompt_note_index(stdscr, notes_list):
    if not notes_list:
        return None
    prompt = f"Select note number (1–{len(notes_list)}): "
    while True:
        index_str = prompt_input(stdscr, prompt)
        try:
            index = int(index_str) - 1
            if 0 <= index < len(notes_list):
                return index
        except ValueError:
            pass

def draw_calendar(stdscr, year, month, selected_day, notes):
    stdscr.clear()
    curses.curs_set(0)
    height, width = stdscr.getmaxyx()
    today = datetime.now().date()
    cal = calendar.monthcalendar(year, month)
    month_name = calendar.month_name[month]

    # Calculate column widths: calendar takes 40% of the screen, tasks take the rest
    calendar_width = min(40, width // 2)  # Ensure calendar width is reasonable
    tasks_width = max(10, width - calendar_width - 2)  # Leave a small gap, ensure minimum width

    # Draw calendar in the left column
    if height > 0 and width > 0:  # Ensure there's space to draw
        stdscr.addstr(0, 0, f"{month_name} {year}".center(calendar_width), curses.A_BOLD)

        days = ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]
        for i, day in enumerate(days):
            if i * 4 + 2 <= calendar_width and 2 < height:  # Ensure day labels fit within calendar width and screen height
                stdscr.addstr(2, i * 4, day, curses.A_UNDERLINE)

        for row_idx, week in enumerate(cal):
            if 3 + row_idx >= height:  # Stop if we reach the bottom of the screen
                break
            for col_idx, day in enumerate(week):
                if day == 0:
                    continue
                y, x = 3 + row_idx, col_idx * 4
                attr = curses.A_NORMAL
                date_obj = datetime(year, month, day).date()
                if date_obj == today:
                    attr = curses.A_REVERSE
                if day == selected_day:
                    attr |= curses.A_STANDOUT
                if x < calendar_width and y < height:  # Ensure we don't draw outside the calendar column or screen
                    stdscr.addstr(y, x, f"{day:2}", attr)

        selected_date = get_date_string(year, month, selected_day)
        if 10 < height and calendar_width > len(f"Selected: {selected_date}"):
            stdscr.addstr(10, 0, f"Selected: {selected_date}", curses.A_BOLD)

        # Show notes for the selected date
        row = 12
        if row < height and selected_date in notes and notes[selected_date]:
            stdscr.addstr(row, 0, "Notes:")
            for idx, note in enumerate(notes[selected_date]):
                if row + 1 >= height:  # Check if there's space for the note
                    break
                wrapped = textwrap.wrap(note, calendar_width - 2)
                if wrapped:
                    note_line = f"{idx + 1}. {wrapped[0][:calendar_width - 6]}"
                    if len(note_line) <= calendar_width:
                        stdscr.addstr(row + 1, 2, note_line)
                    else:
                        stdscr.addstr(row + 1, 2, note_line[:calendar_width - 2])
                    for i, w in enumerate(wrapped[1:], 1):
                        if row + 1 + i >= height - 1:  # Ensure we don't draw outside the screen
                            break
                        line = w[:calendar_width - 6]
                        stdscr.addstr(row + 1 + i, 6, line)
                    row += len(wrapped) + 1
        elif row < height:
            stdscr.addstr(row, 0, "No notes for this date.")

        # Draw upcoming tasks in the right column
        if tasks_width > 10:  # Only display if there's enough width
            upcoming_tasks = []
            for date_str in sorted(notes.keys()):
                try:
                    date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
                    if date_obj >= today:
                        for note in notes[date_str]:
                            upcoming_tasks.append((date_obj, note))
                except ValueError:
                    continue

            # Sort upcoming tasks by date
            upcoming_tasks.sort(key=lambda x: x[0])

            # Display upcoming tasks header
            if 0 < height and calendar_width + 2 < width:
                tasks_header = "Upcoming Tasks"
                stdscr.addstr(0, calendar_width + 2, tasks_header.center(tasks_width), curses.A_BOLD)

            # Display upcoming tasks
            row = 1
            for date_obj, note in upcoming_tasks:
                if row >= height - 2:  # Stop if we reach near the bottom of the screen
                    break
                date_str = date_obj.strftime("%Y-%m-%d")
                wrapped = textwrap.wrap(note, tasks_width - len(date_str) - 3)  # Leave space for date and ": "
                if wrapped:
                    line = f"{date_str}: {wrapped[0]}"
                    if calendar_width + 2 + len(line) <= width and row < height:
                        stdscr.addstr(row, calendar_width + 2, line)
                    for i, w in enumerate(wrapped[1:], 1):
                        if row + i >= height - 1:  # Ensure we don't draw outside the screen
                            break
                        line = " " * (len(date_str) + 2) + w
                        if calendar_width + 2 + len(line) <= width:
                            stdscr.addstr(row + i, calendar_width + 2, line)
                    row += len(wrapped) + 1  # Add spacing between tasks

    # Draw footer at the bottom of the screen spanning both columns
    footer = "←↑→↓: Move  a: Add  m: Modify  d: Delete  q: Quit"
    if height > 0 and width > 0:
        # Ensure the footer fits within the screen width
        if width >= len(footer):
            footer_str = footer.ljust(width)
        else:
            footer_str = footer[:width]
        # Ensure we don't write to the last line if it's beyond screen height
        if height > 0:  # Ensure there's at least one row
            footer_row = height - 1
            if footer_row >= 0 and footer_row < height:
                try:
                    stdscr.addstr(footer_row, 0, footer_str, curses.A_REVERSE)
                except curses.error:
                    # Handle cases where even after checks, there might be an issue
                    pass

    stdscr.refresh()

def calendar_app(stdscr):
    notes = load_notes()
    now = datetime.now()
    year, month = now.year, now.month
    selected_day = now.day
    while True:
        draw_calendar(stdscr, year, month, selected_day, notes)
        key = stdscr.getch()
        max_day = calendar.monthrange(year, month)[1]
        if key == curses.KEY_RIGHT and selected_day < max_day:
            selected_day += 1
        elif key == curses.KEY_LEFT and selected_day > 1:
            selected_day -= 1
        elif key == curses.KEY_UP:
            selected_day = max(1, selected_day - 7)
        elif key == curses.KEY_DOWN:
            selected_day = min(max_day, selected_day + 7)
        elif key == ord('a'):
            date_str = get_date_string(year, month, selected_day)
            if datetime(year, month, selected_day).date() >= datetime.now().date():
                note = prompt_input(stdscr, "Add note: ")
                if note.strip():
                    notes.setdefault(date_str, []).append(note.strip())
                    save_notes(notes)
        elif key == ord('m'):
            date_str = get_date_string(year, month, selected_day)
            if datetime(year, month, selected_day).date() >= datetime.now().date():
                if date_str in notes and notes[date_str]:
                    index = prompt_note_index(stdscr, notes[date_str])
                    if index is not None:
                        new_note = prompt_input(stdscr, "Modify note: ")
                        if new_note.strip():
                            notes[date_str][index] = new_note.strip()
                            save_notes(notes)
        elif key == ord('d'):
            date_str = get_date_string(year, month, selected_day)
            if datetime(year, month, selected_day).date() >= datetime.now().date():
                if date_str in notes and notes[date_str]:
                    index = prompt_note_index(stdscr, notes[date_str])
                    if index is not None:
                        del notes[date_str][index]
                        if not notes[date_str]:
                            del notes[date_str]
                        save_notes(notes)
        elif key == ord('q'):
            break

def run():
    import curses
    curses.wrapper(calendar_app)
