#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FastAPI全栈模板环境搭建脚本（修复版）
作者: Adams
创建日期: 2026-04-24
修复日期: 2026-04-24
"""

import os
import sys
import subprocess
import json
from pathlib import Path


class FastApiEnvironmentSetup:
    """FastAPI环境搭建类"""

    def __init__(self, project_path: str = None):
        """初始化环境搭建类

        Args:
            project_path: 项目路径，默认为当前工作目录
        """
        self.project_path = Path(project_path) if project_path else Path.cwd()
        self.src_path = self.project_path / "src" / "full-stack-fastapi-template"
        self.config_path = self.project_path / "config" / "project_config.yaml"

        # 颜色输出
        self.colors = {
            'green': '\033[92m',
            'red': '\033[91m',
            'yellow': '\033[93m',
            'blue': '\033[94m',
            'end': '\033[0m'
        }

    def log_info(self, message: str):
        """输出信息日志"""
        print(f"{self.colors['blue']}[INFO]{self.colors['end']} {message}")

    def log_success(self, message: str):
        """输出成功日志"""
        print(f"{self.colors['green']}[SUCCESS]{self.colors['end']} {message}")

    def log_warning(self, message: str):
        """输出警告日志"""
        print(f"{self.colors['yellow']}[WARNING]{self.colors['end']} {message}")

    def log_error(self, message: str):
        """输出错误日志"""
        print(f"{self.colors['red']}[ERROR]{self.colors['end']} {message}")

    def check_docker(self) -> tuple:
        """检查Docker和Docker Compose

        Returns:
            tuple: (docker_available, docker_compose_available)
        """
        docker_available = False
        docker_compose_available = False

        # 检查Docker
        try:
            result = subprocess.run(['docker', '--version'],
                                   capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                self.log_success(f"Docker 已安装: {result.stdout.strip()}")
                docker_available = True
            else:
                self.log_error("Docker 未安装")
        except (subprocess.TimeoutExpired, FileNotFoundError):
            self.log_error("Docker 未安装或不可用")

        # 检查Docker Compose
        try:
            result = subprocess.run(['docker', 'compose', 'version'],
                                   capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                self.log_success(f"Docker Compose 已安装: {result.stdout.strip()}")
                docker_compose_available = True
            else:
                self.log_warning("Docker Compose 未安装")
        except (subprocess.TimeoutExpired, FileNotFoundError):
            self.log_warning("Docker Compose 未安装")

        return docker_available, docker_compose_available

    def check_prerequisites(self) -> dict:
        """检查前置条件

        Returns:
            dict: 检查结果
        """
        self.log_info("检查前置条件...")

        results = {
            'project_path': False,
            'src_path': False,
            'docker': False,
            'docker_compose': False,
            'python': False,
            'node': False
        }

        # 检查项目路径
        if self.project_path.exists():
            self.log_success(f"项目路径存在: {self.project_path}")
            results['project_path'] = True
        else:
            self.log_error(f"项目路径不存在: {self.project_path}")

        # 检查源码路径
        if self.src_path.exists():
            self.log_success(f"源码路径存在: {self.src_path}")
            results['src_path'] = True
        else:
            self.log_error(f"源码路径不存在: {self.src_path}")

        # 检查Docker
        docker_available, docker_compose_available = self.check_docker()
        results['docker'] = docker_available
        results['docker_compose'] = docker_compose_available

        # 检查Python
        try:
            result = subprocess.run(['python3', '--version'],
                                   capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                version = result.stdout.strip()
                self.log_success(f"Python 已安装: {version}")
                results['python'] = True
        except (subprocess.TimeoutExpired, FileNotFoundError):
            self.log_warning("Python 未安装")

        # 检查Node.js
        try:
            result = subprocess.run(['node', '--version'],
                                   capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                version = result.stdout.strip()
                self.log_success(f"Node.js 已安装: {version}")
                results['node'] = True
        except (subprocess.TimeoutExpired, FileNotFoundError):
            self.log_warning("Node.js 未安装")

        return results

    def setup_environment_file(self) -> bool:
        """设置环境变量文件

        Returns:
            bool: 是否成功
        """
        self.log_info("设置环境变量文件...")

        env_file = self.src_path / ".env"
        env_example = self.src_path / ".env.example"

        if not env_example.exists():
            self.log_warning(".env.example 文件不存在，跳过")
            return True

        # 如果.env文件不存在，复制.env.example
        if not env_file.exists():
            try:
                import shutil
                shutil.copy(env_example, env_file)
                self.log_success("已创建 .env 文件")
            except Exception as e:
                self.log_error(f"创建 .env 文件失败: {e}")
                return False
        else:
            self.log_info(".env 文件已存在")

        return True

    def provide_manual_instructions(self):
        """提供手动安装Docker的指导"""
        self.log_info("\n" + "=" * 60)
        self.log_info("Docker安装指导")
        self.log_info("=" * 60)
        self.log_info("\n由于Docker未安装，您需要手动安装Docker：")
        self.log_info("\n1. Ubuntu/Debian:")
        self.log_info("   curl -fsSL https://get.docker.com -o get-docker.sh")
        self.log_info("   sudo sh get-docker.sh")
        self.log_info("   sudo usermod -aG docker $USER")
        self.log_info("   newgrp docker")
        self.log_info("\n2. CentOS/RHEL:")
        self.log_info("   sudo yum install -y yum-utils")
        self.log_info("   sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo")
        self.log_info("   sudo yum install docker-ce docker-ce-cli containerd.io")
        self.log_info("\n3. 官方文档:")
        self.log_info("   https://docs.docker.com/get-docker/")
        self.log_info("\n安装完成后，重新运行此脚本")
        self.log_info("=" * 60)

    def provide_project_structure_guide(self):
        """提供项目结构指导"""
        self.log_info("\n" + "=" * 60)
        self.log_info("项目结构说明")
        self.log_info("=" * 60)
        self.log_info("\n当前项目结构:")
        self.log_info(f"项目路径: {self.project_path}")
        self.log_info(f"源码路径: {self.src_path}")
        self.log_info("\n主要目录:")
        self.log_info("  src/                  - 项目源码")
        self.log_info("  scripts/              - 学习脚本")
        self.log_info("  docs/                 - 学习文档")
        self.log_info("  config/               - 项目配置")
        self.log_info("  outputs/              - 输出结果")
        self.log_info("\n重要文件:")
        self.log_info("  README.md             - 项目说明")
        self.log_info("  docs/学习计划.md      - 12周学习计划")
        self.log_info("  docs/快速开始指南.md  - 快速上手指南")
        self.log_info("=" * 60)

    def generate_status_report(self, results: dict) -> str:
        """生成状态报告

        Args:
            results: 检查结果

        Returns:
            str: 状态报告
        """
        self.log_info("\n生成状态报告...")

        report = []
        report.append("=" * 60)
        report.append("FastAPI全栈模板环境检查报告")
        report.append("=" * 60)
        report.append(f"项目路径: {self.project_path}")
        report.append(f"源码路径: {self.src_path}")
        report.append(f"检查时间: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")

        report.append("环境检查结果:")
        report.append(f"  项目路径: {'✓ 存在' if results['project_path'] else '✗ 不存在'}")
        report.append(f"  源码路径: {'✓ 存在' if results['src_path'] else '✗ 不存在'}")
        report.append(f"  Docker: {'✓ 已安装' if results['docker'] else '✗ 未安装'}")
        report.append(f"  Docker Compose: {'✓ 已安装' if results['docker_compose'] else '✗ 未安装'}")
        report.append(f"  Python: {'✓ 已安装' if results['python'] else '✗ 未安装'}")
        report.append(f"  Node.js: {'✓ 已安装' if results['node'] else '✗ 未安装'}")
        report.append("")

        # 状态判断
        if results['docker'] and results['docker_compose']:
            report.append("状态: ✅ 环境就绪，可以启动服务")
            report.append("")
            report.append("下一步:")
            report.append("  1. 进入源码目录: cd src/full-stack-fastapi-template")
            report.append("  2. 启动服务: docker compose up --build -d")
            report.append("  3. 查看日志: docker compose logs -f")
            report.append("  4. 访问应用: http://localhost")
        else:
            report.append("状态: ⚠️ 环境不完整，需要安装Docker")
            report.append("")
            report.append("建议:")
            report.append("  1. 安装Docker和Docker Compose")
            report.append("  2. 重新运行此脚本")
            report.append("  3. 或者先进行源码学习（不需要Docker）")

        report.append("")
        report.append("=" * 60)

        return '\n'.join(report)

    def run_setup(self) -> bool:
        """运行环境检查和指导

        Returns:
            bool: 检查是否通过
        """
        self.log_info("开始FastAPI环境检查...")

        # 1. 检查前置条件
        results = self.check_prerequisites()

        # 2. 如果Docker未安装，提供指导
        if not results['docker']:
            self.log_error("\n❌ Docker未安装，无法启动服务")
            self.provide_manual_instructions()

            # 3. 但项目文件已经准备好，提供项目结构指导
            self.provide_project_structure_guide()

            # 4. 生成报告
            report = self.generate_status_report(results)
            self.log_info("\n" + report)

            # 5. 保存报告
            report_file = self.project_path / "outputs" / "logs" / "setup_status_report.txt"
            report_file.parent.mkdir(parents=True, exist_ok=True)
            with open(report_file, 'w', encoding='utf-8') as f:
                f.write(report)

            return False

        # 6. 如果Docker已安装，继续设置
        if not results['project_path'] or not results['src_path']:
            self.log_error("项目路径检查失败")
            return False

        # 7. 设置环境变量文件
        self.setup_environment_file()

        # 8. 生成报告
        report = self.generate_status_report(results)
        self.log_info("\n" + report)

        # 9. 保存报告
        report_file = self.project_path / "outputs" / "logs" / "setup_status_report.txt"
        report_file.parent.mkdir(parents=True, exist_ok=True)
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)

        self.log_success("✅ 环境检查完成！")
        self.log_success(f"报告已保存到: {report_file}")

        # 10. 提供启动指导
        if results['docker'] and results['docker_compose']:
            self.log_info("\n下一步:")
            self.log_info("  1. 进入源码目录: cd src/full-stack-fastapi-template")
            self.log_info("  2. 启动服务: docker compose up --build -d")
            self.log_info("  3. 访问应用: http://localhost")

        return True


def main():
    """主函数"""
    print("=" * 60)
    print("FastAPI全栈模板环境检查脚本")
    print("=" * 60)
    print()

    # 获取项目路径
    if len(sys.argv) > 1:
        project_path = sys.argv[1]
    else:
        project_path = str(Path(__file__).parent.parent)

    print(f"项目路径: {project_path}")
    print()

    # 创建并运行环境检查
    setup = FastApiEnvironmentSetup(project_path)
    success = setup.run_setup()

    if success:
        print(f"\n{setup.colors['green']}✅ 环境检查通过！{setup.colors['end']}")
        sys.exit(0)
    else:
        print(f"\n{setup.colors['yellow']}⚠️ 环境不完整，请查看上面的指导{setup.colors['end']}")
        sys.exit(0)  # 返回0因为这是预期情况


if __name__ == "__main__":
    main()