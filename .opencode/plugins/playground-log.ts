import { appendFile, mkdir } from "node:fs/promises"
import { join } from "node:path"
import { Plugin } from "@opencode/plugin"

export default Plugin.define({
  id: "sloperator.playground-log",
  async setup(ctx) {
    const logFile = join(ctx.location.project.directory, "logs", "plugin-playground.log")

    await ctx.shell.hook("create.before", async (event) => {
      if (!event.command.includes("playground/server.py")) return

      await mkdir(join(ctx.location.project.directory, "logs"), { recursive: true })
      await appendFile(logFile, "playground shell request\n")
    })
  },
})
