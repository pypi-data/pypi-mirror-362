import sys
import time
from pathlib import Path
from typing import Any

import rich_click as click
import toml
from loguru import logger

from sparkctl.config import (
    DEFAULT_SETTINGS_FILENAME,
    RUNTIME,
    sparkctl_settings,
)
from sparkctl.cluster_manager import ClusterManager
from sparkctl.exceptions import SparkctlBaseException
from sparkctl.loggers import setup_logging
from sparkctl.models import (
    BinaryLocations,
    ComputeEnvironment,
    ComputeParams,
    SparkConfig,
    SparkRuntimeParams,
    RuntimeDirectories,
)


@click.group("sparkctl")
@click.option(
    "-c",
    "--console-level",
    default=sparkctl_settings.app.console_level,
    show_default=True,
    help="Console log level",
)
@click.option(
    "-f",
    "--file-level",
    default=sparkctl_settings.app.file_level,
    show_default=True,
    help="Console log level",
)
@click.option(
    "-r",
    "--reraise-exceptions",
    is_flag=True,
    default=sparkctl_settings.app.reraise_exceptions,
    show_default=True,
    help="Reraise unhandled sparkctl exceptions.",
)
@click.pass_context
def cli(ctx: click.Context, console_level: str, file_level: str, reraise_exceptions: bool) -> None:
    """sparkctl comands"""


_default_config_epilog = """
\b
Examples:\n
$ sparkctl default-config \\ \n
    /datasets/images/apache-spark/spark-4.0.0-bin-hadoop3 \\ \n
    /datasets/images/apache-spark/jdk-21.0.7 \\ \n
    -e slurm \\ \n
$ sparkctl default-config ~/apache-spark/spark-4.0.0-bin-hadoop3 ~/jdk-21.0.8 -e native\n
"""


@click.command(epilog=_default_config_epilog)
@click.argument("spark_path", type=click.Path(exists=True), callback=lambda *x: Path(x[2]))
@click.argument("java_path", type=click.Path(exists=True), callback=lambda *x: Path(x[2]))
@click.option(
    "-d",
    "--directory",
    default=Path.home(),
    show_default=True,
    help="Directory in which to create the sparkctl config file.",
    callback=lambda *x: Path(x[2]),
)
@click.option(
    "-e",
    "--compute-environment",
    type=click.Choice([x.value for x in ComputeEnvironment]),
    default=ComputeEnvironment.SLURM.value,
    help="Compute environment",
    callback=lambda *x: ComputeEnvironment(x[2]),
)
@click.option(
    "-H",
    "--hadoop-path",
    help="Directory containing Hadoop binaries.",
    callback=lambda *x: None if x[2] is None else Path(x[2]),
)
@click.option(
    "-h",
    "--hive-tarball",
    help="File containing Hive binaries.",
    callback=lambda *x: None if x[2] is None else Path(x[2]),
)
@click.option(
    "-p",
    "--postgresql-jar-file",
    help="Path to PostgreSQL jar file.",
    callback=lambda *x: None if x[2] is None else Path(x[2]),
)
def default_config(
    spark_path: Path,
    java_path: Path,
    directory: Path,
    compute_environment: ComputeEnvironment,
    hadoop_path: Path | None,
    hive_tarball: Path | None,
    postgresql_jar_file: Path | None,
):
    """Create a sparkctl config file that defines paths to Spark binaries.
    This is a one-time requirement when installing sparkctl in a new environment."""
    config = _create_default_config(spark_path, java_path, directory, compute_environment)
    if hadoop_path is not None:
        config.binaries.hadoop_path = hadoop_path
    if hive_tarball is not None:
        config.binaries.hive_tarball = hive_tarball
    if postgresql_jar_file is not None:
        config.binaries.postgresql_jar_file = postgresql_jar_file
    data = config.model_dump(mode="json", exclude={"directories"})
    # Don't hard-code the password globally.
    data["runtime"].pop("postgres_password")
    filename = directory / DEFAULT_SETTINGS_FILENAME
    with open(filename, "w", encoding="utf-8") as f_out:
        toml.dump(data, f_out)
    print(f"Wrote sparkctl settings to {filename}")


