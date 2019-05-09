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
  """Runs pytest"""
  with open('requirements_dev.txt', 'r') as reqs_file:
    reqs = reqs_file.readlines()
  session.install(*reqs)
  session.run('pip', 'list')
  session.run('pytest')


@nox.session(reuse_venv=True)
def build_docs(session):
  """Builds documentation using Sphinx. Outputs to docs/, will open browser."""
  session.install('Sphinx')

  # clean up a bit first
  for del_file in ['docs/{{cookiecutter.project_slug}}.rst',
	                 'docs/modules.rst']:
    try:
      os.remove(del_file)
    except FileNotFoundError as fnfe: 
      pass
  
  # build docs
  session.run('sphinx-apidoc', '-o', 'docs/', '{{cookiecutter.project_slug}}')
  # TODO: upload to S3? readthedocs? github pages?
  _browser('docs/')


@nox.session(reuse_venv=True)
def build_sdist(session):
  """Builds Source Distribution package. Outputs to dist/"""
  session.run('python3', 'setup.py', 'sdist')
  assert os.path.exists('dist/')