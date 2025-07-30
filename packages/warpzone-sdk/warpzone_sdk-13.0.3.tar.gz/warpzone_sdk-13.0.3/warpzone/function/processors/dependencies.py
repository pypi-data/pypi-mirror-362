from warpzone.function import integrations
from warpzone.monitor import logs, traces
from warpzone.tablestorage.db.client import WarpzoneDatabaseClient

tracer = traces.get_tracer(__name__)
logger = logs.get_logger(__name__)


class DependencyProcessor:
    """Pre-processing dependency binding"""

    return_type: object = None

    def _process(self, value):
        """Internal method for processing dependency"""
        # NOTE: This method currently does nothing
        # but exists to align with OutputProcessor
        return self.process(value)

    def process(self, value):
        return value

    def initialize(self, value):
        return value


class TableDatabaseDependency(DependencyProcessor):
    return_type = WarpzoneDatabaseClient

    def initialize(self, value):
        return integrations.get_db_client()
