const { spawn } = require('child_process');

const server = spawn('node', [
  '/Users/akshayvidhyasagar/AXIOM/.antigravity/scripts/mcp-wrapper.js',
  '/Users/akshayvidhyasagar/.npm/_npx/5e786f48223a616c/node_modules/.bin/gitnexus',
  'mcp'
]);

server.stdout.on('data', (data) => {
  console.log('STDOUT:', data.toString());
});

server.stderr.on('data', (data) => {
  console.log('STDERR:', data.toString());
});

server.on('exit', (code) => {
  console.log('EXIT:', code);
});

const initRequest = {
  jsonrpc: '2.0',
  id: 1,
  method: 'initialize',
  params: {
    protocolVersion: '2024-11-05',
    capabilities: {},
    clientInfo: { name: 'test-client', version: '1.0.0' }
  }
};

server.stdin.write(JSON.stringify(initRequest) + '\n');

setTimeout(() => {
  const listReposRequest = {
    jsonrpc: '2.0',
    id: 2,
    method: 'tools/call',
    params: {
      name: 'list_repos',
      arguments: {}
    }
  };
  server.stdin.write(JSON.stringify(listReposRequest) + '\n');
}, 1000);

setTimeout(() => {
  server.kill();
  process.exit(0);
}, 6000);
