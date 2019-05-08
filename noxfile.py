from os.path import abspath
import os
import sys
import webbrowser

import nox

try:
	from urllib import pathname2url
except:
	from urllib.request import pathname2url


def _browser(path):
  webbrowser.open("file://" + pathname2url(abspath(path)))


@nox.session(reuse_venv=True, python=['2.7', '3.6', '3.7'])
def test(session, python):
  with open('requirements_dev.txt', 'r') as reqs_file:
    reqs = reqs_file.readlines()
  session.install(*reqs)
  session.run('pip', 'list')
  session.run('pytest')


@nox.session(reuse_venv=True)
def check_coverage(session):
  for cmd in [
        ['coverage', 'run', '--source', '{{cookiecutter.project_slug}}', '-m', 'pytest'],
        ['coverage', 'report', '-m'],
        ['coverage', 'html']
      ]:
	  session.run(*cmd)
  _browser('htmlcov/index.html')


@nox.session(reuse_venv=True)
def lint(session):
  session.install('pylint')
  session.run('pylint')


@nox.session(reuse_venv=True)
def build_docs(session):
  session.install('Sphinx')
  
  for del_file in ['docs/{{ cookiecutter.project_slug }}.rst',
	                 'docs/modules.rst']:
    try:
      os.remove(del_file)
    except FileNotFoundError as fnfe: 
      pass
  session.run('sphinx-apidoc', '-o', 'docs/', '{{cookiecutter.project_slug}}')
  _browser('docs/')


@nox.session(reuse_venv=True)
def build_sdist(session):
  session.run('python3', 'setup.py', 'sdist')
  assert os.path.exists('dist/')