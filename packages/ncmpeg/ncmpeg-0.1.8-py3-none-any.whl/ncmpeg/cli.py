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
import subprocess
import os

VIDEO_OPS = [
    "Resize Video", "Crop Video", "Rotate/Flip Video", "Add Subtitles",
    "Extract Frames", "Generate GIF", "Change Playback Speed (Video)",
    "Overlay Image/Watermark", "Strip Metadata (Video)", "Get Media Info (Video)"
]

AUDIO_OPS = [
    "Extract Audio", "Change Audio Volume", "Normalize Audio",
    "Change Playback Speed (Audio)", "Strip Metadata (Audio)", "Get Media Info (Audio)"
]

CORE_OPS = [
    "Convert Format", "Cut Video", "Merge Videos", "Add Audio", "Remove Audio"
]

OPERATIONS = CORE_OPS + VIDEO_OPS + AUDIO_OPS
OPERATION_KEYS = {op: "↵ Confirm   Esc Cancel" for op in OPERATIONS}


def draw_menu(stdscr, selected_idx, files, selected_file_idx):
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    mid = w // 2

    stdscr.addstr(1, 2, "FFmpeg ncurses Interface", curses.A_BOLD)
    stdscr.addstr(3, 2, "Operations:", curses.A_UNDERLINE)
    stdscr.addstr(3, mid + 2, "Files:", curses.A_UNDERLINE)

    for idx, op in enumerate(OPERATIONS):
        mode = curses.A_REVERSE if idx == selected_idx else curses.A_NORMAL
        stdscr.addstr(5 + idx, 4, op, mode)

    draw_file_column(stdscr, files, selected_file_idx)
    draw_footer(stdscr, "Use ↑/↓ to navigate, ↹ Tab to switch panel, ↵ Enter to select, q to quit.")
    stdscr.refresh()


def draw_file_column(stdscr, files, selected_file_idx):
    _, w = stdscr.getmaxyx()
    mid = w // 2
    stdscr.addstr(3, mid + 2, "Files:", curses.A_UNDERLINE)
    for idx, file in enumerate(files):
        mode = curses.A_REVERSE if idx == selected_file_idx else curses.A_NORMAL
        stdscr.addstr(5 + idx, mid + 4, file[:w - mid - 6], mode)


def draw_footer(stdscr, text):
    h, w = stdscr.getmaxyx()
    stdscr.attron(curses.color_pair(1))
    stdscr.addstr(h - 2, 0, " " * w)
    stdscr.addstr(h - 2, 2, text[:w - 4])
    stdscr.attroff(curses.color_pair(1))
    stdscr.refresh()


def input_box(stdscr, y, x, prompt, operation):
    stdscr.addstr(y, x, prompt)
    curses.curs_set(1)
    win = curses.newwin(1, 60, y, x + len(prompt))
    win.keypad(True)
    box = []
    draw_footer(stdscr, OPERATION_KEYS[operation])
    while True:
        win.clear()
        win.addstr(0, 0, ''.join(box))
        win.refresh()
        key = win.getch()
        if key in [10, 13]:  # Enter
            curses.curs_set(0)
            return ''.join(box)
        elif key == 27:  # Esc
            curses.curs_set(0)
            return None
        elif key in [8, 127, curses.KEY_BACKSPACE]:
            if box:
                box.pop()
        elif 32 <= key <= 126:
            box.append(chr(key))


def run_ffmpeg_command(stdscr, command, success_msg, fail_msg):
    stdscr.addstr(8, 2, f"Running: {' '.join(command)}")
    stdscr.refresh()
    try:
        subprocess.run(command, check=True)
        stdscr.addstr(10, 2, success_msg, curses.A_BOLD)
    except subprocess.CalledProcessError:
        stdscr.addstr(10, 2, fail_msg, curses.A_BOLD)
    draw_footer(stdscr, "Press any key to return to menu.")
    stdscr.getch()

def convert_format(stdscr, cwd):
    files = sorted([f for f in os.listdir(cwd) if os.path.isfile(f)])
    stdscr.clear()
    stdscr.addstr(1, 2, "Convert Format", curses.A_BOLD)
    draw_file_column(stdscr, files, -1)
    input_file = input_box(stdscr, 3, 2, "Input file: ", "Convert Format")
    if input_file is None: return
    output_format = input_box(stdscr, 4, 2, "Output format (e.g. mp4): ", "Convert Format")
    if output_format is None: return
    output_file = os.path.splitext(input_file)[0] + "." + output_format
    run_ffmpeg_command(stdscr,
        ["ffmpeg", "-i", input_file, output_file],
        f"Saved as: {output_file}", "Conversion failed.")

