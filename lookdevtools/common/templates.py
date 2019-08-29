"""
.. module:: templates
   :synopsis: File naming templates.

.. moduleauthor:: Ezequiel Mastrasso

"""
from lookdevtools.external import lucidity
from lookdevtools.common.constants import TEXTURESET_ELEMENT_PATTERN
from lookdevtools.common.constants import TEXTURESET_MATCHING_RATIO
from lookdevtools.common.constants import TEXTURESET_ELEMENT_MATCHING_RATIO

#: Texture file lucidity template using TEXTURESET_ELEMENT_PATTERN
texture_file_template = lucidity.Template(
            'textureset_element',
            TEXTURESET_ELEMENT_PATTERN,
            anchor=lucidity.Template.ANCHOR_END
            # TODO (Eze) Add STRICT?
            )

def custom_texture_file_template(custom_pattern=None):
    """
    Get a lucidity Template object using a custom template

    Kwargs:
       custom_pattern (str):  Custom lucidity file pattern.

    Returns:
        lucity.Template object with the custom partern
    """
    texture_file_template = lucidity.Template(
        'textureset_element',
        custom_pattern,
        anchor=lucidity.Template.ANCHOR_END
        # TODO (Eze) Add STRICT?
        )
    return texture_file_template