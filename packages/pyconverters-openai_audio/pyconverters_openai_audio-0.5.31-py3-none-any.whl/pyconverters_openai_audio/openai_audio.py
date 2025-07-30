import os
from enum import Enum
from logging import Logger
from typing import List, cast, Type, Dict, Any

import filetype as filetype
import requests
from pydantic import Field, BaseModel
from pymultirole_plugins.v1.converter import ConverterParameters, ConverterBase
from pymultirole_plugins.v1.schema import Document
from starlette.datastructures import UploadFile

from .openai_utils import NO_DEPLOYED_MODELS, \
    create_asr_model_enum, set_openai

logger = Logger("pymultirole")


class OpenAIAudioBaseParameters(ConverterParameters):
    model_str: str = Field(
        None, extra="internal"
    )
    model: str = Field(
        None, extra="internal"
    )
    language: str = Field(
        None,
        description="""The language of the input audio. Supplying the input language in ISO-639-1 format will improve accuracy and latency""",
    )
    prompt: str = Field(
        None,
        description="""An optional text to guide the model's style or continue a previous audio segment. The prompt should match the audio language.""",
        extra="multiline,advanced",
    )
    temperature: float = Field(
        0.0,
        description="""The sampling temperature, between 0 and 1. Higher values like 0.8 will make the output more 
        random, while lower values like 0.2 will make it more focused and deterministic. If set to 0, the model will 
        use log probability to automatically increase the temperature until certain thresholds are hit.""",
        extra="advanced",
    )


class OpenAIAudioModel(str, Enum):
    whisper_1 = "whisper-1"


class OpenAIAudioParameters(OpenAIAudioBaseParameters):
    model: OpenAIAudioModel = Field(
        OpenAIAudioModel.whisper_1,
        description="""The [OpenAI model](https://platform.openai.com/docs/models) used for speech to text transcription. Options currently available:</br>
                        <li>`whisper-1` - state-of-the-art open source large-v2 Whisper model.
                        """, extra="pipeline-naming-hint"
    )


DEEPINFRA_PREFIX = "DEEPINFRA_"
DEEPINFRA_ASR_MODEL_ENUM, DEEPINFRA_DEFAULT_ASR_MODEL = create_asr_model_enum('DeepInfraAudioModel',
                                                                              prefix=DEEPINFRA_PREFIX)


class DeepInfraOpenAIAudioParameters(OpenAIAudioBaseParameters):
    model: DEEPINFRA_ASR_MODEL_ENUM = Field(
        None,
        description="""The [DeepInfra 'OpenAI compatible' model](https://deepinfra.com/models?type=automatic-speech-recognition) used for speech to text transcription. It must be deployed on your [DeepInfra dashboard](https://deepinfra.com/dash).
                        """, extra="pipeline-naming-hint"
    )


AZURE_PREFIX = "AZURE_"


class AzureOpenAIAudioParameters(OpenAIAudioBaseParameters):
    model: OpenAIAudioModel = Field(
        OpenAIAudioModel.whisper_1,
        description="""The [Azure OpenAI model](https://platform.openai.com/docs/models) used for speech to text transcription. Options currently available:</br>
                        <li>`whisper-1` - state-of-the-art open source large-v2 Whisper model.
                        """, extra="pipeline-naming-hint"
    )