def cut_video(stdscr, cwd):
    files = sorted([f for f in os.listdir(cwd) if os.path.isfile(f)])
    stdscr.clear()
    stdscr.addstr(1, 2, "Cut Video", curses.A_BOLD)
    draw_file_column(stdscr, files, -1)
    input_file = input_box(stdscr, 3, 2, "Input file: ", "Cut Video")
    if input_file is None: return
    start = input_box(stdscr, 4, 2, "Start time (00:00:00): ", "Cut Video")
    if start is None: return
    end = input_box(stdscr, 5, 2, "End time (00:00:00): ", "Cut Video")
    if end is None: return
    output_file = "cut_" + input_file
    run_ffmpeg_command(stdscr,
        ["ffmpeg", "-i", input_file, "-ss", start, "-to", end, "-c", "copy", output_file],
        f"Cut saved as: {output_file}", "Cut failed.")

def merge_videos(stdscr, cwd):
    files = sorted([f for f in os.listdir(cwd) if os.path.isfile(f)])
    stdscr.clear()
    stdscr.addstr(1, 2, "Merge Videos", curses.A_BOLD)
    draw_file_column(stdscr, files, -1)
    files_input = input_box(stdscr, 3, 2, "Comma-separated files: ", "Merge Videos")
    if files_input is None: return
    file_list = [f.strip() for f in files_input.split(",")]
    txt_file = "merge_list.txt"
    with open(txt_file, "w") as f:
        for file in file_list:
            f.write(f"file '{file}'\n")
    output_file = "merged_output.mp4"
    run_ffmpeg_command(stdscr,
        ["ffmpeg", "-f", "concat", "-safe", "0", "-i", txt_file, "-c", "copy", output_file],
        f"Merged to: {output_file}", "Merge failed.")

def add_audio(stdscr, cwd):
    files = sorted([f for f in os.listdir(cwd) if os.path.isfile(f)])
    stdscr.clear()
    stdscr.addstr(1, 2, "Add Audio", curses.A_BOLD)
    draw_file_column(stdscr, files, -1)
    video = input_box(stdscr, 3, 2, "Video file: ", "Add Audio")
    if video is None: return
    audio = input_box(stdscr, 4, 2, "Audio file: ", "Add Audio")
    if audio is None: return
    output_file = "with_audio_" + video
    run_ffmpeg_command(stdscr,
        ["ffmpeg", "-i", video, "-i", audio, "-c:v", "copy", "-c:a", "aac", "-map", "0:v:0", "-map", "1:a:0", output_file],
        f"Saved as: {output_file}", "Add audio failed.")

def remove_audio(stdscr, cwd):
    files = sorted([f for f in os.listdir(cwd) if os.path.isfile(f)])
    stdscr.clear()
    stdscr.addstr(1, 2, "Remove Audio", curses.A_BOLD)
    draw_file_column(stdscr, files, -1)
    video = input_box(stdscr, 3, 2, "Input file: ", "Remove Audio")
    if video is None: return
    output_file = "noaudio_" + video
    run_ffmpeg_command(stdscr,
        ["ffmpeg", "-i", video, "-an", output_file],
        f"Saved as: {output_file}", "Remove audio failed.")

def resize_video(stdscr, cwd):
    files = sorted(os.listdir(cwd))
    stdscr.clear()
    stdscr.addstr(1, 2, "Resize Video", curses.A_BOLD)
    draw_file_column(stdscr, files, -1)
    input_file = input_box(stdscr, 3, 2, "Input file: ", "Resize Video")
    if input_file is None: return
    resolution = input_box(stdscr, 4, 2, "New resolution (e.g. 1280x720): ", "Resize Video")
    if resolution is None: return
    output_file = "resized_" + input_file
    run_ffmpeg_command(stdscr,
        ["ffmpeg", "-i", input_file, "-vf", f"scale={resolution}", output_file],
        f"Saved as: {output_file}", "Resize failed.")

