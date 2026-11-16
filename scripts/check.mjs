import assert from "node:assert/strict";
import * as fs from "node:fs/promises";
import path from "node:path";
import vm from "node:vm";
import {createHash} from "node:crypto";
import {buildSite, projectRoot} from "./build.mjs";
import {startPreview} from "./preview.mjs";

function canonical(value) {
  if (Array.isArray(value)) return value.map(canonical);
  if (value && typeof value === "object") {
    return Object.fromEntries(Object.keys(value).sort().map(key => [key, canonical(value[key])]));
  }
  return value;
}

const script = await fs.readFile(path.join(projectRoot, "features/root-chart/data/wubi86.js"), "utf8");
const context = {window: {}};
vm.runInNewContext(script, context);
const data = JSON.parse(JSON.stringify(context.window.WUBI_DATA));
const baseline = JSON.parse(await fs.readFile(path.join(projectRoot, "features/root-chart/docs/baseline.json"), "utf8"));
const digest = createHash("sha256").update(JSON.stringify(canonical(data))).digest("hex");
assert.equal(digest, baseline.sha256, "Runtime data differs from the approved baseline. Review the per-key changes before updating baseline.json.");
assert.equal(new Set(data.keys.map(key => key.key)).size, 26);
const used = new Set();
for (const key of data.keys) {
  assert.equal(key.roots.flat().length, baseline.keys[key.key].roots, key.key);
  assert.equal(key.short, baseline.keys[key.key].short, key.key);
  for (const value of key.roots.flat()) if (value.startsWith("@")) used.add(value.slice(1));
  if (key.stroke) used.add(key.stroke);
}
assert.deepEqual([...used].sort(), Object.keys(data.glyphs).sort());
for (const definition of Object.values(data.glyphs)) assert.ok(definition.label && definition.paths.length);

await buildSite();
const html = await fs.readFile(path.join(projectRoot, "dist/index.html"), "utf8");
const localLinks = [...html.matchAll(/(?:src|href)="([^"]+)"/g)].map(match => match[1])
  .filter(link => !/^(https?:|data:|#)/.test(link));
for (const base of ["/wubi/", "/preview/wubi/"]) {
  const preview = await startPreview({base, port: 0});
  try {
    for (const link of ["./", ...localLinks]) {
      const response = await fetch(new URL(link, preview.url));
      assert.equal(response.status, 200, base + link);
    }
    for (const file of ["README.md", ".qa/check.js", "features/root-chart/scripts/font_source.py", "../site/index.html"]) {
      assert.equal((await fetch(new URL(file, preview.url))).status, 404, file);
    }
    assert.equal((await fetch(preview.url.slice(0, -1), {redirect: "manual"})).status, 308);
  } finally {
    preview.server.closeAllConnections();
    await new Promise(resolve => preview.server.close(resolve));
  }
}
for (const file of ["site/assets/app.js", "features/root-chart/src/root-chart.js"]) {
  new vm.Script(await fs.readFile(path.join(projectRoot, file), "utf8"));
}
console.log("Passed: baseline data, script syntax, local assets, two path prefixes, publication boundaries.");
