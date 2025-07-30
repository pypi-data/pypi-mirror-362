# 本代码适用于25年3月的纵缝提取
import numpy as np
import zelas2.shield as zs
import multiprocessing as mp
import zelas2.Multispectral as zm
from sympy.codegen.ast import Return
from tqdm import tqdm
import cv2
from scipy.spatial.transform import Rotation
import zelas2.RedundancyElimination as zr
from sklearn.neighbors import KDTree  # 添加机器学习的skl.KDT的函数组

def find_continuous_segments_numpy(arr):
    """
    找到一维数组中所有连续整数段的起始和终止数，返回 NumPy 数组
    :param arr: 一维整数数组（已排序）
    :return: NumPy 数组，每行为 (起始数, 终止数)
    """
    segments = []  # 存储所有连续段
    start = arr[0]  # 当前连续段的起始数
    for i in range(1, len(arr)):
        if arr[i] != arr[i - 1] + 1:  # 检测中断点
            segments.append((start, arr[i - 1]))  # 保存当前连续段
            start = arr[i]  # 开始新的连续段
    # 添加最后一个连续段
    segments.append((start, arr[-1]))
    # 转换为 NumPy 数组
    return np.array(segments, dtype=int)

def get_ρθ(xz_p, xzr):
    '求每个盾构环的极径差和反正切'
    num_p = len(xz_p)  # 当前截面点数量
    ρ = np.sqrt((xz_p[:,0]-xzr[0])**2+(xz_p[:,1]-xzr[1])**2)-xzr[2]
    θ = np.empty(num_p)
    for i in range(num_p):
        θ[i] = zs.get_angle(xz_p[i,0],xz_p[i,1],xzr[0],xzr[1])
    return np.c_[ρ,θ]

def find_seed(θyρvci,ρ_td,r,cpu=mp.cpu_count(),c_ignore=4):
    '寻找符合纵缝特征的种子点'
    θyρvci_up = θyρvci[θyρvci[:,2]>=ρ_td,:]  # 低于衬砌点的不要
    # 准备工作
    pool = mp.Pool(processes=cpu)  # 开启多进程池，数量为cpu
    c_un = np.unique(θyρvci[:,4])
    num_c = len(np.unique(θyρvci[:,4]))  # 截面数
    # good_index = []
    # 并行计算
    multi_res = pool.starmap_async(find_seed_cs, ((θyρvci,np.uint64(θyρvci_up[θyρvci_up[:,4]==c_un[i],5]),c_un[i],r,c_ignore) for i in
                 tqdm(range(num_c),desc='分配任务寻找种子点',unit='个截面',total=num_c)))
    j = 0
    for res in tqdm(multi_res.get(),total=num_c,desc='输出种子点下标'):
        if j==0:
            good_index = res
        else:
            good_index = np.hstack((good_index, res))
        j += 1
    pool.close()  # 关闭所有进程
    pool.join()  # 当所有进程全部计算完毕后，退出并行计算
    return np.int64(good_index)


def find_seed_cs(θyρvci,id_θyρvci_up_c,c,r,c_ignore=4):
    '''
    寻找单个截面符合纵缝特征的种子点
    θyρvci : 点云信息
    id_θyρvci_up_c ：符合搜索的点云下标
    c ：当前截面
    r :当前截面半径
    c_ignore ：忽略的截面数
    '''
    good_ind = []  # 空下标
    θ_l_td = 0.15 * np.pi * r / 180
    for i in id_θyρvci_up_c:
        if θyρvci[i,3]==0:  # 如果当前点为线特征
            # 找到搜索截面
            θyρ_c_ = θyρvci[θyρvci[:, 4] <= c + c_ignore, :]
            θyρ_c_ = θyρ_c_[θyρ_c_[:, 4] >= c - c_ignore, :]
            # 判断左侧是否有球特征
            θ_l_ = θyρvci[i,0] - θ_l_td  # 左侧角度阈值
            θyρ_l_ = θyρ_c_[θyρ_c_[:, 0] < θyρvci[i, 0], :]
            θyρ_l_ = θyρ_l_[θyρ_l_[:, 0] >= θ_l_, :]
            # 判断右侧是否有球特征
            θ_r_ = θyρvci[i,0] + θ_l_td  # 右侧角度阈值
            θyρ_r_ = θyρ_c_[θyρ_c_[:, 0] > θyρvci[i, 0], :]
            θyρ_r_ = θyρ_r_[θyρ_r_[:, 0] <= θ_r_, :]
            if 2 in θyρ_l_[:, 3] and 2 in θyρ_r_[:, 3]:  # 如果左右都有球特征
                good_ind.append(θyρvci[i,5])  # 作为种子点
    return good_ind