def crop_video(stdscr, cwd):
    files = sorted(os.listdir(cwd))
    stdscr.clear()
    stdscr.addstr(1, 2, "Crop Video", curses.A_BOLD)
    draw_file_column(stdscr, files, -1)
    input_file = input_box(stdscr, 3, 2, "Input file: ", "Crop Video")
    if input_file is None: return
    crop_params = input_box(stdscr, 4, 2, "Crop (w:h:x:y): ", "Crop Video")
    if crop_params is None: return
    output_file = "cropped_" + input_file
    run_ffmpeg_command(stdscr,
        ["ffmpeg", "-i", input_file, "-vf", f"crop={crop_params}", output_file],
        f"Saved as: {output_file}", "Crop failed.")

def rotate_flip_video(stdscr, cwd):
    files = sorted(os.listdir(cwd))
    stdscr.clear()
    stdscr.addstr(1, 2, "Rotate/Flip Video", curses.A_BOLD)
    draw_file_column(stdscr, files, -1)
    input_file = input_box(stdscr, 3, 2, "Input file: ", "Rotate/Flip Video")
    if input_file is None: return
    draw_footer(stdscr, "Examples: transpose=1 (rotate 90), hflip, vflip")
    effect = input_box(stdscr, 4, 2, "Effect: ", "Rotate/Flip Video")
    if effect is None: return
    output_file = "rotated_" + input_file
    run_ffmpeg_command(stdscr,
        ["ffmpeg", "-i", input_file, "-vf", effect, output_file],
        f"Saved as: {output_file}", "Rotate/Flip failed.")

def add_subtitles(stdscr, cwd):
    files = sorted(os.listdir(cwd))
    stdscr.clear()
    stdscr.addstr(1, 2, "Add Subtitles", curses.A_BOLD)
    draw_file_column(stdscr, files, -1)
    input_file = input_box(stdscr, 3, 2, "Video file: ", "Add Subtitles")
    if input_file is None: return
    subtitle_file = input_box(stdscr, 4, 2, "Subtitle (.srt) file: ", "Add Subtitles")
    if subtitle_file is None: return
    output_file = "subtitled_" + input_file
    run_ffmpeg_command(stdscr,
        ["ffmpeg", "-i", input_file, "-vf", f"subtitles={subtitle_file}", output_file],
        f"Saved as: {output_file}", "Subtitle failed.")

def extract_frames(stdscr, cwd):
    files = sorted(os.listdir(cwd))
    stdscr.clear()
    stdscr.addstr(1, 2, "Extract Frames", curses.A_BOLD)
    draw_file_column(stdscr, files, -1)
    input_file = input_box(stdscr, 3, 2, "Input file: ", "Extract Frames")
    if input_file is None: return
    rate = input_box(stdscr, 4, 2, "Frames per second (e.g. 1): ", "Extract Frames")
    if rate is None: return
    run_ffmpeg_command(stdscr,
        ["ffmpeg", "-i", input_file, "-vf", f"fps={rate}", "frame_%04d.png"],
        "Frames saved as frame_XXXX.png", "Frame extraction failed.")

def generate_gif(stdscr, cwd):
    files = sorted(os.listdir(cwd))
    stdscr.clear()
    stdscr.addstr(1, 2, "Generate GIF", curses.A_BOLD)
    draw_file_column(stdscr, files, -1)
    input_file = input_box(stdscr, 3, 2, "Input file: ", "Generate GIF")
    if input_file is None: return
    start = input_box(stdscr, 4, 2, "Start time (e.g. 00:00:05): ", "Generate GIF")
    if start is None: return
    duration = input_box(stdscr, 5, 2, "Duration (e.g. 3): ", "Generate GIF")
    if duration is None: return
    output_file = "output.gif"
    run_ffmpeg_command(stdscr,
        ["ffmpeg", "-ss", start, "-t", duration, "-i", input_file, "-vf", "fps=10,scale=320:-1", "-gifflags", "+transdiff", output_file],
        f"GIF saved as: {output_file}", "GIF generation failed.")

def playback_speed_video(stdscr, cwd):
    files = sorted(os.listdir(cwd))
    stdscr.clear()
    stdscr.addstr(1, 2, "Change Video Speed", curses.A_BOLD)
    draw_file_column(stdscr, files, -1)
    input_file = input_box(stdscr, 3, 2, "Input file: ", "Change Playback Speed (Video)")
    if input_file is None: return
    factor = input_box(stdscr, 4, 2, "Speed factor (e.g. 2.0 or 0.5): ", "Change Playback Speed (Video)")
    if factor is None: return
    output_file = "speed_" + input_file
    run_ffmpeg_command(stdscr,
        ["ffmpeg", "-i", input_file, "-filter_complex", f"[0:v]setpts={1/float(factor)}*PTS[v];[0:a]atempo={factor}[a]",
         "-map", "[v]", "-map", "[a]", output_file],
        f"Saved as: {output_file}", "Speed change failed.")

