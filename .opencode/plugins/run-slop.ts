import { spawn } from "node:child_process"
import { resolve } from "node:path"
import { Plugin } from "@opencode/plugin"

interface RunResult {
  stdout: string
  stderr: string
  exitCode: number
}

function runSloperator(file: string, cwd: string, signal?: AbortSignal): Promise<RunResult> {
  return new Promise((resolvePromise, reject) => {
    const child = spawn("uv", ["run", "--no-active", "sloperator.py", file], {
      cwd,
      signal,
      env: process.env,
    })

    let stdout = ""
    let stderr = ""

    child.stdout.setEncoding("utf8")
    child.stderr.setEncoding("utf8")
    child.stdout.on("data", (chunk: string) => {
      stdout += chunk
    })
    child.stderr.on("data", (chunk: string) => {
      stderr += chunk
    })
    child.on("error", (error) => {
      if (signal?.aborted) {
        reject(error)
        return
      }
      resolvePromise({ stdout, stderr: `${stderr}${error.message}\n`, exitCode: 127 })
    })
    child.on("close", (code) => {
      resolvePromise({ stdout, stderr, exitCode: code ?? -1 })
    })
  })
}

export default Plugin.define({
  id: "sloperator.run-slop",
  async setup(ctx) {
    const root = ctx.location.project.directory

    await ctx.tool.transform((tools) => {
      tools.add({
        name: "run_slop",
        description:
          "Run a SlopLang (.slop) program with Sloperator and return its stdout, stderr, and exit code.",
        input: {
          type: "object",
          properties: {
            path: {
              type: "string",
              description: "Path to the .slop file, relative to the project root or absolute.",
            },
          },
          required: ["path"],
          additionalProperties: false,
        },
        output: {
          type: "object",
          properties: {
            stdout: { type: "string" },
            stderr: { type: "string" },
            exitCode: { type: "number" },
          },
          required: ["stdout", "stderr", "exitCode"],
          additionalProperties: false,
        },
        options: { codemode: false },
        execute: async (input, context) => {
          const file = resolve(root, (input as { path: string }).path)
          const signal = (context as { readonly signal?: AbortSignal }).signal
          const result = await runSloperator(file, root, signal)
          return {
            output: result,
            content: JSON.stringify(result, null, 2),
          }
        },
      })
    })
  },
})
