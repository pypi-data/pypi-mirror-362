
from mcp.server.fastmcp import FastMCP


# 1，使用内嵌式 python 解释器时，需要将当前路径加入 Python 系统环境路径
import sys
import os
import subprocess
import time
from typing import Tuple, Dict, Any
from mcp.server.fastmcp import FastMCP
from ATKConnectModule import atkOpen, atkConnect, atkClose

mcp = FastMCP("demo")
@mcp.tool()
def _perform_simulation_logic(conID: int, params: Dict[str, Any]) -> str:
    """
    执行核心的ATK轨道快速转移仿真逻辑。
    这是一个内部函数，不应直接调用。

    Args:
        conID (int): 已建立的ATK连接ID。
        params (Dict[str, Any]): 包含所有仿真参数的字典。

    Returns:
        str: 从ATK获取的报告数据。
    """
    # 5.1，想定新建并设置属性
    atkConnect(conID, 'New', '/ Scenario FastTransfer')
    atkConnect(conID, 'SetAnalysisTimePeriod', f'* "{params["scenario_start_time"]}" "{params["scenario_end_time"]}"')

    # 5.2，卫星新建与轨道预报设置为机动规划
    atkConnect(conID, 'New', '/ Satellite FastTransfer')
    atkConnect(conID, 'Astrogator', '*/Satellite/FastTransfer SetProp')
    atkConnect(conID, 'Graphics', '*/Satellite/FastTransfer Pass2D GrndTrail All')

    # 5.3，机动规划添加段，新添加卫星会有默认初始段
    atkConnect(conID, 'Astrogator', '*/Satellite/FastTransfer InsertSegment MainSequence.SegmentList.- Propagate')
    atkConnect(conID, 'Astrogator', '*/Satellite/FastTransfer InsertSegment MainSequence.SegmentList.- Target_Sequence')
    atkConnect(conID, 'Astrogator',
               '*/Satellite/FastTransfer InsertSegment MainSequence.SegmentList.Target_Sequence.SegmentList.- Maneuver')
    atkConnect(conID, 'Astrogator', '*/Satellite/FastTransfer InsertSegment MainSequence.SegmentList.- Propagate')
    atkConnect(conID, 'Astrogator', '*/Satellite/FastTransfer InsertSegment MainSequence.SegmentList.- Target_Sequence')
    atkConnect(conID, 'Astrogator',
               '*/Satellite/FastTransfer InsertSegment MainSequence.SegmentList.Target_Sequence1.SegmentList.- Maneuver')
    atkConnect(conID, 'Astrogator', '*/Satellite/FastTransfer InsertSegment MainSequence.SegmentList.- Propagate')

    # 5.4，初始段属性设置 (使用传入参数)
    atkConnect(conID, 'Astrogator',
               f'*/Satellite/FastTransfer SetValue MainSequence.SegmentList.Initial_State.InitialState.Epoch "{params["scenario_start_time"]}" UTCG')
    atkConnect(conID, 'Astrogator',
               '*/Satellite/FastTransfer SetValue MainSequence.SegmentList.Initial_State.CoordinateType "Modified Keplerian"')
    atkConnect(conID, 'Astrogator',
               f'*/Satellite/FastTransfer SetValue MainSequence.SegmentList.Initial_State.InitialState.Keplerian.sma {params["initial_sma_m"]} m')
    atkConnect(conID, 'Astrogator',
               f'*/Satellite/FastTransfer SetValue MainSequence.SegmentList.Initial_State.InitialState.Keplerian.ecc {params["initial_ecc"]}')
    atkConnect(conID, 'Astrogator',
               f'*/Satellite/FastTransfer SetValue MainSequence.SegmentList.Initial_State.InitialState.Keplerian.inc {params["initial_inc_deg"]}')
    atkConnect(conID, 'Astrogator',
               f'*/Satellite/FastTransfer SetValue MainSequence.SegmentList.Initial_State.InitialState.Keplerian.RAAN {params["initial_raan_deg"]}')
    atkConnect(conID, 'Astrogator',
               f'*/Satellite/FastTransfer SetValue MainSequence.SegmentList.Initial_State.InitialState.Keplerian.w {params["initial_w_deg"]}')
    atkConnect(conID, 'Astrogator',
               f'*/Satellite/FastTransfer SetValue MainSequence.SegmentList.Initial_State.InitialState.Keplerian.ta {params["initial_ta_deg"]}')

    # 5.5，第一个预报段属性设置
    atkConnect(conID, 'Astrogator',
               '*/Satellite/FastTransfer SetValue MainSequence.SegmentList.Propagate.SegmentColor -16776961')
    atkConnect(conID, 'Astrogator',
               '*/Satellite/FastTransfer SetValue MainSequence.SegmentList.Propagate.Propagator Earth JGM3 20 20 true ENRLMSISE00 false 150 150 14.9186 true true false 0 GGM1 0 0 true 0 GLGM2 0 0')
    atkConnect(conID, 'Astrogator',
               '*/Satellite/FastTransfer SetValue MainSequence.SegmentList.Propagate.StoppingConditions Duration')
    atkConnect(conID, 'Astrogator',
               f'*/Satellite/FastTransfer SetValue MainSequence.SegmentList.Propagate.StoppingConditions.Duration.TripValue {params["propagate1_duration_sec"]} sec')
    atkConnect(conID, 'Astrogator',
               '*/Satellite/FastTransfer SetValue MainSequence.SegmentList.Propagate.StoppingConditions.Duration.Tolerance 0.0001 sec')

    # 5.6，第一个瞄准段中机动段属性设置
    atkConnect(conID, 'Astrogator',
               '*/Satellite/FastTransfer SetValue MainSequence.SegmentList.Target_Sequence.SegmentList.Maneuver.ImpulsiveMnvr.ThrustAxes "Satellite VNC(Earth)"')
    atkConnect(conID, 'Astrogator',
               '*/Satellite/FastTransfer AddMCSSegmentControl MainSequence.SegmentList.Target_Sequence.SegmentList.Maneuver ImpulsiveMnvr.Cartesian.X')

    # 5.7，第一个瞄准段添加属性页
    atkConnect(conID, 'Astrogator',
               '*/Satellite/FastTransfer SetValue MainSequence.SegmentList.Target_Sequence.Profiles Differential_Corrector')
    atkConnect(conID, 'Astrogator',
               '*/Satellite/FastTransfer SetValue MainSequence.SegmentList.Target_Sequence.Action "Run active profiles"')  # 注意：原代码路径有误，已修正

    # 5.8，设置属性页中控制变量属性
    atkConnect(conID, 'Astrogator',
               '*/Satellite/FastTransfer SetMCSControlValue MainSequence.SegmentList.Target_Sequence.Profiles.Differential_Corrector Maneuver ImpulsiveMnvr.Cartesian.X Active true')
    atkConnect(conID, 'Astrogator',
               '*/Satellite/FastTransfer SetMCSControlValue MainSequence.SegmentList.Target_Sequence.Profiles.Differential_Corrector Maneuver ImpulsiveMnvr.Cartesian.X MaxStep 100 m/sec')
    atkConnect(conID, 'Astrogator',
               '*/Satellite/FastTransfer SetMCSControlValue MainSequence.SegmentList.Target_Sequence.Profiles.Differential_Corrector Maneuver ImpulsiveMnvr.Cartesian.X Correction 0 m/sec')
    atkConnect(conID, 'Astrogator',
               '*/Satellite/FastTransfer SetMCSControlValue MainSequence.SegmentList.Target_Sequence.Profiles.Differential_Corrector Maneuver ImpulsiveMnvr.Cartesian.X Perturbation 0.1 m/sec')
    atkConnect(conID, 'Astrogator',
               '*/Satellite/FastTransfer SetMCSControlValue MainSequence.SegmentList.Target_Sequence.Profiles.Differential_Corrector Maneuver ImpulsiveMnvr.Cartesian.X Scale 1 m/sec')

    # 5.9，设置属性页中约束条件属性 (使用传入参数)
    atkConnect(conID, 'Astrogator',
               '*/Satellite/FastTransfer SetValue MainSequence.SegmentList.Target_Sequence.SegmentList.Maneuver.Results "Radius Of Apoapsis"')
    atkConnect(conID, 'Astrogator',
               '*/Satellite/FastTransfer SetMCSConstraintValue MainSequence.SegmentList.Target_Sequence.Profiles.Differential_Corrector Maneuver Radius_Of_Apoapsis Active true')
    atkConnect(conID, 'Astrogator',
               f'*/Satellite/FastTransfer SetMCSConstraintValue MainSequence.SegmentList.Target_Sequence.Profiles.Differential_Corrector Maneuver Radius_Of_Apoapsis Desired {params["target1_apoapsis_radius_m"]} m')
    atkConnect(conID, 'Astrogator',
               '*/Satellite/FastTransfer SetMCSConstraintValue MainSequence.SegmentList.Target_Sequence.Profiles.Differential_Corrector Maneuver Radius_Of_Apoapsis Scale 1 m')
    atkConnect(conID, 'Astrogator',
               '*/Satellite/FastTransfer SetMCSConstraintValue MainSequence.SegmentList.Target_Sequence.Profiles.Differential_Corrector Maneuver Radius_Of_Apoapsis tolerance 0.1 m')
    atkConnect(conID, 'Astrogator',
               '*/Satellite/FastTransfer SetMCSConstraintValue MainSequence.SegmentList.Target_Sequence.Profiles.Differential_Corrector Maneuver Radius_Of_Apoapsis Weight 1')

    # 5.10，第二个预报段属性设置 (使用传入参数)
    atkConnect(conID, 'Astrogator',
               '*/Satellite/FastTransfer SetValue MainSequence.SegmentList.Propagate1.SegmentColor -16711936')
    atkConnect(conID, 'Astrogator',
               '*/Satellite/FastTransfer SetValue MainSequence.SegmentList.Propagate1.Propagator Earth JGM3 20 20 true ENRLMSISE00 false 150 150 14.9186 true true false 0 GGM1 0 0 true 0 GLGM2 0 0')
    atkConnect(conID, 'Astrogator',
               '*/Satellite/FastTransfer SetValue MainSequence.SegmentList.Propagate1.StoppingConditions R_Magnitude')
    atkConnect(conID, 'Astrogator',
               f'*/Satellite/FastTransfer SetValue MainSequence.SegmentList.Propagate1.StoppingConditions.R_Magnitude.TripValue {params["propagate2_stop_radius_m"]} m')
    atkConnect(conID, 'Astrogator',
               '*/Satellite/FastTransfer SetValue MainSequence.SegmentList.Propagate1.StoppingConditions.R_Magnitude.Tolerance 1e-6 m')
    atkConnect(conID, 'Astrogator',
               '*/Satellite/FastTransfer SetValue MainSequence.SegmentList.Propagate1.StoppingConditions.R_Magnitude.RepeatCount 1')
    atkConnect(conID, 'Astrogator',
               '*/Satellite/FastTransfer SetValue MainSequence.SegmentList.Propagate1.StoppingConditions.R_Magnitude.Condition "Cross Either (Inc.or Dec.)"')

    # 5.11，第二个瞄准段中机动段属性设置
    atkConnect(conID, 'Astrogator',
               '*/Satellite/FastTransfer SetValue MainSequence.SegmentList.Target_Sequence1.SegmentList.Maneuver.SegmentColor -16711681')
    atkConnect(conID, 'Astrogator',
               '*/Satellite/FastTransfer SetValue MainSequence.SegmentList.Target_Sequence1.SegmentList.Maneuver.ImpulsiveMnvr.ThrustAxes "Satellite VNC(Earth)"')
    atkConnect(conID, 'Astrogator',
               '*/Satellite/FastTransfer AddMCSSegmentControl MainSequence.SegmentList.Target_Sequence1.SegmentList.Maneuver ImpulsiveMnvr.Cartesian.X')
    atkConnect(conID, 'Astrogator',
               '*/Satellite/FastTransfer AddMCSSegmentControl MainSequence.SegmentList.Target_Sequence1.SegmentList.Maneuver ImpulsiveMnvr.Cartesian.Z')

    # 5.12，第二个瞄准段添加属性页
    atkConnect(conID, 'Astrogator',
               '*/Satellite/FastTransfer SetValue MainSequence.SegmentList.Target_Sequence1.Profiles Differential_Corrector')
    atkConnect(conID, 'Astrogator',
               '*/Satellite/FastTransfer SetValue MainSequence.SegmentList.Target_Sequence1.Action "Run active profiles"')  # 注意：原代码路径有误，已修正

    # 5.13，设置属性页中控制变量属性
    atkConnect(conID, 'Astrogator',
               '*/Satellite/FastTransfer SetMCSControlValue MainSequence.SegmentList.Target_Sequence1.Profiles.Differential_Corrector Maneuver ImpulsiveMnvr.Cartesian.X Active true')
    atkConnect(conID, 'Astrogator',
               '*/Satellite/FastTransfer SetMCSControlValue MainSequence.SegmentList.Target_sequence1.Profiles.Differential_Corrector Maneuver ImpulsiveMnvr.Cartesian.X MaxStep 300 m/sec')
    atkConnect(conID, 'Astrogator',
               '*/Satellite/FastTransfer SetMCSControlValue MainSequence.SegmentList.Target_Sequence1.Profiles.Differential_Corrector Maneuver ImpulsiveMnvr.Cartesian.X Correction 0 m/sec')
    atkConnect(conID, 'Astrogator',
               '*/Satellite/FastTransfer SetMCSControlValue MainSequence.SegmentList.Target_Sequence1.Profiles.Differential_Corrector Maneuver ImpulsiveMnvr.Cartesian.X Perturbation 0.1 m/sec')
    atkConnect(conID, 'Astrogator',
               '*/Satellite/FastTransfer SetMCSControlValue MainSequence.SegmentList.Target_Sequence1.Profiles.Differential_Corrector Maneuver ImpulsiveMnvr.Cartesian.X Scale 1 m/sec')
    atkConnect(conID, 'Astrogator',
               '*/Satellite/FastTransfer SetMCSControlValue MainSequence.SegmentList.Target_Sequence1.Profiles.Differential_Corrector Maneuver ImpulsiveMnvr.Cartesian.Z Active true')
    atkConnect(conID, 'Astrogator',
               '*/Satellite/FastTransfer SetMCSControlValue MainSequence.SegmentList.Target_Sequence1.Profiles.Differential_Corrector Maneuver ImpulsiveMnvr.Cartesian.Z MaxStep 300 m/sec')
    atkConnect(conID, 'Astrogator',
               '*/Satellite/FastTransfer SetMCSControlValue MainSequence.SegmentList.Target_Sequence1.Profiles.Differential_Corrector Maneuver ImpulsiveMnvr.Cartesian.Z Correction 0 m/sec')
    atkConnect(conID, 'Astrogator',
               '*/Satellite/FastTransfer SetMCSControlValue MainSequence.SegmentList.Target_Sequence1.Profiles.Differential_Corrector Maneuver ImpulsiveMnvr.Cartesian.Z Perturbation 0.1 m/sec')
    atkConnect(conID, 'Astrogator',
               '*/Satellite/FastTransfer SetMCSControlValue MainSequence.SegmentList.Target_Sequence1.Profiles.Differential_Corrector Maneuver ImpulsiveMnvr.Cartesian.Z Scale 1 m/sec')

    # 5.14，设置属性页中约束条件属性 (使用传入参数)
    atkConnect(conID, 'Astrogator',
               '*/Satellite/FastTransfer SetValue MainSequence.SegmentList.Target_Sequence1.SegmentList.Maneuver.Results Eccentricity CosineVFPA')
    atkConnect(conID, 'Astrogator',
               '*/Satellite/FastTransfer SetMCSConstraintValue MainSequence.SegmentList.Target_Sequence1.Profiles.Differential_Corrector Maneuver Eccentricity Active true')
    atkConnect(conID, 'Astrogator',
               f'*/Satellite/FastTransfer SetMCSConstraintValue MainSequence.SegmentList.Target_Sequence1.Profiles.Differential_Corrector Maneuver Eccentricity Desired {params["target2_eccentricity"]}')
    atkConnect(conID, 'Astrogator',
               '*/Satellite/FastTransfer SetMCSConstraintValue MainSequence.SegmentList.Target_Sequence1.Profiles.Differential_Corrector Maneuver Eccentricity Scale 1')
    atkConnect(conID, 'Astrogator',
               '*/Satellite/FastTransfer SetMCSConstraintValue MainSequence.SegmentList.Target_Sequence1.Profiles.Differential_Corrector Maneuver Eccentricity tolerance 0.001')
    atkConnect(conID, 'Astrogator',
               '*/Satellite/FastTransfer SetMCSConstraintValue MainSequence.SegmentList.Target_Sequence1.Profiles.Differential_Corrector Maneuver Eccentricity Weight 1')
    atkConnect(conID, 'Astrogator',
               '*/Satellite/FastTransfer SetMCSConstraintValue MainSequence.SegmentList.Target_Sequence1.Profiles.Differential_Corrector Maneuver CosineVFPA Active true')
    atkConnect(conID, 'Astrogator',
               '*/Satellite/FastTransfer SetMCSConstraintValue MainSequence.SegmentList.Target_Sequence1.Profiles.Differential_Corrector Maneuver CosineVFPA Desired 0 rad')
    atkConnect(conID, 'Astrogator',
               '*/Satellite/FastTransfer SetMCSConstraintValue MainSequence.SegmentList.Target_Sequence1.Profiles.Differential_Corrector Maneuver CosineVFPA Scale 1 rad')
    atkConnect(conID, 'Astrogator',
               '*/Satellite/FastTransfer SetMCSConstraintValue MainSequence.SegmentList.Target_Sequence1.Profiles.Differential_Corrector Maneuver CosineVFPA tolerance 0.001 rad')
    atkConnect(conID, 'Astrogator',
               '*/Satellite/FastTransfer SetMCSConstraintValue MainSequence.SegmentList.Target_Sequence1.Profiles.Differential_Corrector Maneuver CosineVFPA Weight 1')

    # 5.15，第三个预报段属性设置
    atkConnect(conID, 'Astrogator',
               '*/Satellite/FastTransfer SetValue MainSequence.SegmentList.Propagate2.SegmentColor -65536')
    atkConnect(conID, 'Astrogator',
               '*/Satellite/FastTransfer SetValue MainSequence.SegmentList.Propagate2.Propagator Earth JGM3 20 20 true ENRLMSISE00 false 150 150 14.9186 true true false 0 GGM1 0 0 true 0 GLGM2 0 0')
    atkConnect(conID, 'Astrogator',
               '*/Satellite/FastTransfer SetValue MainSequence.SegmentList.Propagate2.StoppingConditions Duration')
    atkConnect(conID, 'Astrogator',
               '*/Satellite/FastTransfer SetValue MainSequence.SegmentList.Propagate2.StoppingConditions.Duration.TripValue 172800 sec')
    atkConnect(conID, 'Astrogator',
               '*/Satellite/FastTransfer SetValue MainSequence.SegmentList.Propagate2.StoppingConditions.Duration.Tolerance 0.0001 sec')

    # 5.16，机动规划运行
    print("运行机动规划 (RunMCS)...")
    atkConnect(conID, 'Astrogator', '*/Satellite/FastTransfer RunMCS')
    atkConnect(conID, 'Animate', '* Reset')

    # 5.17，查看报告数据 (使用传入参数)
    print("正在生成报告...")
    report_cmd = f'Report_RM */Satellite/FastTransfer Style "Position" TimePeriod "{params["report_start_time"]}" "{params["report_end_time"]}"'
    report_data = atkConnect(conID, 'Report_RM', report_cmd.split(' ', 1)[1])  # Report_RM的格式需要特殊处理

    # 5.18，想定保存 (使用传入参数)
    if params["scenario_save_path"]:
        print(f"保存想定至: {params['scenario_save_path']}")
        atkConnect(conID, 'Save', f'/ "{params["scenario_save_path"]}"')

    return report_data