def distance_to_line(point, line):
    """计算点到直线的几何距离"""
    x0, y0 = point
    x1, y1, x2, y2 = line
    numerator = abs((y2 - y1) * x0 - (x2 - x1) * y0 + x2 * y1 - y2 * x1)
    denominator = np.sqrt((y2 - y1) ** 2 + (x2 - x1) ** 2)
    return numerator / denominator if denominator != 0 else 0

def merge_similar_lines(lines, angle_thresh=np.pi / 18, rho_thresh=20):
    """合并相似直线（极坐标参数相近的线段）"""
    merged = []
    for line in lines:
        rho, theta = line_to_polar(line[0])
        found = False
        for m in merged:
            m_rho, m_theta = m[0]
            # 检查角度和距离差异
            if abs(theta - m_theta) < angle_thresh and abs(rho - m_rho) < rho_thresh:
                m[0] = ((m_rho + rho) / 2, (m_theta + theta) / 2)  # 合并平均值
                m[1].append(line)
                found = True
                break
        if not found:
            merged.append([(rho, theta), [line]])

    # 转换回线段格式（取合并后的极坐标生成新线段）
    merged_lines = []
    for m in merged:
        rho, theta = m[0]
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a * rho
        y0 = b * rho
        # 生成足够长的线段（覆盖图像范围）
        scale = 1000
        x1 = int(x0 + scale * (-b))
        y1 = int(y0 + scale * (a))
        x2 = int(x0 - scale * (-b))
        y2 = int(y0 - scale * (a))
        merged_lines.append([x1, y1, x2, y2])

    return merged_lines[:5]  # 最多返回前5条

def find_lines(θy):
    '通过数字图像操作将纵缝找到并返回种子点'
    '0.整理数据'
    θy = θy*100
    θy[:, 0] -= np.min(θy[:, 0])
    θy[:, 1] -= np.min(θy[:, 1])
    θy = np.uint64(θy)
    x_max = np.max(θy[:,0])
    y_max = np.max(θy[:,1]) # 求边界
    print('二维边长',x_max,y_max)
    '1.创建图像'
    img = np.zeros((int(y_max)+1, int(x_max)+1), dtype=np.uint8)
    for x,y in θy:
        img[y, x] = 255
    '''
    cv2.imshow("Image", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    '''
    '2.直线检测'
    # 霍夫变换检测直线
    lines = cv2.HoughLinesP(img, rho=1, theta=np.pi / 180, threshold=50, minLineLength=50, maxLineGap=50)  # 检测单位像素、角度、超过像素阈值、最小长度阈值、最大间断阈值
    # --- 提取前5条最长的直线 ---
    detected_lines = []
    if lines is not None:
        lines = lines[:, 0, :]
        # 按线段长度排序（从最长到最短）
        lines = sorted(lines, key=lambda x: np.linalg.norm(x[2:] - x[:2]), reverse=True)[:6]
        detected_lines = lines
    threshold_distance = 2.0  # 点到直线的最大允许距离（根据噪声调整）
    # 初始化：所有点标记为未分配
    assigned = np.zeros(len(θy), dtype=bool)
    line_points_list = []  # 存储每条直线的点
    line_indices_list = []  # 存储每条直线的点索引
    for line in detected_lines:
        distances = np.array([distance_to_line(p, line) for p in θy])
        # 筛选未分配且距离小于阈值的点
        mask = (distances < threshold_distance) & ~assigned
        line_points = θy[mask]
        line_points_list.append(line_points)
        indices = np.where(mask)[0]
        line_indices_list.append(indices)
        assigned |= mask  # 标记已分配的点
    # 合并前5条直线的点
    all_line_points = np.vstack(line_points_list)
    # 分离噪声点
    noise_points = θy[~assigned]
    '''
    # --- 可视化结果 ---
    # 创建彩色图像用于显示
    result_img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    # 绘制检测到的直线（绿色）
    for line in detected_lines:
        x1, y1, x2, y2 = line
        cv2.line(result_img, (x1, y1), (x2, y2), (0, 255, 0), 2)
    # 绘制属于直线的点（红色）
    for p in all_line_points:
        cv2.circle(result_img, tuple(p), 2, (0, 0, 255), -1)
    '''
    '''
        # 预定义5种颜色（BGR格式）
    colors = [
        (0, 0, 255),   # 红色
        (0, 255, 0),   # 绿色
        (255, 0, 0),   # 蓝色
        (0, 255, 255), # 黄色
        (255, 0, 255)  # 品红色
    ]
    # 绘制每条直线及其对应的点
    for i, (line, line_points) in enumerate(zip(detected_lines, line_points_list)):
        color = colors[i % len(colors)]  # 循环使用颜色列表
        # 绘制直线
        x1, y1, x2, y2 = line
        cv2.line(result_img, (x1, y1), (x2, y2), color, 2)
    '''
    '''
    # 绘制噪声点（蓝色）
    for p in noise_points:
        cv2.circle(result_img, tuple(p.astype(int)), 2, (255, 0, 0), -1)
    cv2.imshow("Result", result_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    '''
    # 去除 line_indices_list 中的空元素
    line_indices_list = [indices for indices in line_indices_list if len(indices) > 0]
    return line_indices_list


