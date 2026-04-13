# AR-Initial-Visualizer: 3D Alphabet Rendering on Chessboard

It utilizes the camera's intrinsic parameters to estimate real-time pose from a 13x9 chessboard and renders a 3D initial 'M' in augmented reality (AR).

### 1. Camera Matrix ($K$)
The precise intrinsic parameters obtained from the previous assignment (HW3) were applied.
$$ 
K = \begin{bmatrix} 1922.61898 & 0 & 1091.79010 \\ 0 & 1926.59005 & 1908.48807 \\ 0 & 0 & 1 \end{bmatrix} 
$$


## 2. Results
These are the demonstration screenshots.

| View 1 | View 2 | View 3 | View 4 |
| :---: | :---: | :---: | :---: |
| ![Result 1](./images/image1.png) | ![Result 1](./images/image2.png) | ![Result 1](./images/image3.png) | ![Result 1](./images/image4.png) |


## 3. How to Run
1. Install required libraries: `pip install numpy opencv-python`
2. Run the program: `python m_visualizer.py`
