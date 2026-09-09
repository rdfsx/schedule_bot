import { spawn } from 'node:child_process';
import { accessToken, configure, root } from './cloud.js';

try {
  await configure();
  const child = spawn(process.execPath, [`${root}node_modules/@tgcloud/cli/bin/tgcloud.js`, ...process.argv.slice(2)], {
    cwd: root, stdio: 'inherit', env: { ...process.env, TGCLOUD_TOKEN: await accessToken(), TGCLOUD_DEBUG: '0' },
  });
  child.on('exit', code => { process.exitCode = code ?? 1; });
  child.on('error', error => { console.error(error.message); process.exitCode = 1; });
} catch (error) {
  console.error(error.message);
  process.exitCode = 1;
}
