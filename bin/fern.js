#!/usr/bin/env node
/**
 * npx shim. fern itself is a single stdlib-Python file; this finds a usable
 * interpreter and hands off, passing the tty straight through so colours,
 * the spinner and interactive prompts all behave.
 */
"use strict";
const { spawnSync } = require("child_process");
const path = require("path");

const SCRIPT = path.join(__dirname, "fern");

function usable(cmd) {
  const r = spawnSync(cmd, ["-c", "import sys; sys.exit(0 if sys.version_info >= (3,8) else 1)"],
                      { stdio: "ignore" });
  return r.status === 0;
}

const py = [process.env.FERN_PYTHON, "python3", "python"].find(c => c && usable(c));

if (!py) {
  const b = (s) => (process.stdout.isTTY ? `\x1b[1m${s}\x1b[0m` : s);
  const d = (s) => (process.stdout.isTTY ? `\x1b[38;5;245m${s}\x1b[0m` : s);
  console.error(`\n  ${b("fern needs Python 3.8 or newer, and couldn't find it.")}\n`);
  console.error(d("    macOS:   brew install python3"));
  console.error(d("    Ubuntu:  sudo apt install python3"));
  console.error(d("    Already installed somewhere odd? FERN_PYTHON=/path/to/python3 fern\n"));
  process.exit(1);
}

const r = spawnSync(py, [SCRIPT, ...process.argv.slice(2)], { stdio: "inherit" });
if (r.error) {
  console.error(`\n  fern failed to start: ${r.error.message}\n`);
  process.exit(1);
}
process.exit(r.status === null ? 130 : r.status);
