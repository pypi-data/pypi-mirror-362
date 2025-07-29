from yta_validation.parameter import ParameterValidator
from dataclasses import dataclass


@dataclass
class DiscordConversationCharacter:

    def __init__(
        self,
        username: str,
        avatar_url: str
    ):
        ParameterValidator.validate_mandatory_string('username', username, do_accept_empty = False)
        ParameterValidator.validate_mandatory_string('avatar_url', avatar_url, do_accept_empty = False)
        
        # TODO: Check if 'avatar_url' is valid

        # TODO: Maybe if they don't provide this information we
        # could auto-generate it
        self.username = username
        self.avatar_url = avatar_url