def _create_default_config(
    spark_path: Path, java_path: Path, directory: Path, compute_environment: ComputeEnvironment
) -> SparkConfig:
    """Create the default Spark configuration."""
    return SparkConfig(
        compute=ComputeParams(environment=compute_environment),
        binaries=BinaryLocations(spark_path=spark_path, java_path=java_path),
        directories=RuntimeDirectories(base=directory),
        runtime=SparkRuntimeParams(**RUNTIME),
    )


_configure_epilog = """
Examples:\n
$ sparkctl configure --start\n
$ sparkctl configure --shuffle-partition-multiplier 4 --local-storage\n
$ sparkctl configure --local-storage --thrift-server\n
"""


@click.command(epilog=_configure_epilog)
@click.option(
    "-d",
    "--directory",
    default=Path(),
    show_default=True,
    help="Base directory for the cluster configuration",
    type=click.Path(),
    callback=lambda *x: Path(x[2]),
)
@click.option(
    "-s",
    "--spark-scratch",
    default=Path("spark_scratch"),
    show_default=True,
    help=RuntimeDirectories.model_fields["spark_scratch"].description,
    callback=lambda *x: Path(x[2]),
)
@click.option(
    "-e",
    "--executor-cores",
    default=sparkctl_settings.runtime.get("executor_cores"),
    show_default=True,
    help=SparkRuntimeParams.model_fields["executor_cores"].description,
)
@click.option(
    "-E",
    "--executor-memory-gb",
    default=sparkctl_settings.runtime.get("executor_memory_gb"),
    show_default=True,
    type=int,
    help=SparkRuntimeParams.model_fields["executor_memory_gb"].description,
)
@click.option(
    "-M",
    "--driver-memory-gb",
    default=sparkctl_settings.runtime.get("driver_memory_gb"),
    show_default=True,
    type=int,
    help=SparkRuntimeParams.model_fields["driver_memory_gb"].description,
)
@click.option(
    "-o",
    "--node-memory-overhead-gb",
    default=sparkctl_settings.runtime.get("node_memory_overhead_gb"),
    show_default=True,
    type=int,
    help=SparkRuntimeParams.model_fields["node_memory_overhead_gb"].description,
)
@click.option(
    "--dynamic-allocation/--no-dynamic-allocation",
    is_flag=True,
    default=sparkctl_settings.runtime.get("enable_dynamic_allocation"),
    show_default=True,
    help=SparkRuntimeParams.model_fields["enable_dynamic_allocation"].description,
)
@click.option(
    "-m",
    "--shuffle-partition-multiplier",
    default=sparkctl_settings.runtime.get("shuffle_partition_multiplier"),
    show_default=True,
    help=SparkRuntimeParams.model_fields["shuffle_partition_multiplier"].description,
)
@click.option(
    "-t",
    "--spark-defaults-template-file",
    help=SparkRuntimeParams.model_fields["spark_defaults_template_file"].description,
    callback=lambda *x: None if x[2] is None else Path(x[2]),
)
@click.option(
    "--local-storage/--no-local-storage",
    is_flag=True,
    default=sparkctl_settings.runtime.get("use_local_storage"),
    show_default=True,
    help=SparkRuntimeParams.model_fields["use_local_storage"].description,
)
@click.option(
    "--connect-server/--no-connect-server",
    is_flag=True,
    default=sparkctl_settings.runtime.get("start_connect_server"),
    show_default=True,
    help=SparkRuntimeParams.model_fields["start_connect_server"].description,
)
@click.option(
    "--history-server/--no-history-server",
    is_flag=True,
    default=sparkctl_settings.runtime.get("start_history_server"),
    show_default=True,
    help=SparkRuntimeParams.model_fields["start_history_server"].description,
)
@click.option(
    "--thrift-server/--no-thrift-server",
    is_flag=True,
    default=sparkctl_settings.runtime.get("start_thrift_server"),
    show_default=True,
    help=SparkRuntimeParams.model_fields["start_thrift_server"].description,
)
@click.option(
    "-l",
    "--spark-log-level",
    default=sparkctl_settings.runtime.get("spark_log_level"),
    type=click.Choice(["debug", "info", "warn", "error"]),
    show_default=True,
    help=SparkRuntimeParams.model_fields["spark_log_level"].description,
)
@click.option(
    "--hive-metastore/--no-hive-metastore",
    is_flag=True,
    default=sparkctl_settings.runtime.get("enable_hive_metastore"),
    show_default=True,
    help=SparkRuntimeParams.model_fields["enable_hive_metastore"].description,
)
@click.option(
    "--postgres-hive-metastore/--no-postgres-hive-metastore",
    is_flag=True,
    default=sparkctl_settings.runtime.get("enable_postgres_hive_metastore"),
    show_default=True,
    help=SparkRuntimeParams.model_fields["enable_postgres_hive_metastore"].description,
)
@click.option(
    "-w",
    "--metastore-dir",
    default=Path(),
    show_default=True,
    help=RuntimeDirectories.model_fields["metastore_dir"].description,
    callback=lambda *x: Path(x[2]),
)
@click.option(
    "-P",
    "--python-path",
    help=SparkRuntimeParams.model_fields["python_path"].description,
)
@click.option(
    "--resource-monitor/--no-resource-monitor",
    is_flag=True,
    default=False,
    show_default=True,
    help="Enable resource monitoring.",
)
@click.option(
    "--start/--no-start",
    is_flag=True,
    show_default=True,
    default=False,
    help="Start the cluster after configuration.",
)
@click.option(
    "--use-current-python/--no-use-current-python",
    is_flag=True,
    default=True,
    show_default=True,
    help="Use the Python executable in the current environment for Spark workers. "
    "--python-path takes precedence.",
)
@click.pass_context
def configure(
    ctx: click.Context,
    start: bool,
    directory: Path,
    spark_scratch: Path,
    executor_cores: int,
    executor_memory_gb: int,
    driver_memory_gb: int,
    node_memory_overhead_gb: int,
    dynamic_allocation: bool,
    shuffle_partition_multiplier: int,
    spark_defaults_template_file: Path | None,
    local_storage: bool,
    connect_server: bool,
    history_server: bool,
    thrift_server: bool,
    spark_log_level: str | None,
    hive_metastore: bool,
    postgres_hive_metastore: bool,
    metastore_dir: Path,
    python_path: str | None,
    resource_monitor: bool,
    use_current_python: bool,
):
    """Create a Spark cluster configuration."""
    setup_logging(
        filename="sparkctl.log",
        console_level=ctx.find_root().params["console_level"],
        file_level=ctx.find_root().params["console_level"],
        mode="a",
    )
    if python_path is None and use_current_python:
        logger.info("Use the current Python executable for Spark workers.")
        python_path = sys.executable
    config = SparkConfig(
        binaries=BinaryLocations(
            spark_path=sparkctl_settings.binaries.spark_path,
            java_path=sparkctl_settings.binaries.java_path,
            hadoop_path=sparkctl_settings.binaries.get("hadoop_path"),
            hive_tarball=sparkctl_settings.binaries.get("hive_tarball"),
            postgresql_jar_file=sparkctl_settings.binaries.get("postgresql_jar_file"),
        ),
        runtime=SparkRuntimeParams(
            executor_cores=executor_cores,
            executor_memory_gb=executor_memory_gb,
            driver_memory_gb=driver_memory_gb,
            node_memory_overhead_gb=node_memory_overhead_gb,
            enable_dynamic_allocation=dynamic_allocation,
            shuffle_partition_multiplier=shuffle_partition_multiplier,
            spark_defaults_template_file=spark_defaults_template_file,
            use_local_storage=local_storage,
            start_connect_server=connect_server,
            start_history_server=history_server,
            start_thrift_server=thrift_server,
            spark_log_level=spark_log_level,
            enable_hive_metastore=hive_metastore,
            enable_postgres_hive_metastore=postgres_hive_metastore,
            python_path=python_path,
        ),
        directories=RuntimeDirectories(
            base=directory,
            spark_scratch=spark_scratch,
            metastore_dir=metastore_dir,
        ),
        compute=sparkctl_settings.get("compute", {"environment": "slurm"}),
    )
    config.resource_monitor.enabled = resource_monitor
    res = handle_sparkctl_exception(ctx, _configure, config, start)
    if res[1] != 0:
        ctx.exit(res[1])


