import asyncio
import fractions
import functools
import io
import threading
from abc import ABC, abstractmethod
from collections import deque
from concurrent.futures import Future, ThreadPoolExecutor
from pathlib import Path
from types import TracebackType
from typing import AsyncIterator, Callable, Iterator

import av
import av.container
import av.filter
import av.filter.context
import av.frame
import av.stream
import numpy as np
from pydub import AudioSegment

from .asyncio import run_in_threadpool
from .io import PopIO
from .prefetch import aprefetch_iterator

TIME_BASE = fractions.Fraction(1, 90000)


class PyAVInterface(ABC):
    _container: av.container.Container
    _streams: tuple[av.VideoStream, ...]

    def __init__(self):
        self.__container_init_lock = threading.Lock()

    def _init_container(self):
        if self._container is None:
            with self.__container_init_lock:
                self._create_container()

    @abstractmethod
    def _create_container(self):
        """create container"""

    @property
    def container(self) -> av.container.Container:
        self._init_container()
        return self._container

    @property
    def streams(self) -> tuple[av.VideoStream, ...]:
        self._init_container()
        return self._streams

    @property
    def fps(self):
        return self.streams[0].base_rate or self.streams[0].codec_context.framerate

    @property
    def width(self):
        return self.streams[0].codec_context.width

    @property
    def height(self):
        return self.streams[0].codec_context.height

    @property
    def pix_fmt(self):
        return self.streams[0].format.name

    def __enter__(self):
        self.container.__enter__()
        return self

    def __exit__(self, *args):
        self.container.__exit__(*args)

    async def __aenter__(self):
        await run_in_threadpool(self.container.__enter__)

    async def __aexit__(self):
        await run_in_threadpool(self.container.__exit__)


class BasePyAVReader(PyAVInterface):
    container: av.container.InputContainer

    def __init__(
        self,
        path,
        *,
        format: str,
        buffer_size: int,
        filter: tuple[type[av.frame.Frame]],
        options={},
    ):
        super().__init__()
        self._container = None
        self._path = path
        self._format = format
        self._buffer_size = buffer_size
        self._filter = filter
        self._options = options

        self._codec_contexts = {}

    @abstractmethod
    def __iter__(self):
        raise NotImplementedError

    def _create_container(self):
        if self._container is None:
            container = av.open(
                self._path,
                "r",
                format=self._format,
                buffer_size=self._buffer_size,
                options=self._options,
            )

            self._streams = tuple()
            if av.VideoFrame in self._filter:
                self._streams = container.streams.video
                for stream in self._streams:
                    if stream.codec_context.name in ("vp8", "vp9"):
                        if stream.codec_context.name == "vp8":
                            codec_name = "libvpx"
                        elif stream.codec_context.name == "vp9":
                            codec_name = "libvpx-vp9"
                        codec = av.codec.Codec(codec_name, "r")
                        self._codec_contexts[stream] = codec.create()
                    else:
                        self._codec_contexts[stream] = stream.codec_context

            self._audio_streams = tuple()
            if av.AudioFrame in self._filter:
                self._audio_streams = container.streams.audio
                for stream in self._audio_streams:
                    self._codec_contexts[stream] = stream.codec_context

            self._container = container

    @property
    def codec_contexts(self) -> dict[av.stream.Stream, av.CodecContext]:
        self._init_container()
        return self._codec_contexts

    @property
    def audio_streams(self) -> tuple[av.AudioStream, ...]:
        self._init_container()
        return self._audio_streams


class PyAVReader(BasePyAVReader):
    def __init__(
        self,
        path,
        start=0,
        end=(2 << 62) - 1,
        *,
        format=None,
        buffer_size=32768,
        filter=(av.VideoFrame, av.AudioFrame),
        options={},
    ):
        super().__init__(
            path, format=format, buffer_size=buffer_size, filter=filter, options=options
        )
        self.start = start
        self.end = end
        self._alpha_merger = None

    @property
    def alpha_merger(self) -> "BaseAlphaMerger":
        if self._alpha_merger is None:
            if len(self.streams) < 2:
                self._alpha_merger = NotAlphaMerger()
            elif len(self.streams) == 2:
                self._alpha_merger = AlphaMerger(*self.streams)
            else:
                raise NotImplementedError
        return self._alpha_merger

    def __iter__(self):
        with self:
            for packet in self.container.demux(self.streams + self.audio_streams):
                for frame in self.codec_contexts[packet.stream].decode(packet):
                    if (
                        packet.stream in self.streams
                        and not (
                            self.start
                            <= round(frame.pts * self.fps * frame.time_base)
                            < self.end
                        )
                        or packet.stream in self.audio_streams
                        and not (
                            self.start - frame.time_base
                            <= frame.pts * frame.time_base
                            < self.end + frame.time_base
                        )
                    ):
                        continue

                    if packet.stream in self.audio_streams:
                        yield frame
                    elif packet.stream is self.streams[0]:
                        self.alpha_merger.push_image(frame)
                    else:
                        self.alpha_merger.push_alpha(frame)

                while (result := self.alpha_merger.pull()) is not None:
                    yield result
        if isinstance(self.alpha_merger, AlphaMerger):
            self.alpha_merger.close()


