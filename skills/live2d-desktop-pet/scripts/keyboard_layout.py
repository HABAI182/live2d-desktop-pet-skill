#!/usr/bin/env python3
"""Generate an original 60% keyboard geometry reference, never edit artwork."""
import argparse
import html
import json
from pathlib import Path


def key(code, label, units=1):
    return code, label, units


ROWS = [
    [key('Escape', 'Esc')] + [key('Digit'+c, c) for c in '1234567890']
    + [key('Minus', '-'), key('Equal', '='), key('Backspace', 'Back', 2)],
    [key('Tab', 'Tab', 1.5)] + [key('Key'+c, c) for c in 'QWERTYUIOP']
    + [key('BracketLeft', '['), key('BracketRight', ']'), key('Backslash', '\\', 1.5)],
    [key('CapsLock', 'Caps', 1.75)] + [key('Key'+c, c) for c in 'ASDFGHJKL']
    + [key('Semicolon', ';'), key('Quote', "'"), key('Enter', 'Enter', 2.25)],
    [key('ShiftLeft', 'Shift', 2.25)] + [key('Key'+c, c) for c in 'ZXCVBNM']
    + [key('Comma', ','), key('Period', '.'), key('Slash', '/'), key('ShiftRight', 'Shift', 2.75)],
    [key('ControlLeft', 'Ctrl', 1.25), key('MetaLeft', 'Win', 1.25), key('AltLeft', 'Alt', 1.25),
     key('Space', 'SPACE', 6.25), key('AltRight', 'Alt', 1.25), key('MetaRight', 'Win', 1.25),
     key('ContextMenu', 'Menu', 1.25), key('ControlRight', 'Ctrl', 1.25)],
]


def layout(view='front-facing-pet'):
    if view not in ('front-facing-pet', 'typing-view'):
        raise ValueError('unsupported view')
    result = []
    for row, keys in enumerate(ROWS):
        offset = 0
        for code, label, units in keys:
            x, y = (offset + units/2)/15, (row + .5)/5
            side = 'left' if x < .5 else 'right'
            # Staggered letter rows do not split at a single 50% pixel line.
            if code.startswith('Key'):
                side = 'left' if label in 'QWERTASDFGZXCVB' else 'right'
            elif code.startswith('Digit'):
                side = 'left' if label in '12345' else 'right'
            depth = 'back' if row < 2 else 'front'
            screen_x, screen_y = (1-x, 1-y) if view == 'front-facing-pet' else (x, y)
            result.append({'code': code, 'label': label, 'row': row, 'units': units,
                           'physical': {'x': x, 'y': y, 'side': side, 'depth': depth},
                           'screen': {'x': screen_x, 'y': screen_y},
                           'zone': 'space' if code == 'Space' else side+'-'+depth,
                           'bounds': [offset/15, row/5, (offset+units)/15, (row+1)/5]})
            offset += units
        if offset != 15:
            raise ValueError('row width is not 15u')
    return {'schema': 1, 'layout': '60-percent-example', 'view': view, 'keys': result,
            'regionDefinition': 'Stagger-aware example: T/Y, G/H and B/N; hand ownership remains configurable',
            'scope': 'Geometry only; not a full-size OS keycode map or completed character asset'}


def svg(data):
    view = data['view']

    def project(x, y):
        if view == 'front-facing-pet':
            x, y = 1-x, 1-y
        factor = .86 + .14*y
        return 520 + (x-.5)*940*factor, 90 + y*260

    label = 'PET SIDE / space row' if view == 'front-facing-pet' else 'FAR SIDE / number row'
    parts = ['<svg xmlns="http://www.w3.org/2000/svg" width="1040" height="420" viewBox="0 0 1040 420">',
             '<rect width="1040" height="420" fill="#fffaf5"/>',
             '<g font-family="Arial,sans-serif" text-anchor="middle" fill="#483d3b">',
             '<text x="520" y="36" font-size="24">'+label+'</text>']
    for item in data['keys']:
        x0, y0, x1, y1 = item['bounds']
        gap_x, gap_y = .045/15, .045/5
        corners = [project(x0+gap_x, y0+gap_y), project(x1-gap_x, y0+gap_y),
                   project(x1-gap_x, y1-gap_y), project(x0+gap_x, y1-gap_y)]
        points = ' '.join(f'{x:.2f},{y:.2f}' for x, y in corners)
        fill = '#ffe8b6' if item['zone'] == 'space' else '#f6d3ce' if item['physical']['side'] == 'left' else '#d4e3f5'
        parts.append(f'<polygon id="{item["code"]}" points="{points}" fill="{fill}" stroke="#ad9991" stroke-width="1.5"/>')
        cx, cy = project((x0+x1)/2, (y0+y1)/2)
        parts.append(f'<text x="{cx:.2f}" y="{cy+5:.2f}" font-size="15">{html.escape(item["label"])}</text>')
    note = 'Physical RIGHT = screen left  |  Physical LEFT = screen right' if view == 'front-facing-pet' else 'Physical LEFT = screen left  |  Physical RIGHT = screen right'
    parts += [f'<text x="520" y="394" font-size="18">{note}</text>', '</g></svg>']
    return '\n'.join(parts)+'\n'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--view', choices=('front-facing-pet', 'typing-view'), default='front-facing-pet')
    parser.add_argument('--output-dir', type=Path, required=True)
    args = parser.parse_args()
    destination = args.output_dir.resolve()
    if destination.exists():
        parser.error('output directory exists; use a new directory to preserve earlier work')
    data = layout(args.view)
    destination.mkdir(parents=True)
    (destination/'keyboard.json').write_text(json.dumps(data, indent=2)+'\n', encoding='utf-8')
    (destination/'keyboard.svg').write_text(svg(data), encoding='utf-8')
    print(json.dumps({'output': str(destination), 'keys': len(data['keys']), 'view': args.view}))


if __name__ == '__main__':
    main()
