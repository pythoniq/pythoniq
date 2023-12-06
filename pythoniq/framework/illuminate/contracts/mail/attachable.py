from pythoniq.framework.illuminate.mail.attachment import Attachment


class Attachable:
    # Get an attachment instance for this entity.
    def toMailAttachment(self) -> Attachment:
        pass
