import os

from ..cache import set_cache, get_cache
from ..show_error import show_error
from ..processes import list_process_names
from .vcs_upgrader import VcsUpgrader


class GitUpgrader(VcsUpgrader):

    """
    Allows upgrading a local git-repository-based package
    """

    cli_name = 'git'

    def retrieve_binary(self):
        """
        Returns the path to the git executable

        :return: The string path to the executable or False on error
        """

        name = 'git'
        if os.name == 'nt':
            name += '.exe'
        binary = self.find_binary(name)

        if not binary:
            show_error(
                '''
                Unable to find %s.

                Please set the "git_binary" setting by accessing the
                Preferences > Package Settings > Package Control > Settings
                \u2013 User menu entry.

                The Settings \u2013 Default entry can be used for reference,
                but changes to that will be overwritten upon next upgrade.
                ''',
                name
            )
            return False

        if os.name == 'nt' and 'GIT_SSH' not in os.environ:
            tortoise_plink = self.find_binary('TortoisePlink.exe')
            if tortoise_plink and 'pageant.exe' in list_process_names():
                os.environ.setdefault('GIT_SSH', tortoise_plink)

        return binary

    def get_working_copy_info(self):
        binary = self.retrieve_binary()
        if not binary:
            return False

        # Get the current branch name
        res = self.execute([binary, 'symbolic-ref', '-q', 'HEAD'], self.working_copy)
        # Handle the detached head state
        if not res:
            return False
        branch = res.replace('refs/heads/', '')

        # Figure out the remote and the branch name on the remote
        remote = self.execute(
            [binary, 'config', '--get', 'branch.{}.remote'.format(branch)],
            self.working_copy,
            ignore_errors='.*'
        )
        if not remote:
            return False

        res = self.execute(
            [binary, 'config', '--get', 'branch.{}.merge'.format(branch)],
            self.working_copy,
            ignore_errors='.*'
        )
        if not res:
            return False

        remote_branch = res.replace('refs/heads/', '')

        return {
            'branch': branch,
            'remote': remote,
            'remote_branch': remote_branch
        }

    def run(self):
        """
        Updates the repository with remote changes

        :return: False or error, or True on success
        """

        binary = self.retrieve_binary()
        if not binary:
            return False

        info = self.get_working_copy_info()
        if info is False:
            return False

        args = [binary]
        args.extend(self.update_command)
        args.extend([info['remote'], info['remote_branch']])
        result = self.execute(args, self.working_copy, meaningful_output=True)
        if result is not False:
            cache_key = self.working_copy + '.incoming'
            set_cache(cache_key, None, 0)

        return True

    def incoming(self):
        """:return: bool if remote revisions are available"""

        cache_key = self.working_copy + '.incoming'
        incoming = get_cache(cache_key)
        if incoming is not None:
            return incoming

        binary = self.retrieve_binary()
        if not binary:
            return False

        info = self.get_working_copy_info()
        if info is False:
            return False

        res = self.execute([binary, 'fetch', info['remote']], self.working_copy)
        if res is False:
            return False

        args = [binary, 'log']
        args.append('..{}/{}'.format(info['remote'], info['remote_branch']))
        output = self.execute(args, self.working_copy, meaningful_output=True)
        if output is False:
            return False

        incoming = len(output) > 0

        set_cache(cache_key, incoming, self.cache_length)
        return incoming

    def latest_commit(self):
        """
        :return:
            The latest commit hash
        """

        binary = self.retrieve_binary()
        if not binary:
            return False

        args = [binary, 'rev-parse', '--short', 'HEAD']
        output = self.execute(args, self.working_copy)
        if output is False:
            return False

        return output.strip()