def run_fast_transfer_simulation(
        # --- ATK 连接配置参数 ---
        atk_ip: str,
        atk_port: int,
        atk_path: str,
        auto_open_atk: bool = True,
        wait_time: int = 10,

        # --- 仿真时间参数 ---
        scenario_start_time: str = "5 Nov 2022 00:00:00.000",
        scenario_end_time: str = "6 Nov 2022 00:00:00.000",

        # --- 初始轨道根数参数 (开普勒) ---
        initial_sma_m: float = 6700000.0,
        initial_ecc: float = 0.0,
        initial_inc_deg: float = 0.0,
        initial_raan_deg: float = 0.0,
        initial_w_deg: float = 0.0,
        initial_ta_deg: float = 0.0,

        # --- 机动与瞄准参数 ---
        propagate1_duration_sec: int = 7200,
        target1_apoapsis_radius_m: float = 84328394.0,
        propagate2_stop_radius_m: float = 42164197.0,
        target2_eccentricity: float = 0.0,

        # --- 报告与保存参数 ---
        report_start_time: str = "5 Nov 2022 01:00:00.000",
        report_end_time: str = "5 Nov 2022 02:00:00.000",
        scenario_save_path: str = None
) -> Tuple[bool, str]:
    """
    一个MCP服务，用于执行ATK中的轨道快速转移仿真。

    Args:
        atk_ip (str): ATK服务器的IP地址。
        atk_port (int): ATK服务器的端口。
        atk_path (str): 本地ATK.exe的可执行文件路径。
        auto_open_atk (bool, optional): 是否自动启动ATK.exe。默认为 True。
        wait_time (int, optional): 等待ATK启动和连接的最长时间（秒）。默认为 10。

        scenario_start_time (str, optional): 仿真场景开始时间，格式如 "5 Nov 2022 00:00:00.000"。
        scenario_end_time (str, optional): 仿真场景结束时间，格式如 "6 Nov 2022 00:00:00.000"。

        initial_sma_m (float, optional): 初始轨道半长轴（单位：米）。
        initial_ecc (float, optional): 初始轨道偏心率。
        initial_inc_deg (float, optional): 初始轨道倾角（单位：度）。
        initial_raan_deg (float, optional): 初始轨道升交点赤经（单位：度）。
        initial_w_deg (float, optional): 初始轨道近地点幅角（单位：度）。
        initial_ta_deg (float, optional): 初始轨道真近点角（单位：度）。

        propagate1_duration_sec (int, optional): 第一个预报段的持续时间（单位：秒）。
        target1_apoapsis_radius_m (float, optional): 第一个瞄准段的目标远地点高度（单位：米）。
        propagate2_stop_radius_m (float, optional): 第二个预报段的停止条件轨道半径（单位：米）。
        target2_eccentricity (float, optional): 第二个瞄准段的目标偏心率。

        report_start_time (str, optional): 生成报告的开始时间。
        report_end_time (str, optional): 生成报告的结束时间。
        scenario_save_path (str, optional): 仿真想定保存路径（.sc文件）。如果为None则不保存。

    Returns:
        Tuple[bool, str]:
            - 第一个元素 (bool): True表示成功，False表示失败。
            - 第二个元素 (str): 如果成功，则为ATK返回的报告内容；如果失败，则为错误信息。
    """
    # 将所有仿真相关的参数打包到一个字典中，方便传递
    simulation_params = {
        "scenario_start_time": scenario_start_time,
        "scenario_end_time": scenario_end_time,
        "initial_sma_m": initial_sma_m,
        "initial_ecc": initial_ecc,
        "initial_inc_deg": initial_inc_deg,
        "initial_raan_deg": initial_raan_deg,
        "initial_w_deg": initial_w_deg,
        "initial_ta_deg": initial_ta_deg,
        "propagate1_duration_sec": propagate1_duration_sec,
        "target1_apoapsis_radius_m": target1_apoapsis_radius_m,
        "propagate2_stop_radius_m": propagate2_stop_radius_m,
        "target2_eccentricity": target2_eccentricity,
        "report_start_time": report_start_time,
        "report_end_time": report_end_time,
        "scenario_save_path": scenario_save_path
    }

    # 6，判断是否自动打开 ATK.exe
    if auto_open_atk:
        try:
            subprocess.Popen([atk_path])
            print(f"正在尝试自动打开 ATK: {atk_path}，请等待...")
        except FileNotFoundError:
            error_msg = f"ATK.exe未找到，路径错误: {atk_path}"
            print(error_msg)
            return (False, error_msg)
        except Exception as e:
            error_msg = f"启动ATK时发生未知错误: {e}"
            print(error_msg)
            return (False, error_msg)
    else:
        print(f"请手动打开 ATK，待 {wait_time} 秒后尝试连接...")

    conID = -1
    count = 0

    # 7，循环检测 ATK 连接状态
    while conID == -1 and count < wait_time:
        time.sleep(1)
        count += 1
        print(f"尝试连接 ATK... 第 {count} 秒")
        # 8，建立 ATK 连接
        conID = atkOpen(atk_ip, atk_port)

    # 9，判断连接结果并执行仿真
    if conID != -1:
        print(f"成功连接到 ATK, 连接ID: {conID}")
        try:
            # 调用核心仿真逻辑
            report = _perform_simulation_logic(conID, simulation_params)
            print("仿真执行完毕。")
            return (True, report)
        except Exception as e:
            error_msg = f"执行ATK仿真命令时出错: {e}"
            print(error_msg)
            return (False, error_msg)
        finally:
            # 10，关闭 ATK 连接
            print("关闭ATK连接...")
            atkClose(conID)
    else:
        error_msg = f"连接ATK失败，请确认ATK已在 {atk_ip}:{atk_port} 启动并监听连接。"
        print(error_msg)
        return (False, error_msg)