def overlay_watermark(stdscr, cwd):
    files = sorted(os.listdir(cwd))
    stdscr.clear()
    stdscr.addstr(1, 2, "Overlay Watermark", curses.A_BOLD)
    draw_file_column(stdscr, files, -1)
    input_file = input_box(stdscr, 3, 2, "Video file: ", "Overlay Image/Watermark")
    if input_file is None: return
    image = input_box(stdscr, 4, 2, "Overlay image file: ", "Overlay Image/Watermark")
    if image is None: return
    output_file = "watermarked_" + input_file
    run_ffmpeg_command(stdscr,
        ["ffmpeg", "-i", input_file, "-i", image, "-filter_complex", "overlay=10:10", output_file],
        f"Saved as: {output_file}", "Overlay failed.")

def strip_metadata_video(stdscr, cwd):
    files = sorted(os.listdir(cwd))
    stdscr.clear()
    stdscr.addstr(1, 2, "Strip Metadata (Video)", curses.A_BOLD)
    draw_file_column(stdscr, files, -1)
    input_file = input_box(stdscr, 3, 2, "Input file: ", "Strip Metadata (Video)")
    if input_file is None: return
    output_file = "clean_" + input_file
    run_ffmpeg_command(stdscr,
        ["ffmpeg", "-i", input_file, "-map_metadata", "-1", "-c", "copy", output_file],
        f"Saved as: {output_file}", "Strip metadata failed.")

def get_media_info_video(stdscr, cwd):
    files = sorted(os.listdir(cwd))
    stdscr.clear()
    stdscr.addstr(1, 2, "Get Media Info (Video)", curses.A_BOLD)
    draw_file_column(stdscr, files, -1)
    input_file = input_box(stdscr, 3, 2, "Input file: ", "Get Media Info (Video)")
    if input_file is None: return
    draw_footer(stdscr, "Press any key after output.")
    stdscr.refresh()
    os.system(f"ffprobe -hide_banner -loglevel info '{input_file}'")
    stdscr.getch()

def extract_audio(stdscr, cwd):
    files = sorted(os.listdir(cwd))
    stdscr.clear()
    stdscr.addstr(1, 2, "Extract Audio", curses.A_BOLD)
    draw_file_column(stdscr, files, -1)
    input_file = input_box(stdscr, 3, 2, "Video file: ", "Extract Audio")
    if input_file is None: return
    output_file = os.path.splitext(input_file)[0] + ".mp3"
    run_ffmpeg_command(stdscr,
        ["ffmpeg", "-i", input_file, "-q:a", "0", "-map", "a", output_file],
        f"Audio saved as: {output_file}", "Extraction failed.")

def change_audio_volume(stdscr, cwd):
    files = sorted(os.listdir(cwd))
    stdscr.clear()
    stdscr.addstr(1, 2, "Change Audio Volume", curses.A_BOLD)
    draw_file_column(stdscr, files, -1)
    input_file = input_box(stdscr, 3, 2, "Audio file: ", "Change Audio Volume")
    if input_file is None: return
    factor = input_box(stdscr, 4, 2, "Volume factor (e.g. 1.5 = 150%): ", "Change Audio Volume")
    if factor is None: return
    output_file = "volume_" + input_file
    run_ffmpeg_command(stdscr,
        ["ffmpeg", "-i", input_file, "-filter:a", f"volume={factor}", output_file],
        f"Volume changed: {output_file}", "Volume change failed.")

def normalize_audio(stdscr, cwd):
    files = sorted(os.listdir(cwd))
    stdscr.clear()
    stdscr.addstr(1, 2, "Normalize Audio", curses.A_BOLD)
    draw_file_column(stdscr, files, -1)
    input_file = input_box(stdscr, 3, 2, "Audio file: ", "Normalize Audio")
    if input_file is None: return
    output_file = "normalized_" + input_file
    run_ffmpeg_command(stdscr,
        ["ffmpeg", "-i", input_file, "-filter:a", "loudnorm", output_file],
        f"Normalized audio: {output_file}", "Normalization failed.")

