"""Tests for the Sugar Swarm extension."""

from unittest.mock import MagicMock, patch

import pytest

from sugar.extensions.swarm import SugarSwarm
from sugar.logs import SugarError


@pytest.fixture
def sugar_swarm() -> SugarSwarm:
    """Return a SugarSwarm instance with a mocked backend."""
    swarm = SugarSwarm()
    swarm.backend_app = MagicMock()
    # Set up _call_backend_app to capture stdout/stderr using proper casting
    mock_call = MagicMock()
    setattr(swarm, '_call_backend_app', mock_call)
    return swarm


class TestSwarmInit:
    """Test the swarm init command."""

    def test_init_basic(self, sugar_swarm: SugarSwarm) -> None:
        """Test basic swarm init command."""
        # Call the init command - not passing _out/_err
        # since the decorator doesn't allow it
        sugar_swarm._cmd_init()

        # Check that _call_swarm_command was called with correct args
        mock_call = getattr(sugar_swarm, '_call_backend_app')
        mock_call.assert_called_once()
        call_args_list = mock_call.call_args_list[0][0]
        assert 'init' in call_args_list

    def test_init_with_options(self, sugar_swarm: SugarSwarm) -> None:
        """Test swarm init with options."""
        options = '--advertise-addr 192.168.1.1'

        # Call init with options
        sugar_swarm._cmd_init(options=options)

        # Mock verifications - check that options were passed correctly
        mock_call = getattr(sugar_swarm, '_call_backend_app')
        mock_call.assert_called_once()
        # Get the options_args that were passed to _call_backend_app
        options_args = mock_call.call_args[1].get('options_args', [])
        assert '--advertise-addr' in options_args
        assert '192.168.1.1' in options_args


class TestSwarmNode:
    """Test the swarm node command and subcommands."""

    def test_node_command_help(self, sugar_swarm: SugarSwarm) -> None:
        """Test node command with no subcommand shows help."""
        with patch('sugar.logs.SugarLogs.print_warning') as mock_warning:
            sugar_swarm._cmd_node()
            mock_warning.assert_called_once()

    def test_node_demote(self, sugar_swarm: SugarSwarm) -> None:
        """Test node demote subcommand."""
        # Setup subcmd_node_demote mock
        mock = MagicMock()
        setattr(sugar_swarm, '_subcmd_node_demote', mock)

        # Call node with demote parameter
        sugar_swarm._cmd_node(demote='node1')

        # Verify the correct subcommand was called
        mock.assert_called_once_with(nodes='node1', options='')

    def test_node_inspect(self, sugar_swarm: SugarSwarm) -> None:
        """Test node inspect subcommand."""
        # Setup subcmd_node_inspect mock
        mock = MagicMock()
        setattr(sugar_swarm, '_subcmd_node_inspect', mock)

        # Call node with inspect parameter
        sugar_swarm._cmd_node(inspect='node1,node2')

        # Verify the correct subcommand was called
        mock.assert_called_once_with(nodes='node1,node2', options='')

    def test_node_ls(self, sugar_swarm: SugarSwarm) -> None:
        """Test node ls subcommand."""
        # Setup subcmd_node_ls mock
        mock = MagicMock()
        setattr(sugar_swarm, '_subcmd_node_ls', mock)

        # Call node with ls parameter
        sugar_swarm._cmd_node(ls=True)

        # Verify the correct subcommand was called
        mock.assert_called_once_with(options='')

    def test_node_promote(self, sugar_swarm: SugarSwarm) -> None:
        """Test node promote subcommand."""
        # Setup subcmd_node_promote mock
        mock = MagicMock()
        setattr(sugar_swarm, '_subcmd_node_promote', mock)

        # Call node with promote parameter
        sugar_swarm._cmd_node(promote='node1')

        # Verify the correct subcommand was called
        mock.assert_called_once_with(nodes='node1', options='')

    def test_node_ps(self, sugar_swarm: SugarSwarm) -> None:
        """Test node ps subcommand."""
        # Setup subcmd_node_ps mock
        mock = MagicMock()
        setattr(sugar_swarm, '_subcmd_node_ps', mock)

        # Call node with ps parameter
        sugar_swarm._cmd_node(ps='node1')

        # Verify the correct subcommand was called
        mock.assert_called_once_with(nodes='node1', options='')

    def test_node_rm(self, sugar_swarm: SugarSwarm) -> None:
        """Test node rm subcommand."""
        # Setup subcmd_node_rm mock
        mock = MagicMock()
        setattr(sugar_swarm, '_subcmd_node_rm', mock)

        # Call node with rm parameter
        sugar_swarm._cmd_node(rm='node1')

        # Verify the correct subcommand was called
        mock.assert_called_once_with(nodes='node1', options='')

    def test_node_update(self, sugar_swarm: SugarSwarm) -> None:
        """Test node update subcommand."""
        # Setup subcmd_node_update mock
        mock = MagicMock()
        setattr(sugar_swarm, '_subcmd_node_update', mock)

        # Call node with update parameter
        sugar_swarm._cmd_node(update='node1')

        # Verify the correct subcommand was called
        mock.assert_called_once_with(nodes='node1', options='')


