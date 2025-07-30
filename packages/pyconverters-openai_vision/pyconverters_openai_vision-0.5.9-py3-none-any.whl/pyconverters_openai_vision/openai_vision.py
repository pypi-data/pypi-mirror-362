import base64
import os
import re
from enum import Enum
from logging import Logger
from re import Pattern
from typing import List, cast, Type, Dict, Any

import filetype as filetype
from pydantic import Field, BaseModel
from pymultirole_plugins.v1.converter import ConverterParameters, ConverterBase
from pymultirole_plugins.v1.schema import Document
from starlette.datastructures import UploadFile

from .openai_utils import NO_DEPLOYED_MODELS, \
    openai_chat_completion, create_openai_model_enum

logger = Logger("pymultirole")


class OpenAIVisionBaseParameters(ConverterParameters):
    model_str: str = Field(
        None, extra="internal"
    )
    model: str = Field(
        None, extra="internal"
    )
    prompt: str = Field(
        """If the attached file is an image: describe the image with a lot of details.",
        If the attached file is a PDF document: convert the PDF document into Markdown format. The output must be just the markdown result without any explanation or introductory prefix.""",
        description="""Contains the prompt as a string""",
        extra="multiline",
    )
    max_tokens: int = Field(
        16384,
        description="""The maximum number of tokens to generate in the completion.
    The token count of your prompt plus max_tokens cannot exceed the model's context length.
    Most models have a context length of 2048 tokens (except for the newest models, which support 4096).""",
    )
    system_prompt: str = Field(
        None,
        description="""Contains the system prompt""",
        extra="multiline,advanced",
    )
    temperature: float = Field(
        1.0,
        description="""What sampling temperature to use, between 0 and 2.
    Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic.
    We generally recommend altering this or `top_p` but not both.""",
        extra="advanced",
    )
    top_p: int = Field(
        1,
        description="""An alternative to sampling with temperature, called nucleus sampling, where the model considers the results of the tokens with top_p probability mass.
    So 0.1 means only the tokens comprising the top 10% probability mass are considered.
    We generally recommend altering this or `temperature` but not both.""",
        extra="advanced",
    )
    n: int = Field(
        1,
        description="""How many completions to generate for each prompt.
    Note: Because this parameter generates many completions, it can quickly consume your token quota.
    Use carefully and ensure that you have reasonable settings for `max_tokens`.""",
        extra="advanced",
    )
    best_of: int = Field(
        1,
        description="""Generates best_of completions server-side and returns the "best" (the one with the highest log probability per token).
    Results cannot be streamed.
    When used with `n`, `best_of` controls the number of candidate completions and `n` specifies how many to return – `best_of` must be greater than `n`.
    Use carefully and ensure that you have reasonable settings for `max_tokens`.""",
        extra="advanced",
    )
    presence_penalty: float = Field(
        0.0,
        description="""Number between -2.0 and 2.0.
    Positive values penalize new tokens based on whether they appear in the text so far, increasing the model's likelihood to talk about new topics.""",
        extra="advanced",
    )
    frequency_penalty: float = Field(
        0.0,
        description="""Number between -2.0 and 2.0.
    Positive values penalize new tokens based on their existing frequency in the text so far, decreasing the model's likelihood to repeat the same line verbatim.""",
        extra="advanced",
    )


class OpenAIVisionModel(str, Enum):
    gpt_4o_mini = "gpt-4o-mini"
    gpt_4o = "gpt-4o"
    o3_mini = "o3-mini"


class OpenAIVisionParameters(OpenAIVisionBaseParameters):
    model: OpenAIVisionModel = Field(
        OpenAIVisionModel.gpt_4o_mini,
        description="""The [OpenAI model](https://platform.openai.com/docs/models) used for vision. Options currently available:</br>

                        """, extra="pipeline-naming-hint"
    )


DEEPINFRA_PREFIX = "DEEPINFRA_"
DEEPINFRA_VISION_MODEL_ENUM, DEEPINFRA_DEFAULT_VISION_MODEL = create_openai_model_enum('DeepInfraVisionModel',
                                                                                       prefix=DEEPINFRA_PREFIX)


class DeepInfraOpenAIVisionParameters(OpenAIVisionBaseParameters):
    model: DEEPINFRA_VISION_MODEL_ENUM = Field(
        None,
        description="""The [DeepInfra 'OpenAI compatible' model](https://deepinfra.com/models?type=automatic-speech-recognition) used for speech to text transcription. It must be deployed on your [DeepInfra dashboard](https://deepinfra.com/dash).
                         """, extra="pipeline-naming-hint"
    )


