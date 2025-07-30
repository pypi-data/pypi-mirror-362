import subprocess
import time
from mcp.server.fastmcp import FastMCP

from ATKConnectModule import atkOpen
from ATKConnectModule import atkConnect
from ATKConnectModule import atkClose

ATKIP = '127.0.0.1'
ATKPort = 6655
ATKAutoOpen = True
ATKPath = "C:\\Users\\13329\\Desktop\\ATK-周培源-mcp\\ATK-ZPY15专用版\\ATK-ZPY15专用版\\ATK.exe"
WaitTime = 20

mcp = FastMCP("demo")

@mcp.tool()
def TestFastTransfer(
        # --- 仿真时间参数 ---
        scenario_start_time: str,
        scenario_end_time: str,

        # --- 初始轨道根数参数 (开普勒) ---
        initial_sma_m: float,#半长轴
        initial_ecc: float,#偏心率
        initial_inc_deg: float,#轨道倾角
        initial_raan_deg: float,#升交点赤经
        initial_w_deg: float,#近地点幅角
        initial_ta_deg: float,#真近点角

        # --- 机动与瞄准参数 ---
        propagate1_duration_sec: int,#第一次轨道传播持续时间
        target1_apoapsis_radius_m: float,#第一次机动瞄准的目标远地点半径
        propagate2_stop_radius_m: float,#第二次轨道预报的停止条件
        target2_eccentricity: float,#第二次机动瞄准的目标偏心率

        # --- 报告与保存参数 ---
        report_start_time: str,#生成报告的开始时间
        report_end_time: str,#生成报告的结束时间
) -> str:
    """
    本函数通过链接并调用ATK软件执行一次复杂的轨道快速转移，并返回指定时间段内的卫星位置信息
    Args:
        :param scenario_start_time:整个仿真想定的开始时间
        :param scenario_end_time:整个仿真想定的结束时间
        :param initial_sma_m:半长轴
        :param initial_ecc:偏心率
        :param initial_inc_deg:轨道倾角
        :param initial_raan_deg:升交点赤经
        :param initial_w_deg:近地点幅角
        :param initial_ta_deg:真近点角
        :param propagate1_duration_sec:第一次轨道传播持续时间
        :param target1_apoapsis_radius_m:第一次机动瞄准的目标远地点半径
        :param propagate2_stop_radius_m:第二次轨道预报的停止条件
        :param target2_eccentricity:第二次机动瞄准的目标偏心率
        :param report_start_time:生成报告的开始时间
        :param report_end_time:生成报告的结束时间
        :return: ATK 生成的位置报告字符串。
    """

    if ATKAutoOpen:
        subprocess.Popen([ATKPath])
        print("自动打开 ATK，请等待...")
    else:
        print("请手动打开 ATK，等待" + str(WaitTime) + "秒")

    conID = -1
    count = 0

    # 7，循环检测 ATK 连接状态
    while 0 != conID and count < WaitTime:
        # 等待 1 秒
        time.sleep(1)
        count += 1
        print(count)

        # 8，建立 ATK 连接
        conID = atkOpen(ATKIP, ATKPort)
        # 5.1，想定新建并设置属性
    atkConnect(conID, 'New', '/ Scenario FastTransfer')
    atkConnect(conID, 'SetAnalysisTimePeriod', f'* "{scenario_start_time}" "{scenario_end_time}"')

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

        # 5.4，初始段属性设置
    atkConnect(conID, 'Astrogator',
                   f'*/Satellite/FastTransfer SetValue MainSequence.SegmentList.Initial_State.InitialState.Epoch "{scenario_start_time}" UTCG')
    atkConnect(conID, 'Astrogator',
                   '*/Satellite/FastTransfer SetValue MainSequence.SegmentList.Initial_State.CoordinateType "Modified Keplerian"')
    atkConnect(conID, 'Astrogator',
                   f'*/Satellite/FastTransfer SetValue MainSequence.SegmentList.Initial_State.InitialState.Keplerian.sma {initial_sma_m} m')
    atkConnect(conID, 'Astrogator',
                   f'*/Satellite/FastTransfer SetValue MainSequence.SegmentList.Initial_State.InitialState.Keplerian.ecc {initial_ecc}')
    atkConnect(conID, 'Astrogator',
                   f'*/Satellite/FastTransfer SetValue MainSequence.SegmentList.Initial_State.InitialState.Keplerian.inc {initial_inc_deg}')
    atkConnect(conID, 'Astrogator',
                   f'*/Satellite/FastTransfer SetValue MainSequence.SegmentList.Initial_State.InitialState.Keplerian.RAAN {initial_raan_deg}')
    atkConnect(conID, 'Astrogator',
                   f'*/Satellite/FastTransfer SetValue MainSequence.SegmentList.Initial_State.InitialState.Keplerian.w {initial_w_deg}')
    atkConnect(conID, 'Astrogator',
                   f'*/Satellite/FastTransfer SetValue MainSequence.SegmentList.Initial_State.InitialState.Keplerian.ta {initial_ta_deg}')

        # 5.5，第一个预报段属性设置
    atkConnect(conID, 'Astrogator',
                   '*/Satellite/FastTransfer SetValue MainSequence.SegmentList.Propagate.SegmentColor -16776961')
    atkConnect(conID, 'Astrogator',
                   '*/Satellite/FastTransfer SetValue MainSequence.SegmentList.Propagate.Propagator Earth JGM3 20 20 true ENRLMSISE00 false 150 150 14.9186 true true false 0 GGM1 0 0 true 0 GLGM2 0 0')
    atkConnect(conID, 'Astrogator',
                   '*/Satellite/FastTransfer SetValue MainSequence.SegmentList.Propagate.StoppingConditions Duration')
    atkConnect(conID, 'Astrogator',
                   f'*/Satellite/FastTransfer SetValue MainSequence.SegmentList.Propagate.StoppingConditions.Duration.TripValue {propagate1_duration_sec} sec')
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
                   '*/Satellite/FastTransfer SetValue MainSequence.SegmentList.Target_Sequence.Action Run active profiles')

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

        # 5.9，设置属性页中约束条件属性
    atkConnect(conID, 'Astrogator',
                   '*/Satellite/FastTransfer SetValue MainSequence.SegmentList.Target_Sequence.SegmentList.Maneuver.Results "Radius Of Apoapsis"')
    atkConnect(conID, 'Astrogator',
                   '*/Satellite/FastTransfer SetMCSConstraintValue MainSequence.SegmentList.Target_Sequence.Profiles.Differential_Corrector Maneuver Radius_Of_Apoapsis Active true')
    atkConnect(conID, 'Astrogator',
                   f'*/Satellite/FastTransfer SetMCSConstraintValue MainSequence.SegmentList.Target_Sequence.Profiles.Differential_Corrector Maneuver Radius_Of_Apoapsis Desired {target1_apoapsis_radius_m} m')
    atkConnect(conID, 'Astrogator',
                   '*/Satellite/FastTransfer SetMCSConstraintValue MainSequence.SegmentList.Target_Sequence.Profiles.Differential_Corrector Maneuver Radius_Of_Apoapsis Scale 1 m')
    atkConnect(conID, 'Astrogator',
                   '*/Satellite/FastTransfer SetMCSConstraintValue MainSequence.SegmentList.Target_Sequence.Profiles.Differential_Corrector Maneuver Radius_Of_Apoapsis tolerance 0.1 m')
    atkConnect(conID, 'Astrogator',
                   '*/Satellite/FastTransfer SetMCSConstraintValue MainSequence.SegmentList.Target_Sequence.Profiles.Differential_Corrector Maneuver Radius_Of_Apoapsis Weight 1')

        # 5.10，第二个预报段属性设置
    atkConnect(conID, 'Astrogator',
                   '*/Satellite/FastTransfer SetValue MainSequence.SegmentList.Propagate1.SegmentColor -16711936')
    atkConnect(conID, 'Astrogator',
                   '*/Satellite/FastTransfer SetValue MainSequence.SegmentList.Propagate1.Propagator Earth JGM3 20 20 true ENRLMSISE00 false 150 150 14.9186 true true false 0 GGM1 0 0 true 0 GLGM2 0 0')
    atkConnect(conID, 'Astrogator',
                   '*/Satellite/FastTransfer SetValue MainSequence.SegmentList.Propagate1.StoppingConditions R_Magnitude')
    atkConnect(conID, 'Astrogator',
                   f'*/Satellite/FastTransfer SetValue MainSequence.SegmentList.Propagate1.StoppingConditions.R_Magnitude.TripValue {propagate2_stop_radius_m} m')
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
                   '*/Satellite/FastTransfer SetValue MainSequence.SegmentList.Target_Sequence1.Action Run active profiles')

        # 5.13，设置属性页中控制变量属性
    atkConnect(conID, 'Astrogator',
                   '*/Satellite/FastTransfer SetMCSControlValue MainSequence.SegmentList.Target_Sequence1.Profiles.Differential_Corrector Maneuver ImpulsiveMnvr.Cartesian.X Active true')
    atkConnect(conID, 'Astrogator',
                   '*/Satellite/FastTransfer SetMCSControlValue MainSequence.SegmentList.Target_Sequence1.Profiles.Differential_Corrector Maneuver ImpulsiveMnvr.Cartesian.X MaxStep 300 m/sec')
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

        # 5.14，设置属性页中约束条件属性
    atkConnect(conID, 'Astrogator',
                   '*/Satellite/FastTransfer SetValue MainSequence.SegmentList.Target_Sequence1.SegmentList.Maneuver.Results Eccentricity CosineVFPA')
    atkConnect(conID, 'Astrogator',
                   '*/Satellite/FastTransfer SetMCSConstraintValue MainSequence.SegmentList.Target_Sequence1.Profiles.Differential_Corrector Maneuver Eccentricity Active true')
    atkConnect(conID, 'Astrogator',
                   f'*/Satellite/FastTransfer SetMCSConstraintValue MainSequence.SegmentList.Target_Sequence1.Profiles.Differential_Corrector Maneuver Eccentricity Desired {target2_eccentricity}')
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
    atkConnect(conID, 'Astrogator', '*/Satellite/FastTransfer RunMCS')
    atkConnect(conID, 'Animate', '* Reset')
        #    atkConnect(conID, 'Astrogator', '*/Satellite/FastTransfer ApplyAllProfileChanges')

        # 5.17，查看报告数据
    report = atkConnect(conID, 'Report_RM',
                           f'*/Satellite/FastTransfer Style "Position" TimePeriod "{report_start_time}" "{report_end_time}"')

        # 5.18，想定保存
    atkConnect(conID, 'Save', '/ *')

    return report

if __name__ == "__main__":
    mcp.run(transport="stdio")