from datetime import datetime, date, timedelta
import numpy as np
from scipy.io import loadmat
from scipy.signal import welch

def time_str_to_seconds(time_str:str)-> int:
    """
        DAQ970的yy:mm:dd:hh:mm:ss字符串数据转为起点为0的秒

        parameter
        -----------
        time_str: str
                  DAQ970的yy:mm:dd:hh:mm:ss时间戳字符串

        Returns
        -------
        int
            以其实时间为0时刻的秒

        Examples
        --------
        second = time_str_to_seconds(time_str)
        """
    dt = datetime.strptime(time_str, "%Y/%m/%d %H:%M:%S")

    # 计算与UNIX纪元(1970-01-01)的时间差
    seconds = (dt - datetime(1970,1,1)).total_seconds()
    return seconds


def average_downsample(arr: list[float], new_length: int) -> np.ndarray:
    """
            将数组降采样平均到目标长度

            parameter
            -----------
            arr: list[float]
                原始数据列表或数组
            new_length: int
                        降采样平均后的数据长度

            Returns
            -------
            array[float]
                降采样平均后的数组

            Examples
            --------
            downsample_array = average_downsample(raw_array, 100)
            """
    if len(arr) < new_length:
        raise ValueError("New length must be smaller than original length for downsampling")

    chunk_size = len(arr) / new_length
    result = []
    for i in range(new_length):
        start = int(i * chunk_size)
        end = int((i + 1) * chunk_size)
        result.append(np.mean(arr[start:end]))
    return np.array(result)

def mat2psd(path, name, na=100):
    """
                从路径读取.mat数据并计算其功率谱密度。

                parameter
                -----------
                path: str
                    目标文件路径字符串
                name: str
                     目标文件名(需要带后缀）
                na: int
                    窗函数平均长度

                Returns
                -------
                array[float]
                    傅里叶频率
                array[float]
                    数据的功率谱密度(V^2/Hz)

                Examples
                --------
                f, PSD = mat2psd(path, name, 100)
                """
    data_file = loadmat(path+name, mat_dtype=True)
    data = data_file['A']
    data = data.flatten(order='C')
    fs_array = data_file['Tinterval']
    fs = 1/fs_array[0]
    print(fs)
    nx = len(data)
    #na = 100
    w = np.hanning(np.floor(nx/na))
    freq, psd = welch(data, fs, w)
    return freq, psd