import numpy as np
import xml.etree.ElementTree as ET
from xml.dom import minidom

def gyroid(x, y, z):
    return np.cos(x)*np.sin(y) + np.cos(y)*np.sin(z) + np.cos(z)*np.sin(x)

def iwp(x, y, z):
    return (2*(np.cos(x)*np.cos(y) + np.cos(y)*np.cos(z) + np.cos(z)*np.cos(x))
            - (np.cos(2*x)*np.cos(2*y) + np.cos(2*y)*np.cos(2*z) + np.cos(2*z)*np.cos(2*x)))

def primitive(x, y, z):
    return np.cos(x) + np.cos(y) + np.cos(z)

def isometric_project(x, y, z, scale=1.0, cx=0, cy=0):
    angle = np.pi / 6
    px = cx + (x - y) * np.cos(angle) * scale
    py = cy - z * scale + (x + y) * np.sin(angle) * scale
    return px, py

def extract_contour_segments(func, threshold=0.0, n_grid=40, domain=(0, 2*np.pi)):
    segments = []
    a, b = domain
    x = np.linspace(a, b, n_grid)
    y = np.linspace(a, b, n_grid)
    z_slices = np.linspace(a, b, 8)
    
    for z_val in z_slices:
        X, Y = np.meshgrid(x, y)
        Z = func(X, Y, np.full_like(X, z_val))
        for i in range(n_grid - 1):
            for j in range(n_grid - 1):
                v = [Z[i,j], Z[i+1,j], Z[i+1,j+1], Z[i,j+1]]
                above = [vi > threshold for vi in v]
                if any(above) and not all(above):
                    corners = [
                        (x[i], y[j]), (x[i+1], y[j]),
                        (x[i+1], y[j+1]), (x[i], y[j+1])
                    ]
                    cx_pt = np.mean([c[0] for c in corners])
                    cy_pt = np.mean([c[1] for c in corners])
                    segments.append((cx_pt, cy_pt, z_val))
    return segments

def generate_surface_paths(func, threshold=0.0, n_slices=12, n_points=60, 
                           domain=(0, 2*np.pi), scale=55.0, cx=0, cy=0):
    paths = []
    a, b = domain
    
    for z_idx in range(n_slices):
        z_val = a + (b - a) * z_idx / (n_slices - 1)
        t = np.linspace(0, 2*np.pi, n_points, endpoint=False)
        
        contour_pts = []
        for angle in t:
            r_range = np.linspace(0.1, 2.5, 80)
            found = False
            for method in ['spiral']:
                for a1 in np.linspace(0.5, 3.0, 30):
                    for a2 in np.linspace(0.5, 3.0, 30):
                        x_test = a1 * np.cos(angle)
                        y_test = a2 * np.sin(angle)
                        if abs(func(x_test, y_test, z_val)) < 0.15:
                            contour_pts.append((x_test, y_test, z_val))
                            found = True
                            break
                    if found:
                        break
        
        if len(contour_pts) > 5:
            projected = [isometric_project(p[0], p[1], p[2], scale, cx, cy) for p in contour_pts]
            paths.append(projected)
    
    return paths

def generate_tpms_contour_paths(func, threshold=0.0, n_z_slices=10, 
                                 grid_size=50, domain=(0, 2*np.pi),
                                 scale=55.0, cx=0, cy=0):
    all_paths = []
    a, b = domain
    z_vals = np.linspace(a + 0.3, b - 0.3, n_z_slices)
    
    for z_val in z_vals:
        xs = np.linspace(a, b, grid_size)
        ys = np.linspace(a, b, grid_size)
        X, Y = np.meshgrid(xs, ys)
        Z_vals = func(X, Y, np.full_like(X, z_val))
        
        pts_on_surface = []
        for i in range(grid_size):
            for j in range(grid_size):
                if abs(Z_vals[i, j]) < 0.25:
                    pts_on_surface.append((xs[j], ys[i], z_val))
        
        if len(pts_on_surface) > 3:
            projected = [isometric_project(p[0], p[1], p[2] - np.pi, scale, cx, cy) for p in pts_on_surface]
            all_paths.append((projected, z_val))
    
    return all_paths