class OpenAIAudioConverterBase(ConverterBase):
    __doc__ = """Generate text using [OpenAI Text Completion](https://platform.openai.com/docs/guides/completion) API
    You input some text as a prompt, and the model will generate a text completion that attempts to match whatever context or pattern you gave it."""
    PREFIX: str = ""

    def compute_args(self, params: OpenAIAudioBaseParameters, prompt: str
                     ) -> Dict[str, Any]:
        kwargs = {
            'model': params.model_str,
            'language': params.language,
            'prompt': prompt,
            'temperature': params.temperature,
            'response_format': 'text',
        }
        return kwargs

    def convert(self, source: UploadFile, parameters: ConverterParameters) \
            -> List[Document]:

        params: OpenAIAudioBaseParameters = cast(
            OpenAIAudioBaseParameters, parameters
        )
        OPENAI_MODEL = os.getenv(self.PREFIX + "OPENAI_MODEL", None)
        if OPENAI_MODEL:
            params.model_str = OPENAI_MODEL

        kind = filetype.guess(source.file)
        source.file.seek(0)
        doc: Document = None
        if kind is not None and kind.mime.startswith('audio') or kind.mime.startswith('video'):
            kwargs = self.compute_args(params, params.prompt)
            if kwargs['model'] != NO_DEPLOYED_MODELS:
                try:
                    result = self.compute_result(source, **kwargs)
                    doc = Document(identifier=source.filename,
                                   text=result)
                    doc.properties = {"fileName": source.filename}
                except BaseException as err:
                    raise err
        if doc is None:
            raise TypeError(f"Conversion of audio file {source.filename} failed")
        return [doc]

    @classmethod
    def get_model(cls) -> Type[BaseModel]:
        return OpenAIAudioBaseParameters


class OpenAIAudioConverter(OpenAIAudioConverterBase):
    __doc__ = """Convert audio using [OpenAI Audio](https://platform.openai.com/docs/guides/speech-to-text) API"""

    def convert(self, source: UploadFile, parameters: ConverterParameters) \
            -> List[Document]:
        params: OpenAIAudioParameters = cast(
            OpenAIAudioParameters, parameters
        )
        params.model_str = params.model.value
        return super().convert(source, params)

    def compute_result(self, source: UploadFile, **kwargs):
        client = set_openai(self.PREFIX)
        kwargs['file'] = (source.filename, source.file, source.content_type)
        response = client.audio.transcriptions.create(**kwargs)
        return response

    @classmethod
    def get_model(cls) -> Type[BaseModel]:
        return OpenAIAudioParameters


class AzureOpenAIAudioConverter(OpenAIAudioConverterBase):
    __doc__ = """Convert audio using [Azure OpenAI Audio](https://platform.openai.com/docs/guides/speech-to-text) API"""
    PREFIX = AZURE_PREFIX

    def convert(self, source: UploadFile, parameters: ConverterParameters) \
            -> List[Document]:
        params: DeepInfraOpenAIAudioParameters = cast(
            DeepInfraOpenAIAudioParameters, parameters
        )
        params.model_str = params.model.value
        return super().convert(source, params)

    def compute_result(self, source: UploadFile, **kwargs):
        client = set_openai(self.PREFIX)
        kwargs['file'] = (source.filename, source.file, source.content_type)
        response = client.audio.transcriptions.create(**kwargs)
        return response

    @classmethod
    def get_model(cls) -> Type[BaseModel]:
        return OpenAIAudioParameters


class DeepInfraOpenAIAudioConverter(OpenAIAudioConverterBase):
    __doc__ = """Convert audio using [DeepInfra Audio](https://deepinfra.com/docs/tutorials/whisper) API"""
    PREFIX = DEEPINFRA_PREFIX

    def convert(self, source: UploadFile, parameters: ConverterParameters) \
            -> List[Document]:
        params: DeepInfraOpenAIAudioParameters = cast(
            DeepInfraOpenAIAudioParameters, parameters
        )
        params.model_str = params.model.value
        return super().convert(source, params)

    def compute_result(self, source: UploadFile, **kwargs):
        client = set_openai(self.PREFIX)
        deepinfra_url = client.base_url
        inference_url = f"{deepinfra_url.scheme}://{deepinfra_url.host}/v1/inference/{kwargs['model']}"
        response = requests.post(inference_url,
                                 files={'audio': (source.filename, source.file, source.content_type)},
                                 data={
                                     "task": "transcribe",
                                     "language": kwargs['language'],
                                     "temperature": kwargs['temperature'],
                                     "initial_prompt": kwargs['prompt']
                                 },
                                 headers={'Accept': "application/json", 'Authorization': f"Bearer {client.api_key}"})
        if response.ok:
            result = response.json()
            return result['text']

    @classmethod
    def get_model(cls) -> Type[BaseModel]:
        return DeepInfraOpenAIAudioParameters
