#!/usr/bin/env python3
import subprocess
import sys
import time
import random
from collections import deque
import threading

GLYPHS = list("ᔑʖᓵ↸ᒷ⎓⊣⍑╎⋮ꖌꖎᒲリ𝙹!¡ᑑ∷ᓭℸ ̣⚍⍊∴ ̇/||⨅")

MAX_OBFUSCATION = 50.0

MIN_INCREMENT = 0.5
MAX_INCREMENT = 1.5

class OutputBuffer:
    def __init__(self, max_lines=1000):
        self.lines = deque(maxlen=max_lines)
        self.lock = threading.Lock()
        self.should_stop = False

    def add_line(self, line):
        cells = []
        for ch in line.rstrip('\n'):
            cell = {
                "actual": ch,
                "counter": 0.0,
                "revealed": True if ch.isspace() else False
            }
            cells.append(cell)
        with self.lock:
            self.lines.append(cells)

    def update_cells(self):
        with self.lock:
            for line in self.lines:
                for cell in line:
                    if not cell["revealed"]:
                        increment = random.uniform(MIN_INCREMENT, MAX_INCREMENT)
                        cell["counter"] += increment
                        p = min(cell["counter"] / MAX_OBFUSCATION, 1.0)
                        if random.random() < p:
                            cell["revealed"] = True

    def get_display_output(self):
        lines_str = []
        with self.lock:
            for line in self.lines:
                chars = []
                for cell in line:
                    if cell["revealed"]:
                        chars.append(cell["actual"])
                    else:
                        chars.append(random.choice(GLYPHS))
                lines_str.append(''.join(chars))
        return lines_str

def display_thread(buffer):
    """Continuously update the display with gradually revealing text."""
    while not buffer.should_stop or buffer.lines:
        buffer.update_cells()
        sys.stdout.write('\033[2J\033[H')
        output = buffer.get_display_output()
        sys.stdout.write('\n'.join(output))
        sys.stdout.flush()
        time.sleep(0.1)

def main():
    if len(sys.argv) < 2:
        sys.stderr.write(f"Usage: {sys.argv[0]} <command> [args...]\n")
        sys.exit(1)

    buffer = OutputBuffer()
    disp_thread = threading.Thread(target=display_thread, args=(buffer,))
    disp_thread.daemon = True
    disp_thread.start()
    process = subprocess.Popen(
        sys.argv[1:],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True,
        bufsize=1
    )

    try:
        for line in process.stdout:
            buffer.add_line(line)
        process.stdout.close()
        process.wait()
        buffer.should_stop = True
        time.sleep(1.5)
        sys.stdout.write('\033[2J\033[H')
        with buffer.lock:
            for line in buffer.lines:
                sys.stdout.write(''.join(cell["actual"] for cell in line) + '\n')
        sys.stdout.flush()
        
    except KeyboardInterrupt:
        process.terminate()
        buffer.should_stop = True
        sys.exit(1)

    sys.exit(process.returncode)

if __name__ == "__main__":
    main()

