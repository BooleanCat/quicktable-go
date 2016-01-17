import os
import shutil
import subprocess
from setuptools import setup
from setuptools.command.install import install


PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
LIB_DIR = os.path.join(PROJECT_DIR, 'lib')
PKG_DIR = os.path.join(PROJECT_DIR, 'pkg')
BUILD_DIR = os.path.join(PROJECT_DIR, 'build')
SOURCE_DIR = os.path.join(PROJECT_DIR, 'quicktable')


class InstallQuicktable(install):
    GO_SOURCES = ['table.go', 'utils.go', 'table_bindings.go']
    GO_SOURCE_PATHS = [os.path.join(LIB_DIR, source) for source in GO_SOURCES]
    LIB_NAME = 'libquicktable.so'

    def run(self):
        """Build the quicktable module."""

        self.rm_tree(BUILD_DIR)
        self.build_go()
        self.copy(os.path.join(PKG_DIR, self.LIB_NAME), SOURCE_DIR)

        super().run()

        self.rm_tree(PKG_DIR)
        self.rm_tree(os.path.join(PROJECT_DIR, 'quicktable.egg-info'))
        self.unlink(os.path.join(SOURCE_DIR, self.LIB_NAME))

    @staticmethod
    def rm_tree(path):
        print('removing %s' % path)
        try:
            shutil.rmtree(path)
        except FileNotFoundError:
            pass

    @staticmethod
    def unlink(path):
        print('removing %s' % path)
        try:
            os.unlink(path)
        except FileNotFoundError:
            pass

    @staticmethod
    def copy(source, target):
        print('copying %s -> %s' % (source, target))
        shutil.copy(source, target)

    @classmethod
    def build_go(cls):
        """Build Go libraries requires for quicktable.

        For each source file in PROJECT_DIR/lib, produce a lib{source}.so file in PROJECT_DIR/pkg.

        """

        print('building Go package')

        subprocess.call([
            'go',
            'build',
            '-buildmode=c-shared',
            '-o',
            os.path.join(PKG_DIR, cls.LIB_NAME),
        ] + cls.GO_SOURCE_PATHS)


setup(
    name='quicktable',
    version='0.0.1',
    cmdclass={'install': InstallQuicktable},
    packages=['quicktable'],
    package_data={'quicktable': [InstallQuicktable.LIB_NAME]}
)
