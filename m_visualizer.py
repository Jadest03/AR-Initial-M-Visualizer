import numpy as np
import cv2 as cv

# 1. 원본 4K 기준 K 행렬 (HW3 결과)
K_orig = np.array([[1922.61898, 0, 1091.79010],
                   [0, 1926.59005, 1908.48807],
                   [0, 0, 1]])
dist_coeff = np.array([0.02343, -0.09022, 0.00025, 0.00084, 0.08888])

# 13x9 보드 설정 (내부 코너 개수)
board_pattern = (13, 9)
board_cellsize = 0.020 

# 2. 'M'자 좌표 재설계 (중앙 배치 및 크기 최적화)
unit = board_cellsize * 1.0
cx, cy = 6 * board_cellsize, 4 * board_cellsize # 13x9 중앙

m_base = np.float32([
    [cx - unit, cy + unit, 0], [cx - unit, cy - unit, 0],
    [cx, cy, 0], [cx + unit, cy - unit, 0], [cx + unit, cy + unit, 0]
])
m_top = m_base.copy()
m_top[:, 2] = -board_cellsize * 2.0 # 높이 조절
m_3d_points = np.vstack((m_base, m_top))

obj_points = board_cellsize * np.array([[c, r, 0] for r in range(board_pattern[1]) for c in range(board_pattern[0])], dtype=np.float32)

video = cv.VideoCapture('data.MOV')

# 목표 처리 해상도 (가로/세로 비율 유지 필수)
target_w, target_h = 720, 1280

while True:
    valid, img = video.read()
    if not valid: break

    # 원본 비율 유지하며 리사이즈
    display_img = cv.resize(img, (target_w, target_h))
    gray = cv.cvtColor(display_img, cv.COLOR_BGR2GRAY)

    # 코너 찾기
    ret, corners = cv.findChessboardCorners(gray, board_pattern, cv.CALIB_CB_ADAPTIVE_THRESH)
    
    if ret:
        # [핵심] 서브픽셀 정밀도 추가 (물체 떨림 방지)
        criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)
        corners = cv.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)

        # [핵심] 리사이즈 비율에 맞춰 K 행렬 스케일링
        scale_x = target_w / img.shape[1]
        scale_y = target_h / img.shape[0]
        K_res = K_orig.copy()
        K_res[0, 0] *= scale_x # fx
        K_res[1, 1] *= scale_y # fy
        K_res[0, 2] *= scale_x # cx
        K_res[1, 2] *= scale_y # cy

        # Pose Estimation (5점)
        success, rvec, tvec = cv.solvePnP(obj_points, corners, K_res, dist_coeff)

        if success:
            # Projection (15점)
            img_pts, _ = cv.projectPoints(m_3d_points, rvec, tvec, K_res, dist_coeff)
            img_pts = np.int32(img_pts).reshape(-1, 2)

            # 그리기 로직 (생략 - 이전과 동일)
            cv.polylines(display_img, [img_pts[:5]], False, (255, 0, 0), 3)
            cv.polylines(display_img, [img_pts[5:]], False, (0, 0, 255), 3)
            for i in range(5):
                cv.line(display_img, tuple(img_pts[i]), tuple(img_pts[i+5]), (0, 255, 0), 2)

    cv.imshow('HW4 AR: Stable M', display_img)
    if cv.waitKey(1) == 27: break

video.release()
cv.destroyAllWindows()