from typing import Any, Literal, TypedDict, Union

from typing_extensions import Required


class ActionElementEvent(TypedDict, total=False):
    """
    ActionElementEvent.

    Notify the game about changes to an action element.
    """

    type: Required[Literal["ActionElementEvent"]]
    """


    Required property
    """

    actionElementId: Required[str]
    """
    The id of the action element

    Required property
    """

    value: str
    """ The current value of the action element """

    event: Required["_ActionElementEventevent"]
    """
    The event that happened

    Required property
    """


class ActivateMovementType(TypedDict, total=False):
    """
    ActivateMovementType.

    Ask the game to activate different movement modes.
    """

    type: Required[Literal["ActivateMovementType"]]
    """


    Required property
    """

    movementType: Required["_ActivateMovementTypemovementType"]
    """
    The movement mode to activate

    Required property
    """


class BusinessCard(TypedDict, total=False):
    """
    BusinessCard.

    Tell the game that the visitor profile data (business-card) has been updated. The entire JSON is blindly serialized and sent back to web by the game. OLDER VERSION (pre-March 2021): On a new connection, this also lets unreal know to spawn the player.

    deprecated: True
    """

    type: Required[Literal["BusinessCard"]]
    """


    Required property
    """

    firstName: Required[str]
    """
    The first name

    Required property
    """

    lastName: Required[str]
    """
    The last name

    Required property
    """

    email: Required[str]
    """
    The email

    Required property
    """

    city: Required[str]
    """
    The city

    Required property
    """

    avatarColor: Required["GameColor"]
    """
    GameColor.

    A representation of a color.

    Required property
    """

    avatarId: Required[str]
    """
    The avatar id

    Required property
    """

    customAvatarUrl: Required[str]
    """
    The url for the custom avatar (RPM)

    Required property
    """

    customAvatarPreviewImgUrl: Required[str]
    """
    A thumbnail image for the custom avatar

    Required property
    """

    company: Required[str]
    """
    The company

    Required property
    """

    orgCode: Required[str]
    """
    The org code

    Required property
    """

    country: Required[str]
    """
    The country

    Required property
    """

    website: Required[str]
    """
    The personal website link

    Required property
    """

    twitter: Required[str]
    """
    The twitter account link

    Required property
    """

    xing: Required[str]
    """
    The xing account link

    Required property
    """

    instagram: Required[str]
    """
    The instagram account link

    Required property
    """

    linkedin: Required[str]
    """
    The linkedin account link

    Required property
    """

    facebook: Required[str]
    """
    The facebook account link

    Required property
    """

    userEmail: Required[str]
    """
    The user email

    Required property
    """

    msTeamsEmail: Required[str]
    """
    The ms teams email

    Required property
    """

    guestEmail: Required[str]
    """
    The guest email

    Required property
    """

    age: Required[int | float]
    """
    The age

    Required property
    """

    environment: Required[str]
    """
    The environment id (to be confirmed)

    Required property
    """

    jobTitle: Required[str]
    """
    The job title

    Required property
    """

    playerId: Required[int | float]
    """
    Unique id of the player (photon)

    Required property
    """

    roomId: Required[str]
    """
    Unique id of the player's room (photon)

    Required property
    """


class ClientInfo(TypedDict, total=False):
    """
    ClientInfo.

    Information about the client (browser) sent to the game on connection.
    """

    type: Required[Literal["ClientInfo"]]
    """


    Required property
    """

    isTouchDevice: Required[bool]
    """
    Whether the client is a touch device

    Required property
    """

    langCode: str
    """ The language code of the client """

    userAgent: str
    """ The user agent of the client """

    webBackgroundColor: str
    """ A color for background panels that matches the web theme. To be used on in game UI elements (e.g. for the the avatar nameplate). """

    webTextColor: str
    """ A color for text that matches the web theme. To be used on in game UI elements (e.g. for the the avatar nameplate). """


class CustomMessage(TypedDict, total=False):
    """
    CustomMessage.

    The customest of messages
    """

    type: Required[Literal["CustomMessage"]]
    """


    Required property
    """

    messageType: Required[str]
    """


    Required property
    """

    data: Required[dict[str, Any]]
    """


    Required property
    """


class DeleteMessage(TypedDict, total=False):
    """
    DeleteMessage.

    Ask the game to delete a chat message.
    """

    type: Required[Literal["DeleteMessage"]]
    """


    Required property
    """

    userId: Required[int | float]
    """
    The id of the user to which the message belongs

    Required property
    """

    messageId: Required[int | float]
    """
    The id of the message to delete

    Required property
    """