def _configure(config: SparkConfig, start: bool) -> ClusterManager:
    mgr = ClusterManager(config)
    mgr.configure()
    if start:
        mgr.start()
    return mgr


_start_epilog = """
Examples:\n
$ sparkctl start\n
$ sparkctl start --directory ./my-spark-config\n
$ sparkctl start --wait\n
"""


@click.command(epilog=_start_epilog)
@click.option(
    "--wait/--no-wait",
    is_flag=True,
    default=False,
    show_default=True,
    help="If True, wait until the user presses Ctrl-C or timeout is reached and then stop the "
    "cluster. If False, start the cluster and exit.",
)
@click.option(
    "-d",
    "--directory",
    default=Path(),
    show_default=True,
    help="Base directory for the cluster configuration",
    type=click.Path(),
    callback=lambda *x: Path(x[2]),
)
@click.option(
    "-t",
    "--timeout",
    type=float,
    help="If --wait is set, timeout in minutes. Defaults to no timeout.",
)
@click.pass_context
def start(ctx: click.Context, wait: bool, directory: Path, timeout: float | None) -> None:
    """Start a Spark cluster with an existing configuration."""
    setup_logging(
        filename="sparkctl.log",
        console_level=ctx.find_root().params["console_level"],
        file_level=ctx.find_root().params["console_level"],
        mode="a",
    )
    mgr = ClusterManager.load(directory)
    mgr.start()
    if wait:
        if timeout is None:
            msg = "Press Ctrl-C to shut down all Spark processes."
            end = sys.maxsize
        else:
            msg = f"Wait until Ctrl-C is detected or {timeout} minutes"
            end = int(time.time() + timeout * 60)
        logger.info(msg)
        interval = min((end - time.time(), 3600))
        try:
            while time.time() < end:
                time.sleep(interval)
            logger.info("Timeout expired, shutting down the cluster.")
        except KeyboardInterrupt:
            logger.info("Detected Ctrl-c, shutting down the cluster.")
        finally:
            mgr.stop()


