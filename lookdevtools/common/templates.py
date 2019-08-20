from lookdevtools.external import lucidity
from lookdevtools.common.constants import TEXTURESET_ELEMENT_PATTERN
from lookdevtools.common.constants import TEXTURESET_MATCHING_RATIO
from lookdevtools.common.constants import TEXTURESET_ELEMENT_MATCHING_RATIO

texture_file_template = lucidity.Template(
            'textureset_element',
            TEXTURESET_ELEMENT_PATTERN,
            anchor=lucidity.Template.ANCHOR_END
            # Add STRICT?
            )

def custom_texture_file_template(custom_pattern=None):
    """Get a lucidity Template object using a custom template"""
    if custom_pattern:
        texture_file_template = lucidity.Template(
            'textureset_element',
            custom_pattern,
            anchor=lucidity.Template.ANCHOR_END
            # Add STRICT?
            )
        return texture_file_template
    else:
        return None