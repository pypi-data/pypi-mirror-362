"""
命令行入口点，用于运行 MCP 服务器
"""
import sys
import logging
from mcp.server.fastmcp import FastMCP
from mcp_software_ccopyright.server import mcp

# 设置日志格式
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def main():
    """主函数，运行MCP服务器"""
    try:
        print("启动 MCP ...", file=sys.stderr)
        # 运行服务器
        mcp.run(transport='stdio')
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main() 