_stop_epilog = """
Examples:\n
$ sparkctl stop\n
$ sparkctl stop --directory ./my-spark-config\n
"""


@click.command(epilog=_stop_epilog)
@click.option(
    "-d",
    "--directory",
    default=Path(),
    show_default=True,
    help="Base directory for the cluster configuration",
    type=click.Path(),
    callback=lambda *x: Path(x[2]),
)
def stop(directory: Path) -> None:
    """Stop a Spark cluster."""
    mgr = ClusterManager.load(directory)
    mgr.stop()


@click.command()
@click.argument("directory", callback=lambda *x: Path(x[2]))
def clean(directory: Path) -> None:
    """Delete all Spark runtime files in the directory."""
    mgr = ClusterManager.load(directory)
    mgr.clean()


def handle_sparkctl_exception(ctx: click.Context, func, *args, **kwargs) -> Any:
    """Handle any sparkctl exceptions as specified by the CLI parameters."""
    res = None
    try:
        res = func(*args, **kwargs)
        return res, 0
    except SparkctlBaseException:
        exc_type, exc_value, exc_tb = sys.exc_info()
        filename = exc_tb.tb_frame.f_code.co_filename  # type: ignore
        line = exc_tb.tb_lineno  # type: ignore
        msg = f'{func.__name__} failed: exception={exc_type.__name__} message="{exc_value}" {filename=} {line=}'  # type: ignore
        logger.error(msg)
        if ctx.find_root().params["reraise_exceptions"]:
            raise
        return res, 1


cli.add_command(default_config)
cli.add_command(configure)
cli.add_command(start)
cli.add_command(stop)
# cli.add_command(clean)
