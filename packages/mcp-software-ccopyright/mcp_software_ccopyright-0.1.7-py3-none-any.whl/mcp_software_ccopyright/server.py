from mcp.server.fastmcp import FastMCP
import shutil
import os
from mcp_software_ccopyright.yu.project import Project
from mcp_software_ccopyright.yu.processors import FileProcessor
import os


def ensure_folder_exists(folder_path):
    try:
        os.makedirs(folder_path, exist_ok=True)
    except FileExistsError as err:
        raise err
    

def extract(project_name, project_root, output_dir, lines_to_extract=3000):
    ensure_folder_exists(output_dir)
    output_file = f'{output_dir}/{project_name}系统-代码.docx'
    project = Project(project_root, lines_to_extract, output_file=output_file)
    project.run()
    return



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
    result = {
        "output_dir": output_dir
    }

    extract(project_name, code_path, output_dir=output_dir)

    # os.path.join(os.path.dirname(__file__), 'data/template.docx'))
    data_dir = os.path.dirname(__file__)
    src_file = os.path.join(data_dir, 'data/xxxxxx系统-使用说明.docx')
    dst_file = os.path.join(output_dir, f'示例-{project_name}系统-使用说明.docx')
    shutil.copy(src_file, dst_file)

    src_file = os.path.join(data_dir, 'data/xxxxxx系统-设计说明.docx')
    dst_file = os.path.join(output_dir, f'示例-{project_name}系统-设计说明.docx')
    shutil.copy(src_file, dst_file)

    src_file = os.path.join(data_dir, 'data/软件著作权登记授权委托书.png')
    dst_file = os.path.join(output_dir, f'示例-软件著作权登记授权委托书.png')
    shutil.copy(src_file, dst_file)


    src_file = os.path.join(data_dir, 'data/page1.png')
    dst_file = os.path.join(output_dir, f'示例-计算机软件著作权登记申请表1.png')
    shutil.copy(src_file, dst_file)

    src_file = os.path.join(data_dir, 'data/page2.png')
    dst_file = os.path.join(output_dir, f'示例-计算机软件著作权登记申请表2.png')
    shutil.copy(src_file, dst_file)

    src_file = os.path.join(data_dir, 'data/page3.png')
    dst_file = os.path.join(output_dir, f'示例-计算机软件著作权登记申请表3.png')
    shutil.copy(src_file, dst_file)

    src_file = os.path.join(data_dir, 'data/page4.png')
    dst_file = os.path.join(output_dir, f'示例-计算机软件著作权登记申请表4.png')
    shutil.copy(src_file, dst_file)

    src_file = os.path.join(data_dir, 'data/软件著作权证书.png')
    dst_file = os.path.join(output_dir, f'示例-软件著作权证书.png')
    shutil.copy(src_file, dst_file)

    
    if type == '院校合作':
        result['material'] = """
            院校合作申请<br>
                * 申请表（单面打印，第三页盖学校的公章）<br>
                * 源码文档（单面打印）<br>
                * 软件设计文档或者使用说明文档<br>
                * 学校的事业单位法人证书副本复印件（盖公章）<br>
                * 代理申请人的身份证复印件（正反面都要复印）<br>
                * 两个院校之前的关系如果是合作开发，则需要一份合作开发合同，盖上两个单位的公章；<br>
                * 两个院校之间的关系如果是委托开发，则需要一份委托开发合同，盖上两个单位的公章<br>
        """
    elif type == '院校':
        result['material'] = """
            院校单独申请<br>
                * 申请表（单面打印，第三页盖学校的公章）<br>
                * 源码文档（单面打印）<br>
                * 软件设计文档或者使用说明文档<br>
                * 学校的事业单位法人证书副本复印件（盖公章）<br>
                * 代理申请人的身份证复印件（正反面都要复印）<br>
        """
    elif type == '多个企业':
        result['material'] = """
            申请表（单面打印，第三页盖企业的公章）<br>
                * 源码文档（单面打印）<br>
                * 软件设计文档或者使用说明文档<br>
                * 企业营业执照复印件（复印件需要盖上企业公章）<br>
                * 代理申请人的身份证复印件（正反面都要复印）<br>
                * 两个企业之前的关系如果是合作开发，则需要一份合作开发合同，盖上两个单位的公章；<br>
                * 两个企业之间的关系如果是委托开发，则需要一份委托开发合同，盖上两个单位的公章<br>
        """

        src_file = os.path.join(data_dir, 'data/合作开发协议（企业版）.docx')
        dst_file = os.path.join(output_dir, f'示例-{project_name}合作开发协议（企业版）.docx')
        shutil.copy(src_file, dst_file)

    elif type == '多人':
        result['material'] = """
            申请材料<br>
                * 申请表（单面打印，签名）<br>
                * 源码文档（单面打印）<br>
                * 软件设计文档或者使用说明文档<br>
                * 所有著作权个人身份证复印件（正反面都要复印）<br>
                * 一份合作开发协议，所有著作权人要签名或者签章<br>
                * 如果是帮别人代理申请，则需要代理人也提供身份复印件，以及一份委托说明，委托人签字<br>
        """
        src_file = os.path.join(data_dir, 'data/合作开发协议（个人版）.docx')
        dst_file = os.path.join(output_dir, f'示例-{project_name}合作开发协议（个人版）.docx')
        shutil.copy(src_file, dst_file)

    elif type == '单人':
        result['material'] = """
            申请表（单面打印，签名）<br>
                * 源码文档（单面打印）<br>
                * 软件设计文档或者使用说明文档<br>
                * 个人身份证复印件（正反面都要复印）<br>
                * 如果是帮别人代理申请，则需要代理人也提供身份复印件，以及一份委托说明，委托人签字<br>
        """
    
    else :
        result['material'] = """
            企业申请材料<br>
            * 申请表（单面打印，第三页盖企业的公章）<br>
            * 源码文档（单面打印）<br>
            * 软件设计文档或者使用说明文档<br>
            * 企业营业执照复印件（复印件需要盖上企业公章）<br>
            * 代理申请人的身份证复印件（正反面都要复印）<br>
        """
    return result
        



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