class DidFakeTouch(TypedDict, total=False):
    """
    DidFakeTouch.

    Tell the game the first time a fake mouse event is (artificially) sent (when using fakeMouseWithTouch == true).
    """

    type: Required[Literal["DidFakeTouch"]]
    """


    Required property
    """


class EditingBusinessCard(TypedDict, total=False):
    """
    EditingBusinessCard.

    Tell the game that the profile panel (business-card) has been open/closed (this is normally used to adjust the camera view).

    deprecated: True
    """

    type: Required[Literal["EditingBusinessCard"]]
    """


    Required property
    """

    opened: Required[bool]
    """
    open/close

    Required property
    """


class GameColor(TypedDict, total=False):
    """
    GameColor.

    A representation of a color.
    """

    r: Required[int | float]
    """
    Red channel (0..255)

    minimum: 0
    maximum: 255

    Required property
    """

    g: Required[int | float]
    """
    Green channel (0..255)

    minimum: 0
    maximum: 255

    Required property
    """

    b: Required[int | float]
    """
    Blue channel (0..255)

    minimum: 0
    maximum: 255

    Required property
    """

    a: Required[int | float]
    """
    Alpha channel (0..255) ... sure?

    minimum: 0
    maximum: 255

    Required property
    """


class GetScreenSharingStatus(TypedDict, total=False):
    """
    GetScreenSharingStatus.

    Request the screen sharing status.
    """

    type: Required[Literal["GetScreenSharingStatus"]]
    """


    Required property
    """

    broadcast: Required[Literal[True]]
    """
    Broadcast to all users.

    Required property
    """


class LanguageSelected(TypedDict, total=False):
    """
    LanguageSelected.

    Tell the game that the client language has changed.
    """

    type: Required[Literal["LanguageSelected"]]
    """


    Required property
    """

    langCode: Required[str]
    """
    The language code of the client

    Required property
    """


class LoadExternalAsset(TypedDict, total=False):
    """
    LoadExternalAsset.

    Ask the game to load an external asset.
    """

    type: Required[Literal["LoadExternalAsset"]]
    """


    Required property
    """

    uri: Required[str]
    """
    Full asset URI (with protocol specified) that should be loaded

    Required property
    """

    provider: Required[str]
    """
    Asset provider ID (for example "readyplayerme" for ReadyPlayerMe, "journee" for Journee-hosted assets, etc.)

    Required property
    """

    intent: Required[str | dict[str, Any]]
    """
    Where the asset should be used (e.g. "customAvatar" to use as the model for the RPM custom avatar)

    Required property
    """


class MediaCaptureEvent(TypedDict, total=False):
    """
    MediaCaptureEvent.

    Notify the game about media capture progress.
    """

    type: Required[Literal["MediaCaptureEvent"]]
    """


    Required property
    """

    mediaType: Required["_MediaCaptureEventmediaType"]
    """
    The type of media being captured

    Required property
    """

    event: Required["_MediaCaptureEventevent"]
    """
    The state of the capture

    Required property
    """


class OnStartAction(TypedDict, total=False):
    """
    OnStartAction.

    Tell the world that the user made their first interaction which normally implies that: 1) They are ready to start playing 2) The login UI is fully dismissed 3) The audio stream is playing
    """

    type: Required[Literal["OnStartAction"]]
    """


    Required property
    """


class OnStreamIsShown(TypedDict, total=False):
    """
    OnStreamIsShown.

    Tell the game that the stream is now being displayed to the user.
    """

    type: Required[Literal["OnStreamIsShown"]]
    """


    Required property
    """


class PauseStream(TypedDict, total=False):
    """
    PauseStream.

    Ask the game to pause the stream.
    """

    type: Required[Literal["PauseStream"]]
    """


    Required property
    """


class PhotoCaptureEvent(TypedDict, total=False):
    """
    PhotoCaptureEvent.

    Tell the game about specific UI action related to the Photo Capture UI.

    deprecated: True
    """

    type: Required[Literal["PhotoCaptureEvent"]]
    """


    Required property
    """

    event: Required["_PhotoCaptureEventevent"]
    """


    Required property
    """


