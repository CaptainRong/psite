(() => {
  "use strict";
  window.mountRootChart(document.getElementById("root-chart"), window.WUBI_DATA);
  const tableScroll = document.querySelector(".table-scroll");
  const tableObserver = new ResizeObserver(() => {
    tableScroll.tabIndex = tableScroll.scrollWidth > tableScroll.clientWidth + 1 ? 0 : -1;
  });
  tableObserver.observe(tableScroll);
  const corrections = [
    ["全部键位", "成字与片形的笔形、留白不一致", "采用宋体，逐项校准字形与间距。"],
    ["Q / W / E", "犬旁、登字头、豕去顶横等片形有误", "按逐键清单修正并补齐变体。"],
    ["U / I", "圈内两点、三点方向有误", "按冫与氵的方向纵向排列。"],
    ["J / K", "字根区与圈内笔画重复或有误", "J 列日、早、刂、虫，K 圈内列川。"],
    ["A / B / N 等", "印刷变体遗漏", "逐项登记并补绘。"],
    ["Z", "键内含参考作者彩蛋", "灰色空键帽，作者署名移至页脚。"]
  ];
  const correctionRows = document.getElementById("correction-rows");
  for (const values of corrections) {
    const row = document.createElement("tr");
    for (const value of values) {
      const cell = document.createElement("td");
      cell.textContent = value;
      row.append(cell);
    }
    correctionRows.append(row);
  }

  // 锚点导航自动展开记录，直接打开本地文件时同样有效。
  function revealCorrections() {
    if (window.location.hash === "#proofreading") {
      document.getElementById("proofreading").open = true;
    }
  }
  window.addEventListener("hashchange", revealCorrections);
  revealCorrections();
})();
