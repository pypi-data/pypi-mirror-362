from operator import attrgetter
from pathlib import Path

from arkindex_export.models import (
    Classification,
    Dataset,
    DatasetElement,
    Element,
    ElementPath,
    EntityType,
    ExportVersion,
    Image,
    ImageServer,
    Metadata,
    Transcription,
    TranscriptionEntity,
    WorkerRun,
    WorkerVersion,
    database,
)

MODELS = [
    Classification,
    Dataset,
    DatasetElement,
    Element,
    ElementPath,
    EntityType,
    ExportVersion,
    Image,
    ImageServer,
    Metadata,
    Transcription,
    TranscriptionEntity,
    WorkerRun,
    WorkerVersion,
]

PRAGMAS = {
    # Recommended settings from peewee
    # http://docs.peewee-orm.com/en/latest/peewee/database.html#recommended-settings
    # Do not set journal mode to WAL as it writes in the database
    "cache_size": -1 * 64000,  # 64MB
    "foreign_keys": 1,
    "ignore_check_constraints": 0,
    "synchronous": 0,
}


# Expose all these models to library users if they want to import them all
__all__ = list(map(attrgetter("__name__"), MODELS))


def create_database(path: Path, version: int | None = None) -> None:
    """
    Create a SQLite database with the Arkindex export models
    and open connection towards it
    """
    path.parent.mkdir(parents=True, exist_ok=True)

    # Initialisation
    database.init(path, pragmas=PRAGMAS)

    # Create tables
    database.create_tables(MODELS)

    # Add an optional export version
    if version is not None:
        existing_version = ExportVersion.select().first()
        if existing_version is None:
            ExportVersion.create(version=version)
        else:
            assert (
                existing_version.version == version
            ), f"Database (version {existing_version.version}) is not compatible with version {version}"


def open_database(path: Path, minimum_version: int | None = None) -> None:
    """
    Open connection towards an SQLite database
    and use it as source for Arkindex export models
    """
    assert path.exists(), f"SQLite database {path} not found"

    database.init(path, pragmas=PRAGMAS)

    # Check this database is compatible with the minimum version requested
    if minimum_version is not None:
        version = ExportVersion.select().first().version
        if version < minimum_version:
            raise Exception(
                f"Database (version {version}) is not compatible with minimum version {minimum_version}"
            )
