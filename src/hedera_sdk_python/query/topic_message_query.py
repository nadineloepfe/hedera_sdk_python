from datetime import datetime
from typing import Optional, Callable, Union
import asyncio
from hedera_sdk_python.consensus.topic_message import TopicMessage
from hedera_sdk_python.hapi.mirror import consensus_service_pb2 as mirror_proto
from hedera_sdk_python.hapi.services import basic_types_pb2, timestamp_pb2
from hedera_sdk_python.consensus.topic_id import TopicId

class TopicMessageQuery:
    """
    A query to subscribe to messages from a specific HCS topic, via a mirror node.
    """

    def __init__(
        self,
        topic_id: Optional[Union[str, TopicId]] = None,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        limit: Optional[int] = None,
        chunking_enabled: bool = False,
    ):
        """
        Initializes a new TopicMessageQuery instance.

        Args:
            topic_id (str or TopicId, optional): The ID of the topic to subscribe to.
            start_time (datetime, optional): Start time for the subscription.
            end_time (datetime, optional): End time for the subscription.
            limit (int, optional): Maximum number of messages to retrieve.
            chunking_enabled (bool, optional): Whether to enable chunking.
        """
        self._topic_id = self._parse_topic_id(topic_id) if topic_id else None
        self._start_time = self._parse_timestamp(start_time) if start_time else None
        self._end_time = self._parse_timestamp(end_time) if end_time else None
        self._limit = limit
        self._chunking_enabled = chunking_enabled

    def _parse_topic_id(self, topic_id: Union[str, TopicId]):
        if isinstance(topic_id, str):
            parts = topic_id.strip().split(".")
            if len(parts) != 3:
                raise ValueError(f"Invalid topic ID string: {topic_id}")
            shard, realm, topic = map(int, parts)
            return basic_types_pb2.TopicID(shardNum=shard, realmNum=realm, topicNum=topic)
        elif isinstance(topic_id, TopicId):
            return topic_id.to_proto()
        else:
            raise TypeError("Invalid topic_id format. Must be a string or TopicId.")

    def _parse_timestamp(self, dt: datetime):
        seconds = int(dt.timestamp())
        nanos = int((dt.timestamp() - seconds) * 1e9)
        return timestamp_pb2.Timestamp(seconds=seconds, nanos=nanos)

    def set_topic_id(self, topic_id: Union[str, TopicId]):
        self._topic_id = self._parse_topic_id(topic_id)
        return self

    def set_start_time(self, dt: datetime):
        self._start_time = self._parse_timestamp(dt)
        return self

    def set_end_time(self, dt: datetime):
        self._end_time = self._parse_timestamp(dt)
        return self

    def set_limit(self, limit: int):
        self._limit = limit
        return self

    def set_chunking_enabled(self, enabled: bool):
        self._chunking_enabled = enabled
        return self

    async def subscribe(
        self,
        client,
        on_message: Callable[[TopicMessage], None],
        on_error: Optional[Callable[[Exception], None]] = None,
    ):
        """
        Subscribes to messages from the configured topic. For each received message, `on_message` is invoked.
        If an error occurs, `on_error` is invoked (if provided).

        Args:
            client: The async client with a mirror_stub to use for streaming messages.
            on_message: A callback function invoked for each new TopicMessage.
            on_error: An optional callback function invoked if an error occurs.
        """
        if not self._topic_id:
            raise ValueError("Topic ID must be set before subscribing.")
        if not client.mirror_stub:
            raise ValueError("Client has no mirror_stub. Did you configure a mirror node address?")

        request = mirror_proto.ConsensusTopicQuery(topicID=self._topic_id)
        if self._start_time:
            request.consensusStartTime.CopyFrom(self._start_time)
        if self._end_time:
            request.consensusEndTime.CopyFrom(self._end_time)
        if self._limit is not None:
            request.limit = self._limit

        try:
            async for response in client.mirror_stub.subscribeTopic(request):
                msg_obj = TopicMessage.from_proto(response)
                on_message(msg_obj)
        except Exception as e:
            if on_error:
                on_error(e)
