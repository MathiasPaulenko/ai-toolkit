---
name: paramiko-ssh
version: 1.0.0
author: Mathias Paulenko Echeverz
description: SSH automation with Paramiko. Covers connection handling, command execution, file transfer (SFTP), key-based auth, bastion hosts, and async patterns for remote server management.
tags: [python, ssh, paramiko, sftp, remote, automation, devops]
role: automation-engineer
model: any
trigger: When the user mentions SSH, Paramiko, remote command execution, SFTP, SCP, bastion/jump hosts, or server automation with Python.
---

# Paramiko SSH

## 1. Connection Setup

### Basic Password Auth

```python
import paramiko

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(hostname='192.168.1.10', username='admin', password='secret')
```

### Key-Based Auth

```python
client.connect(
    hostname='192.168.1.10',
    username='admin',
    key_filename='/home/user/.ssh/id_rsa',
    # Or load key from string/memory
    pkey=paramiko.RSAKey.from_private_key_file('/home/user/.ssh/id_rsa'),
)
```

### Connection Manager (Context Manager)

```python
from contextlib import contextmanager

@contextmanager
def ssh_client(hostname, username, key_filename):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(hostname=hostname, username=username, key_filename=key_filename)
        yield client
    finally:
        client.close()

with ssh_client('192.168.1.10', 'admin', '~/.ssh/id_rsa') as client:
    stdin, stdout, stderr = client.exec_command('uptime')
    print(stdout.read().decode())
```

## 2. Command Execution

### Simple Commands

```python
stdin, stdout, stderr = client.exec_command('df -h')
output = stdout.read().decode()
errors = stderr.read().decode()
```

### Sudo Commands

```python
stdin, stdout, stderr = client.exec_command('sudo -S systemctl restart nginx')
stdin.write('sudo_password\n')
stdin.flush()
print(stdout.read().decode())
```

### Streaming Output

```python
stdin, stdout, stderr = client.exec_command('tail -f /var/log/app.log', get_pty=True)
for line in iter(stdout.readline, ''):
    print(line, end='')
```

## 3. SFTP File Transfer

```python
with client.open_sftp() as sftp:
    # Upload
    sftp.put('local/file.txt', '/remote/file.txt')
    # Download
    sftp.get('/remote/file.txt', 'local/file.txt')
    # List directory
    for entry in sftp.listdir('/var/log'):
        print(entry)
    # Create remote directory
    sftp.mkdir('/remote/new_dir')
    # Remove remote file
    sftp.remove('/remote/old_file.txt')
```

## 4. Bastion / Jump Host

```python
# Connect to bastion first
bastion = paramiko.SSHClient()
bastion.set_missing_host_key_policy(paramiko.AutoAddPolicy())
bastion.connect('bastion.example.com', username='jumpuser', key_filename='~/.ssh/bastion')

# Open channel through bastion to target
vm_transport = bastion.get_transport()
dest_addr = ('target.internal', 22)
local_addr = ('127.0.0.1', 0)
channel = vm_transport.open_channel('direct-tcpip', dest_addr, local_addr)

# Connect to target through the channel
target = paramiko.SSHClient()
target.set_missing_host_key_policy(paramiko.AutoAddPolicy())
target.connect('target.internal', username='admin', sock=channel)

stdin, stdout, stderr = target.exec_command('hostname')
print(stdout.read().decode())
```

## 5. Async with AsyncSSH

```python
import asyncssh
import asyncio

async def run_remote(host, command):
    async with asyncssh.connect(host, username='admin', client_keys=['~/.ssh/id_rsa']) as conn:
        result = await conn.run(command)
        return result.stdout, result.stderr, result.exit_status

output, errors, code = asyncio.run(run_remote('server1', 'uptime'))
```

## 6. Best Practices

- Always close connections (`with` or `finally`).
- Use `AutoAddPolicy()` only in dev; use `RejectPolicy()` + known_hosts in prod.
- Load keys from environment/secrets, not hardcoded strings.
- Set `timeout` and `banner_timeout` for network resilience.
- Log all commands for audit trails.
- Use `get_pty=True` only when needed (adds overhead).

## 7. Common Patterns

### Parallel Execution on Multiple Hosts

```python
from concurrent.futures import ThreadPoolExecutor

def run_on_host(host, command):
    with ssh_client(host, 'admin', '~/.ssh/id_rsa') as client:
        _, stdout, _ = client.exec_command(command)
        return host, stdout.read().decode()

hosts = ['web1', 'web2', 'web3']
command = 'systemctl status nginx'

with ThreadPoolExecutor(max_workers=10) as pool:
    results = pool.map(lambda h: run_on_host(h, command), hosts)
```