PyAVDisposableReader = PyAVReader


def create_stream(
    container,
    codec_name: str,
    rate: int | fractions.Fraction,
    width: int,
    height: int,
    pix_fmt: str,
    bit_rate: int,
    time_base: fractions.Fraction,
    options: dict,
):
    stream = container.add_stream(codec_name=codec_name, rate=rate)
    stream.width = width
    stream.height = height
    stream.pix_fmt = pix_fmt
    stream.bit_rate = bit_rate
    stream.time_base = time_base
    stream.options = options
    return stream


class PyAVWriter(PyAVInterface):
    container: av.container.OutputContainer

    def __init__(
        self,
        path: str | Path | io.IOBase | None,
        width: int = None,
        height: int = None,
        fps: fractions.Fraction = None,
        *,
        codec_name="libvpx-vp9",
        pix_fmt="yuva420p",
        buffer_size=32768,
        bit_rate=1024 * 1024,
        alpha_stream: bool | str = False,
        audio_codec_name=None,
        audio_sample_rate=48000,
        audio_format="s16",
        audio_layout="stereo",
        audio_bit_rate=192000,
        format=None,
        options={},
    ):
        super().__init__()

        assert codec_name is not None or audio_codec_name is not None

        if codec_name is not None:
            if pix_fmt == "rgb24" and codec_name == "rawvideo" and alpha_stream:
                pix_fmt = "rgba"
                alpha_stream = False
            elif (
                pix_fmt == "yuv420p"
                and codec_name.startswith("libvpx")
                and alpha_stream
            ):
                pix_fmt = "yuva420p"
                alpha_stream = False
            elif (pix_fmt.startswith("yuva") or pix_fmt == "rgba") and alpha_stream:
                alpha_stream = False

        self._path = path
        self._width = width
        self._height = height
        self._fps = fps
        self._codec_name = codec_name
        self._pix_fmt = pix_fmt
        self._buffer_size = buffer_size
        self._bit_rate = bit_rate
        self._alpha_stream = alpha_stream
        self._audio_codec_name = audio_codec_name
        self._audio_sample_rate = audio_sample_rate
        self._audio_format = audio_format
        self._audio_layout = audio_layout
        self._audio_bit_rate = audio_bit_rate
        self._format = format
        self._options = options

        self._container = None
        self._alpha_extractor = None

        self.__frames = 0

        self.pool = None
        self.future: Future[av.VideoFrame | av.AudioFrame] = None

        self.write_lazy = self.lazy(self.write)
        self.write_video_frame_lazy = self.lazy(self.write_video_frame)
        self.write_audio_lazy = self.lazy(self.write_audio)
        self.write_audio_frame_lazy = self.lazy(self.write_audio_frame)

    def lazy_register_path(self, path: str | Path | io.IOBase):
        if self._path is not None:
            raise ValueError
        self._path = path

    def _create_container(self):
        if self._path is None:
            raise ValueError

        container = av.open(
            self._path,
            "w",
            buffer_size=self._buffer_size,
            format=self._format,
            options=self._options,
        )
        streams = []
        if self._codec_name is not None:
            pix_fmts = [self._pix_fmt]
            if self._alpha_stream:
                pix_fmts.append(
                    self._pix_fmt if self._alpha_stream == True else self._alpha_stream
                )

            for pf in pix_fmts:
                stream = create_stream(
                    container,
                    codec_name=self._codec_name,
                    rate=self._fps,
                    width=self._width,
                    height=self._height,
                    pix_fmt=pf,
                    bit_rate=self._bit_rate,
                    time_base=TIME_BASE,
                    options=self._options,
                )
                streams.append(stream)

        audio_stream = None
        if self._audio_codec_name is not None:
            audio_stream = container.add_stream(
                codec_name=self._audio_codec_name, rate=self._audio_sample_rate
            )
            audio_stream.format = self._audio_format
            audio_stream.layout = self._audio_layout
            audio_stream.bit_rate = self._audio_bit_rate

        self._streams = streams
        self._audio_stream = audio_stream
        self._container = container

    @property
    def audio_stream(self) -> av.AudioStream:
        self._init_container()
        return self._audio_stream

    @property
    def alpha_extractor(self):
        if self._alpha_extractor is None and self._alpha_stream:
            self._alpha_extractor = AlphaExtractor(self._width, self._height)
        return self._alpha_extractor

    def array_to_frame(self, array):
        if self.streams[0].pix_fmt.startswith("yuva") or len(self.streams) == 2:
            frame = av.VideoFrame.from_ndarray(array, format="rgba")
        else:
            frame = av.VideoFrame.from_ndarray(array[..., :3], format="rgb24")
        return frame

    def lazy(self, func):
        @functools.wraps(func)
        def _func(*args, **kwargs):
            if self.pool is None:
                self.pool = ThreadPoolExecutor(1)

            if self.future is not None:
                self.future.result()
                del self.future

            self.future = self.pool.submit(func, *args, **kwargs)

        return func

    def write(self, array):
        frame = self.array_to_frame(array)
        self.write_video_frame(frame)

    def encode_video_frame(self, frame: av.VideoFrame):
        frames = [frame]
        if self.alpha_extractor is not None:
            frames.append(self.alpha_extractor(frame))

        for stream, frame in zip(self.streams, frames):
            frame.time_base = TIME_BASE
            frame.pts = round(self.__frames / self.fps / TIME_BASE)
            for packet in stream.encode_lazy(frame):
                packet.stream = stream
                yield packet

        self.__frames += 1

    def write_video_frame(self, frame: av.VideoFrame):
        for packet in self.encode_video_frame(frame):
            self.container.mux_one(packet)

    def encode_video_frames(self, iterator: Iterator[av.VideoFrame]):
        for frame in iterator:
            for packet in self.encode_video_frame(frame):
                yield packet

    def write_audio(self, audio_segment: AudioSegment):
        audio_segment = (
            audio_segment.set_channels(self.audio_stream.layout.nb_channels)
            .set_sample_width(self.audio_stream.format.bytes)
            .set_frame_rate(self.audio_stream.sample_rate)
        )
        frame = av.AudioFrame.from_ndarray(
            np.array(audio_segment.get_array_of_samples()).reshape(1, -1),
            format=self.audio_stream.format.name,
            layout=self.audio_stream.layout.name,
        )
        frame.sample_rate = audio_segment.frame_rate
        self.write_audio_frame(frame)

    def write_audio_frame(self, frame: av.AudioFrame):
        for packet in self.encode_audio_frames([frame]):
            self.container.mux_one(packet)

    def encode_audio_frames(self, iterator: Iterator[av.AudioFrame]):
        for frame in iterator:
            for packet in self.audio_stream.codec_context.encode_lazy(frame):
                packet.stream = self.audio_stream
                yield packet

    def flush(self):
        if self.future is not None:
            self.future.result()
            del self.future
            self.future = None

        if self.alpha_extractor is not None:
            self.alpha_extractor.close()
        for stream in self.streams:
            self.container.mux(stream.encode())
        if self.audio_stream is not None:
            self.container.mux(self.audio_stream.encode())

    def __exit__(
        self,
        t: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ):
        if exc is None:
            self.flush()
        super().__exit__(t, exc, tb)


