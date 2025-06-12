import json
from kafka import KafkaProducer, KafkaConsumer


class KafkaUtils:
    """
    JSON 직렬화 설정으로 Kafka 프로듀서와 컨슈머를 생성하는 유틸리티 클래스
    """
    BROKERS = ['localhost:9092']  # Kafka 브로커 주소 목록

    @classmethod
    def get_producer(cls) -> KafkaProducer:
        """
        JSON 직렬화를 설정한 KafkaProducer 인스턴스를 반환합니다.
        """
        return KafkaProducer(
            bootstrap_servers=cls.BROKERS,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')  # 메시지를 JSON으로 직렬화
        )

    @classmethod
    def get_consumer(cls, topic: str, group_id: str = None, auto_offset_reset: str = 'earliest') -> KafkaConsumer:
        """
        지정된 토픽의 메시지를 JSON 역직렬화로 수신하는 KafkaConsumer 인스턴스를 반환합니다.
        :param topic: 구독할 Kafka 토픽 이름
        :param group_id: 컨슈머 그룹 ID (선택)
        :param auto_offset_reset: 오프셋 초기화 방식(default='earliest')
        """
        return KafkaConsumer(
            topic,
            bootstrap_servers=cls.BROKERS,
            auto_offset_reset=auto_offset_reset,
            group_id=group_id,
            value_deserializer=lambda v: json.loads(v.decode('utf-8'))  # JSON 역직렬화
        )