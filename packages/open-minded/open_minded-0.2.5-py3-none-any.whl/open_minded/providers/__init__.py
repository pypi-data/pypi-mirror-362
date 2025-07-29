import random

from open_minded.providers.base import LlmApiProvider
from open_minded.providers.pollinations import PollinationsProvider
from open_minded.providers.deepai import DeepAiProvider


PROVIDER_CLASSES: list[type[LlmApiProvider]] = [DeepAiProvider, PollinationsProvider]


def get_provider_classes_shuffled():
    new_provider_classes = PROVIDER_CLASSES.copy()

    for provider_index in range(len(new_provider_classes)):
        provider_to_swap_index = random.randint(0, provider_index)
        (
            new_provider_classes[provider_index],
            new_provider_classes[provider_to_swap_index],
        ) = (
            new_provider_classes[provider_to_swap_index],
            new_provider_classes[provider_index],
        )

    return new_provider_classes