# AZURE_PREFIX = "AZURE_"
#
#
# class AzureOpenAIVisionParameters(OpenAIVisionBaseParameters):
#     model: OpenAIVisionModel = Field(
#         OpenAIVisionModel.whisper_1,
#         description="""The [Azure OpenAI model](https://platform.openai.com/docs/models) used for speech to text transcription. Options currently available:</br>
#                         <li>`whisper-1` - state-of-the-art open source large-v2 Whisper model.
#                         """, extra="pipeline-naming-hint"
#     )


class OpenAIVisionConverterBase(ConverterBase):
    __doc__ = """Generate text using [OpenAI Text Completion](https://platform.openai.com/docs/guides/completion) API
    You input some text as a prompt, and the model will generate a text completion that attempts to match whatever context or pattern you gave it."""
    PREFIX: str = ""

    def compute_args(self, params: OpenAIVisionBaseParameters, source: UploadFile, kind
                     ) -> Dict[str, Any]:
        data = source.file.read()
        rv = base64.b64encode(data)
        if kind.mime.startswith("image"):
            binary_block = {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{rv.decode('utf-8')}"
                }
            }
        else:
            binary_block = {
                "type": "file",
                "file": {
                    "filename": source.filename,
                    "file_data": f"data:application/pdf;base64,{rv.decode('utf-8')}"}
            }
        messages = [{"role": "system", "content": params.system_prompt}] if params.system_prompt is not None else []
        messages.append({"role": "user",
                         "content": [
                             {
                                 "type": "text",
                                 "text": params.prompt
                             },
                             binary_block
                         ]})
        kwargs = {
            'model': params.model_str,
            'messages': messages,
            'max_tokens': params.max_tokens,
            'temperature': params.temperature,
            'top_p': params.top_p,
            'n': params.n,
            'frequency_penalty': params.frequency_penalty,
            'presence_penalty': params.presence_penalty,
        }
        return kwargs

    def compute_result(self, **kwargs):
        pattern: Pattern = re.compile(r"```(?:markdown\s+)?(\W.*?)```", re.DOTALL)
        """Regex pattern to parse the output."""
        response = openai_chat_completion(self.PREFIX, **kwargs)
        contents = []
        for choice in response.choices:
            if choice.message.content:
                if "```" in choice.message.content:
                    action_match = pattern.search(choice.message.content)
                    if action_match is not None:
                        contents.append(action_match.group(1).strip())
                else:
                    contents.append(choice.message.content)
        if contents:
            result = "\n".join(contents)
        return result

    def convert(self, source: UploadFile, parameters: ConverterParameters) \
            -> List[Document]:

        params: OpenAIVisionBaseParameters = cast(
            OpenAIVisionBaseParameters, parameters
        )
        OPENAI_MODEL = os.getenv(self.PREFIX + "OPENAI_MODEL", None)
        if OPENAI_MODEL:
            params.model_str = OPENAI_MODEL
        doc = None
        try:
            kind = filetype.guess(source.file)
            source.file.seek(0)
            if kind.mime.startswith("image") or kind.mime.endswith("pdf"):
                result = None
                kwargs = self.compute_args(params, source, kind)
                if kwargs['model'] != NO_DEPLOYED_MODELS:
                    result = self.compute_result(**kwargs)
                if result:
                    doc = Document(identifier=source.filename, text=result)
                    doc.properties = {"fileName": source.filename}
        except BaseException as err:
            raise err
        if doc is None:
            raise TypeError(f"Conversion of file {source.filename} failed")
        return [doc]

    @classmethod
    def get_model(cls) -> Type[BaseModel]:
        return OpenAIVisionBaseParameters


class OpenAIVisionConverter(OpenAIVisionConverterBase):
    __doc__ = """Convert audio using [OpenAI Audio](https://platform.openai.com/docs/guides/speech-to-text) API"""

    def convert(self, source: UploadFile, parameters: ConverterParameters) \
            -> List[Document]:
        params: OpenAIVisionParameters = cast(
            OpenAIVisionParameters, parameters
        )
        params.model_str = params.model.value
        return super().convert(source, params)

    @classmethod
    def get_model(cls) -> Type[BaseModel]:
        return OpenAIVisionParameters


class DeepInfraOpenAIVisionConverter(OpenAIVisionConverterBase):
    __doc__ = """Convert images using [DeepInfra Vision](https://deepinfra.com/docs/tutorials/whisper) API"""
    PREFIX = DEEPINFRA_PREFIX

    def convert(self, source: UploadFile, parameters: ConverterParameters) \
            -> List[Document]:
        params: DeepInfraOpenAIVisionParameters = cast(
            DeepInfraOpenAIVisionParameters, parameters
        )
        params.model_str = params.model.value
        return super().convert(source, params)

    @classmethod
    def get_model(cls) -> Type[BaseModel]:
        return DeepInfraOpenAIVisionParameters