class PollResultSubmitted(TypedDict, total=False):
    """
    PollResultSubmitted.

    Notify the game that the user has submitted a poll.
    """

    type: Required[Literal["PollResultSubmitted"]]
    """


    Required property
    """

    slug: Required[str]
    """
    The slug of the poll.

    Required property
    """

    userId: Required[str]
    """
    The id of the visitor that submitted the poll.

    Required property
    """

    entries: Required[str]
    """
    The poll results.

    Required property
    """


class Reaction(TypedDict, total=False):
    """
    Reaction.

    Tell the game that the user has sent a reaction.
    """

    type: Required[Literal["Reaction"]]
    """


    Required property
    """

    reaction: Required[str]
    """
    The name of the reaction

    Required property
    """

    stage: int | float
    """ Stage of the reaction """

    playerId: Required[int | float]
    """
    Nakama id of the visitor

    Required property
    """

    roomId: Required[str]
    """
    Nakama room id the visitor belongs to

    Required property
    """

    broadcast: Required[Literal[True]]
    """
    Broadcast the reaction to all users.

    Required property
    """


class RequestQuestsInfo(TypedDict, total=False):
    """
    RequestQuestsInfo.

    Request the quests info.
    """

    type: Required[Literal["RequestQuestsInfo"]]
    """


    Required property
    """


class ResumeStream(TypedDict, total=False):
    """
    ResumeStream.

    Ask the game to resume the stream.
    """

    type: Required[Literal["ResumeStream"]]
    """


    Required property
    """


class ScreenSharing(TypedDict, total=False):
    """
    ScreenSharing.

    Communicate the screen sharing status.
    """

    type: Required[Literal["ScreenSharing"]]
    """


    Required property
    """

    participantId: Required[str]
    """
    The id of the participant sharing the screen.

    Required property
    """

    isSharing: Required[bool]
    """
    Whether the participant is sharing the screen.

    Required property
    """

    broadcast: Required[Literal[True]]
    """
    Broadcast to all users.

    Required property
    """


class ScreenSize(TypedDict, total=False):
    """
    ScreenSize.

    Tell the game that the size of the screen (the game video element on the web), both initially and on changes.
    """

    type: Required[Literal["ScreenSize"]]
    """


    Required property
    """

    w: Required[int | float]
    """
    Width of game video element (in web px, not real device pixels)

    Required property
    """

    h: Required[int | float]
    """
    Height of game video element (in web px, not real device pixels)

    Required property
    """

    croppedLeft: Required[int | float]
    """
    The left cropping of the game video from the game video element.

    Required property
    """

    croppedRight: Required[int | float]
    """
    The right cropping of the game video from the game video element.

    Required property
    """

    croppedTop: Required[int | float]
    """
    The top cropping of the game video from the game video element.

    Required property
    """

    croppedBottom: Required[int | float]
    """
    The bottom cropping of the game video from the game video element.

    Required property
    """


class SendChatMessage(TypedDict, total=False):
    """
    SendChatMessage.

    Tell the game that the user submitted a chat message in the chat input.
    """

    type: Required[Literal["SendChatMessage"]]
    """


    Required property
    """

    content: Required[str]
    """
    Content of the message

    Required property
    """


class SendEmoji(TypedDict, total=False):
    """
    SendEmoji.

    Ask the game to trigger an emoji dance (this might be coupled witht he emission of an emoji taxture above the avatar).
    """

    type: Required[Literal["SendEmoji"]]
    """


    Required property
    """

    emoji: Required[str]
    """
    The slug of the emoji

    Required property
    """


class SmartChatUserAction(TypedDict, total=False):
    """
    SmartChatUserAction.

    Tell the game that the user has done a specific action in relation to a smart chat.
    """

    type: Required[Literal["SmartChatUserAction"]]
    """


    Required property
    """

    smartChatSlug: Required[str]
    """
    The sulg (CMS) of the smart-chat to which the action has been submitted to

    Required property
    """

    action: Required["_SmartChatUserActionaction"]
    """
    `openChat` and `coseChat` indicates that the user has opened or closed the smart-chat

    Required property
    """


class SmartChatUserPrompt(TypedDict, total=False):
    """
    SmartChatUserPrompt.

    Tell the game that the user has submitted a message in a smart-chat.
    """

    type: Required[Literal["SmartChatUserPrompt"]]
    """


    Required property
    """

    smartChatSlug: Required[str]
    """
    The sulg (CMS) of the smart-chat to which the message has been submitted to

    Required property
    """

    message: Required[str]
    """
    The actual message

    Required property
    """


