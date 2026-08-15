"""
9个热电偶在样品中的三维布放位置图
"""
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# 样品尺寸（假设正方形截面，单位：mm）
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
z_top = sample_height
side_top = 25  # 边长25mm
h_top = side_top / 2  # 半边长12.5mm
t6 = (-h_top, 0, z_top)
t7 = (0, -h_top, z_top)
t8 = (h_top, 0, z_top)
t9 = (0, h_top, z_top)

# 创建图形
fig = plt.figure(figsize=(14, 10))
ax = fig.add_subplot(111, projection='3d')

# 绘制样品边框（立方体线框）
edges = [
    # 底面边框
    ([-sample_size/2, -sample_size/2, 0], [sample_size/2, -sample_size/2, 0]),
    ([sample_size/2, -sample_size/2, 0], [sample_size/2, sample_size/2, 0]),
    ([sample_size/2, sample_size/2, 0], [-sample_size/2, sample_size/2, 0]),
    ([-sample_size/2, sample_size/2, 0], [-sample_size/2, -sample_size/2, 0]),
    # 顶面边框
    ([-sample_size/2, -sample_size/2, sample_height], [sample_size/2, -sample_size/2, sample_height]),
    ([sample_size/2, -sample_size/2, sample_height], [sample_size/2, sample_size/2, sample_height]),
    ([sample_size/2, sample_size/2, sample_height], [-sample_size/2, sample_size/2, sample_height]),
    ([-sample_size/2, sample_size/2, sample_height], [-sample_size/2, -sample_size/2, sample_height]),
    # 竖直边框
    ([-sample_size/2, -sample_size/2, 0], [-sample_size/2, -sample_size/2, sample_height]),
    ([sample_size/2, -sample_size/2, 0], [sample_size/2, -sample_size/2, sample_height]),
    ([sample_size/2, sample_size/2, 0], [sample_size/2, sample_size/2, sample_height]),
    ([-sample_size/2, sample_size/2, 0], [-sample_size/2, sample_size/2, sample_height]),
]
for edge in edges:
    ax.plot3D([edge[0][0], edge[1][0]], [edge[0][1], edge[1][1]], [edge[0][2], edge[1][2]], 
              'k-', linewidth=2, alpha=0.6)

# 绘制中间层传感器正方形（z = 10mm，边长25mm，连接T2-T5）
mid_square = [t2, t3, t4, t5, t2]
for i in range(4):
    ax.plot3D([mid_square[i][0], mid_square[i+1][0]], 
              [mid_square[i][1], mid_square[i+1][1]], 
              [mid_square[i][2], mid_square[i+1][2]], 
              'b--', linewidth=1.5, alpha=0.6)

# 绘制上层传感器正方形（z = 20mm，边长25mm，连接T6-T9，相对中层旋转45度）
top_square = [t6, t7, t8, t9, t6]
for i in range(4):
    ax.plot3D([top_square[i][0], top_square[i+1][0]], 
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
    ax.scatter(pos[0], pos[1], pos[2], s=300, c=colors[name], marker='o', 
               edgecolors='black', linewidths=2, zorder=10, depthshade=False)
    # 添加标签
    ax.text(pos[0], pos[1], pos[2] + 2.5, name, fontsize=14, fontweight='bold',
            ha='center', va='bottom', color=colors[name],
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white', 
                     edgecolor=colors[name], alpha=0.9, linewidth=1.5))

# 绘制加热器（底面中心圆盘，用线条表示）
heater_radius = 10
theta = np.linspace(0, 2*np.pi, 50)
heater_x = heater_radius * np.cos(theta)
heater_y = heater_radius * np.sin(theta)
heater_z = np.zeros_like(theta) - 3  # 略低于底面
ax.plot(heater_x, heater_y, heater_z, 'r-', linewidth=3, alpha=0.7)
# 添加十字线表示加热器中心
ax.plot([-heater_radius, heater_radius], [0, 0], [-3, -3], 'r-', linewidth=2, alpha=0.5)
ax.plot([0, 0], [-heater_radius, heater_radius], [-3, -3], 'r-', linewidth=2, alpha=0.5)

# 设置坐标轴
ax.set_xlabel('X (mm)', fontsize=12, fontweight='bold', labelpad=10)
ax.set_ylabel('Y (mm)', fontsize=12, fontweight='bold', labelpad=10)
ax.set_zlabel('Z (mm)', fontsize=12, fontweight='bold', labelpad=10)
ax.set_title('Thermocouple Layout in TPMS/PCM Sample\n9 Thermocouples 3D Position', 
             fontsize=14, fontweight='bold', pad=20)

# 设置坐标轴范围
ax.set_xlim([-sample_size/2 - 5, sample_size/2 + 5])
ax.set_ylim([-sample_size/2 - 5, sample_size/2 + 5])
ax.set_zlim([-10, sample_height + 10])

