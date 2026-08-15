"""
9个热电偶在样品中的三维轴测图
"""
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

# 样品尺寸（单位：mm）
sample_size = 50  # 50mm x 50mm
sample_height = 20  # 20mm 高

# 传感器位置定义
# T1: 底面中心
t1 = (0, 0, 0)

# T2-T5: 中间层（z = 10mm），边长25mm正方形的4个角
z_mid = 10  # 10mm
side_mid = 25  # 边长25mm
h_mid = side_mid / 2  # 半边长12.5mm
t2 = (-h_mid, -h_mid, z_mid)
t3 = (h_mid, -h_mid, z_mid)
t4 = (h_mid, h_mid, z_mid)
t5 = (-h_mid, h_mid, z_mid)

# T6-T9: 上表面（z = 20mm），边长25mm正方形的四个边中心点
z_top = 20  # 20mm
side_top = 25  # 边长25mm
h_top = side_top / 2  # 半边长12.5mm
t6 = (-h_top, 0, z_top)
t7 = (0, -h_top, z_top)
t8 = (h_top, 0, z_top)
t9 = (0, h_top, z_top)

# 创建图形 - 使用轴测投影
fig = plt.figure(figsize=(16, 12))
ax = fig.add_subplot(111, projection='3d')

# 设置轴测视图（等轴测）——azim=60 使 T4 不再遮挡 T1
ax.view_init(elev=35, azim=60)

# 绘制样品 - 使用半透明面
# 底面
verts_bottom = [
    [(-sample_size/2, -sample_size/2, 0), (sample_size/2, -sample_size/2, 0), 
     (sample_size/2, sample_size/2, 0), (-sample_size/2, sample_size/2, 0)]
]
bottom_face = Poly3DCollection(verts_bottom, alpha=0.1, facecolor='lightblue', edgecolor='black', linewidth=2)
ax.add_collection3d(bottom_face)

# 顶面
verts_top = [
    [(-sample_size/2, -sample_size/2, sample_height), (sample_size/2, -sample_size/2, sample_height), 
     (sample_size/2, sample_size/2, sample_height), (-sample_size/2, sample_size/2, sample_height)]
]
top_face = Poly3DCollection(verts_top, alpha=0.1, facecolor='lightcoral', edgecolor='black', linewidth=2)
ax.add_collection3d(top_face)

# 前面（Y = -sample_size/2）
verts_front = [
    [(-sample_size/2, -sample_size/2, 0), (sample_size/2, -sample_size/2, 0), 
     (sample_size/2, -sample_size/2, sample_height), (-sample_size/2, -sample_size/2, sample_height)]
]
front_face = Poly3DCollection(verts_front, alpha=0.05, facecolor='lightyellow', edgecolor='black', linewidth=2)
ax.add_collection3d(front_face)

# 右面（X = sample_size/2）
verts_right = [
    [(sample_size/2, -sample_size/2, 0), (sample_size/2, sample_size/2, 0), 
     (sample_size/2, sample_size/2, sample_height), (sample_size/2, -sample_size/2, sample_height)]
]
right_face = Poly3DCollection(verts_right, alpha=0.05, facecolor='lightyellow', edgecolor='black', linewidth=2)
ax.add_collection3d(right_face)

# 绘制中间层传感器正方形（z = 10mm，边长25mm，连接T2-T5）
mid_square = [t2, t3, t4, t5, t2]
for i in range(4):
    ax.plot([mid_square[i][0], mid_square[i+1][0]],
            [mid_square[i][1], mid_square[i+1][1]],
            [mid_square[i][2], mid_square[i+1][2]],
            'b--', linewidth=1.5, alpha=0.6)

# 绘制上层传感器正方形（z = 20mm，边长25mm，连接T6-T9，相对中层旋转45度）
top_square = [t6, t7, t8, t9, t6]
for i in range(4):
    ax.plot([top_square[i][0], top_square[i+1][0]],
            [top_square[i][1], top_square[i+1][1]],
            [top_square[i][2], top_square[i+1][2]],
            'g--', linewidth=1.5, alpha=0.6)

# 绘制传感器位置
sensors = {
    'T1': t1,
    'T2': t2, 'T3': t3, 'T4': t4, 'T5': t5,
    'T6': t6, 'T7': t7, 'T8': t8, 'T9': t9
}

colors = {
    'T1': 'red',
    'T2': 'blue', 'T3': 'blue', 'T4': 'blue', 'T5': 'blue',
    'T6': 'green', 'T7': 'green', 'T8': 'green', 'T9': 'green'
}