class StreamDiffusionSettings(TypedDict, total=False):
    """
    StreamDiffusionSettings.

    Notify the game about changes to the stream diffusion.
    """

    type: Required[Literal["StreamDiffusionSettings"]]
    """


    Required property
    """

    data: Required["_StreamDiffusionSettingsdata"]
    """
    Properties of the stream diffusion

    Required property
    """


class StreamingStats(TypedDict, total=False):
    """
    StreamingStats.

    The streaming stats
    """

    id: Required[str]
    """


    Required property
    """

    type: Required[str]
    """


    Required property
    """

    isRemote: Required[bool]
    """


    Required property
    """

    mediaType: Required[str]
    """


    Required property
    """

    timestamp: Required[int | float]
    """


    Required property
    """

    bytesReceived: Required[int | float]
    """


    Required property
    """

    framesDecoded: Required[int | float]
    """


    Required property
    """

    packetsLost: Required[int | float]
    """
    Total packets lost in the session

    Required property
    """

    jitter: Required[int | float]
    """


    Required property
    """

    jitterBufferDelay: Required[int | float]
    """


    Required property
    """

    jitterBufferEmittedCount: Required[int | float]
    """


    Required property
    """

    jitterBufferDelayAvg: Required[int | float]
    """


    Required property
    """

    totalDecodeTime: Required[int | float]
    """


    Required property
    """

    totalInterFrameDelay: Required[int | float]
    """


    Required property
    """

    totalProcessingDelay: Required[int | float]
    """


    Required property
    """

    bytesReceivedStart: Required[int | float]
    """


    Required property
    """

    timestampStart: Required[int | float]
    """


    Required property
    """

    avgBitrate: Required[int | float]
    """


    Required property
    """

    kind: Required[str]
    """


    Required property
    """

    trackIdentifier: Required[str]
    """


    Required property
    """

    bitrate: Required[int | float]
    """


    Required property
    """

    lowBitrate: Required[int | float]
    """


    Required property
    """

    highBitrate: Required[int | float]
    """


    Required property
    """

    framesDecodedStart: Required[int | float]
    """


    Required property
    """

    framesDroppedPercentage: Required[int | float]
    """


    Required property
    """

    framerate: Required[int | float]
    """


    Required property
    """

    avgframerate: Required[int | float]
    """


    Required property
    """

    highFramerate: Required[int | float]
    """


    Required property
    """

    lowFramerate: Required[int | float]
    """


    Required property
    """

    framesDropped: Required[int | float]
    """


    Required property
    """

    framesReceived: Required[int | float]
    """


    Required property
    """

    frameHeight: Required[int | float]
    """


    Required property
    """

    frameHeightStart: Required[int | float]
    """


    Required property
    """

    frameWidth: Required[int | float]
    """


    Required property
    """

    frameWidthStart: Required[int | float]
    """


    Required property
    """

    sessionPacketsLost: Required[int | float]
    """


    Required property
    """

    sessionPacketsReceived: Required[int | float]
    """


    Required property
    """

    sessionFreezeCount: Required[int | float]
    """


    Required property
    """

    sessionTotalFreezesDuration: Required[int | float]
    """


    Required property
    """

    sessionAvgFreezesDuration: Required[int | float]
    """


    Required property
    """

    sessionFreezedSpentTime: Required[int | float]
    """


    Required property
    """

    sessionAvgProcessingDelay: Required[int | float]
    """


    Required property
    """

    sessionAvgDecodingDelay: Required[int | float]
    """


    Required property
    """

    currentRoundTripTime: Required[int | float]
    """


    Required property
    """

    currentPacketLostPercent: Required[int | float]
    """


    Required property
    """

    currentJitterBufferDelay: Required[int | float]
    """


    Required property
    """

    currentFreezeCount: Required[int | float]
    """


    Required property
    """

    currentFreezeDurationPercent: Required[int | float]
    """


    Required property
    """

    currentProcessingDelay: Required[int | float]
    """


    Required property
    """

    currentDecodeDelay: Required[int | float]
    """


    Required property
    """


class TeleportPlayer(TypedDict, total=False):
    """
    TeleportPlayer.

    Ask the game to teleport the visitor to a spawn point.
    """

    type: Required[Literal["TeleportPlayer"]]
    """


    Required property
    """

    spawnPoint: Required[int | float]
    """
    The spawn point id

    Required property
    """


class TeleportTo(TypedDict, total=False):
    """
    TeleportTo.

    Ask the game to teleport the visitor to another player.
    """

    type: Required[Literal["TeleportTo"]]
    """


    Required property
    """

    playerId: Required[int | float]
    """
    The id of the player the to teleprot to

    Required property
    """

    roomId: str
    """ The id of the room to teleport to (if empty the current room will be assumed) """