class TestNodeErrorHandling:
    """Test error handling in node subcommands."""

    def test_node_demote_no_nodes(self, sugar_swarm: SugarSwarm) -> None:
        """Test node demote fails without nodes."""
        with patch(
            'sugar.logs.SugarLogs.raise_error', side_effect=SystemExit
        ) as mock_error:
            with pytest.raises(SystemExit):
                # Using an empty string should trigger the error
                sugar_swarm._subcmd_node_demote(nodes='')
            mock_error.assert_called_once_with(
                'Node name(s) must be provided for the "demote" command.',
                SugarError.SUGAR_INVALID_PARAMETER,
            )

    def test_node_inspect_no_nodes(self, sugar_swarm: SugarSwarm) -> None:
        """Test node inspect fails without nodes."""
        with patch(
            'sugar.logs.SugarLogs.raise_error', side_effect=SystemExit
        ) as mock_error:
            with pytest.raises(SystemExit):
                # Using an empty string should trigger the error
                sugar_swarm._subcmd_node_inspect(nodes='')
            mock_error.assert_called_once_with(
                'Node name(s) must be provided for the "inspect" command.',
                SugarError.SUGAR_INVALID_PARAMETER,
            )

    def test_node_promote_no_nodes(self, sugar_swarm: SugarSwarm) -> None:
        """Test node promote fails without nodes."""
        with patch(
            'sugar.logs.SugarLogs.raise_error', side_effect=SystemExit
        ) as mock_error:
            with pytest.raises(SystemExit):
                # Using an empty string should trigger the error
                sugar_swarm._subcmd_node_promote(nodes='')
            mock_error.assert_called_once_with(
                'Node name(s) must be provided for the "promote" command.',
                SugarError.SUGAR_INVALID_PARAMETER,
            )

    def test_node_ps_no_nodes(self, sugar_swarm: SugarSwarm) -> None:
        """Test node ps fails without nodes."""
        with patch(
            'sugar.logs.SugarLogs.raise_error', side_effect=SystemExit
        ) as mock_error:
            with pytest.raises(SystemExit):
                # Using an empty string should trigger the error
                sugar_swarm._subcmd_node_ps(nodes='')
            mock_error.assert_called_once_with(
                'Node name(s) must be provided for the "ps" command.',
                SugarError.SUGAR_INVALID_PARAMETER,
            )

    def test_node_rm_no_nodes(self, sugar_swarm: SugarSwarm) -> None:
        """Test node rm fails without nodes."""
        with patch(
            'sugar.logs.SugarLogs.raise_error', side_effect=SystemExit
        ) as mock_error:
            with pytest.raises(SystemExit):
                # Using an empty string should trigger the error
                sugar_swarm._subcmd_node_rm(nodes='')
            mock_error.assert_called_once_with(
                'Node name(s) must be provided for the "rm" command.',
                SugarError.SUGAR_INVALID_PARAMETER,
            )

    def test_node_update_no_nodes(self, sugar_swarm: SugarSwarm) -> None:
        """Test node update fails without nodes."""
        with patch(
            'sugar.logs.SugarLogs.raise_error', side_effect=SystemExit
        ) as mock_error:
            with pytest.raises(SystemExit):
                # Using an empty string should trigger the error
                sugar_swarm._subcmd_node_update(nodes='')
            mock_error.assert_called_once_with(
                'Node name(s) must be provided for the "update" command.',
                SugarError.SUGAR_INVALID_PARAMETER,
            )


