from pathlib import Path
from typing import List

import pytest
from pymultirole_plugins.v1.schema import Document
from starlette.datastructures import UploadFile

from pyconverters_openai_audio.openai_audio import (
    OpenAIAudioConverter,
    DeepInfraOpenAIAudioConverter, DeepInfraOpenAIAudioParameters, OpenAIAudioParameters, AzureOpenAIAudioParameters,
    AzureOpenAIAudioConverter
)


def test_openai_audio_basic():
    model = OpenAIAudioConverter.get_model()
    model_class = model.construct().__class__
    assert model_class == OpenAIAudioParameters

    model = DeepInfraOpenAIAudioConverter.get_model()
    model_class = model.construct().__class__
    assert model_class == DeepInfraOpenAIAudioParameters


@pytest.mark.skip(reason="Not a test")
def test_openai_en():
    converter = OpenAIAudioConverter()
    parameters = OpenAIAudioParameters(language='en')
    testdir = Path(__file__).parent
    source = Path(testdir, 'data/2.wav')
    with source.open("rb") as fin:
        docs: List[Document] = converter.convert(UploadFile(source.name, fin, 'audio/wav'), parameters)
        assert len(docs) == 1
        doc0 = docs[0]
        assert doc0.text.lower().startswith('on bed 7')

    source = Path(testdir, 'data/DRAFT Voice for Kairntech Intro Vincent Version 20220218.mp4')
    with source.open("rb") as fin:
        docs: List[Document] = converter.convert(UploadFile(source.name, fin, 'audio/mp4'), parameters)
        assert len(docs) == 1
        doc0 = docs[0]
        assert 'software' in doc0.text


@pytest.mark.skip(reason="Not a test")
def test_openai_fr():
    converter = OpenAIAudioConverter()
    parameters = OpenAIAudioParameters(language='fr')
    testdir = Path(__file__).parent
    source = Path(testdir, 'data/ae26ccf4-ea2b-4bc7-b112-9bdb00931577.webm')
    with source.open("rb") as fin:
        docs: List[Document] = converter.convert(UploadFile(source.name, fin, 'audio/webm'), parameters)
        assert len(docs) == 1
        doc0 = docs[0]
        assert 'personnes' in doc0.text

    source = Path(testdir, 'data/Terrorisme_1.m4a')
    with source.open("rb") as fin:
        docs: List[Document] = converter.convert(UploadFile(source.name, fin, 'audio/m4a'), parameters)
        assert len(docs) == 1
        doc0 = docs[0]
        assert 'attaque' in doc0.text


@pytest.mark.skip(reason="Not a test")
def test_deepinfra_en():
    converter = DeepInfraOpenAIAudioConverter()
    parameters = DeepInfraOpenAIAudioParameters(model="openai/whisper-large", language='en')
    testdir = Path(__file__).parent
    source = Path(testdir, 'data/2.wav')
    with source.open("rb") as fin:
        docs: List[Document] = converter.convert(UploadFile(source.name, fin, 'audio/wav'), parameters)
        assert len(docs) == 1
        doc0 = docs[0]
        assert 'on bed 7' in doc0.text.lower()

    source = Path(testdir, 'data/DRAFT Voice for Kairntech Intro Vincent Version 20220218.mp4')
    with source.open("rb") as fin:
        docs: List[Document] = converter.convert(UploadFile(source.name, fin, 'audio/mp4'), parameters)
        assert len(docs) == 1
        doc0 = docs[0]
        assert 'software' in doc0.text


@pytest.mark.skip(reason="Not a test")
def test_deepinfra_fr():
    converter = DeepInfraOpenAIAudioConverter()
    parameters = DeepInfraOpenAIAudioParameters(model="openai/whisper-large-v3-turbo", language='fr')
    testdir = Path(__file__).parent
    source = Path(testdir, 'data/ae26ccf4-ea2b-4bc7-b112-9bdb00931577.webm')
    with source.open("rb") as fin:
        docs: List[Document] = converter.convert(UploadFile(source.name, fin, 'audio/webm'), parameters)
        assert len(docs) == 1
        doc0 = docs[0]
        assert 'personnes' in doc0.text

    source = Path(testdir, 'data/Terrorisme_1.m4a')
    with source.open("rb") as fin:
        docs: List[Document] = converter.convert(UploadFile(source.name, fin, 'audio/m4a'), parameters)
        assert len(docs) == 1
        doc0 = docs[0]
        assert 'attaque' in doc0.text


@pytest.mark.skip(reason="Not a test")
def test_azure_openai_en():
    converter = AzureOpenAIAudioConverter()
    parameters = AzureOpenAIAudioParameters(language='en')
    testdir = Path(__file__).parent
    source = Path(testdir, 'data/2.wav')
    with source.open("rb") as fin:
        docs: List[Document] = converter.convert(UploadFile(source.name, fin, 'audio/wav'), parameters)
        assert len(docs) == 1
        doc0 = docs[0]
        assert doc0.text.lower().startswith('on bed 7')

    source = Path(testdir, 'data/DRAFT Voice for Kairntech Intro Vincent Version 20220218.mp4')
    with source.open("rb") as fin:
        docs: List[Document] = converter.convert(UploadFile(source.name, fin, 'audio/mp4'), parameters)
        assert len(docs) == 1
        doc0 = docs[0]
        assert 'software' in doc0.text