def merge_similar_lines(lines, angle_thresh=5, dist_thresh=10):
    """
    合并角度和位置相近的线段
    :param lines: 线段列表，格式为 [[x1,y1,x2,y2], ...]
    :param angle_thresh: 角度差阈值（度）
    :param dist_thresh: 线段中心点距离阈值（像素）
    :return: 合并后的线段列表
    """
    merged = []
    for line in lines:
        x1, y1, x2, y2 = line
        # 计算线段角度（弧度）
        angle = np.arctan2(y2 - y1, x2 - x1) * 180 / np.pi
        # 计算线段中心点
        cx, cy = (x1 + x2) / 2, (y1 + y2) / 2

        # 检查是否与已合并线段近似
        found = False
        for m in merged:
            m_angle, m_cx, m_cy = m['angle'], m['cx'], m['cy']
            # 角度差和中心点距离
            angle_diff = abs(angle - m_angle)
            dist = np.sqrt((cx - m_cx) ** 2 + (cy - m_cy) ** 2)

            if angle_diff < angle_thresh and dist < dist_thresh:
                # 合并线段（延长端点）
                m['x1'] = min(m['x1'], x1, x2)
                m['y1'] = min(m['y1'], y1, y2)
                m['x2'] = max(m['x2'], x1, x2)
                m['y2'] = max(m['y2'], y1, y2)
                found = True
                break

        if not found:
            merged.append({
                'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2,
                'angle': angle, 'cx': cx, 'cy': cy
            })
    # 转换为坐标格式
    return [[m['x1'], m['y1'], m['x2'], m['y2']] for m in merged]


def fit_3d_line(points):
    """
    Fit a 3D line to a point cloud using PCA.
    Parameters:
    points (numpy.ndarray): Nx3 array of 3D points.
    Returns:
    tuple: (centroid, direction_vector)
        centroid is a point on the line (numpy.ndarray of shape (3,)),
        direction_vector is the direction vector of the line (numpy.ndarray of shape (3,)).
    """
    # 计算点云的质心
    centroid = np.mean(points, axis=0)
    # 将点云中心化
    centered_points = points - centroid
    # 计算协方差矩阵
    cov_matrix = np.cov(centered_points.T)
    # 计算协方差矩阵的特征值和特征向量
    eigenvalues, eigenvectors = np.linalg.eigh(cov_matrix)
    # 找到最大特征值对应的特征向量作为方向向量
    direction_vector = eigenvectors[:, np.argmax(eigenvalues)]
    # Centroid (a point on the line): [1.5 1.5 1.5]
    # Direction vector: [0.57735027 0.57735027 0.57735027]
    return centroid, direction_vector


