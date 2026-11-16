(() => {
  "use strict";
  let instanceNumber = 0;

  function mountRootChart(container, data) {
    const instanceId = "root-chart-" + ++instanceNumber;
    const guideId = instanceId + "-guide";
    const hintId = instanceId + "-hint";
    const keys = new Map(data.keys.map(key => [key.key, key]));
    const svgNamespace = "http://www.w3.org/2000/svg";
    const root = document.createElement("div");
    root.className = "root-chart";
    const scrollHint = document.createElement("p");
    scrollHint.className = "scroll-hint";
    scrollHint.id = hintId;
    scrollHint.hidden = true;
    scrollHint.textContent = "左右滑动，查看完整键盘 ⟷";
    const chartScroll = document.createElement("section");
    chartScroll.className = "chart-scroll";
    const chartName = container.getAttribute("aria-label") || "五笔 86 字根键盘，第 " + instanceNumber + " 张";
    chartScroll.setAttribute("aria-label", chartName);
    const canvas = document.createElement("div");
    canvas.className = "chart-canvas";
    const topLabels = document.createElement("div");
    topLabels.className = "top-labels";
    topLabels.setAttribute("aria-hidden", "true");
    for (const zone of ["left", "dot"]) {
      const label = document.createElement("span");
      label.className = "zone-title";
      label.dataset.zone = zone;
      label.textContent = data.zones[zone].name;
      topLabels.append(label);
    }
    const keyboard = document.createElement("div");
    keyboard.className = "keyboard";
    const bottomLabels = document.createElement("div");
    bottomLabels.className = "bottom-labels";
    bottomLabels.setAttribute("aria-hidden", "true");
    const foldLabel = document.createElement("span");
    foldLabel.className = "zone-title";
    foldLabel.dataset.zone = "fold";
    foldLabel.textContent = data.zones.fold.name;
    bottomLabels.append(foldLabel);
    canvas.append(topLabels, keyboard, bottomLabels);
    chartScroll.append(canvas);
    const guide = document.createElement("div");
    guide.className = "reading-guide";
    guide.id = guideId;
    const paragraph = document.createElement("p");
    paragraph.append("每键首项是键名，左下是键位，右下是一级简码。");
    const ring = document.createElement("span");
    ring.className = "stroke-ring";
    ring.setAttribute("aria-hidden", "true");
    ring.textContent = "一";
    paragraph.append(ring, "圈内为笔画字根。");
    guide.append(paragraph);
    root.append(scrollHint, chartScroll, guide);
    container.append(root);

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


    function updateOverflow() {
      const overflows = chartScroll.scrollWidth > chartScroll.clientWidth + 1;
      scrollHint.hidden = !overflows;
      chartScroll.tabIndex = overflows ? 0 : -1;
      chartScroll.setAttribute("aria-describedby", overflows ? guideId + " " + hintId : guideId);
    }
    const observer = new ResizeObserver(updateOverflow);
    observer.observe(chartScroll);
    observer.observe(canvas);
    updateOverflow();
    let mounted = true;
    document.fonts.ready.then(() => {
      if (!mounted) return;
      const context = document.createElement("canvas").getContext("2d");
      for (const text of root.querySelectorAll(".root-text")) {
        context.font = "64px " + getComputedStyle(text).fontFamily;
        const metrics = context.measureText(text.textContent);
        const inkCenter = (metrics.actualBoundingBoxRight - metrics.actualBoundingBoxLeft) / 2;
        const ascent = metrics.fontBoundingBoxAscent ?? 56;
        const descent = metrics.fontBoundingBoxDescent ?? 8;
        const baseline = (64 - ascent - descent) / 2 + ascent;
        const inkMiddle = baseline + (metrics.actualBoundingBoxDescent - metrics.actualBoundingBoxAscent) / 2;
        text.style.setProperty("--ink-x", ((32 - inkCenter) / 64) + "em");
        text.style.setProperty("--ink-y", ((32 - inkMiddle) / 64) + "em");
      }
      updateOverflow();
    });
    return function unmountRootChart() {
      mounted = false;
      observer.disconnect();
      root.remove();
    };
  }

  window.mountRootChart = mountRootChart;
})();
