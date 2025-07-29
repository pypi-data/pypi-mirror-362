from enum import Enum


class TemplateOrderField(Enum):
    """An enumeration representing different categories.

    :cvar TEMPLATEID: "TEMPLATE_ID"
    :vartype TEMPLATEID: str
    :cvar TEMPLATECREATIONDATE: "TEMPLATE_CREATION_DATE"
    :vartype TEMPLATECREATIONDATE: str
    :cvar TEMPLATEMODIFICATIONDATE: "TEMPLATE_MODIFICATION_DATE"
    :vartype TEMPLATEMODIFICATIONDATE: str
    :cvar TEMPLATENAME: "TEMPLATE_NAME"
    :vartype TEMPLATENAME: str
    """

    TEMPLATEID = "TEMPLATE_ID"
    TEMPLATECREATIONDATE = "TEMPLATE_CREATION_DATE"
    TEMPLATEMODIFICATIONDATE = "TEMPLATE_MODIFICATION_DATE"
    TEMPLATENAME = "TEMPLATE_NAME"

    def list():
        """Lists all category values.

        :return: A list of all category values.
        :rtype: list
        """
        return list(map(lambda x: x.value, TemplateOrderField._member_map_.values()))
