import neovim as nvim
import os
import os.path
import re

@nvim.plugin
class LBuildFileHinter(object):
  def __init__(self, vim):
    self.vim = vim

  @nvim.function('_lbuild_get_build_root', sync=True)
  def _get_root_path(self, args):
    try:
      return self.get_root_path()
    except:
      pass

  @nvim.function('_lbuild_root_relative_path', sync=True)
  def _get_relative_path(self, args):
    curr = self.vim.command_output("echo expand('%:p')")
    try:
      curr = os.path.relpath(curr, self.get_root_path())
      return curr
    except:
      return curr

  @nvim.function('_lbuild_get_hints', sync=True)
  def _load_file_and_get_hints(self, args):
    try:
      path = self.get_buildfile_on_current_pos()
      if path is not None:
        return self.load_file_and_get_hints(path)
      return []
    except:
      return []

  @nvim.function('_lbuild_all_targets', sync=True)
  def _get_all_target(self, args):
    try:
      return self.get_all_targets()
    except:
      return []

  @nvim.function('_lbuild_current_build', sync=True)
  def _get_buildfile_on_current_pos(self, args):
    try:
      return self.get_buildfile_on_current_pos()
    except:
      pass

  def get_buildfile_on_current_pos(self):
    line = self.vim.current.line
    _, col = self.vim.current.window.cursor
    line = line[:col]
    res = re.findall(r'\s*"(.*)?:', line)
    if not res:
      return None
    
    path = res[-1]
    
    if path.startswith('//'):
      path = os.path.join(self.get_root_path(), path[2:])
    else:
      path = self.vim.command_output("echo expand('%:p')")
    return path

  def get_root_path(self):
    current_file = self.vim.command_output("echo expand('%:p')")
    current_path, _ = os.path.split(current_file)

    def find_blade_root(p):
      filename = os.path.join(p, 'BLADE_ROOT')
      if os.path.exists(filename):
        return True
      return False

    while current_path != '/':
      if find_blade_root(current_path):
        return current_path
      current_path, _ = os.path.split(current_path)

    return None

  def get_all_targets(self):
    import glob
    root_path = self.get_root_path()
    build_files = glob.glob(os.path.join(root_path, '**', 'BUILD'), recursive=True)
    result = []
    for build in build_files:
      res = self.load_file_and_get_hints(build)
      if res is not None:
        for target in res:
          result.append({
            'target': target['word'],
            'file': os.path.relpath(build, root_path)
          })
    return result

  def load_file_and_get_hints(self, filename):
    if filename is None:
      return []

    libraries = []
    def cc_library(**kwargs):
      libraries.append(kwargs['name'])
    
    def cc_binary(**kwargs):
      pass

    def cc_test(**kwargs):
      pass

    with open(filename, 'r') as fp:
      content = fp.read()

    exec(content, {
      'cc_library': cc_library,
      'cc_binary': cc_binary,
      'cc_test': cc_test,
    })

    complete_items = []
    for item in libraries:
      complete_items.append({
        "word": item,
        "menu": 'RULE at {}'.format(os.path.relpath(filename, self.get_root_path()))
      })

    return complete_items

if __name__ == '__main__':
  nvi = nvim.attach('socket', path='/var/folders/wc/5nws943d0j5c76mn60w8vvsr0000gn/T/nvimv3xPId/0')

  finder = LBuildFileHinter(nvi)

  filename = finder.get_buildfile_on_current_pos()
  print(filename)
  print(finder.load_file_and_get_hints(filename))
