# TPS302

基于 OPENTPS v1.1.1 并结合 Proton Arc 相关功能进行优化扩展，可以实现单Spot和单野、多野IMPT计划的创建和优化，鲁棒性优化和评价，DICOM dose gamma index比较和DVH绘制，以及Arc相关功能。
目前已在 **Windows 11/Ubuntu 22.04.4LTS + Python 3.9.21** 环境下完成调试与运行验证。

---

## 📌 更新记录

- **2025/04/13 v1.0.0**
  - Windows 系统测试通过
  - 完善 7 个使用示例（examples）
- **2025/04/13 v1.0.1**
  - 完善Readme文档
- **2025/05/13 v1.0.2**
  - 修复了Linux系统不能正常进行布点和剂量计算的bug(测试环境“Ubuntu 22.04.4 LTS”)
  - 修改了WriteRTdose和WriteRTPlan的储存方式，使文件名可以包含小数点和横杠等常用特殊符号
  - 修改了ELSA.py使基于ELSA的ProtonArc测试例可以正常运行
- **2025/7/15 v1.0.3**
  - 修复了Linux系统上运行时的bug
  - 删除了部分调试用输出字段

  

---

## ⚙️ 环境要求

请确保使用 **Python 3.9.x** 版本运行本项目。

推荐使用 [Anaconda](https://www.anaconda.com/) 创建独立的 Python 3.9 环境。

---

## 📄 使用说明文档

👉 点击查看详细文档（含部署方式、功能介绍、使用示例等）：  
[📘使用文档（飞书链接）](https://ulxzeda6cz.feishu.cn/docx/W921dGNgHofYcUxi19XcOK09nsf?from=from_copylink)

---

## 📂 示例路径说明

| 说明           | 路径示例                                                                 |
|----------------|--------------------------------------------------------------------------|
| 安装后的包路径 | `D:\Anaconda\envs\OpenTPS_env\Lib\site-packages\opentps`                |
| 示例路径       | `...\opentps\core\examples\planOptimization`                             |

---

## 👨‍💻 作者信息

- **项目作者**：gcy  
- **许可证**：Apache-2.0

---

## 🧭 支持平台

- ✅ Windows 11，Ubuntu 22.04.4 LTS (已验证)
- ⛔ macOS（暂未测试）

---

## 📞 联系与反馈

如有任何问题或建议，欢迎通过项目主页或文档页面进行反馈。
