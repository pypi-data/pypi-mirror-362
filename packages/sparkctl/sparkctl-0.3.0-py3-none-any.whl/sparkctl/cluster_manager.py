import fileinput
import os
import re
import shlex
import shutil
import subprocess
import sys
from contextlib import contextmanager
from pathlib import Path
from socket import gethostname
from typing import Generator, Self

from loguru import logger
from pyspark.sql import SparkSession

import sparkctl
from sparkctl.config import make_default_spark_config
from sparkctl.compute_interface_factory import make_compute_interface
from sparkctl.exceptions import InvalidConfiguration
from sparkctl.hive import setup_postgres_metastore, write_postgres_hive_site_file
from sparkctl.models import SparkConfig, StatusTracker
from sparkctl.spark_process_runner import SparkProcessRunner
from sparkctl.system_utils import make_spark_url


class ClusterManager:
    """Manages operation of the Spark cluster."""

    CONFIG_FILENAME = "config.json"
    STATUS_FILENAME = "status.json"

    def __init__(self, config: SparkConfig, status: StatusTracker | None = None) -> None:
        self._config = config
        self._status = status
        self._intf = make_compute_interface(config)
        self._intf.run_checks()

    @classmethod
    def from_config(cls, config: SparkConfig) -> Self:
        """Create a ClusterManager from a config instance.

        Examples
        --------
        >>> from sparkctl import ClusterManager, make_default_spark_config
        >>> config = make_default_spark_config()
        >>> config.runtime.start_connect_server = True
        >>> mgr = ClusterManager.from_config(config)

        See also
        --------
        from_config_file
        """
        return cls(config)

    @classmethod
    def from_config_file(cls, config_file: Path | str | None = None) -> Self:
        """Create a ClusterManager from a config file. If filename is None, use the default
        config file (e.g., ~/.sparkctl.toml).

        Examples
        --------
        >>> from sparkctl import ClusterManager
        >>> mgr = ClusterManager.from_config_file(config_file="config.json")

        See also
        --------
        from_config
        """
        config = (
            make_default_spark_config()
            if config_file is None
            else SparkConfig.from_file(config_file)
        )
        return cls.from_config(config)

    @classmethod
    def load(cls, directory: Path | str | None = None) -> Self:
        """Load an active cluster manager from a directory containg a previously-created sparkctl
        config.

        Parameters
        ----------
        directory
            Directory containing the sparkctl configuration files.
            Defaults to the current directory.

        Examples
        --------
        >>> from sparkctl import ClusterManager
        >>> mgr = ClusterManager.load()

        >>> mgr = ClusterManager.load(directory="path/to/sparkctl/config")

        See also
        --------
        from_config
        """
        path = Path() if directory is None else Path(directory)
        config_file = path / cls.CONFIG_FILENAME
        if not config_file.exists():
            msg = f"{path} is not a valid cluster manager directory because {config_file} does not exist"
            raise InvalidConfiguration(msg)

        config = SparkConfig.model_validate_json(config_file.read_text(encoding="utf-8"))
        status_file = path / cls.STATUS_FILENAME
        if status_file.exists():
            status = StatusTracker.model_validate_json(status_file.read_text(encoding="utf-8"))
        else:
            status = None
        return cls(config, status=status)

    def clean(self) -> None:
        """Delete all Spark runtime files in the directory."""
        logger.warning("clean is not implemented yet")

    def configure(self) -> None:
        """Configure a Spark cluster based on the input parameters.

        Examples
        --------
        >>> from sparkctl import ClusterManager
        >>> mgr = ClusterManager.from_config_file("config.json")
        >>> mgr.configure()
        """
        self._config.directories.clean_spark_conf_dir()
        log_config = self._config.directories.get_spark_log_file()
        shutil.copyfile(self._get_spark_log_file_template(), log_config)
        if self._config.runtime.spark_log_level is not None:
            self._customize_spark_log_level(log_config)
        spark_defaults_template = self._get_spark_defaults_template()
        spark_defaults = self._config.directories.get_spark_defaults_file()
        spark_env_template = self._get_spark_env_template()
        spark_env = self._config.directories.get_spark_env_file()
        scratch = self._config.directories.spark_scratch.absolute()
        scratch.mkdir(exist_ok=True)
        shutil.copyfile(spark_defaults_template, spark_defaults)
        shutil.copyfile(spark_env_template, spark_env)
        self._add_spark_settings_to_defaults_file(spark_defaults)
        with open(spark_env, "a", encoding="utf-8") as f_out:
            f_out.write(f"SPARK_LOG_DIR={scratch}/logs\n")
            f_out.write(f"SPARK_WORKER_DIR={scratch}/workers\n")
            if self._config.runtime.use_local_storage:
                scratch = self._intf.get_scratch_dir()
            f_out.write(f"SPARK_LOCAL_DIRS={scratch}/local\n")
            if self._config.runtime.python_path is not None:
                f_out.write(f"PYSPARK_PYTHON={self._config.runtime.python_path}\n")
            logger.info("Configured Spark workers to use {} for shuffle data.", scratch)

        workers = self._intf.get_worker_node_names()
        self._write_workers(workers)

        config_file = self._config.directories.base / self.CONFIG_FILENAME
        with open(config_file, "w", encoding="utf-8") as f_out:
            f_out.write(self._config.model_dump_json(indent=2))
            logger.info("Wrote sparkctl configuration to {}", config_file)

    def get_spark_session(self) -> SparkSession:
        """Return a SparkSession for the current cluster.

        Examples
        --------
        >>> spark = mgr.get_spark_session()
        >>> spark.createDataFrame([(1, 2), (3, 4)], ["a", "b"]).show()
        """
        if not self._config.runtime.start_connect_server:
            msg = "The Spark config does not enable the Spark Connect Server."
            raise InvalidConfiguration(msg)
        return SparkSession.builder.remote("sc://localhost:15002").getOrCreate()

    def set_workers(self, workers: list[str]) -> None:
        """Set the workers for the cluster. Must be called after :meth:`configure` and before
        :meth:`start`.

        Parameters
        ----------
        workers:
            Worker node names or IP addresses, will be used as ssh targets.

        Examples
        --------
        >>> from sparkctl import ClusterManager
        >>> mgr = ClusterManager.from_config(make_default_spark_config())
        >>> mgr.configure()
        >>> mgr.set_workers(["worker1", "worker2"])
        >>> mgr.start()
        """
        self._write_workers(workers)

    def get_workers(self) -> list[str]:
        """Return the current worker node names."""
        return self._read_workers()

    def start(self, print_env_paths: bool = True) -> None:
        """Start the Spark cluster. The caller must have called :meth:`configure` beforehand.

        The environment variables `SPARK_CONF_DIR` and `JAVA_HOME` are set to correct values for
        the current process.

        Examples
        --------
        >>> from sparkctl import ClusterManager
        >>> mgr = ClusterManager.from_config_file("config.json")
        >>> mgr.configure()
        >>> mgr.start()
        """
        url = make_spark_url(gethostname())
        runner = SparkProcessRunner(self._config, url)

        tracker = StatusTracker()
        try:
            self._start(runner, tracker)
        except Exception:
            logger.error("Stopping all processes after unhandled exception")
            if tracker.started_master:
                runner.stop_master_process()
            if tracker.started_connect_server:
                runner.stop_connect_server()
            if tracker.started_history_server:
                runner.stop_history_server()
            if tracker.started_thrift_server:
                runner.stop_thrift_server()
            if tracker.started_workers:
                workers = self._read_workers()
                if len(workers) == 1:
                    runner.stop_worker_process()
                else:
                    runner.stop_worker_processes(workers)
            if tracker.started_postgres:
                self._stop_postgres()
            raise

        if print_env_paths:
            _print_env_paths_msg(
                self._config.directories.get_spark_conf_dir(), self._config.binaries.java_path
            )
        status_file = self._config.directories.base / self.STATUS_FILENAME
        with open(status_file, "w", encoding="utf-8") as f_out:
            f_out.write(tracker.model_dump_json(indent=2))

        os.environ["SPARK_CONF_DIR"] = str(self._config.directories.get_spark_conf_dir())
        os.environ["JAVA_HOME"] = str(self._config.binaries.java_path)

    @contextmanager
    def managed_cluster(self) -> Generator[SparkSession, None, None]:
        """Configure and start the Spark cluster, yield a SparkSession in a context manager,
        stop the cluster after exit.

        The environment variables `SPARK_CONF_DIR` and `JAVA_HOME` are set to correct values for
        the current process while the context is active and cleared when complete.

        Examples
        --------
        >>> from sparkctl import ClusterManager
        >>> mgr = ClusterManager.from_config_file("config.json")
        >>> with mgr.managed_start() as spark:
            df = spark.createDataFrame([(1, 2), (3, 4)], ["a", "b"])
            df.show()
        """
        try:
            if not self._config.runtime.start_connect_server:
                logger.info("Enabling the Spark Connect Server.")
                self._config.runtime.start_connect_server = True
            self.configure()
            self.start(print_env_paths=False)
            spark = self.get_spark_session()
            yield spark
        finally:
            self.stop()
            logger.info("Stopped Spark cluster processes and SparkSession")
            # Clear the environment variables set by start()
            os.environ.pop("SPARK_CONF_DIR", None)
            os.environ.pop("JAVA_HOME", None)

    def _start(self, runner: SparkProcessRunner, tracker: StatusTracker) -> None:
        workers = self._read_workers()
        is_single_node_cluster = self._is_single_node_cluster(workers)
        if self._config.runtime.enable_postgres_hive_metastore:
            self._setup_postgres()
            tracker.started_postgres = True

        runner.start_master_process()
        tracker.started_master = True
        logger.info("Started Spark master processes on {}", gethostname())

        if self._config.runtime.start_connect_server:
            runner.start_connect_server()
            tracker.started_connect_server = True
            logger.info("Started Spark connect server")

        if self._is_history_server_enabled():
            runner.start_history_server()
            tracker.started_history_server = True
            logger.info("Started Spark history server")

        if self._config.runtime.start_thrift_server:
            runner.start_thrift_server()
            tracker.started_thrift_server = True
            logger.info("Started Apache Thrift Server")

        worker_memory_gb = self._get_worker_memory_gb(self._get_runtime_spark_driver_memory_gb())
        if is_single_node_cluster:
            runner.start_worker_process(worker_memory_gb)
            tracker.started_workers = True
        else:
            runner.start_worker_processes(workers, worker_memory_gb)
            tracker.started_workers = True
        logger.info("Spark worker memory = {} GB", worker_memory_gb)

    def stop(self) -> None:
        """Stop all Spark processes.

        Examples
        --------
        >>> from sparkctl import ClusterManager
        >>> mgr = ClusterManager.from_config_file("config.json")
        >>> mgr.configure()
        >>> mgr.start()
        >>> mgr.stop()
        """
        status_file = self._config.directories.base / self.STATUS_FILENAME
        if status_file.exists():
            tracker = StatusTracker.model_validate_json(status_file.read_text(encoding="utf-8"))
        else:
            logger.warning(
                "Status file {} does not exist, assume all processes are running.", status_file
            )
            tracker = StatusTracker(
                started_master=True,
                started_workers=True,
                started_thrift_server=True,
                started_history_server=True,
                started_connect_server=True,
            )
            if self._config.runtime.enable_postgres_hive_metastore:
                tracker.started_postgres = True
        url = make_spark_url(gethostname())
        runner = SparkProcessRunner(self._config, url)
        if tracker.started_master:
            runner.stop_master_process()
        if tracker.started_connect_server:
            runner.stop_connect_server()
        if tracker.started_history_server:
            runner.stop_history_server()
        if tracker.started_thrift_server:
            runner.stop_thrift_server()
        if tracker.started_workers:
            workers = self._intf.get_worker_node_names()
            is_single_node_cluster = self._is_single_node_cluster(workers)
            if is_single_node_cluster:
                runner.stop_worker_process()
            else:
                workers = self._read_workers()
                runner.stop_worker_processes(workers)
        if tracker.started_postgres:
            self._stop_postgres()
        status_file.write_text(StatusTracker().model_dump_json(indent=2), encoding="utf-8")

    def _get_spark_defaults_template(self) -> Path:
        if self._config.runtime.spark_defaults_template_file is None:
            path = Path(next(iter(sparkctl.__path__))) / "conf" / "spark-defaults.conf.template"
        else:
            path = Path(self._config.runtime.spark_defaults_template_file)
            logger.info("Use custom Spark defaults template %s", path)
        return path

    def _get_spark_env_template(self) -> Path:
        return Path(next(iter(sparkctl.__path__))) / "conf" / "spark-env.sh"

    def _get_spark_log_file_template(self) -> Path:
        return Path(next(iter(sparkctl.__path__))) / "conf" / "log4j2.properties"

    def _get_worker_memory_gb(self, driver_memory_gb: int) -> int:
        node_memory_overhead_gb = self._intf.get_node_memory_overhead_gb(
            driver_memory_gb,
            self._config.runtime.node_memory_overhead_gb,
        )
        if self._config.runtime.enable_postgres_hive_metastore:
            # Postgres should be idle most of the time. We aren't adding any CPU overhead.
            # Add a conservative cushion for memory.
            node_memory_overhead_gb += 2

        return self._intf.get_worker_memory_gb() - node_memory_overhead_gb

    @staticmethod
    def _is_single_node_cluster(workers: list[str]) -> bool:
        return len(workers) == 1 and gethostname() == workers[0]

    def _add_spark_settings_to_defaults_file(self, defaults_file: Path) -> None:
        rt_params = self._config.runtime
        with open(defaults_file, "a") as f_out:
            f_out.write(f"spark.driver.memory {rt_params.driver_memory_gb}g\n")
            f_out.write(f"spark.driver.maxResultSize {rt_params.driver_memory_gb}g\n")
            logger.info("Set driver memory to {} GB", rt_params.driver_memory_gb)

        self._config_executors(defaults_file)
        if rt_params.enable_dynamic_allocation:
            self._enable_dynamic_allocation(defaults_file)

        if rt_params.start_history_server:
            self._enable_history_server(defaults_file)

        if rt_params.enable_hive_metastore or rt_params.enable_postgres_hive_metastore:
            self._enable_metastore(defaults_file)
            if not rt_params.enable_dynamic_allocation:
                logger.info("Enable dynamic allocation because the Hive metastore is enabled.")
                self._enable_dynamic_allocation(defaults_file)
        else:
            hive_site = self._config.directories.get_hive_site_file()
            if hive_site.exists():
                hive_site.unlink()

    def _enable_dynamic_allocation(self, defaults_file: Path) -> None:
        with open(defaults_file, "a") as f_out:
            f_out.write(
                """
spark.dynamicAllocation.enabled true
spark.dynamicAllocation.shuffleTracking.enabled = true
spark.dynamicAllocation.executorIdleTimeout 60s
spark.dynamicAllocation.cachedExecutorIdleTimeout 300s
spark.shuffle.service.enabled true
spark.shuffle.service.db.enabled = true
spark.worker.cleanup.enabled = true
"""
            )

        logger.info("Enabled dynamic allocation")

    def _config_executors(self, defaults_file: Path) -> None:
        num_workers = self._intf.get_num_workers()
        worker_memory_gb = self._get_worker_memory_gb(self._config.runtime.driver_memory_gb)
        worker_num_cpus = self._intf.get_worker_num_cpus()
        # Leave one CPU for OS and management software.
        worker_num_cpus -= 1

        min_executors_per_node = worker_num_cpus // self._config.runtime.executor_cores
        if self._config.runtime.executor_memory_gb is None:
            executor_memory_gb = worker_memory_gb // min_executors_per_node
        else:
            executor_memory_gb = self._config.runtime.executor_memory_gb
        if executor_memory_gb > worker_memory_gb:
            msg = (
                f"{executor_memory_gb=} cannot be more than {worker_memory_gb=}. "
                "Please adjust the settings."
            )
            raise InvalidConfiguration(msg)
        executors_by_mem = worker_memory_gb // executor_memory_gb
        executors_by_cpu = worker_num_cpus // self._config.runtime.executor_cores
        if executors_by_cpu <= executors_by_mem:
            executors_per_node = executors_by_cpu
        else:
            executors_per_node = executors_by_mem

        total_num_cpus = executors_per_node * self._config.runtime.executor_cores * num_workers
        total_num_executors = executors_per_node * num_workers
        partitions = total_num_cpus * self._config.runtime.shuffle_partition_multiplier
        with open(defaults_file, "a") as f_out:
            f_out.write(
                f"""
spark.executor.cores {self._config.runtime.executor_cores}
spark.sql.shuffle.partitions {partitions}
spark.executor.memory {executor_memory_gb}g
"""
            )
        logger.info("Configured Spark to start {} executors", total_num_executors)
        logger.info(
            "Set spark.sql.shuffle.partitions={} and spark.executor.memory={}g",
            partitions,
            executor_memory_gb,
        )

    def _customize_spark_log_level(self, log_config: Path) -> None:
        changed = False
        with fileinput.input(files=[log_config], inplace=True) as f_out:
            for line in f_out:
                if line.startswith("rootLogger.level"):
                    line = f"rootLogger.level = {self._config.runtime.spark_log_level}\n"
                    changed = True
                print(line, end="")

        if changed:
            logger.info("Set custom Spark log level = {}", self._config.runtime.spark_log_level)

    def _enable_metastore(self, defaults_file: Path) -> None:
        rt_params = self._config.runtime
        hive_site_file = self._config.directories.get_hive_site_file()
        with open(defaults_file, "a") as f_out:
            f_out.write(
                f"spark.sql.warehouse.dir {self._config.directories.metastore_dir}/spark-warehouse\n"
            )
            postgres_jar = self._config.binaries.postgresql_jar_file
            f_out.write(f"spark.driver.extraClassPath {postgres_jar}\n")
            f_out.write(f"spark.executor.extraClassPath {postgres_jar}\n")

        if rt_params.enable_postgres_hive_metastore:
            if rt_params.postgres_password is None:
                msg = "posgres_password cannot be None"
                raise InvalidConfiguration(msg)
            write_postgres_hive_site_file(rt_params.postgres_password, hive_site_file)
        else:
            hive_template = Path(next(iter(sparkctl.__path__))) / "conf" / "hive-site.xml.template"
            shutil.copyfile(hive_template, hive_site_file)
            new_path = f"{self._config.directories.metastore_dir}/metastore_db"
            with fileinput.input(files=[hive_site_file], inplace=True) as f_hive:
                for line in f_hive:
                    line = line.replace("REPLACE_ME_WITH_CUSTOM_PATH", new_path)
                    print(line, end="")

    def _enable_history_server(self, defaults_file: Path) -> None:
        events_dir = self._config.directories.get_events_dir()
        events_dir.mkdir()
        with open(defaults_file, "a") as f_out:
            f_out.write(
                f"""
spark.eventLog.enabled true
spark.eventLog.compress true
spark.history.fs.cleaner.enabled true
spark.history.fs.cleaner.interval 1d
spark.history.fs.cleaner.maxAge 7d
spark.eventLog.dir file://{events_dir}
spark.history.fs.logDirectory file://{events_dir}
"""
            )
        logger.info("Enabled Spark history server at {}", events_dir)

    def _get_runtime_spark_driver_memory_gb(self) -> int:
        # Note that spark-defaults.conf takes precedence over our config.json.
        regex = re.compile(r"^\s*spark.driver.memory\s*=?\s*(\d+)g")
        for line in self._read_spark_defaults():
            match = regex.search(line)
            if match:
                return int(match.group(1))

        msg = "Did not find Spark driver memory in spark-defaults.conf"
        raise InvalidConfiguration(msg)

    def _is_history_server_enabled(self) -> bool:
        """Return True if the history server is enabled."""
        # Note that spark-defaults.conf takes precedence over our config.json.
        regex = re.compile(r"^\s*spark\.eventLog\.enabled\s*=*\s*true")
        for line in self._read_spark_defaults():
            match = regex.search(line)
            if match:
                return True
        return False

    def _read_spark_defaults(self) -> list[str]:
        """Return a list of lines containing the contents of spark-defaults.conf.
        All lines beginning with a # (designating a comment) are removed.
        """
        filename = self._config.directories.base / "conf" / "spark-defaults.conf"
        lines: list[str] = []
        for line in filename.read_text(encoding="utf-8").splitlines():
            line_ = line.strip()
            if line and not line_.startswith("#"):
                lines.append(line_)

        return lines

    def _setup_postgres(self) -> None:
        script = self._config.compute.postgres.get_script_path("start_container")
        pg_data = self._config.directories.base / "pg_data"
        pg_run = self._config.directories.base / "pg_run"
        cmd = f"bash {script} {pg_data} {pg_run} {self._config.runtime.postgres_password}"
        subprocess.run(shlex.split(cmd), check=True)
        setup_postgres_metastore(self._config)

    def _stop_postgres(self) -> None:
        script = self._config.compute.postgres.get_script_path("stop_container")
        proc = subprocess.run(["bash", str(script)])
        if proc.returncode != 0:
            logger.warning("Failed to stop the postgres container: {}", proc.returncode)

    def _write_workers(self, workers: list[str]) -> None:
        filename = self._config.directories.get_workers_file()
        with open(filename, "w", encoding="utf-8") as f_out:
            f_out.write("\n".join(workers))
            f_out.write("\n")
        num_workers = len(workers)
        tag = "worker" if num_workers == 1 else "workers"
        logger.info("Wrote {} {} to {}", tag, num_workers, filename)

    def _read_workers(self) -> list[str]:
        workers_file = self._config.directories.get_workers_file()
        if not workers_file.exists():
            msg = (
                f"The workers file does not exist at {workers_file}. Have you called "
                "ClusterManager.configure()?"
            )
            raise InvalidConfiguration(msg)

        return [x for x in workers_file.read_text(encoding="utf-8").splitlines() if x]


def _print_env_paths_msg(conf_dir: Path, java_dir: Path) -> None:
    print(
        f"""
###############################################################################

Set these environment variables to use the Spark configuration:

export SPARK_CONF_DIR={conf_dir}
export JAVA_HOME={java_dir}

###############################################################################
""",
        file=sys.stderr,
    )
