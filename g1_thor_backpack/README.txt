G1 Thor 背包独立资产包

这是从当前 G1 OPT 的 backpack_link.STL 单独拆出的背包。原 STL 原样保留，
SHA256 为 f8ad0d2dbcd54111315733deaca32b372353c24998856606c8e7829f5baf0a40。
所有安装位置、质量和惯量均沿用原 G1 模型，没有根据外观重新估算。

文件选择
- meshes/backpack_link.STL：原始网格，用于 URDF、MuJoCo 或 CAD。
- meshes/backpack_link.obj：相同几何的通用 OBJ，单位为米。
- meshes/backpack_link.glb：可独立查看的 glTF 文件；glTF 按标准使用 Y-up，
  正常导入 Blender 后会恢复本包使用的 Z-up 坐标。
- backpack.blend：只含背包网格的 Blender 工程，原点为原背包 link 原点。
- usd/backpack_visual.usda：独立视觉 USD，无整机依赖。
- usd/backpack_rigid.usda：引用视觉 USD，另含质量、惯量和凸包碰撞。
- urdf/backpack.urdf：可单独载入的 URDF，mount_reference 为虚拟安装参考。
- urdf/backpack_fragment.urdf：供合并到整机 URDF 的 link 和 fixed joint。
- mujoco/backpack.xml：可独立编译的 MuJoCo 模型。
- mujoco/backpack_body.xml：供放入目标 torso body 的原始背包 body。
- mount_and_physics.json：坐标、安装位置、尺寸、质量与惯量。
- previews/：背包两侧的检查图，中性灰仅用于预览，原 STL 不含材质或贴图。

尺寸与坐标
原网格单位是米；不要再按毫米缩放。源机器人坐标为 X 向前、Y 向左、Z 向上。
背包约为前后 9.27 cm、左右 19.24 cm、上下 24.64 cm。
网格坐标已经以 thor_backpack_link 原点表示；不要居中后仍沿用原安装位姿。
源机器人上父 link 为 torso_link，父到背包的变换为：
  xyz = -0.094605 -0.0005 0.165324（米）
  rpy = 0 0 0（弧度）
源模型质量 1.9 kg，质心在背包 link 原点；完整惯量见 JSON/URDF。

接到 23DOF G1 的 URDF
只增加一个固定关节，不增加驱动自由度。先确认目标躯干 link 名称及其坐标系。
如果目标 torso_link 和当前 G1 使用相同的 CAD 坐标系，可直接用上面的安装变换。
如果父坐标不同，应先换算安装变换；不能只看都是 G1 就默认原点一致。

在解压目录中执行（输入、输出请换成对方的模型路径）：
  python3 attach_to_urdf.py --input /path/to/g1_23dof.urdf \
    --output /path/to/g1_23dof_with_thor.urdf --parent torso_link

也可以通过 --xyz x y z 和 --rpy r p y 指定目标父坐标系下的新安装变换。
脚本保留原有非固定关节，只添加 thor_backpack_link 和 thor_backpack_joint，
会拒绝覆盖已有输出文件或重复添加背包。相对网格路径会按新输出位置换算；
package:// 路径保留，需要对方已有对应 ROS package。

手动合并 MuJoCo
将 backpack_body.xml 的 body 放到目标躯干 body 内，并在目标 asset 中增加：
  <mesh name="backpack_link" file="实际相对路径/meshes/backpack_link.STL"/>
不要把独立模型里的 mount_reference 或一整段 worldbody 合并进目标躯干。
原碰撞、惯量和接触参数保存在 body 中。若目标已经合并背包质量，避免重复计重。

合并 USD
引用 backpack_visual.usda 可作为目标 torso 下的视觉附件，并用上述位姿安装。
需要物理背包时，引用 backpack_rigid.usda 并用 fixed joint 连接目标 torso 刚体；
body0 为躯干、body1 为背包，localPos0 为上述 xyz，localPos1 为零，旋转为单位。
初始背包世界位姿也必须与安装变换一致。不要另建一个机器人 articulation。
USD 仅使用本包内相对引用；整个 usd 子目录需要一起保留。

验证范围
核对原 STL 哈希、几何大小、转换后的拓扑与坐标、USD 引用、URDF 固定关节和
MuJoCo 独立模型。未收到对方 23DOF 资产，因此没有在对方整机上验证实际安装、
碰撞或控制效果。质量、惯量是源模型数值，并非本次称重或测量。
