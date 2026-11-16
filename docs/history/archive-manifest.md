# 整理前资料去向

基线为 `songti-v1`（fad7cbf）和 `kaiti-draft-v1`（56811e1）。原始反馈原文保存在 nextstep.txt。

| 原位置 | 长期位置或用途 |
| --- | --- |
| 五笔.jpg | features/root-chart/docs/references/original.jpg |
| nextstep.txt | docs/history/nextstep.txt |
| .qa/reference-chart.png | features/root-chart/docs/references/reference-chart.png |
| .qa/reference-book.pdf | features/root-chart/docs/references/reference-book.pdf |
| .qa/book-keyboard.png | features/root-chart/docs/references/book-keyboard.png |
| .qa/desktop.jpg | docs/history/kaiti-draft.jpg |
| .qa/songti-desktop.jpg | docs/history/songti-v1.jpg |
| .qa/key-S.png | docs/history/examples/songti-S.png |
| .qa/actual-Q.png | docs/history/examples/songti-Q.svg-preview.png |
| .qa/actual-N.png | docs/history/examples/songti-N.svg-preview.png |
| .qa/build-*.py 与共享字形工具 | features/root-chart/scripts/，按正式目录修复路径 |
| .qa/verify-data.py | features/root-chart/scripts/verify_data.py |
| .qa/axe.min.js | tools/qa/vendor/，版本与许可证随工具保存 |
| .qa/inventory-*.png、inspect-*.png、font-*.png | 临时放大图，由原图或字形检查脚本重建 |
| .qa/key-*.json、key-*.png、actual-*.png | 工作产物，逐键重建；精选图已归档 |
| .qa/reference-page-*.png、reference-G-large.png | 从参考图与出版物重建的裁图 |
| .qa/npm-cache、pdf-lib、__pycache__ | 本地依赖与缓存，验证后清理 |
| .qa/modern-web-guidance-main、modern-web-guidance.tar.gz | 指南临时副本，长期保留官方来源链接 |
| .qa/*commit.txt、kaiti-tag.txt、key-worker.txt、extract-guidance.py、search-guidance.cmd | 当轮操作草稿，经验进入维护指引 |
| .qa/a11y.html、check.js、render-reference.py | 检查方法迁入 tools/qa 与功能脚本 |

原始依据与人工调整进入 Git，重建产物默认写入 .qa。历史截图用于版本对照，网站运行资源由构建脚本单独收集。
