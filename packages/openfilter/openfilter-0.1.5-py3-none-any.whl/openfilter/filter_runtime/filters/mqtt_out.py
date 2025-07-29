import base64
import json
import logging
import os
from dataclasses import asdict, is_dataclass
from datetime import datetime
from time import time
from typing import Literal

import cv2
import numpy as np

from openfilter.filter_runtime.filter import FilterConfig, Filter
from openfilter.filter_runtime.mq import is_mq_addr
from openfilter.filter_runtime.utils import json_getval, dict_without, split_commas_maybe, rndstr, adict

__all__ = ['MQTTOutConfig', 'MQTTOut']

logger = logging.getLogger(__name__)

DEBUG_MQTT        = bool(json_getval((os.getenv('DEBUG_MQTT') or 'false').lower()))

RECONNECT_IVL     = int(os.getenv('MQTT_RECONNECT_IVL') or 1)
RECONNECT_IVL_MAX = int(os.getenv('MQTT_RECONNECT_IVL_MAX') or 60)


class MQTTOutConfig(FilterConfig):
    class Mapping(adict):
        class Options(adict):
            qos:    int | None
            retain: bool | None

        dst_topic: str               # MQTT destination topic (a/b/c)
        src_topic: str | None        # our source topic, a single topic name (no path)
        src_path:  list[str] | None  # path in our source topic
        options:   Options | None

    mappings:    str | list[str | Mapping]

    broker_host: str | None
    broker_port: int | None
    username:    str | None
    password:    str | None
    client_id:   str | Literal[True] | None
    keepalive:   int | None
    base_topic:  str | None

    interval:    float | None  # sampling interval, if present will only sample and send roughly once per this many seconds

    # setting these here will make them default for all topics (overridable individually)
    qos:    int | None
    retain: bool | None


