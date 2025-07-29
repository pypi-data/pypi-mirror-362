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
import csv
import datetime
import os

CSV_FILE = "runs.csv"
FIELDS = ["date", "distance", "pace", "heart_rate", "cadence", "quality"]

def load_data():
    if not os.path.exists(CSV_FILE):
        return []
    with open(CSV_FILE, newline='') as f:
        reader = csv.DictReader(f)
        return list(reader)

def save_data(data):
    with open(CSV_FILE, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(data)

def get_today_entry(data):
    today = datetime.date.today().isoformat()
    for entry in data:
        if entry["date"] == today:
            return entry
    new_entry = {"date": today, "distance": "", "pace": "", "heart_rate": "", "cadence": "", "quality": ""}
    data.append(new_entry)
    return new_entry

def edit_entry(stdscr, entry):
    curses.echo()
    stdscr.clear()
    stdscr.addstr(0, 2, f"Edit Entry for {entry['date']}", curses.A_BOLD | curses.A_UNDERLINE)

    def prompt(row, label, key, default=""):
        stdscr.addstr(row, 2, f"{label} [{entry.get(key, default)}]: ")
        val = stdscr.getstr(row, len(label) + 6 + len(entry.get(key, default))).decode().strip()
        if val:
            entry[key] = val

    prompt(2, "Distance (km)", "distance")
    prompt(3, "Pace (min/km)", "pace")
    prompt(4, "Heart Rate", "heart_rate")
    prompt(5, "Cadence", "cadence")
    prompt(6, "Quality Run (1=yes, 0=no)", "quality", "0")

    curses.noecho()
    stdscr.addstr(8, 2, "Saved! Press any key to return...")
    stdscr.getch()

def draw_ui(stdscr, data, selected_idx):
    curses.curs_set(0)
    stdscr.clear()
    height, width = stdscr.getmaxyx()
    mid = width // 2

    if height < 24 or width < 80:
        stdscr.addstr(2, 2, "Terminal too small. Please resize to at least 80x24.")
        stdscr.refresh()
        stdscr.getch()
        return

    stdscr.addstr(0, 2, "Running Tracker", curses.A_BOLD | curses.A_UNDERLINE)
    stdscr.vline(1, mid, '|', height - 5)

    total_dist, total_hr, total_cad, total_pace, count = 0, 0, 0, 0, 0
    sorted_data = sorted(data, key=lambda x: x["date"], reverse=True)
    chart_data = sorted_data[:15][::-1]

    for i, entry in enumerate(sorted_data):
        highlight = curses.A_REVERSE if i == selected_idx else curses.A_NORMAL
        line = f"{entry['date']} | {entry['distance']:>5} | {entry['pace']:>5} | {entry['heart_rate']:>3} | {entry['cadence']:>3} | {'✓' if entry['quality']=='1' else ' '}"
        stdscr.addstr(2 + i, 2, line[:mid-2], highlight)
        try:
            dist = float(entry["distance"])
            pace = float(entry["pace"])
            hr = int(entry["heart_rate"])
            cad = int(entry["cadence"])
            total_dist += dist
            total_hr += hr
            total_cad += cad
            total_pace += pace
            count += 1
        except:
            continue

    if count > 0:
        avg_pace = total_pace / count
        avg_hr = total_hr / count
        avg_cad = total_cad / count
    else:
        avg_pace = avg_hr = avg_cad = 0

    stdscr.hline(height - 4, 2, '-', width - 4)
    stdscr.addstr(height - 3, 2, f"Total Distance: {total_dist:.2f} km")
    stdscr.addstr(height - 2, 2, f"Avg Pace: {avg_pace:.2f}  |  Avg HR: {avg_hr:.0f} bpm  |  Avg Cadence: {avg_cad:.0f} spm")
    stdscr.addstr(height - 1, 2, "[↑/↓] Select  [Enter] Edit  [D] Delete  [Q] Quit")

    # Chart setup
    chart_rows_total = height - 5
    chart_zone_height = chart_rows_total // 3
    chart_width = min(len(chart_data), 15)

    def draw_line_chart(y_start, label, metric_key, symbol='●'):
        stdscr.addstr(y_start, mid + 2, label, curses.A_BOLD)
        chart_top = y_start + 1
        chart_left = mid + 8
        try:
            max_val = max(float(d[metric_key]) for d in chart_data if d[metric_key])
        except:
            max_val = 1
        scale = chart_zone_height / max_val if max_val > 0 else 1

        # Gridlines & Y-axis
        grid_steps = 4
        for i in range(grid_steps + 1):
            rel_y = int(i * chart_zone_height / grid_steps)
            y_pos = chart_top + rel_y
            val = max_val * (1 - (i / grid_steps))
            label_str = f"{val:>5.1f} -"
            if y_pos < height - 1:
                stdscr.addstr(y_pos, mid + 2, label_str[:6])
                for x in range(chart_width):
                    col = chart_left + x
                    if col < width - 1:
                        stdscr.addstr(y_pos, col, '-')

        # Points and lines
        prev_y = None
        for i, entry in enumerate(chart_data):
            try:
                val = float(entry[metric_key])
                y_val = int(val * scale)
                row = chart_top + chart_zone_height - y_val
                col = chart_left + i
                if 1 <= row < height - 1 and col < width - 1:
                    stdscr.addstr(row, col, symbol)

                if prev_y is not None:
                    lower = min(prev_y, row)
                    upper = max(prev_y, row)
                    for y in range(lower + 1, upper):
                        if 1 <= y < height - 1 and col < width - 1:
                            stdscr.addstr(y, col, '|')
                prev_y = row
            except:
                continue

        # Horizontal divider under chart
        hline_row = chart_top + chart_zone_height + 1
        if hline_row < height - 1:
            stdscr.hline(hline_row, mid + 2, '-', width - mid - 4)

    draw_line_chart(1, "Last 15 Days - Distance", "distance")
    draw_line_chart(1 + chart_zone_height + 3, "Heart Rate", "heart_rate")
    draw_line_chart(1 + 2 * (chart_zone_height + 3), "Pace", "pace")

    stdscr.refresh()

def confirm_dialog(stdscr, message):
    stdscr.clear()
    stdscr.addstr(2, 2, message)
    stdscr.refresh()
    while True:
        key = stdscr.getch()
        if key in [ord('y'), ord('Y')]:
            return True
        elif key in [ord('n'), ord('N')]:
            return False

def main():
    import curses
    curses.wrapper(_main)

def _main(stdscr):
    data = load_data()
    get_today_entry(data)
    selected_idx = 0

    while True:
        draw_ui(stdscr, data, selected_idx)
        key = stdscr.getch()
        sorted_data = sorted(data, key=lambda x: x["date"], reverse=True)

        if key in [ord('q'), ord('Q')]:
            save_data(data)
            break
        elif key == curses.KEY_UP:
            selected_idx = max(0, selected_idx - 1)
        elif key == curses.KEY_DOWN:
            selected_idx = min(len(data) - 1, selected_idx + 1)
        elif key in [10, 13]:
            entry = sorted_data[selected_idx]
            edit_entry(stdscr, entry)
        elif key in [ord('d'), ord('D')]:
            entry = sorted_data[selected_idx]
            confirm = confirm_dialog(stdscr, f"Delete entry for {entry['date']}? (y/n): ")
            if confirm:
                data.remove(entry)
                selected_idx = max(0, selected_idx - 1)