class Filter(ABC):
    graph: av.filter.Graph

    def __init__(self):
        self.graph = av.filter.Graph()

    def close(self):
        self.graph.push(None)


class _Formatter(Filter):
    def __init__(self, width: int, height: int, from_pix_fmt: str, to_pix_format: str):
        super().__init__()
        src = self.graph.add_buffer(
            width=width,
            height=height,
            format=from_pix_fmt,
            time_base=fractions.Fraction(1, 1000),
        )

        reformat = self.graph.add("format", to_pix_format)
        src.link_to(reformat)

        sink = self.graph.add("buffersink")
        reformat.link_to(sink)

        self.graph.configure()

    def __call__(self, frame: av.VideoFrame) -> av.VideoFrame:
        self.graph.push(frame)
        ret = self.graph.pull()
        ret.pts = None
        return ret


def to_rgba(reader: Iterator[av.VideoFrame]):
    formatter: dict[str, _Formatter] = {}

    for frame in reader:
        if frame.format.name not in formatter:
            formatter[frame.format.name] = _Formatter(
                frame.width, frame.height, frame.format.name, "rgba"
            )

        yield formatter[frame.format.name](frame)

    for f in formatter.values():
        f.close()


def to_array(iterator: list[av.VideoFrame]):
    for frame in iterator:
        yield frame.to_ndarray()


