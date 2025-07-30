from mcp_software_ccopyright.yu.processors import FileProcessorBase
from mcp_software_ccopyright.yu.processors import BlankLineFilter
from mcp_software_ccopyright.yu.processors.c_style_comment_block_filter import CStyleCommentBlockFilter
from mcp_software_ccopyright.yu.processors.double_slash_comment_filter import DoubleSlashCommentFilter


class OCProcessor(FileProcessorBase):
    expected_extensions = ['.m']

    def __init__(self):
        self.filters.append(BlankLineFilter())
        self.filters.append(CStyleCommentBlockFilter())
        self.filters.append(DoubleSlashCommentFilter())
        return
