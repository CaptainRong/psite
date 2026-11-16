(() => {
  "use strict";

  const data = window.WUBI_DATA;
  const keyboard = document.getElementById("keyboard");
  const keys = new Map(data.keys.map(key => [key.key, key]));
  const svgNamespace = "http://www.w3.org/2000/svg";

  function makeGlyph(id) {
    const definition = data.glyphs[id];
    const svg = document.createElementNS(svgNamespace, "svg");
    svg.setAttribute("viewBox", "0 0 64 64");
    svg.setAttribute("class", "glyph");
    svg.setAttribute("role", "img");
    svg.setAttribute("aria-label", definition.label);
    const title = document.createElementNS(svgNamespace, "title");
    title.textContent = definition.label;
    svg.append(title);
    for (const stroke of definition.paths) {
      const path = document.createElementNS(svgNamespace, "path");
      path.setAttribute("d", stroke);
      svg.append(path);
    }
    return svg;
  }

  function makeRoot(value) {
    const root = document.createElement("span");
    root.className = "root";
    if (value.startsWith("@")) {
      root.append(makeGlyph(value.slice(1)));
    } else {
      const text = document.createElement("span");
      text.className = "root-text";
      text.textContent = value;
      root.append(text);
    }
    return root;
  }

  function makeKey(key) {
    const card = document.createElement("article");
    card.className = "keycap";
    card.dataset.key = key.key;
    card.dataset.zone = key.zone;
    if (key.key === "Z") {
      card.setAttribute("aria-hidden", "true");
      return card;
    }
    card.setAttribute("aria-label", `${key.key}，${data.zones[key.zone].name}，键名${key.name}，一级简码${key.short}`);

    const roots = document.createElement("div");
    roots.className = "roots";
    for (const values of key.roots) {
      const row = document.createElement("div");
      row.className = "root-row";
      row.append(...values.map(makeRoot));
      roots.append(row);
    }
    card.append(roots);

    const bottom = document.createElement("div");
    bottom.className = "key-bottom";
    const letter = document.createElement("span");
    letter.className = "key-letter";
    letter.textContent = key.key;
    bottom.append(letter);
    const stroke = document.createElement("span");
    if (key.stroke) {
      stroke.className = "stroke-root";
      stroke.append(makeGlyph(key.stroke));
    }
    bottom.append(stroke);
    const shortCode = document.createElement("span");
    shortCode.className = "short-code";
    shortCode.textContent = key.short;
    bottom.append(shortCode);
    card.append(bottom);
    return card;
  }

  for (const [index, letters] of data.rows.entries()) {
    const row = document.createElement("div");
    row.className = "key-row";
    row.append(...Array.from(letters, letter => makeKey(keys.get(letter))));
    if (index === 1 || index === 2) {
      const label = document.createElement("span");
      label.className = `zone-title ${index === 1 ? "side-label" : "right-label"}`;
      label.dataset.zone = index === 1 ? "horizontal" : "vertical";
      label.textContent = data.zones[label.dataset.zone].name;
      label.setAttribute("aria-hidden", "true");
      row.append(label);
    }
    keyboard.append(row);
  }

  // 根据实际溢出显示提示，浏览器缩放和窗口调整都会重新测量。
  const chartScroll = document.querySelector(".chart-scroll");
  const scrollHint = document.getElementById("scroll-hint");
  const tableScroll = document.querySelector(".table-scroll");
  function updateOverflow() {
    const overflows = chartScroll.scrollWidth > chartScroll.clientWidth + 1;
    scrollHint.hidden = !overflows;
    chartScroll.tabIndex = overflows ? 0 : -1;
    chartScroll.setAttribute("aria-describedby", overflows ? "reading-guide scroll-hint" : "reading-guide");
    tableScroll.tabIndex = tableScroll.scrollWidth > tableScroll.clientWidth + 1 ? 0 : -1;
  }
  const resizeObserver = new ResizeObserver(updateOverflow);
  resizeObserver.observe(chartScroll);
  resizeObserver.observe(document.querySelector(".chart-canvas"));
  resizeObserver.observe(tableScroll);
  updateOverflow();

  // 按实际墨迹中心校准偏旁，消除钅、亻等字在全角字面中的偏左留白。
  document.fonts.ready.then(() => {
    const context = document.createElement("canvas").getContext("2d");
    for (const text of document.querySelectorAll(".root-text")) {
      context.font = `64px ${getComputedStyle(text).fontFamily}`;
      const metrics = context.measureText(text.textContent);
      const inkCenter = (metrics.actualBoundingBoxRight - metrics.actualBoundingBoxLeft) / 2;
      const ascent = metrics.fontBoundingBoxAscent ?? 56;
      const descent = metrics.fontBoundingBoxDescent ?? 8;
      const baseline = (64 - ascent - descent) / 2 + ascent;
      const inkMiddle = baseline + (metrics.actualBoundingBoxDescent - metrics.actualBoundingBoxAscent) / 2;
      text.style.setProperty("--ink-x", `${(32 - inkCenter) / 64}em`);
      text.style.setProperty("--ink-y", `${(32 - inkMiddle) / 64}em`);
    }
    updateOverflow();
  });

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
