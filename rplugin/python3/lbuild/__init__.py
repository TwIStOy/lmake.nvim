import neovim as nvim
import os
import os.path


@nvim.plugin
class LBuildFileHinter(object):
  def __init__(self, vim):
    self.vim = vim

  @nvim.function('_lbuild_get_build_root', sync=True)
  def _get_root_path(self, args):
    return self.get_root_path()

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

  @nvim.function('_lbuild_get_hints', sync=True)
  def load_file_and_get_hints(self, args):
    filename = args[0]

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
    print(libraries)
    return libraries