class TestSwarmUpdate:
    """Test the swarm update command."""

    def test_update_basic(self, sugar_swarm: SugarSwarm) -> None:
        """Test basic update command."""
        # Setup _call_service_command mock
        mock = MagicMock()
        setattr(sugar_swarm, '_call_service_command', mock)

        # Call update with image parameter
        sugar_swarm._cmd_update(services='my-web', image='nginx:alpine')

        # Verify the correct options were passed
        mock.assert_called_once()
        args = mock.call_args
        assert (
            'update' == args[0][0]
        )  # First positional arg should be 'update'
        assert ['my-web'] == args[1]['services']
        assert '--image' in args[1]['options_args']
        assert 'nginx:alpine' in args[1]['options_args']

    def test_update_env_add(self, sugar_swarm: SugarSwarm) -> None:
        """Test update with environment variables."""
        mock = MagicMock()
        setattr(sugar_swarm, '_call_service_command', mock)

        sugar_swarm._cmd_update(
            services='my-web', env_add='DEBUG=1,LOG_LEVEL=info'
        )

        args = mock.call_args
        options_args = args[1]['options_args']
        # Check that both env vars were added with their own --env-add flags
        assert '--env-add' in options_args
        assert 'DEBUG=1' in options_args
        assert 'LOG_LEVEL=info' in options_args

    def test_update_label_add(self, sugar_swarm: SugarSwarm) -> None:
        """Test update with service labels."""
        mock = MagicMock()
        setattr(sugar_swarm, '_call_service_command', mock)

        sugar_swarm._cmd_update(
            services='my-web', label_add='env=prod,tier=frontend'
        )

        args = mock.call_args
        options_args = args[1]['options_args']
        # Check that labels were added correctly
        assert '--label-add' in options_args
        assert 'env=prod' in options_args
        assert 'tier=frontend' in options_args

    def test_update_flags(self, sugar_swarm: SugarSwarm) -> None:
        """Test update with flag options."""
        mock = MagicMock()
        setattr(sugar_swarm, '_call_service_command', mock)

        # Test all flags together
        sugar_swarm._cmd_update(
            services='my-web',
            detach=True,
            quiet=True,
            force=True,
            rollback=True,
        )

        args = mock.call_args
        options_args = args[1]['options_args']
        # Check that all flags were added
        assert '--detach' in options_args
        assert '--quiet' in options_args
        assert '--force' in options_args
        assert '--rollback' in options_args

    def test_update_replicas(self, sugar_swarm: SugarSwarm) -> None:
        """Test update with replicas."""
        mock = MagicMock()
        setattr(sugar_swarm, '_call_service_command', mock)

        sugar_swarm._cmd_update(services='my-web', replicas='3')

        args = mock.call_args
        options_args = args[1]['options_args']
        # Check replicas parameter is passed correctly
        assert '--replicas' in options_args
        assert '3' in options_args

    def test_update_combined_options(self, sugar_swarm: SugarSwarm) -> None:
        """Test update with multiple options combined."""
        mock = MagicMock()
        setattr(sugar_swarm, '_call_service_command', mock)

        # Test combination of different option types
        sugar_swarm._cmd_update(
            services='my-web',
            image='nginx:latest',
            replicas='5',
            env_add='DEBUG=1',
            detach=True,
            options='--with-registry-auth',  # Pass additional raw option
        )

        args = mock.call_args
        options_args = args[1]['options_args']
        # Check for all expected options
        assert '--image' in options_args
        assert 'nginx:latest' in options_args
        assert '--replicas' in options_args
        assert '5' in options_args
        assert '--env-add' in options_args
        assert 'DEBUG=1' in options_args
        assert '--detach' in options_args
        assert '--with-registry-auth' in options_args

    def test_update_error_no_service(self, sugar_swarm: SugarSwarm) -> None:
        """Test error when no service is specified."""
        with patch(
            'sugar.logs.SugarLogs.raise_error', side_effect=SystemExit
        ) as mock_error:
            with pytest.raises(SystemExit):
                sugar_swarm._cmd_update(services='')

            # Verify the correct error was raised
            mock_error.assert_called_once_with(
                """Service name must be provided for this command
                (use --services service1,service2)""",
                SugarError.SUGAR_INVALID_PARAMETER,
            )


class TestSwarmScale:
    """Test the swarm scale command."""

    def test_scale_basic(self, sugar_swarm: SugarSwarm) -> None:
        """Test basic scale command."""
        mock = MagicMock()
        setattr(sugar_swarm, '_call_service_command', mock)

        sugar_swarm._cmd_scale(services='my-web', replicas='my-web=3')

        mock.assert_called_once()
        args = mock.call_args
        assert 'scale' == args[0][0]
        # Check that service=replicas format was used
        assert ['my-web=3'] == args[1]['services']


# Similar tests for rollback and other commands...


# Skip the CLI integration tests that are incomplete
@pytest.mark.skip('CLI integration tests need implementation')
class TestCLIIntegration:
    """Test that the CLI properly handles node commands."""

    pass


# Skip the CLI tests that are incomplete
@pytest.mark.skip('CLI tests need implementation')
class TestSwarmWithCLI:
    """Integration tests with CLI."""

    pass
