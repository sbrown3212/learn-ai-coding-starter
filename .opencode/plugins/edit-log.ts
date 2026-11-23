import { appendFile, mkdir } from "node:fs/promises"
import { join } from "node:path"
import { Plugin } from "@opencode/plugin"

const LOGGED_TOOLS = new Set(["edit", "write", "patch"])

export default Plugin.define({
  id: "sloperator.edit-log",
  async setup(ctx) {
    const logs = join(ctx.location.project.directory, "logs")
    const logFile = join(logs, "plugin-tools.log")

    await ctx.tool.hook("execute.after", async (event) => {
      if (event.status !== "completed") return
      if (!LOGGED_TOOLS.has(event.tool)) return

      await mkdir(logs, { recursive: true })
      await appendFile(logFile, `${JSON.stringify({ tool: event.tool, status: "completed" })}\n`)
    })
  },
})
