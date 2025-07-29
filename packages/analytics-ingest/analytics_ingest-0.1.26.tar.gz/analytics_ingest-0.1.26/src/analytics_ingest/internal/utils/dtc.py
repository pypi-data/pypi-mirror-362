from analytics_ingest.internal.schemas.dtc_schema import DTCSchema
from analytics_ingest.internal.schemas.inputs.dtc_input import make_dtc_input
from analytics_ingest.internal.utils.batching import Batcher
from analytics_ingest.internal.utils.graphql_executor import GraphQLExecutor
from analytics_ingest.internal.utils.mutations import GraphQLMutations
from analytics_ingest.internal.utils.serialization import serialize_payload


def create_dtc(
    executor: GraphQLExecutor,
    config_id: str,
    variables: dict,
    message_id: str,
    batch_size: int,
):
    file_id = variables.get("fileId", "")
    messageDate = variables.get("messageDate", "")
    inputs = build_batched_dtc_inputs(
        config_id, variables, message_id, file_id, messageDate, batch_size
    )
    for payload in inputs:
        payload = serialize_payload(payload)
        print("payload dtc ", payload)
        executor.execute(GraphQLMutations.upsert_dtc_mutation(), payload)


def build_batched_dtc_inputs(
    config_id, variables, message_id, fileId, messageDate, batch_size
):
    dtc_items = DTCSchema.from_variables(variables)
    batches = Batcher.create_batches(dtc_items, batch_size)
    return [
        make_dtc_input(config_id, batch, message_id, fileId, messageDate)
        for batch in batches
    ]
