# 五笔学习站维护约定

## 当前结构与入口

站点可独立部署在 `/wubi/`。首页在 site/index.html，发布产物由 `npm run build` 生成到 dist。使用 `npm run dev` 从本机 HTTP 访问 /wubi/，使用 `npm run check` 检查数据和发布资源。源代码与网页资源使用相对路径，使站点能挂在不同前缀下。

## 修改范围

- 全站导航、页脚、主题变量与公共样式在 site 中维护。后续亮色模式围绕 site/assets/site.css 的主题变量实现，并检查对比度、原生控件和强制颜色模式。
- 新功能放在 features 下，以容器和明确数据接口接入页面。未来教程、练习共享五笔数据，避免各自复制键位和简码。
- 修改字根图、字形、键位数据或相关工具时，先读 [局部 AGENTS.md](features/root-chart/AGENTS.md)。具体画法、原图取舍和楷体事项由该文件指导。
- README 说明当前可运行的方法与建设方向。设计过程稿保存在 docs/history 和 Git 标签中，网页菜单随实际可用功能增加。

## 网页实现

沿用原图暗色五区配色、宋体与圆角键帽。实现界面改动前按 GoogleChrome Modern Web Guidance 检索相关指南，使用[官方指南](https://github.com/GoogleChrome/modern-web-guidance)。公共设计变量集中在 site/assets/site.css，功能样式限定在对应容器内。保留语义 HTML、可见焦点和用户文字缩放能力。

## 验证与交付

- 运行 npm run check。验证 /wubi/ 和另一个前缀的页面、脚本、样式与资料链接。
- 影响字根图时核对局部基线及相关浏览器检查。影响布局时检查 320/390 像素窄屏、200% 文字、缩放往返、实际溢出与键盘操作。浏览器夹具见 tools/qa/README.md。
- 发布范围由构建脚本明确收集。保留 dist/index.html 的现有离线回归能力，正式部署以 HTTP 访问为验收方式。
- 用户的原始反馈按原文归档。独有参考、手工输入先进入 Git，再清理可重建输出。生成图和验收产物放在 .qa，虚拟环境及工具缓存由 .gitignore 忽略。
- 按资料归档、代码变动和验收结果分步提交。保留已发布的历史标签，完成后报告实际检查结果与仍有疑点的字形。
