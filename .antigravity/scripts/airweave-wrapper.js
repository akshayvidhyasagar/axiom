#!/usr/bin/env node
const { spawn } = require('child_process');

process.stderr.write('[wrapper] Starting airweave-mcp-search wrapper...\n');

const child = spawn('npx', ['-y', 'airweave-mcp-search'], {
  env: process.env,
  stdio: ['pipe', 'pipe', 'pipe']
});

process.stdin.pipe(child.stdin);

child.stdout.on('data', (data) => {
  const content = data.toString();
  const lines = content.split(/\r?\n/);
  
  for (const line of lines) {
    if (!line.trim()) continue;
    
    try {
      const parsed = JSON.parse(line);
      if (parsed && (parsed.jsonrpc === '2.0' || parsed.method || parsed.result || parsed.error)) {
        process.stdout.write(JSON.stringify(parsed) + '\n');
        continue;
      }
    } catch (e) {
      // Not JSON
    }
    
    // Redirect non-JSON stdout to stderr
    process.stderr.write('[airweave-stdout] ' + line + '\n');
  }
});

child.stderr.on('data', (data) => {
  process.stderr.write('[airweave-stderr] ' + data.toString());
});

child.on('exit', (code) => {
  process.stderr.write('[wrapper] airweave-mcp-search exited with code ' + code + '\n');
  process.exit(code);
});

child.on('error', (err) => {
  process.stderr.write('[wrapper] Failed to start airweave-mcp-search: ' + err.message + '\n');
  process.exit(1);
});
