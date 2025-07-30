# mcp_server_yunxiao 包初始化
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("yunxiao")

from . import tools_data360
from . import tools_insight
from . import tools_beacon
from . import tools_compass
from . import tools_rubik
from . import tools_weaver
from . import tools_spot
from . import tool_honeycomb
# 如有其它工具文件，继续补充import

def main():
    mcp.run()

if __name__ == "__main__":
    main() 