import os
import shutil
import subprocess
from setuptools import setup
from contextlib import contextmanager
from setuptools.command.install import install


PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
LIB_DIR = os.path.join(PROJECT_DIR, 'lib')
PKG_DIR = os.path.join(PROJECT_DIR, 'pkg')
BUILD_DIR = os.path.join(PROJECT_DIR, 'build')


class InstallQuicktable(install):
    GO_LIBS = {
        'add.go': 'libadd.so',
    }

    def run(self):
        """Build the quicktable module."""

        try:
            shutil.rmtree(BUILD_DIR)
        except FileNotFoundError:
            pass

        try:
            shutil.rmtree(PKG_DIR)
        except FileNotFoundError:
            os.mkdir(PKG_DIR)

        self.build_go()

        with self._manage_libs():
            super().run()

        try:
            shutil.rmtree(os.path.join(PROJECT_DIR, 'quicktable.egg-info'))
        except FileNotFoundError:
            pass

    @classmethod
    def build_go(cls):
        """Build Go libraries requires for quicktable.

        For each source file in PROJECT_DIR/lib, produce a lib{source}.so file in PROJECT_DIR/pkg.

        """

        print('building Go packages')

        for source, lib in cls.GO_LIBS.items():
            print('%s -> %s' % (source, lib))

            subprocess.call([
                'go',
                'build',
                '-buildmode=c-shared',
                '-o',
                os.path.join(PKG_DIR, lib),
                os.path.join(LIB_DIR, source),
            ])

        print('finished building go packages')

    @classmethod
    @contextmanager
    def _manage_libs(cls):
        try:
            libs = cls.join_paths([PKG_DIR], cls.GO_LIBS.values())
            for lib in libs:
                path = os.path.join(PROJECT_DIR, 'quicktable')

                print('copying %s -> %s' % (lib, path))
                shutil.copy(lib, os.path.join(PROJECT_DIR, path))
            yield
        finally:
            libs = cls.join_paths([PROJECT_DIR, 'quicktable'], cls.GO_LIBS.values())
            for lib in libs:
                print('removing %s' % lib)

                try:
                    os.remove(lib)
                except FileNotFoundError:
                    pass

    @staticmethod
    def join_paths(root, suffixes):
        """Join root path to each of suffixes.

        :param root: path in the from ['my', 'awesome', 'path']
        :param suffixes: list of suffices to join to root

        :returns: a map of os.path.join(root, suffix) of suffixes

        """
        
        return map(lambda suffix: os.path.join(*root, suffix), suffixes)


setup(
    name='quicktable',
    version='0.0.1',
    cmdclass={'install': InstallQuicktable},
    packages=['quicktable'],
    package_data={'quicktable': list(InstallQuicktable.GO_LIBS.values())}
)
