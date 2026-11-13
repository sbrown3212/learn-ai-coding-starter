---
description: Start the Sloperator web playground on a port
---

Start the Sloperator playground server.

Requested port: `$ARGUMENTS`. If that is empty, use `8080`. If it is not a number, stop
and ask rather than guessing.

Listeners already on this machine:

!`lsof -nP -iTCP -sTCP:LISTEN`

Use that list before starting anything:

1. If a listener is already the playground, do not start a second one. Confirm by
   running `ps -p <pid> -o command=` and looking for `playground/server.py`; if it
   matches, report its port and PID and stop.

2. If the chosen port is held by any other process, report what holds it and stop. Do
   not kill it — it may be someone else's work.

3. Otherwise start the server as a background process, so the session stays usable:

   ```bash
   uv run playground/server.py <port>
   ```

   Substitute the resolved port (the argument, or `8080`). Start it in the background
   and keep the PID; do not run it in the foreground, where it would block.

4. Report the URL (`http://localhost:<port>`) and the PID.
