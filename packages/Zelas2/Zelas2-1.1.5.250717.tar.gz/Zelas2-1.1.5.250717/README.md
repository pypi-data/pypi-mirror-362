Warming：推荐的pyvista版本为0.43.7，推荐的vtk版本为9.4.1

1.1.5250717更新日志

1.shield_plus

(1).Curvature_r_mp:按照球半径并行计算曲率(建议每次数据量不要超过3个盾构环)
(2).Curvature_r_block:分块按照球半径计算曲率
(3).Curvature_r_block:非并行按照球半径计算曲率

1.1.4.250714更新日志

1.shield_plus

(1).find_CS_25: 环缝提取_固定长度版_25年修补版
(2).fit_3d_circle: 拟合单个三维圆
(3).fit_3d_circle_mp: 并行拟合三维圆
(4).STSD_add_C: 对STSD数据集添加截面序列号
(5).get_nei_dis_mp: 并行求每个点的平均凸起（占用内存巨大，建议线程数不超过核心数）
(6).get_nei_line_density_mp: 并行求每个的点所在截面的左右密度比(结果会打乱顺序，要求点云按照截面从小到大排序：ps = ps[ps[:, 4].argsort()]后再合并)

1.1.3.250421更新日志

1.shield.cut_down 进行了优化，对各个线程都比较友好

1.1.2.250310更新日志
1.新增shield_plus项目文件

(1).find_continuous_segments_numpy:找到一维数组中所有连续整数段的起始和终止数，返回 NumPy 数组

(2).get_ρθ:求每个盾构环的极径差和反正切

(3).find_seed:寻找符合纵缝特征的种子点[setup.py](setup.py)

(4).find_seed_cs:寻找单个截面符合纵缝特征的种子点

(5).distance_to_line:计算点到直线的几何距离(二维)[setup.py](setup.py)

(6).merge_similar_lines:合并相似直线（极坐标参数相近的线段）

(7).find_lines:通过数字图像操作将纵缝找到并返回种子点

(8).merge_similar_lines:合并角度和位置相近的线段

(9).fit_3d_line:拟合三维直线

(10).distance_to_line_3D:计算点到三维直线的距离

2.shield项目文件新增了三种环缝提取算法

1.1.1.241227更新日志

1.新增了.mmdet3d_base 深度学习自定义数据集支撑代码（需要加装pytorch和mmengine）：

（1）.get_pts_paths：批量获得点云数据路径

（2）.cut_points：将大点云分割成小块点云，并将绝对坐标系转换成相对中心坐标系

（3）.reset_z_intensity：重置点云的z坐标和强度值

（4）.np2bin_batch：numpy点云批量转为.bin格式

（5）.np2label_batch：numpy点云标签批量生成.bin格式标签

（6）.np2ImageSets_batch：生成训练集、验证集和测试集.txt

（7）.create_pkl：通过数据集生成mmdet3d所能接受的仿seg_kitti的.pkl

2.暂停了图割和超体素理论的开发项目

3.对.TheHeartOfTheMilitaryGod新增了一些功能

（1）.ground_ps2DEM：地面点转DEM,并返回网格坐标（可自行填补空洞）

（2）.get_buildDSM：在建立DEM网格的情况下建立建筑物DSM

1.0.3.241205更新日志

1.增加了基于点集拟合直线到椭圆\圆的切角剔除非衬砌点的算法，效果和基于角度差的不相上下

2.删除了部分含有bug或已经无法使用的代码

1.0.2.241111更新日志

1.增加了改进PCA算法

2.修复了zelas转zelas2的问题

3.新增了图割和超体素理论的开发项目