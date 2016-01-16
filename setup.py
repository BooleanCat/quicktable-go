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
        try:
            shutil.rmtree(BUILD_DIR)
        except FileNotFoundError:
            pass

        try:
            shutil.rmtree(PKG_DIR)
        except FileNotFoundError:
            os.mkdir(PKG_DIR)

        self.build_go()

        with self.manage_libs():
            super().run()

        try:
            shutil.rmtree(os.path.join(PROJECT_DIR, 'quicktable.egg-info'))
        except FileNotFoundError:
            pass

    @classmethod
    def build_go(cls):
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
    def manage_libs(cls):
        try:
            libs = map(lambda lib_name: os.path.join(PKG_DIR, lib_name), cls.GO_LIBS.values())
            for lib in libs:
                path = os.path.join(PROJECT_DIR, 'quicktable')

                print('copying %s -> %s' % (lib, path))
                shutil.copy(lib, os.path.join(PROJECT_DIR, path))
            yield
        finally:
            libs = map(lambda lib_name: os.path.join(PROJECT_DIR, 'quicktable', lib_name), cls.GO_LIBS.values())
            for lib in libs:
                print('removing %s' % lib)

                try:
                    os.remove(lib)
                except FileNotFoundError:
                    pass


setup(
    name='quicktable',
    version='0.0.1',
    cmdclass={'install': InstallQuicktable},
    packages=['quicktable'],
    package_data={'quicktable': list(InstallQuicktable.GO_LIBS.values())}
)