class TimeTravel(TypedDict, total=False):
    """
    TimeTravel.

    NOT IMPLEMNTED - Ask the game to travel to another time (to trigger events for testing/debugging).
    """

    type: Required[Literal["TimeTravel"]]
    """


    Required property
    """

    date: Required[str]
    """
    The time to travel to (Date ISO 8601)

    Required property
    """


class UIElementCoords(TypedDict, total=False):
    """
    UIElementCoords.

    Tell the game about the new position of a specific UI element to for advanced UI coordination. It is sent for the initial position as well.
    """

    type: Required[Literal["UIElementCoords"]]
    """


    Required property
    """

    id: Required[str]
    """
    The id of the Ui element, for example `tutorialvideo`.

    Required property
    """

    x: Required[int | float]
    """
    Position x (percentage from the top-left screen corner)

    Required property
    """

    y: Required[int | float]
    """
    Position Y (percentage from the top-left screen corner)

    Required property
    """

    w: Required[int | float]
    """
    Width of the element (percentage of the screen width)

    Required property
    """

    h: Required[int | float]
    """
    Height of the element (percentage of the screen height)

    Required property
    """


class UiEvent(TypedDict, total=False):
    """
    UiEvent.

    Tell the game about changes (open/close) to the UI panels.
    """

    type: Required[Literal["UiEvent"]]
    """


    Required property
    """

    uiEventType: Required["_UiEventuiEventType"]
    """
    The type of event

    Required property
    """

    uiElement: Required["_UiEventuiElement"]
    """
    The panel this happens to

    Required property
    """

    slug: str
    """ The slug of the info card or the popup """


class ValidatorResponse(TypedDict, total=False):
    """
    ValidatorResponse.

    NOT IMPLEMENTED - Tell the web about the result of the user submission for the current validator.
    """

    type: Required[Literal["ValidatorResponse"]]
    """


    Required property
    """

    requestId: Required[str]
    """
    The id of the current validator negotiation

    Required property
    """

    validatorId: Required[str]
    """
    The slug of the validator (CMS)

    Required property
    """

    password: str
    """ The password that may have been submitted by the user """

    access: Required["_ValidatorResponseaccess"]
    """
    The result of the submission

    Required property
    """


class VoiceChatGroupStateChanged(TypedDict, total=False):
    """
    VoiceChatGroupStateChanged.

    NOT IMPLEMENTED - Notify the game that the voice chat group state has changed.
    """

    type: Required[Literal["VoiceChatGroupStateChanged"]]
    """


    Required property
    """

    groupId: Required[str]
    """
    Nakama room id the user belongs to

    Required property
    """

    videoSharingUrl: Required[str]
    """
    Url of the screenshare stream

    Required property
    """


class VoiceChatUserGroupChanged(TypedDict, total=False):
    """
    VoiceChatUserGroupChanged.

    Notify the game when a user joins a new group.
    """

    type: Required[Literal["VoiceChatUserGroupChanged"]]
    """


    Required property
    """

    userId: Required[str]
    """
    Nakama id of the user

    Required property
    """

    groupId: Required[str]
    """
    Nakama room id the user belongs to

    Required property
    """


class VoiceChatUserStateChanged(TypedDict, total=False):
    """
    VoiceChatUserStateChanged.

    Notify the game that the voice chat user state has changed. Used to start and stop screensharing, presenting etc
    """

    type: Required[Literal["VoiceChatUserStateChanged"]]
    """


    Required property
    """

    userId: Required[str]
    """
    Nakama id of the user

    Required property
    """

    isSpeaking: Required[bool]
    """
    Is the user speaking

    Required property
    """

    isMuted: Required[bool]
    """
    Is the user's audio input disabled

    Required property
    """

    isPresenter: bool
    """ Is the user a presenter (has the floor). This is used to notify the game that the user is presenting. """

    isVideoSharing: Required[bool]
    """
    Is the user screensharing

    Required property
    """


class WebRtcStreamingStats(TypedDict, total=False):
    """
    WebRtcStreamingStats.

    Tell the game some metrics about the WebRtc streaming.
    """

    type: Required[Literal["WebRtcStreamingStats"]]
    """


    Required property
    """

    data: Required["StreamingStats"]
    """
    StreamingStats.

    The streaming stats

    Required property
    """


