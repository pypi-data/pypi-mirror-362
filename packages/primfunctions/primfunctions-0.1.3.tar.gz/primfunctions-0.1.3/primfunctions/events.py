import json


class Event:
    def __init__(self, name: str, data: dict = {}):
        self.name = name
        self.data = data


class CustomEvent(Event):
    def __init__(self, name: str, data: dict = {}):
        super().__init__(name, {**data, "custom": True})


class StartEvent(Event):
    def __init__(self):
        super().__init__("start")


class StopEvent(Event):
    def __init__(self):
        super().__init__("stop")


class InterruptEvent(Event):
    def __init__(self):
        super().__init__("interrupt")


class TimeoutEvent(Event):
    def __init__(self):
        super().__init__("timeout")


class TextEvent(Event):
    def __init__(self, source: str, text: str):
        super().__init__("text", {"source": source, "text": text})


class TextToSpeechEvent(Event):
    def __init__(self, text: str, voice="nova", cache=True, interruptable=True):
        super().__init__(
            "text_to_speech",
            {
                "text": text,
                "voice": voice,
                "cache": cache,
                "interruptable": interruptable,
            },
        )


class AudioEvent(Event):
    def __init__(self, path: str):
        super().__init__("audio", {"path": path})


class SilenceEvent(Event):
    def __init__(self, duration: int):
        super().__init__("silence", {"duration": duration})


class TransferCallEvent(Event):
    def __init__(self, phone_number: str):
        super().__init__("transfer_call", {"phone_number": phone_number})


class WarmTransferEvent(Event):
    def __init__(self, phone_number: str, data: dict):
        super().__init__("warm_transfer", {"phone_number": phone_number, "data": data})


class MergeCallEvent(Event):
    def __init__(self, call_sid: str):
        super().__init__("merge_call", {"call_sid": call_sid})


class ContextUpdateEvent(Event):
    def __init__(self, context: dict):
        super().__init__("context", {"context": context})


class ErrorEvent(Event):
    def __init__(self, message: str):
        super().__init__("error", {"message": message})


class LogEvent(Event):
    def __init__(self, message: str):
        super().__init__("log", {"message": message})


class CollectPaymentEvent(Event):
    def __init__(self, amount: float):
        super().__init__("collect_payment", {"amount": amount})


class CollectPaymentSuccessEvent(Event):
    def __init__(self):
        super().__init__("collect_payment_success")


class SupervisorRequestEvent(Event):
    def __init__(self, content: str):
        super().__init__("supervisor_request", {"content": content})


class SupervisorResponseEvent(Event):
    def __init__(self, content: str):
        super().__init__("supervisor_response", {"content": content})


class ConnectSTSEvent(Event):
    def __init__(self, configuration: dict):
        super().__init__("connect_sts", {"configuration": configuration})


class DisconnectSTSEvent(Event):
    def __init__(self):
        super().__init__("disconnect_sts", {})


def event_to_str(event: Event) -> str:
    return json.dumps({"name": event.name, "data": event.data})


def event_from_str(event_str: str) -> Event:
    event = json.loads(event_str)
    name = event["name"]
    data = event["data"]

    event_types = {
        "audio": lambda: AudioEvent(data["path"]),
        "context": lambda: ContextUpdateEvent(data["context"]),
        "error": lambda: ErrorEvent(data["message"]),
        "interrupt": InterruptEvent,
        "log": lambda: LogEvent(data["message"]),
        "merge_call": lambda: MergeCallEvent(data["call_sid"]),
        "silence": lambda: SilenceEvent(data["duration"]),
        "start": StartEvent,
        "stop": StopEvent,
        "text_to_speech": lambda: TextToSpeechEvent(data["text"], data["voice"]),
        "text": lambda: TextEvent(data["source"], data["text"]),
        "timeout": TimeoutEvent,
        "transfer_call": lambda: TransferCallEvent(data["phone_number"]),
        "warm_transfer": lambda: WarmTransferEvent(data["phone_number"], data["data"]),
        "collect_payment": lambda: CollectPaymentEvent(data["amount"]),
        "collect_payment_success": CollectPaymentSuccessEvent,
        "supervisor_request": lambda: SupervisorRequestEvent(data["content"]),
        "supervisor_response": lambda: SupervisorResponseEvent(data["content"]),
        "connect_sts": lambda: ConnectSTSEvent(data["configuration"]),
        "disconnect_sts": DisconnectSTSEvent,
    }

    if name in event_types:
        return event_types[name]()

    raise ValueError(f"Unknown event type: {name}")


def format_event(event: Event) -> bytes:
    event_string = event_to_str(event)

    return bytes(f"{event_string}\n", "utf-8")
