import collections
import enum
import re
import sys


Scene = collections.namedtuple(
    'Scene',
    (
        'index',
        'shot',
        'action',
        'dialogue',
    )
)


def err(*args, **kwargs):
    kwargs['file'] = sys.stderr
    return print(*args, **kwargs)


def main(inp_path):
    with open(inp_path, 'r') as inp:
        blocks = re.finditer(r'^(-.*)(\n|\r\n)?((^\s*$|^ +.*)(\n|\r\n)?)*', inp.read(), re.MULTILINE)
        blocks = [block.group(0)[1:].strip() for block in blocks]
        blocks = [re.sub(r'^ +', '', block, flags=re.MULTILINE) for block in blocks]

        print(\
r'''<!DOCTYPE html>
<html>
<style>
table, th, td {
  border: 1px solid;
}

table {
    width: 100%;
    border-collapse: collapse;
}

table td, table td * {
    vertical-align: top;
}

table td {
    padding: 0.2em;
}

tr td:first-child, tr td:nth-child(2) {
    width: 1%;
    white-space: nowrap;
}
</style>
<body>
<table>
    <tr>
        <th>###</th>
        <th>SHOT</th>
        <th>ACTION</th>
        <th>DIALOGUE</th>
    </tr>''')

        for i, (a, b, c) in enumerate(zip(blocks[::3], blocks[1::3], blocks[2::3])):
            scene = Scene(i, a, b, c)

            dialogue = scene.dialogue.replace('\n', '<br/>')

            print(\
f'''    <tr>
    <td>{scene.index:03d}.000</td>
    <td>{scene.shot}</td>
    <td>{scene.action}</td>
    <td>{dialogue}</td>
</tr>
''', end='')

    print(r'''</table>
</html>
</body>''')


if __name__ == '__main__':
    main(*sys.argv[1:])