WorldMessages = Union[
    "OnStartAction",
    "OnStreamIsShown",
    "UiEvent",
    "ActivateMovementType",
    "SendChatMessage",
    "DeleteMessage",
    "TimeTravel",
    "SendEmoji",
    "DidFakeTouch",
    "UIElementCoords",
    "LoadExternalAsset",
    "WebRtcStreamingStats",
    "SmartChatUserPrompt",
    "SmartChatUserAction",
    "ScreenSize",
    "TeleportTo",
    "TeleportPlayer",
    "PhotoCaptureEvent",
    "CustomMessage",
    "BusinessCard",
    "EditingBusinessCard",
    "ValidatorResponse",
    "ClientInfo",
    "LanguageSelected",
    "PollResultSubmitted",
    "VoiceChatUserStateChanged",
    "VoiceChatGroupStateChanged",
    "VoiceChatUserGroupChanged",
    "MediaCaptureEvent",
    "Reaction",
    "ScreenSharing",
    "GetScreenSharingStatus",
    "PauseStream",
    "ResumeStream",
    "RequestQuestsInfo",
    "StreamDiffusionSettings",
    "ActionElementEvent",
]
"""
Aggregation type: anyOf
Subtype: "OnStartAction", "OnStreamIsShown", "UiEvent", "ActivateMovementType", "SendChatMessage", "DeleteMessage", "TimeTravel", "SendEmoji", "DidFakeTouch", "UIElementCoords", "LoadExternalAsset", "WebRtcStreamingStats", "SmartChatUserPrompt", "SmartChatUserAction", "ScreenSize", "TeleportTo", "TeleportPlayer", "PhotoCaptureEvent", "CustomMessage", "BusinessCard", "EditingBusinessCard", "ValidatorResponse", "ClientInfo", "LanguageSelected", "PollResultSubmitted", "VoiceChatUserStateChanged", "VoiceChatGroupStateChanged", "VoiceChatUserGroupChanged", "MediaCaptureEvent", "Reaction", "ScreenSharing", "GetScreenSharingStatus", "PauseStream", "ResumeStream", "RequestQuestsInfo", "StreamDiffusionSettings", "ActionElementEvent"
"""


_ActionElementEventevent = Literal["click"] | Literal["change"] | Literal["open"] | Literal["close"]
""" The event that happened """
_ACTIONELEMENTEVENTEVENT_CLICK: Literal["click"] = "click"
"""The values for the 'The event that happened' enum"""
_ACTIONELEMENTEVENTEVENT_CHANGE: Literal["change"] = "change"
"""The values for the 'The event that happened' enum"""
_ACTIONELEMENTEVENTEVENT_OPEN: Literal["open"] = "open"
"""The values for the 'The event that happened' enum"""
_ACTIONELEMENTEVENTEVENT_CLOSE: Literal["close"] = "close"
"""The values for the 'The event that happened' enum"""


_ActivateMovementTypemovementType = Literal["walk"] | Literal["fly"] | Literal["hover"]
""" The movement mode to activate """
_ACTIVATEMOVEMENTTYPEMOVEMENTTYPE_WALK: Literal["walk"] = "walk"
"""The values for the 'The movement mode to activate' enum"""
_ACTIVATEMOVEMENTTYPEMOVEMENTTYPE_FLY: Literal["fly"] = "fly"
"""The values for the 'The movement mode to activate' enum"""
_ACTIVATEMOVEMENTTYPEMOVEMENTTYPE_HOVER: Literal["hover"] = "hover"
"""The values for the 'The movement mode to activate' enum"""


_MediaCaptureEventevent = (
    Literal["start"]
    | Literal["progress"]
    | Literal["complete"]
    | Literal["cancel"]
    | Literal["error"]
)
""" The state of the capture """
_MEDIACAPTUREEVENTEVENT_START: Literal["start"] = "start"
"""The values for the 'The state of the capture' enum"""
_MEDIACAPTUREEVENTEVENT_PROGRESS: Literal["progress"] = "progress"
"""The values for the 'The state of the capture' enum"""
_MEDIACAPTUREEVENTEVENT_COMPLETE: Literal["complete"] = "complete"
"""The values for the 'The state of the capture' enum"""
_MEDIACAPTUREEVENTEVENT_CANCEL: Literal["cancel"] = "cancel"
"""The values for the 'The state of the capture' enum"""
_MEDIACAPTUREEVENTEVENT_ERROR: Literal["error"] = "error"
"""The values for the 'The state of the capture' enum"""


