"""Implementation of rbt alias."""

from collections import defaultdict
from subprocess import list2cmdline

from rbtools.commands import command_exists
from rbtools.commands.base import BaseCommand, CommandError, Option
from rbtools.config import get_config_paths, parse_config_file
from rbtools.utils.aliases import expand_alias


class Alias(BaseCommand):
    """A command for managing aliases defined in .reviewboardrc files."""

    name = 'alias'
    author = 'The Review Board Project'
    description = 'Manage aliases defined in .reviewboardrc files.'
    option_list = [
        Option('--list',
               action='store_true',
               dest='list_aliases',
               default=False,
               help='List all aliases defined in .reviewboardrc files.'),
        Option('--dry-run',
               metavar='ALIAS',
               dest='dry_run_alias',
               default=None,
               help='Print the command as it would be executed with the given '
                    'command-line arguments.'),
    ]

    def list_aliases(self):
        """Print a list of .reviewboardrc aliases to the command line.

        This function shows in which file each alias is defined in and if the
        alias is valid (that is, if it won't be executable because an rbt
        command exists with the same name).
        """
        # A mapping of configuration file paths to aliases.
        aliases = defaultdict(dict)

        # A mapping of aliases to configuration file paths. This allows us to
        # determine where aliases are overridden.
        predefined_aliases = {}

        config_paths = get_config_paths()

        for config_path in config_paths:
            config = parse_config_file(config_path)

            if 'ALIASES' in config:
                for alias_name, alias_cmd in config['ALIASES'].items():
                    predefined = alias_name in predefined_aliases

                    aliases[config_path][alias_name] = {
                        'command': alias_cmd,
                        'overridden': predefined,
                        'invalid': command_exists(alias_name),
                    }

                    if not predefined:
                        predefined_aliases[alias_name] = config_path

        for config_path in config_paths:
            if aliases[config_path]:
                self.stdout.write('[%s]' % config_path)

                for alias_name, entry in aliases[config_path].items():
                    self.stdout.write('    %s = %s'
                                      % (alias_name, entry['command']))

                    if entry['invalid']:
                        self.stdout.write('      !! This alias is overridden '
                                          'by an rbt command !!')
                    elif entry['overridden']:
                        self.stdout.write('      !! This alias is overridden '
                                          'by another alias in "%s" !!'
                                          % predefined_aliases[alias_name])
                self.stdout.new_line()

    def main(self, *args):
        """Run the command."""
        if ((self.options.list_aliases and self.options.dry_run_alias) or
            not (self.options.list_aliases or self.options.dry_run_alias)):
            raise CommandError('You must provide exactly one of --list or '
                               '--dry-run.')

        if self.options.list_aliases:
            self.list_aliases()
        elif self.options.dry_run_alias:
            try:
                alias = self.config['ALIASES'][self.options.dry_run_alias]
            except KeyError:
                raise CommandError('No such alias "%s"'
                                   % self.options.dry_run_alias)

            command = expand_alias(alias, args)[0]

            if isinstance(command, list):
                command = list2cmdline(command)

            self.stdout.write(command)
