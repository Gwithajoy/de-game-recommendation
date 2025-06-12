from kafka.utils import KafkaUtils


class Producer:
    """
    JSON 메시지를 Kafka 토픽으로 전송하는 프로듀서 래퍼 클래스
    """
    def __init__(self):
        self._producer = KafkaUtils.get_producer()  # KafkaProducer 생성

    def send(self, topic: str, message: dict) -> None:
        """
        지정된 Kafka 토픽에 메시지를 전송합니다.
        :param topic: Kafka 토픽 이름
        :param message: JSON 직렬화 가능한 딕셔너리 데이터
        """
        future = self._producer.send(topic, message)
        future.get(timeout=10)  # 전송 성공 대기

    def close(self) -> None:
        """
        프로듀서를 flush 하고 닫습니다.
        """
        self._producer.flush()  # 남은 메시지 전송
        self._producer.close()  # 연결 종료