_MediaCaptureEventmediaType = Literal["image"] | Literal["video"]
""" The type of media being captured """
_MEDIACAPTUREEVENTMEDIATYPE_IMAGE: Literal["image"] = "image"
"""The values for the 'The type of media being captured' enum"""
_MEDIACAPTUREEVENTMEDIATYPE_VIDEO: Literal["video"] = "video"
"""The values for the 'The type of media being captured' enum"""


_PhotoCaptureEventevent = Literal["open"] | Literal["close"] | Literal["cancel"] | Literal["taken"]
"""  """
_PHOTOCAPTUREEVENTEVENT_OPEN: Literal["open"] = "open"
"""The values for the '' enum"""
_PHOTOCAPTUREEVENTEVENT_CLOSE: Literal["close"] = "close"
"""The values for the '' enum"""
_PHOTOCAPTUREEVENTEVENT_CANCEL: Literal["cancel"] = "cancel"
"""The values for the '' enum"""
_PHOTOCAPTUREEVENTEVENT_TAKEN: Literal["taken"] = "taken"
"""The values for the '' enum"""


_SmartChatUserActionaction = Literal["openChat"] | Literal["closeChat"]
""" `openChat` and `coseChat` indicates that the user has opened or closed the smart-chat """
_SMARTCHATUSERACTIONACTION_OPENCHAT: Literal["openChat"] = "openChat"
"""The values for the '`openChat` and `coseChat` indicates that the user has opened or closed the smart-chat' enum"""
_SMARTCHATUSERACTIONACTION_CLOSECHAT: Literal["closeChat"] = "closeChat"
"""The values for the '`openChat` and `coseChat` indicates that the user has opened or closed the smart-chat' enum"""


class _StreamDiffusionSettingsdata(TypedDict, total=False):
    """Properties of the stream diffusion"""

    num_inference_steps: int | float
    """ The number of inference steps """

    guidance_scale: int | float
    """ The guidance scale """

    enabled: bool
    """ Is the stream diffusion enabled """

    prompt: str
    """ The prompt """

    negative_prompt: str
    """ The negative prompt """

    delta: int | float
    """ The delta """


