# Current task

Goal: 在当前 `main` 分支为 BeyondMimic 增加可选的 Unitree G1 23-DOF 动作预处理、仿真和训练入口，并保持现有 29-DOF 链路行为不变。
Do not: 不新建分支；不修改 GMR 上游实现；不把 29-DOF 动作裁剪或补零当成 23-DOF；不连接真机、不训练、不部署。

Current identity:
- Repository: `/Users/chengyuxuan/ArtiIntComVis/BeyondMimic`
- Branch: `main`
- Baseline: `3a87906 remove unwanted weights & logs`
- Upstream contract: GMR 23-DOF 资产、关节顺序和输出 schema 由另一个会话维护

Confirmed decisions:
- 23-DOF 作为新增显式 robot/task 变体；现有 29-DOF 配置、任务 ID 和默认 CSV→NPZ 路径保持不变。
- 按粗到细执行：接口与资产契约 → motion preprocessing → robot/env/task owner → 双路径回归与离线验证。
- 先冻结 23-DOF 资产契约并交给上游 Agent 核对；路径名可以调整，joint/body/schema 语义不能漂移。
- 每个步骤先写局部 `engineering-plan`，实现尚未授权。

Progress:
- [x] 系统总体路线 — Done when: 明确 GMR CSV、CSV→NPZ、URDF/FK、Articulation、task/training 的 owner 和兼容不变量
  - Evidence: 当前 `csv_to_npz.py` 固定 29 个 joint names；`robots/g1.py` 固定 29-DOF asset/actuators；`config/g1` 只注册 29-DOF tasks。
- [x] 资产与接口契约 — Done when: 23-DOF URDF 路径、23 个 joint/body 名称顺序、CSV/NPZ schema 和 GMR 输出逐项对照完成
  - Evidence: 新增本地 `assets/unitree_description/urdf/g1_23dof/main.urdf` 与 27 个官方 mesh，来源为 Unitree `unitree_ros` 的 `g1_23dof_rev_1_0.urdf`（commit `ccfc6fd8430a17ba3dacef9a1e2faf64ff3b0aee`）；23 个 actuated joint 名称/顺序、轴、位置限位、link tree 与 GMR `g1_mocap_23dof.xml` 对齐，14 个 GMR IK body 全部可映射；9 个随机姿态 FK 对比最大位置误差 `4.17e-7 m`、旋转矩阵误差 `1.46e-6`，所有 mesh/material/inertia 引用通过检查。
  - Current action: 资产已独立于 29-DOF `main.urdf`；下一步只接入 preprocessing，不改写 29-DOF owner。
- [x] Motion preprocessing — Done when: `csv_to_npz.py` 可显式选择 23-DOF，默认 29-DOF 行为不变
  - Evidence: 新增 `robots/robot_registry.py`，注册 `g1`（29 joints）和 `g1_23dof`（23 joints）；`csv_to_npz.py` 新增 `--robot`，按 registry 选择 Articulation/joint order，并在仿真前拒绝 motion DOF 宽度不匹配；29DoF 默认配置和 NPZ 字段路径保持不变。`py_compile`、`git diff --check` 和静态 joint-count 检查通过。
- [x] Robot/env/task integration — Done when: 23-DOF Articulation、env config 和 task ID 可独立加载，不改写 29-DOF owner
  - Evidence: `g1.py` 暴露 23DoF action scale；`flat_env_cfg.py` 新增 23DoF tracking body、wrist-roll end effectors 和独立 env variants；`g1/__init__.py` 新增三个 `Tracking-Flat-G1-23DoF-*` task ID；runner 使用独立 experiment name。Python compile、diff check 和静态注册检查通过，未启动训练。
- [ ] Regression and offline validation — Done when: 29-DOF 回归保持一致，23-DOF CSV→NPZ/FK/shape/limit checks 通过

Blockers:
- 已解除 URDF/mesh 阻塞。23DoF task 仍需一次 IsaacLab 单环境加载确认；官方 URDF 四个 ankle joint 的静态 effort limit 为 `35`，当前 23DoF actuator runtime contract 显式沿用 GMR 的 `50`，两者差异已保留为可见配置。

Next:
- 执行第 4 步 engineering-plan：做 23/29 双路径离线验证和最小 IsaacLab 配置加载检查，不训练、不部署。