# ==============================================================================
# --- MCP服务调用示例 ---
# ==============================================================================
if __name__ == "__main__":

    # 1. 设置ATK配置参数
    # 请根据您的实际情况修改这些路径和地址
    atk_config = {
        "atk_ip": "127.0.0.1",
        "atk_port": 6655,
        "atk_path": "C:\\Users\\13329\\Desktop\\ATK-周培源-mcp\\ATK-ZPY15专用版\\ATK-ZPY15专用版\\ATK.exe",  # 请务必修改为您的ATK.exe或AGIAtk.exe的正确路径
        "auto_open_atk": True,
        "wait_time": 20  # 启动ATK可能需要更长时间，可以适当增加
    }

    # 2. 设置仿真输入参数
    # 这里使用了与原脚本相同的默认值，您可以根据需要修改它们
    sim_inputs = {
        "scenario_start_time": "5 Nov 2022 00:00:00.000",
        "scenario_end_time": "6 Nov 2022 00:00:00.000",
        "initial_sma_m": 6700000.0,
        "initial_ecc": 0.0,
        "initial_inc_deg": 0.0,
        "initial_raan_deg": 0.0,
        "initial_w_deg": 0.0,
        "initial_ta_deg": 0.0,
        "propagate1_duration_sec": 7200,
        "target1_apoapsis_radius_m": 84328394.0,
        "propagate2_stop_radius_m": 42164197.0,
        "target2_eccentricity": 0.0,
        "report_start_time": "5 Nov 2022 01:00:00.000",
        "report_end_time": "5 Nov 2022 02:00:00.000",
        # 设置一个保存路径，如果不需要保存，则设为None
        "scenario_save_path": "D:\\ATK_Simulations\\FastTransferResult.sc"
    }

    # 确保保存路径的目录存在
    save_dir = os.path.dirname(sim_inputs["scenario_save_path"])
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
        print(f"已创建目录: {save_dir}")

    # 3. 调用MCP服务函数
    # 使用 **kwargs 语法可以方便地将字典解包为函数参数
    success, result_data = run_fast_transfer_simulation(**atk_config, **sim_inputs)

    # 4. 处理返回结果
    if success:
        print("\n--- 仿真成功 ---")
        print("报告内容:")
        print(result_data)
    else:
        print("\n--- 仿真失败 ---")
        print("错误信息:")
        print(result_data)
    mcp.run(transport="stdio")
