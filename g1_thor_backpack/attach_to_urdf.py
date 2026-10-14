"""Attach the frozen backpack to an existing URDF through one fixed joint."""
import argparse
import copy
import os
from pathlib import Path
import xml.etree.ElementTree as ET

def attach(source, output, parent='torso_link', xyz=None, rpy=None):
    source, output = Path(source).resolve(), Path(output).resolve()
    if output.exists():
        raise ValueError('Output already exists; choose a new file.')
    robot = ET.parse(source).getroot()
    if robot.tag != 'robot':
        raise ValueError('Input must be a URDF robot.')
    if robot.find(f"link[@name='{parent}']") is None:
        raise ValueError(f'No target parent link: {parent}')
    if robot.find("link[@name='thor_backpack_link']") is not None or robot.find("joint[@name='thor_backpack_joint']") is not None:
        raise ValueError('Target already contains this backpack link or joint.')
    actuated_before = [(j.get('name'), j.get('type')) for j in robot.findall('joint') if j.get('type') != 'fixed']
    # Keep target geometry paths valid when writing to a different directory.
    for mesh in robot.iter('mesh'):
        name = mesh.get('filename', '')
        if name and '://' not in name and not Path(name).is_absolute():
            mesh.set('filename', os.path.relpath(source.parent / name, output.parent))
    root = Path(__file__).resolve().parent
    fragment = ET.parse(root / 'urdf/backpack_fragment.urdf').getroot()
    link = copy.deepcopy(fragment.find('link'))
    joint = copy.deepcopy(fragment.find('joint'))
    joint.find('parent').set('link', parent)
    for key, value in [('xyz', xyz), ('rpy', rpy)]:
        if value is not None:
            joint.find('origin').set(key, ' '.join(str(x) for x in value))
    for mesh in link.iter('mesh'):
        mesh.set('filename', os.path.relpath(root / 'meshes/backpack_link.STL', output.parent))
    robot.extend([link, joint])
    actuated_after = [(j.get('name'), j.get('type')) for j in robot.findall('joint') if j.get('type') != 'fixed']
    assert actuated_before == actuated_after
    output.parent.mkdir(parents=True, exist_ok=True)
    ET.indent(robot, space='  ')
    ET.ElementTree(robot).write(output, encoding='utf-8', xml_declaration=True)
    print(f'Wrote {output}; non-fixed joints unchanged: {len(actuated_after)}; added one fixed joint.')

if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--input', required=True)
    p.add_argument('--output', required=True)
    p.add_argument('--parent', default='torso_link')
    p.add_argument('--xyz', type=float, nargs=3, help='Optional mount translation in target parent frame, metres.')
    p.add_argument('--rpy', type=float, nargs=3, help='Optional mount rotation in target parent frame, radians.')
    a = p.parse_args()
    attach(a.input, a.output, a.parent, a.xyz, a.rpy)