# 绘制传感器点
for name, pos in sensors.items():
    # 绘制传感器球体
    ax.scatter(pos[0], pos[1], pos[2], s=400, c=colors[name], marker='o', 
               edgecolors='black', linewidths=2.5, zorder=10, depthshade=False)
    
    # 添加标签（带背景框）
    label_offset = 3
    ax.text(pos[0], pos[1], pos[2] + label_offset, name, 
            fontsize=16, fontweight='bold', ha='center', va='bottom',
            color=colors[name],
            bbox=dict(boxstyle='round,pad=0.4', facecolor='white', 
                     edgecolor=colors[name], alpha=0.95, linewidth=2))

# 绘制加热器（底面中心圆盘）
heater_radius = 10
theta = np.linspace(0, 2*np.pi, 60)
heater_x = heater_radius * np.cos(theta)
heater_y = heater_radius * np.sin(theta)
heater_z = np.full_like(theta, -2)  # 略低于底面

# 绘制加热器圆盘
ax.plot(heater_x, heater_y, heater_z, 'r-', linewidth=3, alpha=0.8)
# 填充加热器
verts_heater = []
for i in range(len(theta)-1):
    verts_heater.append([
        (0, 0, -2),
        (heater_x[i], heater_y[i], -2),
        (heater_x[i+1], heater_y[i+1], -2)
    ])
heater_face = Poly3DCollection(verts_heater, alpha=0.3, facecolor='red', edgecolor='none')
ax.add_collection3d(heater_face)

# 添加加热器标签
ax.text(0, 0, -5, 'Heater\n(Dia.20mm)', fontsize=11, fontweight='bold',
        ha='center', va='top', color='red',
        bbox=dict(boxstyle='round,pad=0.3', facecolor='white', 
                 edgecolor='red', alpha=0.9, linewidth=1.5))

# 设置坐标轴
ax.set_xlabel('X (mm)', fontsize=13, fontweight='bold', labelpad=15)
ax.set_ylabel('Y (mm)', fontsize=13, fontweight='bold', labelpad=15)
ax.set_zlabel('Z (mm)', fontsize=13, fontweight='bold', labelpad=15)

# 设置标题
ax.set_title('Thermocouple Layout in TPMS/PCM Sample\nIsometric View', 
             fontsize=16, fontweight='bold', pad=25)

# 设置坐标轴范围
margin = 8
ax.set_xlim([-sample_size/2 - margin, sample_size/2 + margin])
ax.set_ylim([-sample_size/2 - margin, sample_size/2 + margin])
ax.set_zlim([-12, sample_height + margin])

# 设置等比例坐标轴
ax.set_box_aspect((1, 1, 1))

# 添加图例说明
legend_text = """
Sensor Groups:
  T1 (Red):    Group A - Bottom center (z=0mm)
  T2-T5 (Blue): Group B - Mid-layer (z=10mm), corners of 25mm square
  T6-T9 (Green): Group C - Top surface (z=20mm), edge midpoints of 25mm square
                (top square rotated 45 deg vs mid square)

Sample: 50x50x20 mm^3
Heater: Dia.20mm cartridge heater
"""
ax.text2D(0.02, 0.98, legend_text, transform=ax.transAxes, 
          fontsize=11, verticalalignment='top', family='monospace',
          bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.95, 
                   edgecolor='gray', linewidth=1.5))

# 添加尺寸标注
# X方向尺寸
ax.plot([-sample_size/2, sample_size/2], [-sample_size/2-5, -sample_size/2-5], [0, 0], 
        'k-', linewidth=1)
ax.plot([-sample_size/2, -sample_size/2], [-sample_size/2-5, -sample_size/2-3], [0, 0], 
        'k-', linewidth=1)
ax.plot([sample_size/2, sample_size/2], [-sample_size/2-5, -sample_size/2-3], [0, 0], 
        'k-', linewidth=1)
ax.text(0, -sample_size/2-7, 0, '50mm', fontsize=10, ha='center', va='top', fontweight='bold')

# Z方向尺寸
ax.plot([sample_size/2+5, sample_size/2+5], [-sample_size/2, -sample_size/2], [0, sample_height], 
        'k-', linewidth=1)
ax.plot([sample_size/2+3, sample_size/2+5], [-sample_size/2, -sample_size/2], [0, 0], 
        'k-', linewidth=1)
