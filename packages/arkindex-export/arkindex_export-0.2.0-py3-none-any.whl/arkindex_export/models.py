from peewee import (
    SQL,
    BareField,
    CharField,
    FloatField,
    ForeignKeyField,
    IntegerField,
    Model,
    SqliteDatabase,
    TextField,
    fn,
)
from playhouse.hybrid import hybrid_property

# Use a database unknown before runtime
database = SqliteDatabase(None)


class BaseModel(Model):
    class Meta:
        database = database


class ExportVersion(BaseModel):
    version = BareField(adapt=int)

    class Meta:
        table_name = "export_version"
        primary_key = False


class WorkerVersion(BaseModel):
    id = CharField(primary_key=True, max_length=37)
    # Export limits worker version slug to 100 chars
    slug = CharField(max_length=100)
    name = CharField(max_length=100)
    repository_url = CharField(null=True, max_length=250)
    # Full URL of the revision
    revision = CharField(null=True, max_length=200)
    version = IntegerField(null=True)
    # Slug of the worker's type, defaulting to max 50 characters
    type = CharField(max_length=50)

    class Meta:
        table_name = "worker_version"


class WorkerRun(BaseModel):
    id = CharField(primary_key=True, max_length=37)
    worker_version = ForeignKeyField(
        column_name="worker_version_id", field="id", model=WorkerVersion
    )
    model_version_id = CharField(null=True, max_length=37)
    model_id = CharField(null=True, max_length=37)
    model_name = CharField(null=True, max_length=100)
    configuration_id = CharField(null=True, max_length=37)
    configuration = TextField(null=True)

    class Meta:
        table_name = "worker_run"


class ImageServer(BaseModel):
    id = IntegerField(primary_key=True)
    url = CharField(unique=True, max_length=200)
    display_name = CharField(max_length=250)
    max_width = IntegerField(null=True)
    max_height = IntegerField(null=True)

    class Meta:
        table_name = "image_server"


class Image(BaseModel):
    id = CharField(primary_key=True, max_length=37)
    server = ForeignKeyField(column_name="server_id", field="id", model=ImageServer)
    url = TextField(unique=True)
    width = IntegerField()
    height = IntegerField()

    class Meta:
        table_name = "image"


class Element(BaseModel):
    id = CharField(primary_key=True, max_length=37)
    name = CharField(max_length=250)
    # Slug of the element's type, defaulting to max 50 characters
    type = CharField(max_length=50)
    image = ForeignKeyField(column_name="image_id", field="id", model=Image, null=True)
    polygon = TextField(null=True)
    confidence = FloatField(null=True)
    rotation_angle = IntegerField(constraints=[SQL("DEFAULT 0")])
    mirrored = IntegerField(constraints=[SQL("DEFAULT 0")])
    worker_run = ForeignKeyField(
        column_name="worker_run_id", field="id", model=WorkerRun, null=True
    )

    created = FloatField()
    updated = FloatField()

    class Meta:
        table_name = "element"


class Classification(BaseModel):
    id = CharField(primary_key=True, max_length=37)
    class_name = CharField(max_length=1024)
    confidence = FloatField()
    state = CharField(constraints=[SQL("DEFAULT 'pending'")], max_length=16)
    element = ForeignKeyField(column_name="element_id", field="id", model=Element)
    high_confidence = IntegerField(constraints=[SQL("DEFAULT 0")])
    # Email of the user that did the moderation
    moderator = CharField(null=True, max_length=255)
    worker_run = ForeignKeyField(
        column_name="worker_run_id", field="id", model=WorkerRun, null=True
    )

    class Meta:
        table_name = "classification"


class ElementPath(BaseModel):
    id = CharField(primary_key=True, max_length=37)
    parent = ForeignKeyField(
        backref="element_parent_set", column_name="parent_id", field="id", model=Element
    )
    child = ForeignKeyField(column_name="child_id", field="id", model=Element)
    ordering = IntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "element_path"
        indexes = ((("parent", "child"), True),)


class EntityType(BaseModel):
    id = CharField(primary_key=True, max_length=37)
    color = CharField(constraints=[SQL("DEFAULT 'ff0000'")], max_length=6)
    name = CharField(unique=True, max_length=250)

    class Meta:
        table_name = "entity_type"


class Metadata(BaseModel):
    id = CharField(primary_key=True, max_length=37)
    name = CharField(max_length=250)
    value = TextField()
    type = CharField(max_length=50)
    element = ForeignKeyField(column_name="element_id", field="id", model=Element)
    worker_run = ForeignKeyField(
        column_name="worker_run_id", field="id", model=WorkerRun, null=True
    )

    class Meta:
        table_name = "metadata"


class Transcription(BaseModel):
    id = CharField(primary_key=True, max_length=37)
    orientation = TextField(constraints=[SQL("DEFAULT 'horizontal-lr'")])
    text = TextField()
    confidence = FloatField(null=True)
    element = ForeignKeyField(column_name="element_id", field="id", model=Element)
    worker_run = ForeignKeyField(
        column_name="worker_run_id", field="id", model=WorkerRun, null=True
    )

    class Meta:
        table_name = "transcription"


class TranscriptionEntity(BaseModel):
    id = CharField(primary_key=True, max_length=37)
    type = ForeignKeyField(column_name="type_id", field="id", model=EntityType)
    length = IntegerField()
    offset = IntegerField()
    confidence = FloatField(null=True)
    transcription = ForeignKeyField(
        column_name="transcription_id", field="id", model=Transcription
    )
    worker_run = ForeignKeyField(
        column_name="worker_run_id", field="id", model=WorkerRun, null=True
    )

    class Meta:
        table_name = "transcription_entity"
        indexes = ((("transcription", "type", "offset", "length", "worker_run"), True),)

    @hybrid_property
    def text(self):
        return self.transcription.text[self.offset : self.offset + self.length]

    @text.expression
    def text(cls):
        return fn.SUBSTR(cls.transcription.text, cls.offset + 1, cls.length)


class Dataset(BaseModel):
    id = CharField(primary_key=True, max_length=37)
    name = CharField(max_length=100)
    description = TextField()
    state = CharField(constraints=[SQL("DEFAULT 'open'")], max_length=50)
    sets = TextField()


class DatasetElement(BaseModel):
    id = CharField(primary_key=True, max_length=37)
    element = ForeignKeyField(column_name="element_id", field="id", model=Element)
    dataset = ForeignKeyField(column_name="dataset_id", field="id", model=Dataset)
    set_name = CharField(max_length=50)

    class Meta:
        table_name = "dataset_element"
