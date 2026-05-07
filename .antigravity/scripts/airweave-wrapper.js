#!/usr/bin/env node
const { spawn } = require('child_process');

// Silent wrapper for airweave-mcp-search
// Redirects everything except valid JSON-RPC from stdout to stderr.

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
      // Not valid JSON-RPC
    }
    
    // Redirect non-JSON stdout to stderr
    process.stderr.write(line + '\n');
  }
});

child.stderr.on('data', (data) => {
  process.stderr.write(data);
});

child.on('exit', (code) => {
  process.exit(code);
});

child.on('error', (err) => {
  process.stderr.write(err.message + '\n');
  process.exit(1);
});
