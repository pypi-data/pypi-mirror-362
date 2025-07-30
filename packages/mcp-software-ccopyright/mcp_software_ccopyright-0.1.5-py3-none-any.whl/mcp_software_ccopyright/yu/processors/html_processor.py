from yu.processors import FileProcessorBase
from yu.processors import BlankLineFilter
from yu.processors.c_style_comment_block_filter import CStyleCommentBlockFilter
from yu.processors.double_slash_comment_filter import DoubleSlashCommentFilter
from yu.processors.html_comment_block_filter import HtmlCommentBlockFilter


class HtmlProcessor(FileProcessorBase):
    expected_extensions = ['.html', '.htm']

    def __init__(self):
        self.filters.append(BlankLineFilter())
        self.filters.append(CStyleCommentBlockFilter())
        self.filters.append(DoubleSlashCommentFilter())
        self.filters.append(HtmlCommentBlockFilter())
        return