class _AlphaExtractor(Filter):
    def __init__(self, width: int, height: int, pix_fmt: str):
        super().__init__()
        src = self.graph.add_buffer(
            width=width,
            height=height,
            format=pix_fmt,
            time_base=fractions.Fraction(1, 1000),
        )

        alphaextract = self.graph.add("alphaextract")
        src.link_to(alphaextract)

        alpha = self.graph.add("buffersink")
        alphaextract.link_to(alpha)

        self.graph.configure()

    def __call__(self, frame: av.VideoFrame):
        self.graph.push(frame)
        return self.graph.pull()


class AlphaExtractor:
    def __init__(self, width: int, height: int):
        assert height % 2 == 0

        self.rgba = _AlphaExtractor(width, height, "rgba")
        self.yuva420p = _AlphaExtractor(width, height, "yuva420p")

    def __call__(self, frame: av.VideoFrame):
        if frame.format.name == "rgba":
            return self.rgba(frame)
        elif frame.format.name == "yuva420p":
            return self.yuva420p(frame)
        else:
            raise NotImplementedError

    def close(self):
        self.rgba.close()
        self.yuva420p.close()


class BaseAlphaMerger:
    @abstractmethod
    def push_image(self, frame: av.VideoFrame):
        """push image to merger"""

    @abstractmethod
    def push_alpha(self, frame: av.VideoFrame):
        """push alpha to merger"""

    @abstractmethod
    def pull(self):
        """pull merged image"""


class AlphaMerger(Filter, BaseAlphaMerger):
    def __init__(self, template1: av.VideoStream, template2: av.VideoStream):
        super().__init__()

        self.image = self.graph.add_buffer(template=template1)
        self.alpha = self.graph.add_buffer(template=template2)
        format = self.graph.add("format", "gray")
        self.alpha.link_to(format)

        alphamerge = self.graph.add("alphamerge")
        self.image.link_to(alphamerge, input_idx=0)
        format.link_to(alphamerge, input_idx=1)

        self.result = self.graph.add("buffersink")
        alphamerge.link_to(self.result)

        self.graph.configure()

    def push_image(self, frame: av.VideoFrame):
        self.image.push(frame)

    def push_alpha(self, frame: av.VideoFrame):
        self.alpha.push(frame)

    def pull(self) -> av.VideoFrame:
        try:
            return self.graph.pull()
        except BlockingIOError:
            return None


class NotAlphaMerger(BaseAlphaMerger):
    def __init__(self):
        self.queue = deque()

    def push_image(self, frame: av.VideoFrame):
        self.queue.append(frame)

    def push_alpha(self, frame: av.VideoFrame):
        raise NotImplementedError

    def pull(self) -> av.VideoFrame:
        try:
            return self.queue.popleft()
        except IndexError:
            return None


def get_dst_size(dst_size: tuple[int, int], background_image: np.ndarray):
    target_height, target_width = background_image.shape[:2]

    width, height = dst_size
    if target_height / height < target_width / width:
        width = round(target_height / height * width)
        height = target_height
    else:
        height = round(target_width / width * height)
        width = target_width

    width, height = width - width % 16, height - height % 16

    bg_top = (target_height - height) // 2
    bg_left = (target_width - width) // 2

    return (width, height), background_image[
        bg_top : bg_top + height, bg_left : bg_left + width, :
    ]


def get_src_size(
    left: float,
    top: float,
    height: float,
    dst_size: tuple[int, int],
    src_size: tuple[int, int],
):
    dst_width, dst_height = dst_size
    src_width, src_height = src_size

    target_frame_height = dst_height * height
    frame_width = min(
        round(src_width * target_frame_height / src_height),
        dst_width,
    )
    frame_height = round(src_height * frame_width / src_width)

    left = (left + 1) / 2
    left_limit = dst_width - frame_width

    x = round(left * left_limit)
    y = round(top * dst_height)

    return (x, y), (frame_width, frame_height)


