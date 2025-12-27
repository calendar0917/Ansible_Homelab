# Homelab Ansible Automation

这是一个基于 Ansible 的自动化运维项目，旨在通过“一键式”部署，完成从 **PVE (Proxmox VE) 物理宿主机** 到 **Debian 虚拟机** 的全栈监控与网关环境配置。

## 🚀 项目概览

本项目实现了以下功能的自动化集成：

* **物理层 (PVE Host)**：校园网自动认证维护、网络转发 (NAT/DNAT) 配置、物理硬件监控 。


* **系统层 (VM Init)**：自动换源、Docker 引擎安装、大容量数据盘 (240G) 自动挂载 。


* **应用层 (Docker Services)**：部署网关 (NPM)、监控 (Prometheus/Grafana/cAdvisor/Node-Exporter) 及容器管理 (Portainer) 。



## 🏗 目录结构

```txt
homelab-ansible
├── inventory.ini           # 定义物理机与虚拟机的 IP 及连接方式 
├── group_vars/             # 分组变量配置（包含加密的认证信息）
├── roles/
│   ├── pve_host            # PVE 宿主机：网络转发、校园网认证 
│   ├── vm_init             # VM 初始化：环境清理、磁盘挂载 
│   └── deploy_services     # Docker 应用：全家桶部署及监控发现 
└── site.yml                # 总调度入口文件

```

## 🛠 核心功能说明

### 1. 网络与转发逻辑

* **SNAT (出网)**：确保虚拟机通过 `vmbr1` 网桥共享宿主机网络 。


* **DNAT (入网)**：自动将宿主机的 `80/443/81` 端口流量转发至虚拟机的网关容器 。


* **校园网守护**：通过 `keep_alive.py` 脚本自动检测网络状态并在断网时重新认证 。



### 2. 自动化监控体系

* **指标采集**：整合 `Node-Exporter` (系统级) 与 `cAdvisor` (容器级) 。


* **服务发现**：Prometheus 采用 `docker_sd_configs` 模式，只需在 `docker-compose.yml` 中为新服务添加 `monitor: "true"` 标签即可自动纳入监控，无需修改配置文件 。


* **日志优化**：全局限制 Docker 日志大小为 10MB，保留 3 个副本，防止磁盘溢出 。



## 📋 部署指南

### 前提条件

1. 已安装 Ansible 的管理端电脑。
2. PVE 宿主机已开启 SSH 访问。
3. 已建立 Tailscale 连接以实现安全远程管理 。



### 部署步骤

1. **克隆仓库**
```bash
git clone https://github.com/your-username/homelab-ansible.git
cd homelab-ansible

```


2. **配置变量与加密**
修改 `group_vars/pve.yml` 填入你的认证信息，并使用 Ansible Vault 加密 ：


```bash
ansible-vault encrypt group_vars/pve.yml

```


3. **运行部署**
```bash
ansible-playbook -i inventory.ini site.yml --ask-vault-pass

```



## ⚠️ 敏感信息处理说明

本仓库已对敏感数据进行脱敏处理：

* **校园网凭证**：存储在 `group_vars/pve.yml` 中，上传前必须使用 `ansible-vault` 加密。
* **IP 地址**：请在 `inventory.ini` 中根据实际 Tailscale 或内网 IP 进行修改。