def distance_to_line_3D(points, centroid, direction):
    """
    计算点到三维直线的距离。
    Parameters:
    points (numpy.ndarray): Nx3 的3D点。
    centroid (numpy.ndarray): 直线上的一点，形状为 (3,)。
    direction (numpy.ndarray): 直线的单位方向向量，形状为 (3,)。
    Returns:
    numpy.ndarray: 每个点到直线的距离，形状为 (N,)。
    """
    # 计算点与质心的向量差
    vec = points - centroid
    # 计算叉乘 (支持批量计算)
    cross_product = np.cross(vec, direction)
    # 距离为叉乘的模长
    distances = np.linalg.norm(cross_product, axis=1)
    return distances

def find_CS_25(xyzic,GirthInterval=245,num_cpu=mp.cpu_count(),z_range=1):
    '环缝提取，固定长度版，25年修补版'
    xyzic[:, 3] = zm.normalization(xyzic[:, 3], 255)  # 强度值离散化
    # 计算每个环的平均强度值
    c_un = np.unique(xyzic[:, 4])  # 圆环从小到大排列
    num_C = len(c_un)  # 截面数量
    # 并行计算准备
    tik = zs.cut_down(num_C, num_cpu)  # 分块起止点
    pool = mp.Pool(processes=num_cpu)  # 开启多进程池，数量为cpu
    # 限制参与计算的比例
    z_max = np.max(xyzic[:, 2])
    z_min = np.min(xyzic[:, 2])
    d_z = z_max - z_min
    t_z = z_min + d_z * (1 - z_range)  # 参与统计的阈值
    ps_free = xyzic[xyzic[:, 2] >= t_z, :]  # 参与统计的点云
    i_c = np.empty(num_C)  # 新建一个存储圆环平均强度值的容器
    multi_res = [pool.apply_async(zs.find_cImean_block, args=(ps_free, c_un, tik[i], tik[i + 1])) for i in
                 range(num_cpu)]  # 将每个block需要处理的点云区间发送到每个进程当中
    tik_ = 0  # 计数器
    for res in multi_res:
        i_c[tik[tik_]:tik[tik_ + 1]] = res.get()
        tik_ += 1
    pool.close()  # 禁止进程池再接收任务
    pool.join()  # 当所有进程全部计算完毕后，退出并行计算
    # 后期整理
    i_c = zm.normalization(i_c, 255)  # 均值离散化
    i_c_mean = np.mean(i_c)  # 平均强度值均值
    i_c_std = np.std(i_c)  # 平均强度值方差
    print('截面强度值均值', i_c_mean, '截面强度值标准差', i_c_std)
    # 找到强度值的最低点以及其他的极低点
    id_min = np.argmin(i_c)
    num_CS_0 = int(np.round(num_C / GirthInterval))  # 假想环缝数量
    print('理论的环缝数量为',str(num_CS_0))
    Begin_CS_0 = id_min % GirthInterval  # 假想起始位置
    id_CS_0 = np.arange(Begin_CS_0, num_C, GirthInterval)  # 假想环缝位置
    print('假想环缝位置',c_un[id_CS_0])
    belong_i = 75  # 强度值搜索半径  # 30
    mid_ = 2  # 余量区间 3
    RB_S = np.array(c_un[0])  # 衬砌开始位置
    RB_E = []  # 衬砌结束位置
    c_name_ins = np.empty(num_CS_0)  # 极低值容器
    c_ = []  # 环缝的存储名
    c_id = []  # 环缝的存储下标器
    N = 8  # 环缝间隔
    #   dis_max = i_c_mean - i_c_std * 3  # 最大差值
    for i in range(num_CS_0):
        # 确保索引在有效范围内
        id_start = max(0, id_CS_0[i] - belong_i)
        id_end = min(len(i_c), id_CS_0[i] + belong_i)
        # 求强度值极低点
        id_min_i_ = np.argmin(i_c[id_start:id_end]) + id_start
        c_name_ins[i] = c_un[id_min_i_]  # 强度值极低点位置
        print('修改后的第', i, '个极低值位置为', c_un[id_min_i_])
        # 寻找以强度值为主的开始和结束位置
        id_min = int(c_name_ins[i] - N)
        id_max = int(c_name_ins[i] + N)
        # 添加衬砌表面起止位置
        RB_E = np.append(RB_E, id_min)  # 添加结束位置
        RB_S = np.append(RB_S, id_max)  # 添加起始位置
    RB_E = np.append(RB_E, c_un[-1])  # 结束位置封顶
    for i in range(num_CS_0):
        if i == 0:
            seams_all = np.arange(RB_E[i], RB_S[i + 1])  # IndexError: too many indices for array: array is 1-dimensional, but 2 were indexed
        else:
            seams_all = np.append(seams_all, np.arange(RB_E[i], RB_S[i + 1]))
    c_xyzic = xyzic[np.isin(xyzic[:, 4], seams_all), :]  # 返回xyzic[:, -1]中有c[c_in]的行数
    # 精简衬砌表面
    id_del = np.isin(np.isin(xyzic[:, 4], seams_all), False)  # 除去环缝点云的点云下标
    txti_delC = xyzic[id_del, :]  # 去除环缝的点云

    return  txti_delC, c_xyzic

