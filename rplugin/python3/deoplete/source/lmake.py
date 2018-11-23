from .base import Base


CompleteOutputs = "g:LanguageClient_omniCompleteResults"


class Source(Base):
    def __init__(self, vim):
        super().__init__(vim)

        self.name = "LMAKE"
        self.mark = "[LM]"
        self.rank = 1000
        self.min_pattern_length = 1
        self.filetypes = ['bzl']
        self.input_pattern += r'(:)\w*$'

    def gather_candidates(self, context):
        hints = self.vim.call('_lbuild_get_hints')
        return hints


