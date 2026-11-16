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
      root.textContent = value;
    }
    return root;
  }

  function makeStick() {
    // 沿用原稿灰框里的像素棍彩蛋，使用本地矢量保持离线可用。
    const svg = document.createElementNS(svgNamespace, "svg");
    svg.setAttribute("viewBox", "0 0 100 130");
    svg.setAttribute("class", "stick-art");
    svg.setAttribute("aria-hidden", "true");
    for (let step = 0; step < 13; step += 1) {
      const rect = document.createElementNS(svgNamespace, "rect");
      rect.setAttribute("x", 9 + step * 5.5);
      rect.setAttribute("y", 110 - step * 7);
      rect.setAttribute("width", "8");
      rect.setAttribute("height", "10");
      rect.setAttribute("fill", step % 3 === 0 ? "#82603a" : "#544329");
      svg.append(rect);
      const highlight = document.createElementNS(svgNamespace, "rect");
      highlight.setAttribute("x", 10 + step * 5.5);
      highlight.setAttribute("y", 110 - step * 7);
      highlight.setAttribute("width", "3");
      highlight.setAttribute("height", "4");
      highlight.setAttribute("fill", "#9a7845");
      svg.append(highlight);
    }
    return svg;
  }

  function makeKey(key) {
    const card = document.createElement("article");
    card.className = "keycap";
    card.dataset.key = key.key;
    card.dataset.zone = key.zone;
    card.setAttribute("aria-label", key.easterEgg
      ? "Z，彩蛋，无辜的老棍"
      : `${key.key}，${data.zones[key.zone].name}，键名${key.name}，一级简码${key.short}`);

    const roots = document.createElement("div");
    roots.className = "roots";
    for (const values of key.roots) {
      const row = document.createElement("div");
      row.className = "root-row";
      row.append(...values.map(makeRoot));
      roots.append(row);
    }
    card.append(roots);

    if (key.easterEgg) {
      card.classList.add("easter-egg");
      card.append(makeStick());
      const caption = document.createElement("span");
      caption.className = "easter-caption";
      caption.textContent = "无辜的老棍";
      card.append(caption);
    }

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
    tableScroll.tabIndex = tableScroll.scrollWidth > tableScroll.clientWidth + 1 ? 0 : -1;
  }
  const resizeObserver = new ResizeObserver(updateOverflow);
  resizeObserver.observe(chartScroll);
  resizeObserver.observe(document.querySelector(".chart-canvas"));
  resizeObserver.observe(tableScroll);
  updateOverflow();

  const corrections = [
    ["R / D", "𠂆与厂的小字形接近", "分别画清撇起笔与横起笔。"],
    ["F", "雨旁的小形难以辨认", "明确绘为革字底。"],
    ["H / E", "具字头与且字片形相近", "具字头保留底横，且字片形去底横。"],
    ["K", "川与圈内三竖共用一个位置", "川列入字根栏，圈内单列三竖。"],
    ["N", "已、己、巳的手写开口接近", "三字分列，键名采用已。"],
    ["P / X", "片形容易被看成完整偏旁", "摘礻衤、母外框按片形绘制。"]
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