def fit_3d_circle(xyz):
    '拟合三维圆'
    num, dim = xyz.shape
    # 求解平面法向量
    L1 = np.ones((num, 1))
    A = np.linalg.inv(xyz.T @ xyz) @ xyz.T @ L1
    # 构建矩阵B和向量L2
    B_rows = (num - 1) * num // 2
    B = np.zeros((B_rows, 3))
    L2 = np.zeros(B_rows)
    count = 0
    for i in range(num):
        for j in range(i + 1, num):
            B[count] = xyz[j] - xyz[i]
            L2[count] = 0.5 * (np.sum(xyz[j] ** 2) - np.sum(xyz[i] ** 2))
            count += 1
    # 构造矩阵D和向量L3
    D = np.zeros((4, 4))
    D[0:3, 0:3] = B.T @ B
    D[0:3, 3] = A.flatten()  # 前三行第四列为A
    D[3, 0:3] = A.T  # 第四行前三列为A的转置
    B_transpose_L2 = B.T @ L2
    L3 = np.concatenate([B_transpose_L2, [1]]).reshape(4, 1)
    # 求解圆心坐标C
    C = np.linalg.inv(D.T) @ L3
    C = C[:3].flatten()  # 提取前三个元素作为圆心
    # 计算半径
    distances = np.linalg.norm(xyz - C, axis=1)
    r = np.mean(distances)
    return np.concatenate([C, [r]])

def fit_3d_circle_mp(xyzc,num_thread=mp.cpu_count()):
    '并行拟合三维圆算法'
    c_un = np.unique(xyzc[:,3])  # 截面序列
    num_c = len(c_un)  # 截面数量
    xyzr_all = np.empty([num_c,4])  # 输出容器
    pool = mp.Pool(processes=num_thread)  # 开启多进程池，数量为cpu
    j = 0  # 分块输出计时器
    # 并行计算
    multi_res = pool.starmap_async(fit_3d_circle, ((xyzc[xyzc[:,3]==c_un[i],:3],) for i in
                 tqdm(range(num_c),desc='分配任务拟合单个三维圆参数',unit='个cross-section',total=num_c)))
    for res in tqdm(multi_res.get(), total=num_c, desc='导出单个三维圆参数', unit='个cross-section'):
        xyzr_all[j,:] = res
        j += 1
    pool.close()  # 禁止进程池再接收任务  #Prohibit process pools from receiving tasks again
    pool.join()  # 当所有进程全部计算完毕后，退出并行计算  #After all processes have completed their calculations, exit parallel computing
    return xyzr_all

