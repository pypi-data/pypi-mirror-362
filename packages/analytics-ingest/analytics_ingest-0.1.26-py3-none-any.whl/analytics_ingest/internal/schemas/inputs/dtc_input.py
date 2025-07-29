def make_dtc_input(config_id, batch, message_id, file_id="", message_date=None):
    return {
        "input": {
            "configurationId": config_id,
            "messageId": message_id,
            "fileId": str(file_id),
            "messageDate": message_date,
            "data": [item.model_dump() for item in batch],
        }
    }
