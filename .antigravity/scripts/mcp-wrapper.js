#!/usr/bin/env node
const { spawn } = require('child_process');

// Generic MCP wrapper to fix protocol violations (non-JSON on stdout).
// Usage: node mcp-wrapper.js <command> [args...]

const args = process.argv.slice(2);
if (args.length === 0) {
  process.stderr.write('Usage: node mcp-wrapper.js <command> [args...]\n');
  process.exit(1);
}

const command = args[0];
const commandArgs = args.slice(1);

const child = spawn(command, commandArgs, {
  env: process.env,
  stdio: ['pipe', 'pipe', 'pipe']
});

// Pipe stdin directly to child — no intercepting listeners
process.stdin.pipe(child.stdin);

// Filter stdout: only forward valid JSON-RPC lines, redirect everything else to stderr
let stdoutBuffer = '';
child.stdout.on('data', (data) => {
  stdoutBuffer += data.toString();
  let newlineIndex;
  while ((newlineIndex = stdoutBuffer.indexOf('\n')) !== -1) {
    const line = stdoutBuffer.substring(0, newlineIndex);
    stdoutBuffer = stdoutBuffer.substring(newlineIndex + 1);

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

    // Non-JSON-RPC output goes to stderr
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
  process.stderr.write('Failed to start ' + command + ': ' + err.message + '\n');
  process.exit(1);
});