def STSD_add_C(las,inx_d = 0.006168):
    '对STSD数据集添加截面序列号'
    # 整理基本信息
    xyz = las.xyz
    I = las.intensity
    inx = las.inx
    label = las.classification
    # 人工制作截面序列号
    inx_un = np.unique(inx)
    inx_min = np.min(inx)
    inx_max = np.max(inx)
    inx_range = np.arange(start=inx_min, stop=inx_max + inx_d, step=inx_d)
    k = 0
    xyzicl = np.c_[xyz,I,inx,label]
    for i in inx_range:
        j = i+inx_d
        xyzicl_ = xyzicl[xyzicl[:,4]<j,:]
        xyzicl_ = xyzicl_[xyzicl_[:, 4] >= i, :]
        xyzicl_[:,4] = k
        if k == 0:
            xyzicl_out = xyzicl_
        else:
            xyzicl_out = np.r_[xyzicl_out,xyzicl_]
        k += 1
    return xyzicl_out

def get_nei_dis_mp(xyz,r,tree,dis_all,cpu=mp.cpu_count()-6):
    '求每个点的平均凸起(建议线程数不超过核心数)'
    # 准备工作
    num = len(xyz)
    dis_in = np.empty(num)  # 存储平均突起的容器
    tik = zs.cut_down(num, cpu)  # 并行计算分块
    pool = mp.Pool(processes=cpu)  # 开启多进程池，数量为cpu
    # 开始进行并行计算
    multi_res = [pool.apply_async(get_nei_dis_block, args=(xyz[tik[i]:tik[i + 1],:], dis_all, tree, r)) for i in
                 range(cpu)]  # 将每个block需要处理的点云区间发送到每个进程当中
    tik_ = 0  # 计数器
    for res in multi_res:
        dis_in[tik[tik_]:tik[tik_ + 1]] = res.get()
        print('已完成',str(tik[tik_]),'到',str(tik[tik_+1]))
        tik_ += 1
    pool.close()  # 禁止进程池再接收任务
    pool.join()  # 当所有进程全部计算完毕后，退出并行计算
    return dis_in

def get_nei_dis_block(xyz_,dis_all,tree,r):
    '分块求每个点的平均凸起'
    num_ = len(xyz_)
    dis_in_ = np.zeros(num_)  # 存储平均突起的容器
    for i in range(num_):
        xyz__ = xyz_[i,:]
        indices, dises = tree.query_radius(xyz__.reshape(1, -1), r=r, return_distance=True,
                                           sort_results=True)  # 返回每个点的邻近点下标列表
        indices = indices[0]
        if len(indices) >= 2:
            dis_all_ = dis_all[indices]  # 临近点圆心距
            dis_mean = np.mean(dis_all_[1:])  # 当前点平均圆心距
            dis_ = dis_all_[0] - dis_mean  # 求当前点平均突起
            dis_in_[i] = dis_
    return dis_in_

def get_nei_line_density_c(ca_,width):
    '计算截面每个点左右密度差'
    num_ = len(ca_)
    dd_all_ = np.zeros(num_)
    for i in range(num_):
        a_ = ca_[i, 1]
        a_min = a_ - width
        a_max = a_ + width  # 左右角度区间
        count_l = np.sum((ca_[:, 1] > a_min) & (ca_[:, 1] < a_))
        count_r = np.sum((ca_[:, 1] > a_) & (ca_[:, 1] < a_max))  # 左右角度区间点数
        with np.errstate(divide='ignore', invalid='ignore'):
            ratios = np.minimum(count_l, count_r) / np.maximum(count_l, count_r) # 避免除以零的情况
        # 处理NaN和Inf情况（当分母为0时）
        ratios = np.nan_to_num(ratios, nan=0.0, posinf=1.0, neginf=-1.0)
        dd_all_[i] = ratios
    return dd_all_

