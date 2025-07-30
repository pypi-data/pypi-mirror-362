# coding: utf-8
import re
from os.path import (
    abspath,
    dirname,
    join,
)

from pkg_resources import (
    Requirement,
)
from setuptools import (
    find_packages,
    setup,
)


_COMMENT_RE = re.compile(r'(^|\s)+#.*$')


def _get_requirements(file_path):
    with open(file_path, 'r') as file:
        for line in file:
            line = _COMMENT_RE.sub('', line)
            line = line.strip()
            if line.startswith('-r '):
                for req in _get_requirements(join(dirname(abspath(file_path)), line[3:])):
                    yield req
            elif line:
                req = Requirement(line)
                req_str = req.name + str(req.specifier)
                if req.marker:
                    req_str += '; ' + str(req.marker)
                yield req_str


def _read(fname):
    return open(join(dirname(__file__), fname)).read()


setup(
    name='wsfactory',
    url='https://stash.bars-open.ru/projects/M3/repos/wsfactory',
    license=_read('LICENSE'),
    packages=find_packages('src'),
    package_dir={'': 'src'},
    package_data={'': ['schema/*']},
    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Framework :: Django :: 1.11',
        'Framework :: Django :: 2.0',
        'Framework :: Django :: 2.1',
        'Framework :: Django :: 2.2',
        'Framework :: Django :: 3.0',
        'Framework :: Django :: 3.1',
        'Framework :: Django :: 3.2',
        'Framework :: Django :: 4.0',
    ],
    description=_read('README.rst'),
    author='Timur Salyakhutdinov',
    author_email='t.salyakhutdinov@gmail.com',
    install_requires=tuple(_get_requirements('REQUIREMENTS')),
    dependency_links=('http://pypi.bars-open.ru/simple/m3-builder',),
    setup_requires=('m3-builder>=1.2,<2',),
    set_build_info=dirname(__file__),
)