class BaseOverlayer(Filter):
    def __init__(
        self,
        background_image: np.ndarray,
        x: int,
        y: int,
        w: int,
        h: int,
        pix_fmt: str = "yuva420p",
        mode: str = "straight",
        pre_overlay_filter: Callable[
            [av.filter.Graph, av.filter.context.FilterContext],
            av.filter.context.FilterContext,
        ] = lambda g, f: f,
        post_overlay_filter: Callable[
            [av.filter.Graph, av.filter.context.FilterContext],
            av.filter.context.FilterContext,
        ] = lambda g, f: f,
    ):
        super().__init__()
        self.pre_overlay_filter = pre_overlay_filter
        self.post_overlay_filter = post_overlay_filter

        self.background_image = av.VideoFrame.from_ndarray(
            background_image,
            format="rgb24" if background_image.shape[-1] == 3 else "rgba",
        )

        self.src = self.graph.add_buffer(
            width=w,
            height=h,
            format=pix_fmt,
            time_base=fractions.Fraction(1, 1000),
        )
        self.dst = self.graph.add_buffer(
            width=self.background_image.width,
            height=self.background_image.height,
            format=self.background_image.format.name,
            time_base=fractions.Fraction(1, 1000),
        )

        pre_filtered = self.pre_overlay_filter(self.graph, self.src)

        overlay = self.graph.add("overlay", f"x={x}:y={y}:alpha={mode}:format=auto")
        self.dst.link_to(overlay, input_idx=0)
        pre_filtered.link_to(overlay, input_idx=1)

        format = self.graph.add("format", pix_fmt)
        overlay.link_to(format)

        post_filtered = self.post_overlay_filter(self.graph, format)

        sink = self.graph.add("buffersink")
        post_filtered.link_to(sink)

        self.graph.configure()

    def paste(self, src_image):
        src_image.pts = None
        self.src.push(src_image)
        self.dst.push(self.background_image)
        ret = self.graph.pull()
        ret.pts = None
        return ret

    def paste_video(self, iterator: list[av.VideoFrame]):
        for it in iterator:
            yield self.paste(it)
        self.close()

    @property
    def width(self):
        return self.background_image.width

    @property
    def height(self):
        return self.background_image.height


class Overlayer(BaseOverlayer):
    def __init__(
        self,
        background_image: np.ndarray,
        dst_size: tuple[int, int],
        src_size: tuple[int, int],
        left=0.0,
        top=0.0,
        height=1.0,
        pix_fmt: str = "yuva420p",
        mode: str = "straight",
    ):
        origin_src_size = src_size
        dst_size, background_image = get_dst_size(dst_size, background_image)
        src_pos, src_size = get_src_size(left, top, height, dst_size, src_size)

        self.src_size = src_size

        super().__init__(
            background_image,
            x=src_pos[0],
            y=src_pos[1],
            w=origin_src_size[0],
            h=origin_src_size[1],
            pix_fmt=pix_fmt,
            mode=mode,
            pre_overlay_filter=self._pre_overlay_filter,
        )

    def _pre_overlay_filter(
        self, graph: av.filter.Graph, context: av.filter.context.FilterContext
    ) -> av.filter.context.FilterContext:
        scale = graph.add("scale", f"{self.src_size[0]}:{self.src_size[1]}")
        context.link_to(scale)
        return scale


class AsyncDecoder:
    def __init__(self, aiterator: AsyncIterator[bytes], **kwargs):
        self._aiterator = aiterator
        self._f = PopIO()
        self._kwargs = kwargs

    def decode(self) -> AsyncIterator[av.VideoFrame | av.AudioFrame]:
        async def _pull():
            try:
                async for it in self._aiterator:
                    self._f.write(it)
            finally:
                self._f.close()

        pull_task = asyncio.create_task(_pull())

        def _decode():
            try:
                yield from PyAVReader(self._f, **self._kwargs)
            finally:
                if pull_task.done():
                    pull_task.result()
                else:
                    pull_task.cancel()

        return aprefetch_iterator(_decode())


class AsyncEncoder:
    def __init__(self, writer: PyAVWriter):
        self._writer = writer
        self._f = PopIO()
        writer.lazy_register_path(self._f)

    async def encode(self, frame: av.VideoFrame | av.AudioFrame):
        if isinstance(frame, av.VideoFrame):
            await run_in_threadpool(self._writer.write_video_frame_lazy, frame)
        elif isinstance(frame, av.AudioFrame):
            await run_in_threadpool(self._writer.write_audio_frame_lazy, frame)
        else:
            raise NotImplementedError

    async def aclose(self):
        await run_in_threadpool(self._writer.__exit__, None, None, None)
        await run_in_threadpool(self._f.close)

    def __aiter__(self):
        return self

    async def __anext__(self):
        if ret := await run_in_threadpool(self._f.read):
            return ret
        else:
            raise StopAsyncIteration
