from argparse import ArgumentParser, Namespace
from typing import Tuple
from config.configuration import Configuration
from config.configuration_set import ConfigurationSet
from config import config_from_dict, config_from_env, config_from_toml
from hypercorn import Config
from hypercorn.logging import Logger
import warnings

defaults = {
}

def load() -> Configuration:
    [config, args] = hypercorn()

    arguments = {
        'debug': config.debug
    }

    arg_config = config_from_dict(arguments, lowercase_keys=True)
    env_config = config_from_env(prefix='BACKEND', separator='_', lowercase_keys=True)
    def_config = config_from_dict(defaults)

    if args.config != None:
        file_config = config_from_toml(args.config, read_from_file=True, lowercase_keys=True)
        return ConfigurationSet(
            arg_config,
            env_config,
            file_config,
            def_config,
        )
    else:
        return ConfigurationSet(
            arg_config,
            env_config,
            def_config,
        )

def create_logger() -> Logger:
    [config, _args] = hypercorn()
    return config.log

def hypercorn() -> Tuple[Config, Namespace]:
    sentinel = object()
    parser = ArgumentParser(exit_on_error=False)
    parser.add_argument(
        "application", help="The application to dispatch to as path.to.module:instance.path"
    )
    parser.add_argument(
        "-c",
        "--config",
        help="Location of a TOML config file, or when prefixed with `file:` a Python file, or when prefixed with `python:` a Python module.",
        default=None,
    )
    parser.add_argument(
        "--debug",
        help="Enable debug mode, i.e. extra logging and checks",
        action="store_true",
        default=sentinel,
    )
    parser.add_argument("--error-log", help="Deprecated, see error-logfile", default=sentinel)
    parser.add_argument(
        "--error-logfile",
        "--log-file",
        dest="error_logfile",
        help="The target location for the error log, use `-` for stderr",
        default=sentinel,
    )
    parser.add_argument(
        "--log-config",
        help=""""A Python logging configuration file. This can be prefixed with
        'json:' or 'toml:' to load the configuration from a file in
        that format. Default is the logging ini format.""",
        default=sentinel,
    )
    parser.add_argument(
        "--log-level", help="The (error) log level, defaults to info", default=sentinel
    )

    args = parser.parse_args()

    def load_config() -> Config:
        if args.config is None:
            return Config()
        elif args.config.startswith("python:"):
            return Config.from_object(args.config[len("python:"):])
        elif args.config.startswith("file:"):
            return Config.from_pyfile(args.config[len("file:"):])
        else:
            return Config.from_toml(args.config)

    config = load_config()
    config.application_path = args.application

    if args.log_level is not sentinel:
        config.loglevel = args.log_level
    if args.debug is not sentinel:
        config.debug = args.debug
    if args.error_log is not sentinel:
        warnings.warn(
            "The --error-log argument is deprecated, use `--error-logfile` instead",
            DeprecationWarning,
        )
        config.errorlog = args.error_log
    if args.error_logfile is not sentinel:
        config.errorlog = args.error_logfile
    if args.log_config is not sentinel:
        config.logconfig = args.log_config

    return [config, args]