_UiEventuiElement = (
    Literal["actionBar"]
    | Literal["logo"]
    | Literal["social"]
    | Literal["infocard"]
    | Literal["language"]
    | Literal["settings"]
    | Literal["map"]
    | Literal["popup"]
    | Literal["profile"]
    | Literal["cinematicView"]
    | Literal["photo"]
    | Literal["videoCapture"]
    | Literal["mediaShare"]
    | Literal["ending"]
    | Literal["screenSharing"]
    | Literal["videoAvatars"]
    | Literal["hint"]
    | Literal["questHint"]
    | Literal["stats"]
    | Literal["report"]
    | Literal["devOptions"]
    | Literal["presentationBar"]
    | Literal["fullscreenVideo"]
    | Literal["forceLandscape"]
    | Literal["startButton"]
    | Literal["poll"]
    | Literal["textChatPreview"]
    | Literal["walletConnect"]
    | Literal["quest"]
    | Literal["mobileController"]
    | Literal["actionElements"]
    | Literal["aiSettings"]
)
""" The panel this happens to """
_UIEVENTUIELEMENT_ACTIONBAR: Literal["actionBar"] = "actionBar"
"""The values for the 'The panel this happens to' enum"""
_UIEVENTUIELEMENT_LOGO: Literal["logo"] = "logo"
"""The values for the 'The panel this happens to' enum"""
_UIEVENTUIELEMENT_SOCIAL: Literal["social"] = "social"
"""The values for the 'The panel this happens to' enum"""
_UIEVENTUIELEMENT_INFOCARD: Literal["infocard"] = "infocard"
"""The values for the 'The panel this happens to' enum"""
_UIEVENTUIELEMENT_LANGUAGE: Literal["language"] = "language"
"""The values for the 'The panel this happens to' enum"""
_UIEVENTUIELEMENT_SETTINGS: Literal["settings"] = "settings"
"""The values for the 'The panel this happens to' enum"""
_UIEVENTUIELEMENT_MAP: Literal["map"] = "map"
"""The values for the 'The panel this happens to' enum"""
_UIEVENTUIELEMENT_POPUP: Literal["popup"] = "popup"
"""The values for the 'The panel this happens to' enum"""
_UIEVENTUIELEMENT_PROFILE: Literal["profile"] = "profile"
"""The values for the 'The panel this happens to' enum"""
_UIEVENTUIELEMENT_CINEMATICVIEW: Literal["cinematicView"] = "cinematicView"
"""The values for the 'The panel this happens to' enum"""
_UIEVENTUIELEMENT_PHOTO: Literal["photo"] = "photo"
"""The values for the 'The panel this happens to' enum"""
_UIEVENTUIELEMENT_VIDEOCAPTURE: Literal["videoCapture"] = "videoCapture"
"""The values for the 'The panel this happens to' enum"""
_UIEVENTUIELEMENT_MEDIASHARE: Literal["mediaShare"] = "mediaShare"
"""The values for the 'The panel this happens to' enum"""
_UIEVENTUIELEMENT_ENDING: Literal["ending"] = "ending"
"""The values for the 'The panel this happens to' enum"""
_UIEVENTUIELEMENT_SCREENSHARING: Literal["screenSharing"] = "screenSharing"
"""The values for the 'The panel this happens to' enum"""
_UIEVENTUIELEMENT_VIDEOAVATARS: Literal["videoAvatars"] = "videoAvatars"
"""The values for the 'The panel this happens to' enum"""
_UIEVENTUIELEMENT_HINT: Literal["hint"] = "hint"
"""The values for the 'The panel this happens to' enum"""
_UIEVENTUIELEMENT_QUESTHINT: Literal["questHint"] = "questHint"
"""The values for the 'The panel this happens to' enum"""
_UIEVENTUIELEMENT_STATS: Literal["stats"] = "stats"
"""The values for the 'The panel this happens to' enum"""
_UIEVENTUIELEMENT_REPORT: Literal["report"] = "report"
"""The values for the 'The panel this happens to' enum"""
_UIEVENTUIELEMENT_DEVOPTIONS: Literal["devOptions"] = "devOptions"
"""The values for the 'The panel this happens to' enum"""
_UIEVENTUIELEMENT_PRESENTATIONBAR: Literal["presentationBar"] = "presentationBar"
"""The values for the 'The panel this happens to' enum"""
_UIEVENTUIELEMENT_FULLSCREENVIDEO: Literal["fullscreenVideo"] = "fullscreenVideo"
"""The values for the 'The panel this happens to' enum"""
_UIEVENTUIELEMENT_FORCELANDSCAPE: Literal["forceLandscape"] = "forceLandscape"
"""The values for the 'The panel this happens to' enum"""
_UIEVENTUIELEMENT_STARTBUTTON: Literal["startButton"] = "startButton"
"""The values for the 'The panel this happens to' enum"""
_UIEVENTUIELEMENT_POLL: Literal["poll"] = "poll"
"""The values for the 'The panel this happens to' enum"""
_UIEVENTUIELEMENT_TEXTCHATPREVIEW: Literal["textChatPreview"] = "textChatPreview"
"""The values for the 'The panel this happens to' enum"""
_UIEVENTUIELEMENT_WALLETCONNECT: Literal["walletConnect"] = "walletConnect"
"""The values for the 'The panel this happens to' enum"""
_UIEVENTUIELEMENT_QUEST: Literal["quest"] = "quest"
"""The values for the 'The panel this happens to' enum"""
_UIEVENTUIELEMENT_MOBILECONTROLLER: Literal["mobileController"] = "mobileController"
"""The values for the 'The panel this happens to' enum"""
_UIEVENTUIELEMENT_ACTIONELEMENTS: Literal["actionElements"] = "actionElements"
"""The values for the 'The panel this happens to' enum"""


_UiEventuiEventType = Literal["onOpen"] | Literal["onClose"]
""" The type of event """
_UIEVENTUIEVENTTYPE_ONOPEN: Literal["onOpen"] = "onOpen"
"""The values for the 'The type of event' enum"""
_UIEVENTUIEVENTTYPE_ONCLOSE: Literal["onClose"] = "onClose"
"""The values for the 'The type of event' enum"""


_ValidatorResponseaccess = Literal["granted"] | Literal["denied"] | Literal["validation"]
""" The result of the submission """
_VALIDATORRESPONSEACCESS_GRANTED: Literal["granted"] = "granted"
"""The values for the 'The result of the submission' enum"""
_VALIDATORRESPONSEACCESS_DENIED: Literal["denied"] = "denied"
"""The values for the 'The result of the submission' enum"""
_VALIDATORRESPONSEACCESS_VALIDATION: Literal["validation"] = "validation"
"""The values for the 'The result of the submission' enum"""
