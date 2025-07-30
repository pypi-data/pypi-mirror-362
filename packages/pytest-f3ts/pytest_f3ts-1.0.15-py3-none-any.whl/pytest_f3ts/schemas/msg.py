from pydantic import BaseModel


class Msg(BaseModel):
    msg: str


class Dialog(BaseModel):
    title: str = "INFO:"
    message: str = " Enter dialog message here"
    okButtonText: str = "OK"
    cancelButtonText: str = "Cancel"
    inputType: str = None
    defaultText: str = ""


class Notif(BaseModel):
    title: str = "INFO:"
    message: str = " Enter notification message here"
    okButtonText: str = "OK"


class DialogResponse(BaseModel):
    inputText: str = ""
    okClicked: bool = False
    cancelClicked: bool = False


class StatusBanner(BaseModel):
    status: str = None
    color: str = None


class SocketMsg(BaseModel):
    type: str
    toClient: str
    fromClient: str
    data: dict = None
