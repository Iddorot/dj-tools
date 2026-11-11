"""Interactive tree picker for Serato crates.

Keys:
  up/down (j/k)   move           PgUp/PgDn  jump a page
  space           toggle crate (and everything under it)
  right (l)       expand / step into
  left (h)        collapse / jump to parent
  a / n           select all / none
  e / c           expand all / collapse all
  enter           confirm         q / esc   cancel

Windows needs: pip install windows-curses
"""
import curses
import os

SEP = "%%"  # Serato's subcrate separator in .crate filenames
HELP = "space toggle | <-/-> close/open | a all | n none | e/c expand/collapse | enter export | q quit"


class Node:
    def __init__(self, name, path, parent=None):
        self.name = name
        self.path = path
        self.parent = parent
        self.children = []
        self.checked = False
        self.expanded = True


def build_tree(paths):
    root = Node("", "")
    index = {"": root}
    for p in sorted(paths, key=str.lower):
        parts = p.split(SEP)
        for i in range(1, len(parts) + 1):
            key = SEP.join(parts[:i])
            if key not in index:
                parent = index[SEP.join(parts[: i - 1])]
                node = Node(parts[i - 1], key, parent)
                parent.children.append(node)
                index[key] = node
    return root, index


def _walk(node):
    for c in node.children:
        yield c
        yield from _walk(c)


def _set(node, value):
    node.checked = value
    for c in node.children:
        _set(c, value)


def _refresh_up(node):
    p = node.parent
    while p is not None:
        p.checked = bool(p.children) and all(c.checked for c in p.children)
        p = p.parent


def _partial(node):
    return not node.checked and any(c.checked or _partial(c) for c in node.children)


def _visible(root):
    rows = []

    def walk(n, depth):
        for c in n.children:
            rows.append((c, depth))
            if c.expanded:
                walk(c, depth + 1)

    walk(root, 0)
    return rows


def _selection(node):
    """Smallest set of paths covering everything ticked (a ticked parent covers its children)."""
    out = []
    for c in node.children:
        if c.checked:
            out.append(c.path)
        else:
            out += _selection(c)
    return out


def _run(stdscr, root):
    curses.curs_set(0)
    stdscr.keypad(True)
    cur = top = 0

    while True:
        rows = _visible(root)
        if not rows:
            return []
        cur = max(0, min(cur, len(rows) - 1))
        h, w = stdscr.getmaxyx()
        view = max(1, h - 2)
        if cur < top:
            top = cur
        elif cur >= top + view:
            top = cur - view + 1

        stdscr.erase()
        picked = sum(1 for n in _walk(root) if n.checked)
        stdscr.addnstr(0, 0, f"Select crates to export  ({picked} selected)", w - 1, curses.A_BOLD)
        for i, (node, depth) in enumerate(rows[top : top + view]):
            box = "[x]" if node.checked else "[~]" if _partial(node) else "[ ]"
            arrow = ("-" if node.expanded else "+") if node.children else " "
            count = f"  ({sum(1 for _ in _walk(node))})" if node.children else ""
            line = f"{'    ' * depth}{arrow} {box} {node.name}{count}"
            attr = curses.A_REVERSE if top + i == cur else curses.A_NORMAL
            stdscr.addnstr(i + 1, 0, line, w - 1, attr)
        stdscr.addnstr(h - 1, 0, HELP, w - 1, curses.A_DIM)
        stdscr.refresh()

        key = stdscr.getch()
        node = rows[cur][0]

        if key in (curses.KEY_UP, ord("k")):
            cur -= 1
        elif key in (curses.KEY_DOWN, ord("j")):
            cur += 1
        elif key == curses.KEY_PPAGE:
            cur -= view
        elif key == curses.KEY_NPAGE:
            cur += view
        elif key == ord(" "):
            _set(node, not node.checked)
            _refresh_up(node)
        elif key in (curses.KEY_RIGHT, ord("l")) and node.children:
            if node.expanded:
                cur += 1
            else:
                node.expanded = True
        elif key in (curses.KEY_LEFT, ord("h")):
            if node.children and node.expanded:
                node.expanded = False
            elif node.parent is not root:
                cur = next(i for i, (n, _) in enumerate(rows) if n is node.parent)
        elif key == ord("a"):
            _set(root, True)
        elif key == ord("n"):
            _set(root, False)
        elif key == ord("e"):
            for n in _walk(root):
                n.expanded = True
        elif key == ord("c"):
            for n in _walk(root):
                n.expanded = False
            while node.parent is not root:
                node = node.parent
            cur = root.children.index(node)
        elif key in (10, 13, curses.KEY_ENTER):
            return _selection(root)
        elif key in (ord("q"), 27):
            return None


def pick_crates(paths, preselected=()):
    """paths: crate names like 'Bodiem666%%#UKG%%2-Step'.
    Returns the chosen paths, or None if cancelled."""
    root, index = build_tree(paths)
    for p in preselected:
        if p in index:
            _set(index[p], True)
            _refresh_up(index[p])
    os.environ.setdefault("ESCDELAY", "25")
    return curses.wrapper(_run, root)


if __name__ == "__main__":
    from pathlib import Path

    folder = Path.home() / "Music" / "_Serato_" / "Subcrates"
    crates = [f.stem for f in folder.glob("*.crate")]
    print(pick_crates(crates))