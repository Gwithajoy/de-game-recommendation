from kafka.utils import KafkaUtils


class Consumer:
    """
    JSON 메시지를 Kafka 토픽에서 수신하여 처리하는 컨슈머 래퍼 클래스
    """
    def __init__(self, topic: str, group_id: str = None, auto_offset_reset: str = 'earliest'):
        # KafkaConsumer 생성
        self._consumer = KafkaUtils.get_consumer(topic, group_id, auto_offset_reset)

    def listen(self, handler):
        """
        컨슈머를 실행하여 수신된 메시지마다 handler 함수를 호출합니다.
        :param handler: 메시지를 처리할 콜러블 함수
        """
        try:
            for msg in self._consumer:
                handler(msg.value)  # value는 JSON 역직렬화된 파이썬 객체
        except Exception as e:
            # 예외 발생 시 로깅 혹은 재처리
            raise
        finally:
            self._consumer.close()  # 컨슈머 닫기