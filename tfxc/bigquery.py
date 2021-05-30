from google.cloud import bigquery
from tfx.types.experimental.simple_artifacts import Dataset
from tfx import v1 as tfx


# TODO(sfujiwara): Automatically create dataset if it does not exist.
@tfx.dsl.components.component
def BigQueryTableGen(
    project: tfx.dsl.components.Parameter[str],
    query: tfx.dsl.components.Parameter[str],
    destination: tfx.dsl.components.Parameter[str],
    table: tfx.dsl.components.OutputArtifact[Dataset],
):
    """
    A custom component for TFX Pipelines.
    Executes query and saves the result to destination table.
    """

    table.set_string_custom_property(key="table", value=destination)

    client = bigquery.Client(project=project)
    job_config = bigquery.job.QueryJobConfig(
        destination=destination, write_disposition=bigquery.job.WriteDisposition.WRITE_TRUNCATE
    )
    _ = client.query(query, job_config=job_config)
