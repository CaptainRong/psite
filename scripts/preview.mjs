import * as fs from "node:fs/promises";
import http from "node:http";
import path from "node:path";
import {fileURLToPath} from "node:url";
import {buildSite, projectRoot} from "./build.mjs";

const types = {html: "text/html", css: "text/css", js: "text/javascript",
  jpg: "image/jpeg", png: "image/png", md: "text/plain"};

export async function startPreview({root = projectRoot, base = "/wubi/", port = 4386, qa = false} = {}) {
  if (!/^\/(?:[a-zA-Z0-9_-]+\/)+$/.test(base)) throw new Error("Use a path such as /wubi/ or /preview/wubi/");
  const output = path.join(root, "dist");
  const server = http.createServer(async (request, response) => {
    try {
      const url = new URL(request.url, "http://localhost");
      if (url.pathname === base.slice(0, -1)) {
        response.writeHead(308, {Location: base});
        response.end();
        return;
      }
      if (!url.pathname.startsWith(base)) {
        response.writeHead(404).end();
        return;
      }
      let relative = decodeURIComponent(url.pathname.slice(base.length)) || "index.html";
      let content;
      if (qa && relative === "__qa/") {
        relative = "index.html";
        content = (await fs.readFile(path.join(output, relative), "utf8"))
          .replace("<head>", `<head><base href="${base}">`)
          .replace("</head>", '<script src="./__qa/axe.min.js" defer></script><script src="./__qa/check.js" defer></script></head>');
      } else if (qa && ["__qa/axe.min.js", "__qa/check.js"].includes(relative)) {
        const name = relative.endsWith("axe.min.js") ? "vendor/axe.min.js" : "check.js";
        content = await fs.readFile(path.join(root, "tools/qa", name));
      } else {
        const target = path.resolve(output, relative);
        if (!target.startsWith(output + path.sep)) {
          response.writeHead(404).end();
          return;
        }
        content = await fs.readFile(target);
      }
      const extension = relative.split(".").pop();
      response.writeHead(200, {"Content-Type": (types[extension] || "application/octet-stream") +
        (extension === "jpg" || extension === "png" ? "" : "; charset=utf-8"), "Cache-Control": "no-store"});
      response.end(content);
    } catch (error) {
      response.writeHead(error.code === "ENOENT" || error.code === "EISDIR" ? 404 : 400).end();
    }
  });
  await new Promise((resolve, reject) => {
    server.once("error", reject);
    server.listen(port, "127.0.0.1", resolve);
  });
  return {server, url: `http://127.0.0.1:${server.address().port}${base}`};
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  const args = process.argv.slice(2);
  const index = args.indexOf("--base");
  await buildSite();
  const preview = await startPreview({base: index < 0 ? "/wubi/" : args[index + 1], qa: args.includes("--qa")});
  console.log(preview.url);
}
