#pylint: disable=E0401,C0411

from denite.kind.file import Kind as FileKind
from denite.kind.word import Kind as WordKind
from denite.source.base import Base

class Source(Base):
  def __init__(self, vim):
    super().__init__(vim)

    self.name = 'lmake-all-targets'
    self.kind = WordKind(vim)

  def on_init(self, context):
    context['__bufname'] = self.vim.current.buffer.name

  def gather_candidates(self, context):
    items = self.vim.call('_lbuild_all_targets')
    curr = self.vim.call('_lbuild_root_relative_path')
    candidates = []
    for item in items:
      if curr == item['file']:
        word = ':{}'.format(item['target'])
      else:
        word = '//{}:{}'.format(item['file'], item['target'])
      candidates.append({
          'word': '"{}"'.format(word),
          'abbr': word
      })
    return candidates
