import * as fs from "node:fs/promises";
import path from "node:path";
import {fileURLToPath} from "node:url";

export const projectRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");

export async function buildSite(root = projectRoot) {
  const output = path.join(root, "dist");
  const work = path.join(root, ".qa");
  await fs.mkdir(work, {recursive: true});
  const temporary = await fs.mkdtemp(path.join(work, "build-"));
  const backup = temporary + "-previous";
  let replaced = false;
  try {
    await fs.cp(path.join(root, "site"), temporary, {recursive: true});
    for (const directory of ["src", "data"]) {
      await fs.cp(path.join(root, "features/root-chart", directory),
        path.join(temporary, "features/root-chart", directory), {recursive: true});
    }
    await fs.copyFile(path.join(root, "features/root-chart/docs/references/original.jpg"),
      path.join(temporary, "assets/reference.jpg"));
    await fs.copyFile(path.join(root, "features/root-chart/docs/勘误.md"),
      path.join(temporary, "assets/proofreading.md"));
    try {
      await fs.rename(output, backup);
      replaced = true;
    } catch (error) {
      if (error.code !== "ENOENT") throw error;
    }
    try {
      await fs.rename(temporary, output);
    } catch (error) {
      if (replaced) await fs.rename(backup, output);
      throw error;
    }
  } finally {
    // 两个目录均由本次构建在仓库 .qa 下创建。
    for (const directory of [temporary, backup]) {
      if (path.dirname(directory) !== work) throw new Error("Unexpected build cleanup path");
      await fs.rm(directory, {recursive: true, force: true});
    }
  }
  return output;
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  console.log("Built", await buildSite());
}
