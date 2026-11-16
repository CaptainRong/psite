# 字根图维护

本功能将键位、字形数据和绘图工具放在同一目录下，站点从 data/wubi86.js 读取已生成的数据。修改前先读上级目录的 AGENTS.md 与对应键的勘误。

## 组件接入

页面依次加载站点主题样式、src/root-chart.css、data/wubi86.js 和 src/root-chart.js。脚本提供两个现有入口。

```js
const unmount = window.mountRootChart(container, window.WUBI_DATA);
// 页面移除这项内容时调用
unmount();
```

每次挂载产生独立说明 ID 和尺寸监听，卸载函数清理该实例。键位数据结构保持版本、三排键位、五区、字根和轮廓定义，可供后续教程和练习直接读取。

可通过容器的 aria-label 指定当前用途，例如课内参考字根表。默认名称带实例编号，帮助辅助技术区分同页多个区域。

## 配置绘图环境

从仓库根目录执行以下命令。需要 Python 3.11，默认字体是本机 Windows 宋体。字体文件由使用者本机提供。

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r features/root-chart/scripts/requirements.txt
.\.venv\Scripts\python.exe features/root-chart/scripts/rebuild.py Q N
.\.venv\Scripts\python.exe features/root-chart/scripts/rebuild.py
.\.venv\Scripts\python.exe features/root-chart/scripts/verify_data.py
```

输出默认在 `.qa/glyphs/`，包含逐键 JSON、PNG、轮廓检查图和 rebuilt-data.json。命令报告键位与轮廓的差异，有差异时返回非零退出码。看过预览并核对依据后，用 `rebuild.py Q --apply` 更新正式数据。输出位置用 `--output` 指定，字体位置用 `--font` 指定。

当前脚本的轮廓编号对应宋体基线文件，换字体或字体版本后必须逐键复核，尤其是直接选择轮廓的片形。全表重建在本机宋体上应产生零差异。

## 查找源脚本与依据

- scripts/build-Q.py 等 25 个脚本是人工核形后的源参数。共享提取和归一化逻辑在 font_source.py，真实 SVG 圈内预览在 preview_circle.py。
- 重建全部键后，可运行 scripts/crosscheck_svg.py，生成 Q、E、A、N、H、D、L 的实际 SVG 图集，帮助辨别多边形预览误差与真实残笔。
- verify_data.py 检查数量、字体字符覆盖、轮廓引用与 64 × 64 边界。站点完整数据指纹与一级简码检查由仓库 npm run check 完成。
- 图源和页码见 [references/README.md](references/README.md)，字根取舍与已知疑点见 [勘误](勘误.md)，原始修改意见见 [nextstep.txt](../../../docs/history/nextstep.txt)。

图像检查经验和绘图规则集中在局部 AGENTS.md，历史截图与原稿按版本保存在 Git 中。

参考书的键盘裁图可用 `scripts/render_reference.py` 从归档 PDF 重新生成，输出在仓库 `.qa/references/`。
