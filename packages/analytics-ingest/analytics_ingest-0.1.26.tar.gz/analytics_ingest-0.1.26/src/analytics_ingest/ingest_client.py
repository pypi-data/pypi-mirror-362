import asyncio
import time
from threading import Thread
from collections import deque
from typing import Optional
from more_itertools import chunked
from analytics_ingest.internal.schemas.ingest_config_schema import IngestConfigSchema
from analytics_ingest.internal.utils.configuration import ConfigurationService
from analytics_ingest.internal.utils.dtc import create_dtc
from analytics_ingest.internal.utils.gps import create_gps
from analytics_ingest.internal.utils.graphql_executor import GraphQLExecutor
from analytics_ingest.internal.utils.message import create_message
from analytics_ingest.internal.utils.network import create_network
from analytics_ingest.internal.schemas.signal_schema import SignalSchema
from analytics_ingest.internal.utils.mutations import GraphQLMutations


class AnalyticsIngestClient:
    def __init__(self, **kwargs):
        self.config = IngestConfigSchema(**kwargs)
        self.executor = GraphQLExecutor(
            self.config.graphql_endpoint, self.config.jwt_token
        )

        self.configuration_id = ConfigurationService(self.executor).create(
            self.config.model_dump()
        )["data"]["createConfiguration"]["id"]

        self.signal_buffer = deque()
        self.signal_semaphore = asyncio.Semaphore(1)
        self.last_push_time = time.time()
        self.loop = asyncio.new_event_loop()
        self._shutdown = False

        Thread(target=self._start_loop, daemon=True).start()

    def _start_loop(self):
        asyncio.set_event_loop(self.loop)
        self.loop.run_until_complete(self._auto_push_loop())

    async def _auto_push_loop(self):
        while not self._shutdown:
            await asyncio.sleep(1)
            now = time.time()
            if len(self.signal_buffer) >= (
                self.config.batch_size or 0
            ) or now - self.last_push_time >= (self.config.batch_interval_seconds or 0):
                await self._flush_buffer()

    def add_signal(self, signals: Optional[list] = None):
        if not isinstance(signals, list):
            raise ValueError("'signals' should be a list of dicts")

        if not signals:
            raise ValueError("Missing 'signals' list")

        self.signal_buffer.extend(signals)

    async def _flush_buffer(self):
        if not self.signal_buffer:
            return

        async with self.signal_semaphore:
            buffer_copy = list(self.signal_buffer)
            self.signal_buffer.clear()

            try:
                for chunk in chunked(buffer_copy, self.config.max_signal_count):
                    signals = []
                    for item in chunk:
                        message_id = create_message(self.executor, item)
                        signal_input = SignalSchema.from_variables(
                            self.configuration_id, message_id, item["data"], item
                        )
                        signals.append(signal_input.model_dump())

                    payload = {"input": {"signals": signals}}
                    self.executor.execute(
                        GraphQLMutations.upsert_signal_data(), payload
                    )

                self.last_push_time = time.time()

            except Exception as e:
                print(f"Flush failed, retrying next tick: {e}")
                self.signal_buffer.extendleft(reversed(buffer_copy))

    def add_dtc(self, variables: Optional[dict] = None):
        if not variables:
            raise ValueError("Missing 'variables' dictionary")
        try:
            message_id = create_message(self.executor, variables)
            create_dtc(
                executor=self.executor,
                config_id=self.configuration_id,
                variables=variables,
                message_id=message_id,
                batch_size=self.config.batch_size,
            )
        except Exception as e:
            raise RuntimeError(f"Failed to add DTC: {e}")

    def add_gps(self, variables: Optional[dict] = None):
        if not variables:
            raise ValueError("Missing 'variables' dictionary")
        try:
            create_gps(
                executor=self.executor,
                config_id=self.configuration_id,
                variables=variables,
                batch_size=self.config.batch_size,
            )
        except Exception as e:
            raise RuntimeError(f"Failed to add GPS: {e}")

    def add_network_stats(self, variables: Optional[dict] = None):
        if not variables:
            raise ValueError("Missing 'variables' dictionary")
        try:
            create_network(
                executor=self.executor,
                config=self.config,
                variables=variables,
            )
        except Exception as e:
            raise RuntimeError(f"Failed to add network stats: {e}")

    def close(self):
        self._shutdown = True

        if self.signal_buffer:
            future = asyncio.run_coroutine_threadsafe(self._flush_buffer(), self.loop)
            try:
                future.result(timeout=100)
            except Exception as e:
                print(f"❌ Final flush failed: {e}")

        self.loop.call_soon_threadsafe(self.loop.stop)