class MQTTOut(Filter):
    """Remap incoming ZeroMQ data to outgoing MQTT. Both `sources` and `mappings` take part in the remapping, `sources`
    with the standard mapping of incoming topics on the wire to received topics. `mappings` has more control and allows
    setting mqtt publish parameters like `qos` and `retain`. By default images are normally sent at `qos` = 0 unless
    overridden and JSON data as `qos` = 2. All messages are sent with `retain` = False by default.

    config:
        outputs:
            Can take individual parameters in config or most of them in an "mqtt://..." `outputs` of the form:

            mqtt:// [[host][:port]] [/base/topic/] [!qos=?] [!retain] [; [topic] [/cat[/sub]] [>out_topic] [!qos=?] [!retain]]

            Example:
                mqtt://host:port/base_topic/ ; topic ; topic2/image > topic2_frames ; ...

        mappings:
            There can be multiple delimited by commas, whitespace is ignored. You should use either this or the above
            extended output notation but not both together. Examples:

            "" or None  - Map solo existing topic Frame.image to "base_topic/frames" and Frame.data to
                "base_topic/data". Only works if subscribed to one topic exactly.

            "topic" - Map "topic" Frame.image to "base_topic/frames" and Frame.data to "base_topic/data".

            "/image" - Map solo existing topic Frame.image to "base_topic/frames". Only works if subscribed to one
                topic exactly.

            "/data" - Map solo existing topic Frame.data to "base_topic/data". Only works if subscribed to one topic
                exactly.

            "/data/sub" - Map solo existing topic Frame.data['sub'] to "base_topic/sub". Only works if subscribed to
                one topic exactly.

            "topic/image" - Map "topic" Frame.image to "base_topic/frames".

            "topic/image > other" - Map "topic" Frame.image to "base_topic/other".

            "topic/image > other ! qos=0 ! retain=true" - Map "topic" Frame.image to "base_topic/other" with qos = 0
                and retain = True.

            "topic/image" - Map "topic" Frame.image to "base_topic/frames".

            "topic/data/sub" - Map "topic" Frame.data['sub'] to "base_topic/sub".

            "topic/data/sub > other" - Map "topic" Frame.data['sub'] to "base_topic/other".

            "topic/data/sub/more" - Map "topic" Frame.data['sub']['more'] to "base_topic/more".

        broker_host:
            If specifying via `mappings`, you can specify the broker host here.

        broker_port: int | None
            If specifying via `mappings`, you can specify the broker port here.
            
        username:
            If specifying via `mappings`, you can specify the broker username here.

        password:
            If specifying via `mappings`, you can specify the broker password here.

        client_id:
            If you want you can specify an explicit client_id for the MQTT client, Setting this to true will create a
            random client_id string to use for the session. Otherwise no client_id is used.

        keepalive:
            MQTT keepalive in seconds.

        base_topic:
            If specifying via `mappings`, you can specify the base output MQTT topic here.

        interval:
            Sampling interval, if present will only sample topic messages received in process() and send out to MQTT
            roughly once per this many seconds.

        qos:
            QOS value for all topics, can be overridden by individual topics.

        retain:
            Retain value for all topics, can be overridden by individual topics.

    Environment variables:
        DEBUG_MQTT:
            If LOG_LEVEL is DEBUG then will log extra MQTT debug information.

        MQTT_RECONNECT_IVL:
            Starting reconnect wait in seconds.

        MQTT_RECONNECT_IVL_MAX:
            Reconnect exponential backoff max value in milliseconds, 0 for no backoff.
    """

    FILTER_TYPE   = 'Output'
    VALID_OPTIONS = ('qos', 'retain')


    @staticmethod
    def b64_encode_image(image: np.ndarray) -> bytes:
        _, im_arr = cv2.imencode(".jpg", image)
        im_bytes  = im_arr.tobytes()

        return base64.b64encode(im_bytes)

    @staticmethod
    def serialize_obj(obj):
        if isinstance(obj, dict):
            return {k: MQTTOut.serialize_obj(v) for k, v in obj.items()}
        elif isinstance(obj, (list, tuple)):
            return [MQTTOut.serialize_obj(item) for item in obj]
        elif isinstance(obj, (bytes, bytearray)):  # this will wind up handling Frame.jpg
            return base64.b64encode(obj)
        elif isinstance(obj, np.ndarray):
            return MQTTOut.b64_encode_image(obj)  # legacy compatibility
        elif isinstance(obj, (str, int, float)):
            return obj
        elif is_dataclass(obj):
            return MQTTOut.serialize_obj(asdict(obj))
        elif isinstance(obj, datetime):
            return obj.isoformat()
        elif isinstance(obj, np.generic):
            return obj.item()
        else:
            raise TypeError(f"Object of type {type(obj).__name__} is not serializable")

    @staticmethod
    def init_mqtt(host: str, port: int, client_id: str | None, keepalive: int = 60, username: str | None = None, password: str | None = None):
        import paho.mqtt.client as mqtt
        from paho.mqtt import __version__ as paho_mqtt_version
        from paho.mqtt.packettypes import PacketTypes
        from paho.mqtt.properties import Properties

        if paho_mqtt_version[:1] in "01":
            client = mqtt.Client(client_id=client_id or '', protocol=mqtt.MQTTv5)
        else:
            client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, client_id=client_id or '', protocol=mqtt.MQTTv5)
        
        if username is not None and password is not None:
            client.username_pw_set(username, password)

        props                   = Properties(PacketTypes.CONNECT)
        props.MaximumPacketSize = 268435455

        client.connect(host, port, keepalive, properties=props)
        client.loop_start()

        return client

    @classmethod
    def normalize_config(cls, config):
        outputs = split_commas_maybe(config.get('outputs'))  # we do not assume how Filter will normalize sources/outputs in the future
        config  = MQTTOutConfig(super().normalize_config(dict_without(config, 'outputs')))

        if outputs is not None:
            config.outputs = outputs

        if not config.sources:
            raise ValueError('must specify at least one source')

        # convenience, specify almost everything in output string, convert to normal config representation

        if outputs:
            if len(outputs) != 1:
                raise ValueError('filter only takes a single output')
            if not (output := outputs[0]).startswith('mqtt://'):
                raise ValueError('filter only takes mqtt:// output')

            output, mappings = Filter.parse_topics(output[7:], mapping=None)

            if mappings:
                if config.mappings is not None:
                    raise ValueError('topic mappings can not be present in both config.outputs and config.mappings')

                config.mappings = mappings

            addr_n_base_topic, options = Filter.parse_options(output)

            if any((option := o) not in MQTTOut.VALID_OPTIONS for o in options):
                raise ValueError(f'unknown option {option!r} in {output!r}')
            if any(getattr(config, (option := o)) is not None for o in options):
                raise ValueError(f'option {option!r} can not be present in both config.outputs and config.{option}')

            config.update(options)

            addr, *base_topic = addr_n_base_topic.split('/', 1)

            if base_topic:
                if config.base_topic is not None:
                    raise ValueError('base topic can not be present in both config.outputs and config.base_topic')

                config.base_topic = base_topic[0] or None

            host, *port = addr.rsplit(':', 1)

            if host or port:
                if config.broker_host is not None or config.broker_port is not None:
                    raise ValueError('broker can not be present in both config.outputs and config.broker_host/port')

                if host:
                    config.broker_host = host
                if port:
                    config.broker_port = int(port[0])

            del config.outputs

        # parse and validate normal config representation

        if config.client_id is True:
            config.client_id = f'{config.id}_{rndstr(8)}'

        config.mappings = split_commas_maybe(config.mappings)

        for idx, mapping in enumerate(mappings := config.mappings or ()):
            if isinstance(mapping, dict):
                if not isinstance(mapping, MQTTOutConfig.Mapping):
                    mappings[idx] = MQTTOutConfig.Mapping(mapping)  # because silly user might have passed in dicts

            else:
                if is_mq_addr(mapping):
                    raise ValueError(f'mappings must be MQTT topics, not: {mapping!r}')

                srcdst, options = Filter.parse_options(mapping)
                src, dst        = ([s.strip() for s in srcdst.split('>')] + [''])[:2]

                if src:
                    src_topic, *src_path = [s.strip() for s in src.split('/')]

                    if not src_path and dst:
                        raise ValueError(f"can not have a destination '>' topic without a source path '/' as in {mapping!r}")

                elif dst:
                    raise ValueError(f"can not have a destination '>' topic without a source as in {mapping!r}")
                else:
                    src_topic = src_path = None

                mappings[idx] = MQTTOutConfig.Mapping(dst_topic=dst or None, src_topic=src_topic or None,
                    src_path='/'.join(src_path) if src_path else None, options=options)

        for mapping in mappings:
            if not isinstance(options := mapping.options, MQTTOutConfig.Mapping.Options):
                mapping.options = options = MQTTOutConfig.Mapping.Options() if options is None else MQTTOutConfig.Mapping.Options(options)
            if any((option := o) not in MQTTOut.VALID_OPTIONS for o in options):
                raise ValueError(f'unknown option {option!r} in {mapping!r}')
            if (dst := mapping.dst_topic) and dst.endswith('/'):
                raise ValueError(f'invalid destination {dst!r}')

            if not (src_path := mapping.src_path):
                if dst:
                    raise ValueError(f'can not have path without a destination as in {src_path!r}')

            else:
                if src_path.endswith('/'):
                    raise ValueError(f'invalid path {src_path!r} in {mapping}')
                if src_path.startswith('image/'):
                    raise ValueError(f"can not have a subpath '/' from an image as in {src_path!r}")

                elif src_path not in ('image', 'data'):
                    if not src_path.startswith('data/'):
                        raise ValueError(f"first topic subpath can only be 'image' or 'data', not as in {src_path!r}")

                if dst is None:
                    mapping.dst_topic = 'frames' if src_path == 'image' else src_path.rsplit('/', 1)[-1]

        if sum(mapping.dst_topic is None for mapping in mappings) > 1:
            raise ValueError('can not have more than one implicit topic mapping (without an explicit destination)')
        if len(set(mapping.dst_topic for mapping in mappings)) != len(mappings):
            raise ValueError('duplicate destination topics present')

        return config

    def get_client(self):
        """Try to connect to MQTT broker and back off exponentially on fail."""

        if (client := self.client) is not None:
            return client
        if (t := time()) < self.conn_t:
            return None

        self.conn_t    = t + (wait := self.conn_wait)
        self.conn_wait = min(wait * 2, RECONNECT_IVL_MAX)

        try:
            self.client = client = self.init_mqtt(host=self.broker_host, port=self.broker_port, client_id=self.client_id, keepalive=self.keepalive,username=self.username,password=self.password)

        except Exception:
            logger.warning(f'MQTT connect failed: {self.broker_host}:{self.broker_port}  (wait {wait} seconds)')

            return None

        logger.info(f'MQTT connected: {self.broker_host}:{self.broker_port}')

        return client

    def setup(self, config):
        base_topic = ((base_topic := config.base_topic) and str(config.base_topic)) or ''

        if base_topic and not base_topic.endswith('/'):
            base_topic += '/'

        self.base_topic = base_topic

        default_options = {
            **({} if (qos := config.qos) is None else {'qos': qos}),
            **({} if (retain := config.retain) is None else {'retain': retain}),
        }

        self.mappings = mappings = []

        for mapping in config.mappings or (adict(),):
            mappings.append((
                mapping.src_topic,
                (src_path := mapping.src_path) and src_path.split('/'),
                (out := mapping.dst_topic) and (base_topic + out),
                {**({'qos': 0 if src_path == 'image' else 2} if src_path else {}), **default_options, **(mapping.options or {})},
            ))

        if DEBUG_MQTT:
            logger.debug(f'MQTT topic mappings: {self.mappings}')

        self.broker_host = config.broker_host or 'localhost'
        self.broker_port = config.broker_port or 1883
        self.client_id   = config.client_id
        self.keepalive   = config.keepalive or 60
        self.interval    = config.interval or None
        self.interval_f  = {}
        self.interval_t  = time()
        self.conn_t      = -float('inf')
        self.conn_wait   = RECONNECT_IVL
        self.client      = None
        self.username    = config.username
        self.password    = config.password
        self.client      = self.get_client()
        
    def shutdown(self):
        if self.client is not None:
            self.client.loop_stop()
            self.client.disconnect()

    def process(self, frames):
        if (interval := self.interval) is not None:
            frames = {**self.interval_f, **frames}  # accumulate frames from each topic overwriting older with latest

            if (td := (t := time()) - (interval_t := self.interval_t)) < interval:
                self.interval_f = frames

                return

            self.interval_f = {}
            self.interval_t = interval_t + (td // interval) * interval

        if (client := self.get_client()) is None:
            return

        published = set()

        def publish(topic, payload, options):
            if DEBUG_MQTT:
                logger.debug(f'publish to {topic!r}: {(p if len(p := repr(payload)) <= 64 else f"{p[:64]}...")!r}, {options=}')

            if topic in published:
                raise RuntimeError(f'duplicate destination topic detected: {topic!r}')

            published.add(topic)

            if payload is None or (isinstance(payload, (list, tuple, dict)) and not payload):
                return

            if not isinstance(payload, (str, int, float, bytes)):
                payload = MQTTOut.serialize_obj(payload)

            if isinstance(payload, (list, dict)):
                payload = json.dumps(payload)

            client.publish(topic, payload=payload, **options)

        frames = frames.copy()

        for src_topic, src_path, dst, options in self.mappings:
            if src_topic is None:
                if len(frames) != 1:
                    raise RuntimeError(f'implicit topic mapping only valid when there is exactly one received topic, not: {tuple(frames)}')

                src_topic = next(iter(frames))

            if (frame := frames.get(src_topic)) is None:
                # once(logger.warning, f'source topic {src_topic!r} not in received topics: {tuple(frames)}')

                continue

            frames[src_topic] = frame = frame.ro_bgr

            if dst is None:
                publish(self.base_topic + 'data', frame.data, {'qos': 2, **options})

                if jpg := frame.jpg:
                    publish(self.base_topic + 'frames', jpg, {'qos': 0, **options})

            elif src_path == ['image']:
                if jpg := frame.jpg:
                    publish(dst, jpg, options)

            else:
                payload = getattr(frame, next(itr := iter(src_path)))

                for sub in itr:
                    if payload is not None:
                        payload = payload.get(sub)

                publish(dst, payload, options)


if __name__ == '__main__':
    MQTTOut.run()
