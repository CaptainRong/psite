(async () => {
  const params = new URLSearchParams(location.search);
  if (params.has("scale")) document.documentElement.style.fontSize = "200%";
  if (params.has("spacing")) {
    const style = document.createElement("style");
    style.textContent = "* { line-height: 1.5 !important; letter-spacing: .12em !important; word-spacing: .16em !important; } p { margin-block-end: 2em !important; }";
    document.head.append(style);
  }
  const report = document.createElement("pre");
  report.id = "qa-report";
  report.style.whiteSpace = "pre-wrap";
  const main = document.querySelector("main");
  if (params.has("instances")) {
    const probe = document.createElement("div");
    probe.className = "keycap";
    probe.id = "style-probe";
    probe.textContent = "组件外的样式隔离检查";
    main.append(probe);
    const host = document.createElement("div");
    host.id = "second-chart";
    host.style.maxInlineSize = "40rem";
    main.append(host);
    const unmount = window.mountRootChart(host, window.WUBI_DATA);
    const button = document.createElement("button");
    button.textContent = "卸载第二张字根表";
    button.addEventListener("click", () => {
      unmount();
      unmount();
      report.textContent = JSON.stringify({remainingCharts: document.querySelectorAll(".root-chart").length,
        emptyHost: host.childElementCount === 0, primaryKeys: document.querySelectorAll("#root-chart .keycap").length});
    });
    main.append(button);
  }
  document.querySelector("#proofreading").open = true;
  await document.fonts.ready;
  await new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve)));
  const result = await axe.run(document, {runOnly: {type: "tag", values: ["wcag2a", "wcag2aa", "wcag21aa", "best-practice"]}});
  const outside = [...document.querySelectorAll(".root-chart .root,.root-chart .root-text,.root-chart .key-letter,.root-chart .short-code,.root-chart .stroke-root")]
    .filter(element => {
      const bounds = element.getBoundingClientRect();
      const card = element.closest(".keycap").getBoundingClientRect();
      return bounds.left < card.left - 1 || bounds.right > card.right + 1 || bounds.top < card.top - 1 || bounds.bottom > card.bottom + 1;
    }).map(element => element.closest(".keycap").dataset.key);
  const ids = [...document.querySelectorAll("[id]")].map(element => element.id);
  const charts = [...document.querySelectorAll(".root-chart")].map(chart => {
    const scroll = chart.querySelector(".chart-scroll");
    return {keys: chart.querySelectorAll(".keycap").length,
      roots: chart.querySelectorAll(".root").length, circles: chart.querySelectorAll(".stroke-root").length,
      emptyZ: chart.querySelector('[data-key="Z"]').childElementCount === 0,
      client: scroll.clientWidth, content: scroll.scrollWidth,
      hint: !chart.querySelector(".scroll-hint").hidden};
  });
  report.textContent = JSON.stringify({viewport: innerWidth, documentWidth: document.documentElement.scrollWidth,
    charts, uniqueIds: new Set(ids).size === ids.length, outsideCards: outside,
    outsideBorder: document.querySelector("#style-probe") ? getComputedStyle(document.querySelector("#style-probe")).borderTopWidth : null,
    violations: result.violations.map(item => ({id:item.id, targets:item.nodes.map(node=>node.target)})),
    passes:result.passes.length, incomplete:result.incomplete.map(item=>item.id)}, null, 2);
  main.append(report);
})();
