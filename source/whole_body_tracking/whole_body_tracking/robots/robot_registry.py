"""Robot specifications used by motion preprocessing scripts."""

from dataclasses import dataclass

from isaaclab.assets import ArticulationCfg

from .g1 import G1_23DOF_CYLINDER_CFG, G1_23DOF_JOINT_NAMES, G1_CYLINDER_CFG


@dataclass(frozen=True)
class RobotPlatformSpec:
    """Articulation and canonical joint order for one motion platform."""

    name: str
    cfg: ArticulationCfg
    joint_names: tuple[str, ...]


G1_JOINT_NAMES = (
    "left_hip_pitch_joint",
    "left_hip_roll_joint",
    "left_hip_yaw_joint",
    "left_knee_joint",
    "left_ankle_pitch_joint",
    "left_ankle_roll_joint",
    "right_hip_pitch_joint",
    "right_hip_roll_joint",
    "right_hip_yaw_joint",
    "right_knee_joint",
    "right_ankle_pitch_joint",
    "right_ankle_roll_joint",
    "waist_yaw_joint",
    "waist_roll_joint",
    "waist_pitch_joint",
    "left_shoulder_pitch_joint",
    "left_shoulder_roll_joint",
    "left_shoulder_yaw_joint",
    "left_elbow_joint",
    "left_wrist_roll_joint",
    "left_wrist_pitch_joint",
    "left_wrist_yaw_joint",
    "right_shoulder_pitch_joint",
    "right_shoulder_roll_joint",
    "right_shoulder_yaw_joint",
    "right_elbow_joint",
    "right_wrist_roll_joint",
    "right_wrist_pitch_joint",
    "right_wrist_yaw_joint",
)


ROBOT_PLATFORMS = {
    "g1": RobotPlatformSpec("g1", G1_CYLINDER_CFG, G1_JOINT_NAMES),
    "g1_23dof": RobotPlatformSpec("g1_23dof", G1_23DOF_CYLINDER_CFG, tuple(G1_23DOF_JOINT_NAMES)),
}


def available_robot_names() -> list[str]:
    """Return the stable CLI order of registered robot names."""

    return sorted(ROBOT_PLATFORMS)


def get_robot_platform(name: str) -> RobotPlatformSpec:
    """Return a registered robot or raise a useful CLI-facing error."""

    if name not in ROBOT_PLATFORMS:
        available = ", ".join(available_robot_names())
        raise KeyError(f"Unknown robot platform '{name}'. Available: {available}")
    return ROBOT_PLATFORMS[name]