ax.plot([sample_size/2+3, sample_size/2+5], [-sample_size/2, -sample_size/2], [sample_height, sample_height], 
        'k-', linewidth=1)
ax.text(sample_size/2+7, -sample_size/2, sample_height/2, '20mm', fontsize=10, 
        ha='left', va='center', fontweight='bold', rotation=90)

plt.tight_layout()
plt.savefig('output/paper/figures/thermocouple_isometric.png', dpi=300, bbox_inches='tight')
plt.savefig('output/paper/figures/thermocouple_isometric.pdf', bbox_inches='tight')
print('Saved: thermocouple_isometric.png/pdf')

# 创建第二个视图 - 带尺寸标注的详细图
fig2 = plt.figure(figsize=(14, 10))
ax2 = fig2.add_subplot(111, projection='3d')
# 详细图视角——azim=75 进一步错开 T4 与 T1
ax2.view_init(elev=30, azim=75)

# 只绘制线框（更清晰）
# 底面
ax2.plot([-sample_size/2, sample_size/2, sample_size/2, -sample_size/2, -sample_size/2],
         [-sample_size/2, -sample_size/2, sample_size/2, sample_size/2, -sample_size/2],
         [0, 0, 0, 0, 0], 'k-', linewidth=2.5)

# 顶面
ax2.plot([-sample_size/2, sample_size/2, sample_size/2, -sample_size/2, -sample_size/2],
         [-sample_size/2, -sample_size/2, sample_size/2, sample_size/2, -sample_size/2],
         [sample_height, sample_height, sample_height, sample_height, sample_height], 'k-', linewidth=2.5)

# 竖直边
for x, y in [(-sample_size/2, -sample_size/2), (sample_size/2, -sample_size/2), 
             (sample_size/2, sample_size/2), (-sample_size/2, sample_size/2)]:
    ax2.plot([x, x], [y, y], [0, sample_height], 'k-', linewidth=2.5)

# 中间层虚线
ax2.plot([-sample_size/2, sample_size/2, sample_size/2, -sample_size/2, -sample_size/2],
         [-sample_size/2, -sample_size/2, sample_size/2, sample_size/2, -sample_size/2],
         [z_mid, z_mid, z_mid, z_mid, z_mid], 'g--', linewidth=2, alpha=0.7)

# 绘制传感器
for name, pos in sensors.items():
    ax2.scatter(pos[0], pos[1], pos[2], s=500, c=colors[name], marker='o', 
                edgecolors='black', linewidths=3, zorder=10, depthshade=False)
    
    # 详细标签
    label_text = f"{name}\nz={pos[2]:.0f}mm"
    ax2.text(pos[0], pos[1], pos[2] + 4, label_text, 
             fontsize=12, fontweight='bold', ha='center', va='bottom',
             color=colors[name],
             bbox=dict(boxstyle='round,pad=0.4', facecolor='white', 
                      edgecolor=colors[name], alpha=0.95, linewidth=2))

# 加热器
ax2.plot(heater_x, heater_y, heater_z, 'r-', linewidth=3, alpha=0.8)
ax2.text(0, 0, -6, 'Heater', fontsize=12, fontweight='bold',
         ha='center', va='top', color='red',
         bbox=dict(boxstyle='round,pad=0.3', facecolor='white', 
                  edgecolor='red', alpha=0.95, linewidth=2))

# 设置
ax2.set_xlabel('X (mm)', fontsize=13, fontweight='bold', labelpad=15)
ax2.set_ylabel('Y (mm)', fontsize=13, fontweight='bold', labelpad=15)
ax2.set_zlabel('Z (mm)', fontsize=13, fontweight='bold', labelpad=15)
ax2.set_title('Detailed Isometric View with Dimensions', fontsize=16, fontweight='bold', pad=25)
ax2.set_xlim([-sample_size/2 - 10, sample_size/2 + 10])
ax2.set_ylim([-sample_size/2 - 10, sample_size/2 + 10])
ax2.set_zlim([-15, sample_height + 10])
ax2.set_box_aspect((1, 1, 1))

plt.tight_layout()
plt.savefig('output/paper/figures/thermocouple_isometric_detailed.png', dpi=300, bbox_inches='tight')
plt.savefig('output/paper/figures/thermocouple_isometric_detailed.pdf', bbox_inches='tight')
print('Saved: thermocouple_isometric_detailed.png/pdf')

print('\nAll isometric views saved.')