def get_nei_line_density_mp(ca,width=360/500,cpu=mp.cpu_count()):
    '计算每个点左右密度差'
    # 准备工作
    # num = len(ca)
    # dd_all = np.empty(num)
    # 按照第一列进行排序
    ca = ca[ca[:, 0].argsort()]
    # 统计每个截面的点数
    # unique_sections, section_counts = np.unique(ca[:, 0], return_counts=True)
    unique_sections = np.unique(ca[:, 0])
    num_c = len(unique_sections)
    pool = mp.Pool(processes=cpu)  # 开启多进程池，数量为cpu
    # 开始进行并行计算
    multi_res = pool.starmap_async(get_nei_line_density_c, ((ca[ca[:,0]==unique_sections[i],:], width) for i in
                 tqdm(range(num_c),desc='分配任务给每个截面求左右密度差',unit='cross-sections',total=num_c)))
    j = 0  # 分块输出计时器
    for res in tqdm(multi_res.get(), total=num_c, desc='导出每个点的左右密度差', unit='cross-sections'):
        if j==0:
            dd_all = res
        else:
            dd_all= np.append(dd_all,res)
        j += 1
    pool.close()  # 禁止进程池再接收任务  #Prohibit process pools from receiving tasks again
    pool.join()  # 当所有进程全部计算完毕后，退出并行计算  #After all processes have completed their calculations, exit parallel computing
    return dd_all

def Curvature_r_mp(xyz,r=0.04,cpu=mp.cpu_count()):
    '并行按照球半径计算曲率'
    # 准备工作
    pool = mp.Pool(processes=cpu)  # 开启多进程池，数量为cpu
    num = len(xyz)  # 返回点云数量
    # start, end = block(num, cpu)  # 返回每个block的起始点云下标和终止点云下标
    tik = zr.cut_down(num, cpu)  # 去除bug后的分块函数
    tree = KDTree(xyz)  # 创建树
    j = 0  # 分块输出计数器
    curvature_all = np.empty(shape=len(xyz))  # 新建一个容器：整个点云的曲率数集
    multi_res = [pool.apply_async(curvature_r_block, args=(xyz,tik[i],tik[i+1], tree, r)) for i in range(cpu)]  # 将每个block需要处理的点云区间发送到每个进程当中
    for res in multi_res:
        curvature_all[tik[j]:tik[j+1]] = res.get()  # 将每个进程得到的结果分block的发送到容器当中
        print('已完成第', tik[j], '至第', tik[j + 1], '的点云')
        j += 1
    pool.close()  # 禁止进程池再接收任务
    pool.join()  # 当所有进程全部计算完毕后，退出并行计算
    return curvature_all  # 返回全部点云曲率集

def curvature_r_block(xyz,start,end,tree,r):
    '分块按照球半径计算曲率'
    # xyz_32 = np.column_stack((xyz[:, 0], xyz[:, 1], xyz[:, 2])).astype(np.float32)
    # pcd = o3d.geometry.PointCloud()
    # pcd.points = o3d.utility.Vector3dVector(xyz_32)
    # pcd_tree = o3d.geometry.KDTreeFlann(pcd)
    curvature_all = np.empty(end-start)
    # num_ = len(xyz_)
    # curvature_all = np.empty(num_)
    j = 0
    for i in tqdm(range(start,end)):
        # [_, idx, _] = pcd_tree.search_knn_vector_3d(pcd.points[i], n)  # 求每个点最近的n个点
        # id_kntree[i, :] = idx  # 求出每个点最邻近的n个点的下标
        xyz_ = xyz[i,:]
        indices, dises = tree.query_radius(xyz_.reshape(1, -1), r=r, return_distance=True,
                                           sort_results=True)  # 返回每个点的邻近点下标列表
        indices = indices[0]
        xyz_n = xyz[indices, :]
        cv, _ = zr.pca(xyz_n)  # 求每个点的特征值和特征向量
        c = zr.curvature_(cv,-1)  # 求出当前点的曲率
        # print(c)
        curvature_all[j] = c
        j += 1
    return curvature_all


def Curvature_r(xyz,r=0.04,job=-1):
    '按照球半径计算曲率'
    num = len(xyz)
    curvature_all = np.empty(num)
    tree = KDTree(xyz)  # 创建树
    for i in tqdm(range(num)):
        xyz_ = xyz[i,:]
        indices, dises = tree.query_radius(xyz_.reshape(1, -1), r=r, return_distance=True,
                                           sort_results=True)  # 返回每个点的邻近点下标列表
        indices = indices[0]
        xyz_n = xyz[indices, :]
        cv, _ = zr.pca(xyz_n)  # 求每个点的特征值和特征向量
        c = zr.curvature_(cv,job)  # 求出当前点的曲率
        # print(c)
        curvature_all[i] = c

    return curvature_all




