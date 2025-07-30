import os
from enum import Enum
from functools import lru_cache
from logging import Logger
from time import sleep
from typing import List, cast, Type

import requests
import yaml
from pydantic import Field, BaseModel
from pymultirole_plugins.v1.converter import ConverterParameters, ConverterBase
from pymultirole_plugins.v1.schema import Document, Sentence
from starlette.datastructures import UploadFile

logger = Logger("pymultirole")
WHISPERX_URL = os.getenv(
    "WHISPERX_URL", None
)


class InputFormat(str, Enum):
    YamlFile = "YamlFile"


class WhisperXParameters(ConverterParameters):
    whisperx_url: str = Field(
        WHISPERX_URL,
        description="""WhisperX server base url.""",
    )
    input_format: InputFormat = Field(
        InputFormat.YamlFile,
        description="""Format of the input file.""",
    )
    language: str = Field(
        None,
        description="""Optional language of the audio file."""
    )
    initial_prompt: str = Field(
        None,
        description="""Optional text to provide as a prompt for the first window.""",
        extra="advanced",
    )
    temperature: float = Field(
        0,
        description="Temperature to use for sampling",
        extra="advanced",
    )
    batch_size: int = Field(
        32,
        description="Parallelization of input audio transcription",
        extra="advanced",
    )
    align_output: bool = Field(
        True,
        description="Aligns whisper output to get accurate word-level timestamps",
        extra="advanced",
    )
    diarization: bool = Field(
        True, description="Assign speaker ID labels", extra="advanced"
    )

    group_adjacent_speakers: bool = Field(
        False,
        description="Group adjacent segments with same speakers",
        extra="advanced",
    )
    min_speakers: int = Field(
        0,
        description="Minimum number of speakers if diarization is activated (leave blank if unknown)",
        extra="advanced",
    )
    max_speakers: int = Field(
        0,
        description="Maximum number of speakers if diarization is activated (leave blank if unknown)",
        extra="advanced",
    )
    return_embeddings: bool = Field(
        False,
        description="Return representative speaker embeddings",
        extra="advanced",
    )


class WhisperXConverter(ConverterBase):
    """WhisperX converter ."""

    def convert(
        self, source: UploadFile, parameters: ConverterParameters
    ) -> List[Document]:
        params: WhisperXParameters = cast(WhisperXParameters, parameters)
        client = get_client(params.whisperx_url)
        if params.input_format == InputFormat.YamlFile:
            config = yaml.safe_load(source.file)

            bean = client.transcribe(config["url"], params)
            text = ""
            sentences = []
            for seg in bean["result"]["segments"]:
                speaker = seg.get("speaker", "SPEAKER_UNKNOWN")
                start = len(text)
                text = text + f"[{speaker}]: " + seg["text"] + "\n"
                end = len(text)
                sent = Sentence(
                    start=start,
                    end=end,
                    metadata={
                        "speaker": speaker,
                        "timecode": f"{seg['start']}:{seg['end']}",
                    },
                )
                sentences.append(sent)
            metadata = config.get("metadata", {})
            metadata['url'] = config["url"]
            doc = Document(
                identifier=config["url"],
                title=config.get("title", config["url"]),
                text=text,
                sentences=sentences,
                metadata=config.get("metadata", None),
            )
            return [doc]
        return [None]

    @classmethod
    def get_model(cls) -> Type[BaseModel]:
        return WhisperXParameters


@lru_cache(maxsize=None)
def get_client(base_url):
    client = WhisperXClient(base_url)
    return client


def is_success(job_bean):
    return job_bean and job_bean["status"] == "COMPLETED"


class WhisperXClient:
    def __init__(self, base_url):
        self.base_url = base_url[0:-1] if base_url.endswith("/") else base_url
        self.dsession = requests.Session()
        self.dsession.headers.update({"Accept": "application/json"})
        self.dsession.verify = False

    def transcribe(self, url: str, params: WhisperXParameters):
        try:
            resp = self.dsession.post(
                f"{self.base_url}/submit",
                json={
                    "options": {
                        "audio_url": url,
                        "language": params.language,
                        "initial_prompt": params.initial_prompt,
                        "temperature": params.temperature,
                        "batch_size": params.batch_size,
                        "align_output": params.align_output,
                        "diarization": params.diarization,
                        "group_adjacent_speakers": params.group_adjacent_speakers,
                        "min_speakers": params.min_speakers,
                        "max_speakers": params.max_speakers,
                        "return_embeddings": params.return_embeddings,
                    }
                },
                timeout=300,
            )
            if resp.ok:
                job_bean = resp.json()
                job_bean = self.wait_for_completion(job_bean)
                if is_success(job_bean):
                    return job_bean
                else:
                    logger.warning("Unsuccessful transcription: {url}")
                    resp.raise_for_status()
            else:
                logger.warning("Unsuccessful transcription: {url}")
                resp.raise_for_status()
        except BaseException as err:
            logger.warning("An exception was thrown!", exc_info=True)
            raise err

    def wait_for_completion(self, job_bean):
        if job_bean:
            while job_bean["status"] not in [
                "COMPLETED",
                "CANCELLED",
                "FAILED",
            ]:
                sleep(10)
                resp = self.dsession.get(f"{self.base_url}/status/{job_bean['uid']}")
                if resp.ok:
                    job_bean = resp.json()
                else:
                    logger.warning(
                        "Impossible to retrieve status of job: {job_bean['uid']}"
                    )
                    resp.raise_for_status()
        return job_bean
