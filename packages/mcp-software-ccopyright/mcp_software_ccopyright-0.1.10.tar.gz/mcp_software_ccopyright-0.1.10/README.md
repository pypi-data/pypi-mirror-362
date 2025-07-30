<div align="center">

# mcp-software-ccopyright

</div> 

# 🚀 软著大师

[中国版权保护中心官网](https://www.ccopyright.com/mobile/index.php?optionid=1367)


工作中需要申请软件著作权，软件著作权需要提供以不同的材料清单。
根据申请方类型通常包含： 单人/多人/企业/多个企业/院校/院校合作， 不同的申请方需要的材料也不一样。该MCP可以根据不同的申请方给出需要的材料和要求

申请表身份证明比较好准备，文档鉴别材料则必须手写，则用于生成程序鉴别材料。目前支持如下功能：

1. 指定多个源代码目录
2. 指定多中注释风格
3. 指定字体、字号、段前间距、段后间距、行距
4. 排除特定文件、文件夹

## 使用

### 程序鉴别材料要求

1. 每页至少50行
2. 不能含有注释、空行
3. 页眉部分必须包含软件名称、版本号、页码（软件名+版本号居中，页码右侧对齐）

### 如何实现每页50行

上述3点，第2、3两点比较好实现，第1点我通过测试发现，当：

1. 字号为10.5pt
2. 行间距为10.5pt
3. 段前间距为0
4. 段后间距为2.3pt

时，刚好实现每页50行。



## <div align="center">▶️Quick Start</div>


## 安装方法

### 方法一：从PyPI安装

```bash
# 使用pip安装
pip install mcp-software-ccopyright

# 或使用uv安装
uv pip install mcp-software-ccopyright
```

### MCP sever configuration

~~~json
{{
  "mcpServers": {
    "mcp-software-ccopyright": {
      "command": "uvx",
      "args": [
        "mcp-software-ccopyright"
      ]
    }
  }
}
~~~

## MCP 示例：

```

帮忙生成软著相关材料，
- type=企业
- project_name=mcp评估大师
- code_path=/Users/admin/Documents/deeppathai/
- output_dir=/Users/admin/Documents/deeppathai/mcp-software-ccopyright/test6

```

## <div align="center">💭Murmurs</div>
本项目仅用于学习，欢迎催更。如需定制功能、部署为 Web 服务、与内部推广平台对接，请联系产品维护者。

<div align="center"><h1>联系方式</h1></div>
  <img width="380" height="200" src="./doc/dpai.jpg" alt="mcp-software-ccopyright MCP server" />
  
  ## 商务合作联系邮件：  [deeppathai@outlook.com](mailto:deeppathai@outlook.com)

</div>


## 🧠 MCP 接入地址

- 🌐 [魔搭 ModelScope MCP 地址](https://modelscope.cn/mcp/servers/deeppathai/mcp-software-ccopyright)  
  适用于在 ModelScope 平台上调试和集成 `mcp-software-ccopyright` 服务。

