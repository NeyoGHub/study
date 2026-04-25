#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FastAPI全栈模板环境搭建脚本
作者: Adams
创建日期: 2026-04-24
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

    def check_prerequisites(self) -> bool:
        """检查前置条件

        Returns:
            bool: 是否满足前置条件
        """
        self.log_info("检查前置条件...")

        # 检查项目路径
        if not self.project_path.exists():
            self.log_error(f"项目路径不存在: {self.project_path}")
            return False

        # 检查源码路径
        if not self.src_path.exists():
            self.log_error(f"源码路径不存在: {self.src_path}")
            return False

        # 检查Docker
        try:
            result = subprocess.run(['docker', '--version'],
                                   capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                self.log_success(f"Docker 已安装: {result.stdout.strip()}")
            else:
                self.log_error("Docker 未安装")
                return False
        except (subprocess.TimeoutExpired, FileNotFoundError):
            self.log_error("Docker 未安装或不可用")
            return False

        # 检查Docker Compose
        try:
            result = subprocess.run(['docker', 'compose', 'version'],
                                   capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                self.log_success(f"Docker Compose 已安装: {result.stdout.strip()}")
            else:
                self.log_warning("Docker Compose 未安装，尝试使用 docker-compose")
        except (subprocess.TimeoutExpired, FileNotFoundError):
            self.log_warning("Docker Compose 未安装")

        # 检查Python
        try:
            result = subprocess.run(['python3', '--version'],
                                   capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                version = result.stdout.strip()
                self.log_success(f"Python 已安装: {version}")
            else:
                self.log_warning("Python 未安装")
        except (subprocess.TimeoutExpired, FileNotFoundError):
            self.log_warning("Python 未安装")

        # 检查Node.js
        try:
            result = subprocess.run(['node', '--version'],
                                   capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                self.log_success(f"Node.js 已安装: {result.stdout.strip()}")
            else:
                self.log_warning("Node.js 未安装")
        except (subprocess.TimeoutExpired, FileNotFoundError):
            self.log_warning("Node.js 未安装")

        return True

    def setup_environment_file(self) -> bool:
        """设置环境变量文件

        Returns:
            bool: 是否成功
        """
        self.log_info("设置环境变量文件...")

        env_file = self.src_path / ".env"
        env_example = self.src_path / ".env.example"

        if not env_example.exists():
            self.log_warning(".env.example 文件不存在")
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

    def start_docker_services(self) -> bool:
        """启动Docker服务

        Returns:
            bool: 是否成功
        """
        self.log_info("启动Docker服务...")

        if not self.src_path.exists():
            self.log_error("源码路径不存在")
            return False

        try:
            # 检查是否有docker-compose.yml
            compose_files = [
                self.src_path / "docker-compose.yml",
                self.src_path / "compose.yml",
                self.src_path / "docker-compose.yaml"
            ]

            compose_file = None
            for file in compose_files:
                if file.exists():
                    compose_file = file
                    break

            if not compose_file:
                self.log_error("未找到 Docker Compose 配置文件")
                return False

            self.log_info(f"使用配置文件: {compose_file.name}")

            # 构建并启动服务
            self.log_info("构建Docker镜像...")
            result = subprocess.run(
                ['docker', 'compose', '-f', str(compose_file), 'up', '--build', '-d'],
                cwd=self.src_path,
                capture_output=True,
                text=True,
                timeout=600  # 10分钟超时
            )

            if result.returncode == 0:
                self.log_success("Docker服务启动成功")
                return True
            else:
                self.log_error(f"Docker服务启动失败: {result.stderr}")
                return False

        except subprocess.TimeoutExpired:
            self.log_error("Docker服务启动超时")
            return False
        except Exception as e:
            self.log_error(f"启动Docker服务时出错: {e}")
            return False

    def check_service_status(self) -> dict:
        """检查服务状态

        Returns:
            dict: 服务状态信息
        """
        self.log_info("检查服务状态...")

        status = {
            'backend': False,
            'frontend': False,
            'database': False,
            'services': []
        }

        try:
            result = subprocess.run(
                ['docker', 'compose', 'ps'],
                cwd=self.src_path,
                capture_output=True,
                text=True,
                timeout=30
            )

            if result.returncode == 0:
                self.log_success("服务状态查询成功")
                self.log_info(result.stdout)

                # 解析服务状态
                lines = result.stdout.split('\n')
                for line in lines:
                    if 'backend' in line.lower() and 'up' in line.lower():
                        status['backend'] = True
                        status['services'].append('backend')
                    if 'frontend' in line.lower() and 'up' in line.lower():
                        status['frontend'] = True
                        status['services'].append('frontend')
                    if 'postgres' in line.lower() or 'db' in line.lower():
                        if 'up' in line.lower():
                            status['database'] = True
                            status['services'].append('database')

        except Exception as e:
            self.log_error(f"检查服务状态时出错: {e}")

        return status

    def test_api_access(self) -> bool:
        """测试API访问

        Returns:
            bool: API是否可访问
        """
        self.log_info("测试API访问...")

        try:
            import requests
            response = requests.get('http://localhost:8000/docs', timeout=10)

            if response.status_code == 200:
                self.log_success("API文档可访问: http://localhost:8000/docs")
                return True
            else:
                self.log_warning(f"API文档返回状态码: {response.status_code}")
                return False

        except ImportError:
            self.log_warning("requests 库未安装，跳过API测试")
            return True
        except Exception as e:
            self.log_warning(f"API测试失败: {e}")
            return False

    def run_health_check(self) -> bool:
        """运行健康检查

        Returns:
            bool: 健康检查是否通过
        """
        self.log_info("运行健康检查...")

        try:
            result = subprocess.run(
                ['docker', 'compose', 'ps'],
                cwd=self.src_path,
                capture_output=True,
                text=True,
                timeout=30
            )

            if result.returncode == 0:
                # 检查是否有服务正在运行
                if 'Up' in result.stdout:
                    self.log_success("健康检查通过 - 服务正在运行")
                    return True
                else:
                    self.log_warning("健康检查失败 - 服务未运行")
                    return False

        except Exception as e:
            self.log_error(f"健康检查时出错: {e}")

        return False

    def generate_setup_report(self) -> str:
        """生成环境搭建报告

        Returns:
            str: 环境搭建报告
        """
        self.log_info("生成环境搭建报告...")

        report = []
        report.append("=" * 60)
        report.append("FastAPI全栈模板环境搭建报告")
        report.append("=" * 60)
        report.append(f"项目路径: {self.project_path}")
        report.append(f"源码路径: {self.src_path}")
        report.append(f"报告时间: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")

        # 检查服务状态
        status = self.check_service_status()
        report.append("服务状态:")
        report.append(f"  后端服务: {'✓ 运行中' if status['backend'] else '✗ 未运行'}")
        report.append(f"  前端服务: {'✓ 运行中' if status['frontend'] else '✗ 未运行'}")
        report.append(f"  数据库服务: {'✓ 运行中' if status['database'] else '✗ 未运行'}")
        report.append("")

        # 访问信息
        report.append("访问信息:")
        report.append("  前端: http://localhost")
        report.append("  后端API: http://localhost/api/docs")
        report.append("  数据库: localhost:5432")
        report.append("")

        # 下一步
        report.append("下一步:")
        report.append("  1. 访问前端页面查看应用")
        report.append("  2. 访问API文档测试接口")
        report.append("  3. 开始学习源码")
        report.append("  4. 尝试修改代码并测试")
        report.append("")

        report.append("=" * 60)

        return '\n'.join(report)

    def run_setup(self) -> bool:
        """运行完整的环境搭建流程

        Returns:
            bool: 是否成功
        """
        self.log_info("开始FastAPI环境搭建...")

        # 1. 检查前置条件
        if not self.check_prerequisites():
            self.log_error("前置条件检查失败")
            return False

        # 2. 设置环境变量文件
        if not self.setup_environment_file():
            self.log_error("环境变量文件设置失败")
            return False

        # 3. 启动Docker服务
        if not self.start_docker_services():
            self.log_error("Docker服务启动失败")
            return False

        # 等待服务启动
        self.log_info("等待服务启动...")
        import time
        time.sleep(10)

        # 4. 检查服务状态
        status = self.check_service_status()
        if not any(status.values()):
            self.log_error("没有服务成功启动")
            return False

        # 5. 运行健康检查
        if not self.run_health_check():
            self.log_warning("健康检查未通过，但服务可能仍在启动中")

        # 6. 测试API访问
        self.test_api_access()

        # 7. 生成报告
        report = self.generate_setup_report()
        self.log_info("\n" + report)

        # 保存报告
        report_file = self.project_path / "outputs" / "logs" / "setup_report.txt"
        report_file.parent.mkdir(parents=True, exist_ok=True)
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)

        self.log_success("环境搭建完成！")
        self.log_success(f"报告已保存到: {report_file}")

        return True


def main():
    """主函数"""
    print("=" * 60)
    print("FastAPI全栈模板环境搭建脚本")
    print("=" * 60)
    print()

    # 获取项目路径
    if len(sys.argv) > 1:
        project_path = sys.argv[1]
    else:
        project_path = str(Path(__file__).parent.parent)

    print(f"项目路径: {project_path}")
    print()

    # 创建并运行环境搭建
    setup = FastApiEnvironmentSetup(project_path)
    success = setup.run_setup()

    if success:
        print(f"\n{setup.colors['green']}环境搭建成功！{setup.colors['end']}")
        sys.exit(0)
    else:
        print(f"\n{setup.colors['red']}环境搭建失败！{setup.colors['end']}")
        sys.exit(1)


if __name__ == "__main__":
    main()