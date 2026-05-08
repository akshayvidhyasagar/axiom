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

const fs = require('fs');
const logFile = '/Users/akshayvidhyasagar/AXIOM/mcp-wrapper.log';
function log(msg) {
  fs.appendFileSync(logFile, `[${new Date().toISOString()}] ${msg}\n`);
}

const child = spawn(command, commandArgs, {
  env: process.env,
  stdio: ['pipe', 'pipe', 'pipe']
});

log(`Started ${command} ${commandArgs.join(' ')}`);

process.stdin.on('data', (data) => {
  log(`IN: ${data.toString().trim()}`);
});
process.stdin.pipe(child.stdin);

let stdoutBuffer = '';
child.stdout.on('data', (data) => {
  log(`OUT_RAW: ${data.toString().trim()}`);
  stdoutBuffer += data.toString();
  let lastNewlineIndex;
  while ((lastNewlineIndex = stdoutBuffer.indexOf('\n')) !== -1) {
    const line = stdoutBuffer.substring(0, lastNewlineIndex);
    stdoutBuffer = stdoutBuffer.substring(lastNewlineIndex + 1);
    
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
    
    process.stderr.write(line + '\n');
  }
});

child.stderr.on('data', (data) => {
  process.stderr.write(data);
});

child.on('exit', (code) => {
  log(`Child exited with code ${code}`);
  process.exit(code);
});

child.on('error', (err) => {
  log(`Child error: ${err.message}`);
  process.stderr.write('Failed to start ' + command + ': ' + err.message + '\n');
  process.exit(1);
});
