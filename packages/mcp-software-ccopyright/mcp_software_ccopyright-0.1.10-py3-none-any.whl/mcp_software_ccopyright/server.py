from mcp.server.fastmcp import FastMCP
import shutil
import os
from mcp_software_ccopyright.yu.project import Project
from mcp_software_ccopyright.yu.processors import FileProcessor
import os
from string import Template

from .crew import report


mcp = FastMCP("mcp-software-ccopyright")

@mcp.tool(description="开始软著相关要求和材料准备， 入参： type: 单人/多人/企业/多个企业/院校/院校合作 ，project_name: 项目名称， code_path: 代码路径，output_dir: 输出目录 ")  
def kickoff(type:str, project_name: str, code_path: str, output_dir: str) -> dict:
    """
    软著相关要求和材料准备
    
    Args:
        type: 单人/多人/企业/多个企业/院校/院校合作
        project_name: 项目名称
        code_path: 代码路径
        output_dir: 输出目录
        
    Returns:
        操作结果消息
    """
    description = """
    """
    
    return report(type, project_name, code_path, output_dir)

        



# def main():
#     """主函数，运行MCP服务器"""
#     try:
#         print("启动 MCP 服务器...")
#         # 运行服务器
#         mcp.run(transport='stdio')
#     except Exception as e:
#         print(f"Error: {e}")

# if __name__ == "__main__":
#     main() 