def playback_speed_audio(stdscr, cwd):
    files = sorted(os.listdir(cwd))
    stdscr.clear()
    stdscr.addstr(1, 2, "Change Audio Speed", curses.A_BOLD)
    draw_file_column(stdscr, files, -1)
    input_file = input_box(stdscr, 3, 2, "Audio file: ", "Change Playback Speed (Audio)")
    if input_file is None: return
    factor = input_box(stdscr, 4, 2, "Speed factor (0.5–2.0): ", "Change Playback Speed (Audio)")
    if factor is None: return
    output_file = "aspeed_" + input_file
    run_ffmpeg_command(stdscr,
        ["ffmpeg", "-i", input_file, "-filter:a", f"atempo={factor}", output_file],
        f"Saved as: {output_file}", "Speed change failed.")

def strip_metadata_audio(stdscr, cwd):
    files = sorted(os.listdir(cwd))
    stdscr.clear()
    stdscr.addstr(1, 2, "Strip Metadata (Audio)", curses.A_BOLD)
    draw_file_column(stdscr, files, -1)
    input_file = input_box(stdscr, 3, 2, "Input file: ", "Strip Metadata (Audio)")
    if input_file is None: return
    output_file = "clean_" + input_file
    run_ffmpeg_command(stdscr,
        ["ffmpeg", "-i", input_file, "-map_metadata", "-1", "-c", "copy", output_file],
        f"Metadata stripped: {output_file}", "Strip failed.")

def get_media_info_audio(stdscr, cwd):
    files = sorted(os.listdir(cwd))
    stdscr.clear()
    stdscr.addstr(1, 2, "Get Media Info (Audio)", curses.A_BOLD)
    draw_file_column(stdscr, files, -1)
    input_file = input_box(stdscr, 3, 2, "Audio file: ", "Get Media Info (Audio)")
    if input_file is None: return
    draw_footer(stdscr, "Press any key after output.")
    stdscr.refresh()
    os.system(f"ffprobe -hide_banner -loglevel info '{input_file}'")
    stdscr.getch()

def handle_operation(stdscr, operation, cwd):
    ops = {
        "Convert Format": convert_format,
        "Cut Video": cut_video,
        "Merge Videos": merge_videos,
        "Add Audio": add_audio,
        "Remove Audio": remove_audio,

        "Resize Video": resize_video,
        "Crop Video": crop_video,
        "Rotate/Flip Video": rotate_flip_video,
        "Add Subtitles": add_subtitles,
        "Extract Frames": extract_frames,
        "Generate GIF": generate_gif,
        "Change Playback Speed (Video)": playback_speed_video,
        "Overlay Image/Watermark": overlay_watermark,
        "Strip Metadata (Video)": strip_metadata_video,
        "Get Media Info (Video)": get_media_info_video,

        "Extract Audio": extract_audio,
        "Change Audio Volume": change_audio_volume,
        "Normalize Audio": normalize_audio,
        "Change Playback Speed (Audio)": playback_speed_audio,
        "Strip Metadata (Audio)": strip_metadata_audio,
        "Get Media Info (Audio)": get_media_info_audio,
    }

    if operation in ops:
        ops[operation](stdscr, cwd)

def main():
    import curses
    curses.wrapper(run_ui)

def run_ui(stdscr):
    curses.curs_set(0)
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_CYAN)

    cwd = os.getcwd()
    files = sorted([f for f in os.listdir(cwd) if os.path.isfile(f)])
    selected_op = 0
    selected_file = 0
    focus_left = True

    while True:
        draw_menu(stdscr, selected_op, files, selected_file)
        key = stdscr.getch()

        if key == ord('q'):
            break
        elif key in [9, curses.KEY_BTAB]:  # Tab
            focus_left = not focus_left
        elif key == curses.KEY_UP:
            if focus_left and selected_op > 0:
                selected_op -= 1
            elif not focus_left and selected_file > 0:
                selected_file -= 1
        elif key == curses.KEY_DOWN:
            if focus_left and selected_op < len(OPERATIONS) - 1:
                selected_op += 1
            elif not focus_left and selected_file < len(files) - 1:
                selected_file += 1
        elif key in [10, 13]:  # Enter
            handle_operation(stdscr, OPERATIONS[selected_op], cwd)