# 添加图例说明
legend_text = """
Sensor Layout:
 T1 (Red): Bottom center (z=0mm)
 T2-T5 (Blue): Mid-layer (z=10mm), corners of 25mm square
 T6-T9 (Green): Top surface (z=20mm), edge midpoints of 25mm square
                (top square rotated 45 deg vs mid square)

Sample: 50x50x20 mm^3
Heater: Dia.20mm cartridge at bottom
"""
ax.text2D(0.02, 0.98, legend_text, transform=ax.transAxes, 
          fontsize=10, verticalalignment='top', family='monospace',
          bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.9, 
                   edgecolor='gray', linewidth=1))

# 设置视角——azim=60 使 T4 不再遮挡 T1
ax.view_init(elev=35, azim=60)

plt.tight_layout()
plt.savefig('output/paper/figures/thermocouple_layout_3d.png', dpi=300, bbox_inches='tight')
plt.savefig('output/paper/figures/thermocouple_layout_3d.pdf', bbox_inches='tight')
print('Saved: thermocouple_layout_3d.png/pdf')

# 创建第二个视图（俯视图）
fig2 = plt.figure(figsize=(10, 8))
ax2 = fig2.add_subplot(111)

# 绘制样品轮廓
sample_rect = plt.Rectangle((-sample_size/2, -sample_size/2), sample_size, sample_size,
                             fill=False, edgecolor='black', linewidth=2.5)
ax2.add_patch(sample_rect)

# 绘制中间层传感器正方形（边长25mm，连接T2-T5）
mid_sq_pts = [t2, t3, t4, t5, t2]
mx, my = zip(*[(p[0], p[1]) for p in mid_sq_pts])
ax2.plot(mx, my, 'b--', linewidth=1.5, alpha=0.6)
ax2.text(0, h_mid + 4, 'Mid square (0 deg)', fontsize=9, color='blue', fontweight='bold',
         ha='center', va='bottom')

# 绘制上层传感器正方形（边长25mm，旋转45度，连接T6-T9）
top_sq_pts = [t6, t7, t8, t9, t6]
tx, ty = zip(*[(p[0], p[1]) for p in top_sq_pts])
ax2.plot(tx, ty, 'g--', linewidth=1.5, alpha=0.6)
ax2.text(h_top + 4, 0, 'Top square (45 deg)', fontsize=9, color='green', fontweight='bold',
         ha='left', va='center', rotation=45)

# 绘制传感器位置（投影到XY平面，zorder高于加热器）
for name, pos in sensors.items():
    ax2.scatter(pos[0], pos[1], s=300, c=colors[name], marker='o', 
                edgecolors='black', linewidths=2, zorder=20)
    # 添加标签和Z坐标
    label = f"{name}\n(z={pos[2]:.0f}mm)"
    ax2.text(pos[0], pos[1] + 3.5, label, fontsize=10, fontweight='bold',
             ha='center', va='bottom', 
             bbox=dict(boxstyle='round,pad=0.3', facecolor='white', 
                      edgecolor=colors[name], alpha=0.9, linewidth=1.5))

# 绘制加热器（zorder低于传感器，避免遮挡T1）
heater_circle = plt.Circle((0, 0), heater_radius, fill=True, 
                           facecolor='red', alpha=0.3, edgecolor='red', linewidth=2.5,
                           zorder=5)
ax2.add_patch(heater_circle)
ax2.text(0, -heater_radius - 6, 'Heater\n(Dia.20mm)', fontsize=10, 
         ha='center', va='top', color='red', fontweight='bold')

# 设置坐标轴
ax2.set_xlabel('X (mm)', fontsize=12, fontweight='bold')
ax2.set_ylabel('Y (mm)', fontsize=12, fontweight='bold')
ax2.set_title('Top View: Thermocouple Layout', 
              fontsize=14, fontweight='bold')
ax2.set_xlim([-sample_size/2 - 10, sample_size/2 + 10])
ax2.set_ylim([-sample_size/2 - 18, sample_size/2 + 10])
ax2.set_aspect('equal')
ax2.grid(True, alpha=0.3)

# 添加图例
legend_text2 = """
Sensor Groups:
 T1 (Red): Group A - Bottom center (z=0mm)
 T2-T5 (Blue): Group B - Mid-layer (z=10mm), corners of 25mm square
 T6-T9 (Green): Group C - Top surface (z=20mm), edge midpoints of 25mm square

B and C groups on concentric 25mm squares (rotated 45 deg)
"""
ax2.text(0.02, 0.98, legend_text2, transform=ax2.transAxes, 
         fontsize=10, verticalalignment='top', family='monospace',
         bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.9,
                  edgecolor='gray', linewidth=1))

plt.tight_layout()
plt.savefig('output/paper/figures/thermocouple_layout_top.png', dpi=300, bbox_inches='tight')
plt.savefig('output/paper/figures/thermocouple_layout_top.pdf', bbox_inches='tight')
print('Saved: thermocouple_layout_top.png/pdf')

print('\nAll plots saved.')