def points_to_svg_path(points, close=True):
    if len(points) < 2:
        return ""
    d = f"M {points[0][0]:.1f},{points[0][1]:.1f}"
    for i in range(1, len(points)):
        d += f" L {points[i][0]:.1f},{points[i][1]:.1f}"
    if close:
        d += " Z"
    return d

def create_wireframe_cube(cx, cy, size, scale=55.0):
    s = size / 2
    vertices = [
        (-s, -s, -s), (s, -s, -s), (s, s, -s), (-s, s, -s),
        (-s, -s, s), (s, -s, s), (s, s, s), (-s, s, s)
    ]
    projected = [isometric_project(v[0], v[1], v[2], scale, cx, cy) for v in vertices]
    
    edges = [
        (0,1), (1,2), (2,3), (3,0),
        (4,5), (5,6), (6,7), (7,4),
        (0,4), (1,5), (2,6), (3,7)
    ]
    back_edges = [(0,1), (0,3), (3,2), (0,4)]
    
    lines = []
    for e in edges:
        p1 = projected[e[0]]
        p2 = projected[e[1]]
        is_back = e in back_edges
        lines.append((p1, p2, is_back))
    
    return lines

def create_drawio_xml():
    cell_id = [2]
    
    def next_id():
        cell_id[0] += 1
        return str(cell_id[0])
    
    root = ET.Element('mxfile', host='app.diagrams.net', 
                      modified='2026-08-10T00:00:00.000Z',
                      agent='draw.io', version='24.0.0', type='device')
    diagram = ET.SubElement(root, 'diagram', name='TPMS Structures', id='tpms-structures')
    
    page_w, page_h = 2550, 1100
    model = ET.SubElement(diagram, 'mxGraphModel', 
                          dx='1422', dy='794', grid='1', gridSize='10',
                          guides='1', tooltips='1', connect='1', arrows='1',
                          fold='1', page='1', pageScale='1',
                          pageWidth=str(page_w), pageHeight=str(page_h),
                          math='0', shadow='0')
    
    root_cell = ET.SubElement(model, 'root')
    ET.SubElement(root_cell, 'mxCell', id='0')
    ET.SubElement(root_cell, 'mxCell', id='1', parent='0')
    
    cells = []
    
    def add_cell(value, style, x, y, w, h, parent='1', vertex='1'):
        cid = next_id()
        cells.append({
            'id': cid, 'value': value, 'style': style,
            'x': x, 'y': y, 'w': w, 'h': h,
            'parent': parent, 'vertex': vertex
        })
        return cid
    
    def add_edge(style, points, parent='1'):
        cid = next_id()
        cells.append({
            'id': cid, 'type': 'edge', 'style': style,
            'points': points, 'parent': parent
        })
        return cid
    
    panel_w, panel_h = 750, 850
    panel_y = 100
    panel_gap = 50
    start_x = 100
    
    panels = [
        {'cx': start_x + panel_w/2, 'label': 'A', 'name': 'Gyroid',
         'desc': 'Single continuous channel\nwith chiral symmetry',
         'func': gyroid, 'color1': '#3B7DD8', 'color2': '#5B9BD5', 'color3': '#A8CCE8'},
        {'cx': start_x + panel_w + panel_gap + panel_w/2, 'label': 'B', 'name': 'IWP',
         'desc': 'Two independent interpenetrating\nchannels with cage-like enclosure',
         'func': iwp, 'color1': '#3B7DD8', 'color2': '#7B8FA1', 'color3': '#B8C5D6'},
        {'cx': start_x + 2*(panel_w + panel_gap) + panel_w/2, 'label': 'C', 'name': 'Primitive',
         'desc': 'Two independent channels\nconnected through periodic openings',
         'func': primitive, 'color1': '#3B7DD8', 'color2': '#7B8FA1', 'color3': '#B8C5D6'},
    ]
    
    title_x = start_x
    title_w = 3 * panel_w + 2 * panel_gap
    add_cell('Three TPMS topologies investigated in this study',
             'text;html=1;strokeColor=none;fillColor=none;align=center;'
             'verticalAlign=middle;whiteSpace=wrap;rounded=0;'
             'fontSize=18;fontStyle=1;fontColor=#2C3E50;fontFamily=Arial;',
             title_x, 30, title_w, 45)
    
    for pi, panel in enumerate(panels):
        px = start_x + pi * (panel_w + panel_gap)
        pcx = px + panel_w / 2
        pcy = panel_y + panel_h / 2 - 30
        
        add_cell('', 
                 f'rounded=1;whiteSpace=wrap;html=1;fillColor=#FAFBFD;'
                 f'strokeColor=#C8D4E0;strokeWidth=2;arcSize=4;',
                 px, panel_y, panel_w, panel_h)
        
        add_cell(panel['label'],
                 'text;html=1;strokeColor=none;fillColor=none;align=left;'
                 'verticalAlign=top;whiteSpace=wrap;rounded=0;'
                 'fontSize=22;fontStyle=1;fontColor=#2C5F8D;fontFamily=Arial;',
                 px + 15, panel_y + 10, 40, 40)
        
        cube_cx = pcx
        cube_cy = pcy - 20
        cube_size = 2.8
        cube_scale = 75.0
        
        wireframe = create_wireframe_cube(cube_cx, cube_cy, cube_size, cube_scale)
        for p1, p2, is_back in wireframe:
            dash = 'dashed=1;' if is_back else ''
            stroke_w = 1 if is_back else 2
            opacity = 40 if is_back else 70
            add_edge(
                f'endArrow=none;html=1;rounded=0;strokeColor=#8A9BAD;'
                f'strokeWidth={stroke_w};{dash}opacity={opacity};',
                [(p1[0], p1[1]), (p2[0], p2[1])]
            )
        
        func = panel['func']
        n_z = 14
        grid = 60
        domain = (0.2, 2*np.pi - 0.2)
        
        contour_data = generate_tpms_contour_paths(
            func, threshold=0.0, n_z_slices=n_z,
            grid_size=grid, domain=domain,
            scale=cube_scale, cx=cube_cx, cy=cube_cy
        )
        
        for idx, (points, z_val) in enumerate(contour_data):
            if len(points) < 3:
                continue
            
            z_norm = (z_val - domain[0]) / (domain[1] - domain[0])
            
            sorted_pts = sorted(points, key=lambda p: (p[0], p[1]))
            
            if len(sorted_pts) > 4:
                min_x = min(p[0] for p in sorted_pts)
                max_x = max(p[0] for p in sorted_pts)
                min_y = min(p[1] for p in sorted_pts)
                max_y = max(p[1] for p in sorted_pts)
                
                center_x = (min_x + max_x) / 2
                center_y = (min_y + max_y) / 2
                width = max(max_x - min_x, 5)
                height = max(max_y - min_y, 5)
                
                opacity = 15 + int(25 * (1 - abs(z_norm - 0.5) * 2))
                
                blue_val = int(0xD6 - z_norm * 0x40)
                green_val = int(0x8F + z_norm * 0x20)
                fill_color = f'#3B{blue_val:02X}' if blue_val < 256 else '#3B7DD8'
                
                color_choice = panel['color1'] if z_norm < 0.33 else (panel['color2'] if z_norm < 0.66 else panel['color3'])
                
                add_cell('',
                         f'ellipse;fillColor={color_choice};strokeColor=none;'
                         f'opacity={opacity};html=1;',
                         center_x - width/2, center_y - height/2,
                         width, height)
        
        for z_idx in range(n_z):
            z_val = domain[0] + (domain[1] - domain[0]) * z_idx / (n_z - 1)
            z_norm = z_idx / (n_z - 1)
            
            t = np.linspace(0.3, 2*np.pi - 0.3, 80)
            contour_line_pts = []
            
            for angle_param in t:
                r_vals = np.linspace(0.3, 2.8, 100)
                best_pt = None
                best_val = float('inf')
                
                for r in r_vals:
                    x_test = r * np.cos(angle_param) + np.pi
                    y_test = r * np.sin(angle_param) + np.pi
                    if 0 < x_test < 2*np.pi and 0 < y_test < 2*np.pi:
                        val = func(x_test, y_test, z_val)
                        if abs(val) < abs(best_val):
                            best_val = val
                            best_pt = (x_test - np.pi, y_test - np.pi, z_val - np.pi)
                
                if best_pt is not None and abs(best_val) < 0.2:
                    proj = isometric_project(best_pt[0], best_pt[1], best_pt[2], 
                                            cube_scale, cube_cx, cube_cy)
                    contour_line_pts.append(proj)
            
            if len(contour_line_pts) > 3:
                opacity = 30 + int(40 * (1 - abs(z_norm - 0.5) * 2))
                stroke_w = 1.5 if z_norm > 0.3 and z_norm < 0.7 else 1.0
                
                color_choice = panel['color1'] if z_norm < 0.33 else (panel['color2'] if z_norm < 0.66 else panel['color3'])
                
                path_d = f"M {contour_line_pts[0][0]:.1f},{contour_line_pts[0][1]:.1f}"
                for pt in contour_line_pts[1:]:
                    path_d += f" L {pt[0]:.1f},{pt[1]:.1f}"
                
                add_cell('',
                         f'shape=mxgraph.basic.rect;fillColor=none;'
                         f'strokeColor=none;html=1;opacity=0;',
                         contour_line_pts[0][0], contour_line_pts[0][1], 1, 1)
        
        for z_idx in range(n_z):
            z_val = domain[0] + (domain[1] - domain[0]) * z_idx / (n_z - 1)
            z_norm = z_idx / (n_z - 1)
            
            t = np.linspace(0.3, 2*np.pi - 0.3, 120)
            contour_line_pts = []
            
            for angle_param in t:
                r_vals = np.linspace(0.2, 3.0, 150)
                best_pt = None
                best_val = float('inf')
                
                for r in r_vals:
                    x_test = r * np.cos(angle_param) + np.pi
                    y_test = r * np.sin(angle_param) + np.pi
                    if 0.1 < x_test < 2*np.pi - 0.1 and 0.1 < y_test < 2*np.pi - 0.1:
                        val = func(x_test, y_test, z_val)
                        if abs(val) < abs(best_val):
                            best_val = val
                            best_pt = (x_test - np.pi, y_test - np.pi, z_val - np.pi)
                
                if best_pt is not None and abs(best_val) < 0.15:
                    proj = isometric_project(best_pt[0], best_pt[1], best_pt[2], 
                                            cube_scale, cube_cx, cube_cy)
                    contour_line_pts.append(proj)
            
            if len(contour_line_pts) > 5:
                opacity = 35 + int(45 * (1 - abs(z_norm - 0.5) * 2))
                stroke_w = 2.0 if 0.3 < z_norm < 0.7 else 1.2
                
                color_choice = panel['color1'] if z_norm < 0.4 else panel['color2']
                
                pts_str = ';'.join([f'{p[0]:.1f},{p[1]:.1f}' for p in contour_line_pts])
                
                add_edge(
                    f'endArrow=none;html=1;rounded=1;curved=1;'
                    f'strokeColor={color_choice};strokeWidth={stroke_w};'
                    f'opacity={opacity};',
                    [(contour_line_pts[0][0], contour_line_pts[0][1]),
                     (contour_line_pts[-1][0], contour_line_pts[-1][1])]
                )
        
        add_cell(panel['name'],
                 'text;html=1;strokeColor=none;fillColor=none;align=center;'
                 'verticalAlign=middle;whiteSpace=wrap;rounded=0;'
                 'fontSize=20;fontStyle=1;fontColor=#2C5F8D;fontFamily=Arial;',
                 pcx - 100, panel_y + panel_h - 160, 200, 35)
        
        add_cell(panel['desc'],
                 'text;html=1;strokeColor=none;fillColor=none;align=center;'
                 'verticalAlign=top;whiteSpace=wrap;rounded=0;'
                 'fontSize=11;fontColor=#5A6B7D;fontFamily=Arial;spacing=2;',
                 pcx - 150, panel_y + panel_h - 125, 300, 50)
        
        formulas = {
            'Gyroid': 'cos(x)sin(y) + cos(y)sin(z) + cos(z)sin(x) = 0',
            'IWP': '2[\u2211cos(x)cos(y)] \u2212 [\u2211cos(2x)cos(2y)] = \u22122',
            'Primitive': 'cos(x) + cos(y) + cos(z) = 0'
        }
        
        add_cell(formulas[panel['name']],
                 'text;html=0;strokeColor=none;fillColor=none;align=center;'
                 'verticalAlign=middle;whiteSpace=wrap;rounded=0;'
                 'fontSize=9;fontColor=#8A9BAD;fontStyle=2;fontFamily=Arial;',
                 pcx - 175, panel_y + panel_h - 65, 350, 20)
    
    for c in cells:
        if c.get('type') == 'edge':
            edge = ET.SubElement(root_cell, 'mxCell',
                                id=c['id'], value='', style=c['style'],
                                edge='1', parent=c.get('parent', '1'))
            geo = ET.SubElement(edge, 'mxGeometry', relative='1')
            geo.set('as', 'geometry')
            pts = c['points']
            if len(pts) >= 2:
                src = ET.SubElement(geo, 'mxPoint', x=str(pts[0][0]), y=str(pts[0][1]))
                src.set('as', 'sourcePoint')
                tgt = ET.SubElement(geo, 'mxPoint', x=str(pts[-1][0]), y=str(pts[-1][1]))
                tgt.set('as', 'targetPoint')
                if len(pts) > 2:
                    arr = ET.SubElement(geo, 'Array')
                    arr.set('as', 'points')
                    for mid_pt in pts[1:-1]:
                        ET.SubElement(arr, 'mxPoint', x=str(mid_pt[0]), y=str(mid_pt[1]))
        else:
            vertex = ET.SubElement(root_cell, 'mxCell',
                                  id=c['id'], value=c.get('value', ''),
                                  style=c['style'], vertex=c.get('vertex', '1'),
                                  parent=c.get('parent', '1'))
            geo = ET.SubElement(vertex, 'mxGeometry',
                               x=str(c['x']), y=str(c['y']),
                               width=str(c['w']), height=str(c['h']))
            geo.set('as', 'geometry')
    
    xml_str = ET.tostring(root, encoding='unicode')
    try:
        dom = minidom.parseString(xml_str)
        return dom.toprettyxml(indent='  ', encoding=None)
    except:
        return f'<?xml version="1.0" encoding="UTF-8"?>\n{xml_str}'

if __name__ == '__main__':
    xml_content = create_drawio_xml()
    
    if xml_content.startswith("<?xml"):
        lines = xml_content.split('\n')
        out_lines = []
        for line in lines:
            if line.strip().startswith('<?xml'):
                out_lines.append('<?xml version="1.0" encoding="UTF-8"?>')
            else:
                out_lines.append(line)
        xml_content = '\n'.join(out_lines)
    
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(script_dir, 'tpms_structures.drawio')
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(xml_content)
    
    print(f"Generated: {output_path}")
    print(f"File size: {os.path.getsize(output_path)} bytes")
