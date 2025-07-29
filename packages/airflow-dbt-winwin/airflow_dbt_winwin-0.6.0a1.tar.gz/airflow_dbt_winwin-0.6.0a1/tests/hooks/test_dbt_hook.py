from unittest import TestCase
from unittest import mock
import subprocess
from airflow_dbt.hooks.dbt_hook import DbtCliHook


class TestDbtHook(TestCase):

    @mock.patch('subprocess.Popen')
    def test_sub_commands(self, mock_subproc_popen):
        mock_subproc_popen.return_value \
            .communicate.return_value = ('output', 'error')
        mock_subproc_popen.return_value.returncode = 0
        mock_subproc_popen.return_value \
            .stdout.readline.side_effect = [b"placeholder"]

        hook = DbtCliHook()
        hook.run_cli('docs', 'generate')

        mock_subproc_popen.assert_called_once_with(
            [
                'dbt',
                'docs',
                'generate'
                ],
            env={},
            close_fds=True,
            cwd='.',
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT
            )

    @mock.patch('subprocess.Popen')
    def test_vars(self, mock_subproc_popen):
        mock_subproc_popen.return_value \
            .communicate.return_value = ('output', 'error')
        mock_subproc_popen.return_value.returncode = 0
        mock_subproc_popen.return_value \
            .stdout.readline.side_effect = [b"placeholder"]

        hook = DbtCliHook(vars={"foo": "bar", "baz": "true"})
        hook.run_cli('run')

        mock_subproc_popen.assert_called_once_with(
            [
                'dbt',
                'run',
                '--vars',
                '{"foo": "bar", "baz": "true"}'
                ],
            env={},
            close_fds=True,
            cwd='.',
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT
            )

    @mock.patch('subprocess.Popen')
    def test_envs(self, mock_subproc_popen):
        mock_subproc_popen.return_value \
            .communicate.return_value = ('output', 'error')
        mock_subproc_popen.return_value.returncode = 0
        mock_subproc_popen.return_value \
            .stdout.readline.side_effect = [b"placeholder"]

        hook = DbtCliHook(vars={"foo": "bar", "baz": "true"}, env={"foo": "bar", "baz": "true"})
        hook.run_cli('run')

        mock_subproc_popen.assert_called_once_with(
            [
                'dbt',
                'run',
                '--vars',
                '{"foo": "bar", "baz": "true"}'
            ],
            env={"foo": "bar", "baz": "true"},
            close_fds=True,
            cwd='.',
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT
        )
