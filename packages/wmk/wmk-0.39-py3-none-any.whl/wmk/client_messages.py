from typing import Any, Literal, TypedDict, Union

from typing_extensions import Required


class ActionElementStatus(TypedDict, total=False):
    """
    ActionElementStatus.

    Tell the client the status of the action element
    """

    type: Required[Literal["ActionElementStatus"]]
    """


    Required property
    """

    actionElementId: Required[str]
    """
    The id of the action element

    Required property
    """

    value: Required[str]
    """
    The current value of the action element

    Required property
    """

    hidden: bool
    """ Whether the action element is hidden """

    options: "_ActionElementStatusoptions"
    """ Custom options of the action element """


class ActionElementsInfo(TypedDict, total=False):
    """
    ActionElementsInfo.

    Tell the client the status of the action elements
    """

    type: Required[Literal["ActionElementsInfo"]]
    """


    Required property
    """

    elements: Required[list["_ActionElementsInfoelementsitem"]]
    """
    An array of action elements

    Required property
    """


class ActionPanel(TypedDict, total=False):
    """
    ActionPanel.

    The game request an action-panel (popup) to be opened/closed.

    deprecated: True
    """

    type: Required[Literal["ActionPanel"]]
    """


    Required property
    """

    display: Required[bool]
    """
    Close the current action-panel or open a new one.

    Required property
    """

    id: Required[str]
    """
    The slug of the action-panel to open (CMS).

    Required property
    """


class ActiveRegion(TypedDict, total=False):
    """
    ActiveRegion.

    Tell the web to highlight a new active region
    """

    type: Required[Literal["ActiveRegion"]]
    """


    Required property
    """

    regionId: Required[str]
    """
    Id of the active region

    Required property
    """

    categoryId: str
    """ category of the active region """


class AnalyticsEvent(TypedDict, total=False):
    """
    AnalyticsEvent.

    Send an analytics event to the web.
    """

    type: Required[Literal["AnalyticsEvent"]]
    """


    Required property
    """

    eventName: Required[str]
    """
    The name of the event

    Required property
    """


ClientMessages = Union[
    "UiAction",
    "ReceivedChatMessage",
    "OnChatMessageDeleted",
    "PerformanceStats",
    "NearbyPlayers",
    "PhotonPlayerConnected",
    "SmartChatAction",
    "SmartChatEngineReply",
    "SmartChatSubscriptionUpdate",
    "SetIsPresenter",
    "ShareMedia",
    "EndSession",
    "ShowBusinessCard",
    "ActiveRegion",
    "GameIsReady",
    "InfoCard",
    "ActionPanel",
    "PhotonPlayerDisconnected",
    "RoomTeleportStart",
    "RoomTeleportEnd",
    "ExternalAssetLoadStatus",
    "TakeScreenshot",
    "MouseEnterClickableSpot",
    "MouseExitClickableSpot",
    "Validator",
    "CustomMessage",
    "Poll",
    "DisplayMap",
    "PauseMode",
    "SetPointerScheme",
    "LoadingLevelStart",
    "LoadingLevelEnd",
    "UnrealStateUpdate",
    "OpenBusinessCardEditor",
    "HideUi",
    "EnterRegion",
    "ExitRegion",
    "GameQuiz",
    "AnalyticsEvent",
    "MediaCaptureAction",
    "Reaction",
    "ScreenSharing",
    "GetScreenSharingStatus",
    "MovementTypeChanged",
    "ProductSelected",
    "ItemAdded",
    "QuestsInfo",
    "QuestProgress",
    "CurrencyChanged",
    "ActionElementsInfo",
    "ActionElementStatus",
]
"""
Aggregation type: anyOf
Subtype: "UiAction", "ReceivedChatMessage", "OnChatMessageDeleted", "PerformanceStats", "NearbyPlayers", "PhotonPlayerConnected", "SmartChatAction", "SmartChatEngineReply", "SmartChatSubscriptionUpdate", "SetIsPresenter", "ShareMedia", "EndSession", "ShowBusinessCard", "ActiveRegion", "GameIsReady", "InfoCard", "ActionPanel", "PhotonPlayerDisconnected", "RoomTeleportStart", "RoomTeleportEnd", "ExternalAssetLoadStatus", "TakeScreenshot", "MouseEnterClickableSpot", "MouseExitClickableSpot", "Validator", "CustomMessage", "Poll", "DisplayMap", "PauseMode", "SetPointerScheme", "LoadingLevelStart", "LoadingLevelEnd", "UnrealStateUpdate", "OpenBusinessCardEditor", "HideUi", "EnterRegion", "ExitRegion", "GameQuiz", "AnalyticsEvent", "MediaCaptureAction", "Reaction", "ScreenSharing", "GetScreenSharingStatus", "MovementTypeChanged", "ProductSelected", "ItemAdded", "QuestsInfo", "QuestProgress", "CurrencyChanged", "ActionElementsInfo", "ActionElementStatus"
"""


class CurrencyChanged(TypedDict, total=False):
    """
    CurrencyChanged.

    Tell the client that the amount of currency has changed
    """

    type: Required[Literal["CurrencyChanged"]]
    """


    Required property
    """

    currencyId: Required[str]
    """
    The id of the currency

    Required property
    """

    delta: Required[int | float]
    """
    The amount of currency added or removed

    Required property
    """

    newAmount: Required[int | float]
    """
    The new amount of currency

    Required property
    """


class CustomMessage(TypedDict, total=False):
    """
    CustomMessage.

    NOT IMPLEMENTED - Last resort custom message. Use it only for development.
    """

    type: Required[Literal["CustomMessage"]]
    """


    Required property
    """

    messageType: Required[str]
    """
    A sub-type for the message.

    Required property
    """

    data: Required[dict[str, Any]]
    """
    A custom payload.

    Required property
    """


class DisplayMap(TypedDict, total=False):
    """
    DisplayMap.

    NOT IMPLEMENTED - The game request to open/close the map.

    deprecated: True
    """

    type: Required[Literal["DisplayMap"]]
    """


    Required property
    """

    display: Required[bool]
    """
    Open or close the map

    Required property
    """


class EndSession(TypedDict, total=False):
    """
    EndSession.

    Ask the web to end the session, redirecting the user to an end-screen or to a predefined URL (CMS).
    """

    type: Required[Literal["EndSession"]]
    """


    Required property
    """


class EnterRegion(TypedDict, total=False):
    """
    EnterRegion.

    Visitor has entered a region.
    """

    type: Required[Literal["EnterRegion"]]
    """


    Required property
    """

    regionId: Required[str]
    """
    The id of the region

    Required property
    """


class ExitRegion(TypedDict, total=False):
    """
    ExitRegion.

    Visitor has exited a region.
    """

    type: Required[Literal["ExitRegion"]]
    """


    Required property
    """

    regionId: Required[str]
    """
    The id of the region

    Required property
    """


class ExternalAssetLoadStatus(TypedDict, total=False):
    """
    ExternalAssetLoadStatus.

    NOT IMPLEMENTED - Tell the web the status of an external asset load request (a request normally initiated by the web).
    """

    type: Required[Literal["ExternalAssetLoadStatus"]]
    """


    Required property
    """

    target: Required[str]
    """
    The type of assets being loaded (e.g. customAvatarLoadingStatus)

    Required property
    """

    status: Required[str]
    """
    Loading status. "loading" or "loaded"

    Required property
    """

    description: str
    """ Human-readable string that explains status """

    uri: Required[str]
    """
    The full URI (with protocol specified) of the asset that is being loaded

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


class GameColor5265(TypedDict, total=False):
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


class GameIsReady(TypedDict, total=False):
    """
    GameIsReady.

    Tell the web that the experience is now running (we have a video output).
    """

    type: Required[Literal["GameIsReady"]]
    """


    Required property
    """


class GameQuiz(TypedDict, total=False):
    """
    GameQuiz.

    Visitor answered an in-game quiz
    """

    type: Required[Literal["GameQuiz"]]
    """


    Required property
    """

    id: Required[str]
    """
    The id of the quiz.

    Required property
    """

    answer: Required[str]
    """
    The visitor's answer.

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


class HideUi(TypedDict, total=False):
    """
    HideUi.

    NOT IMPLEMENTED - Hide all the UI. Legacy for opening cinematicView.

    deprecated: True
    """

    type: Required[Literal["HideUi"]]
    """


    Required property
    """

    hide: Required[bool]
    """
    Hide or show the ui

    Required property
    """


class InfoCard(TypedDict, total=False):
    """
    InfoCard.

    Ask the web to open/close an infocard.

    deprecated: True
    """

    type: Required[Literal["InfoCard"]]
    """


    Required property
    """

    display: Required[bool]
    """
    Close the current action-panel or open a new one.

    Required property
    """

    id: Required[str]
    """
    The slug of the infocard to open (CMS)

    Required property
    """


class ItemAdded(TypedDict, total=False):
    """
    ItemAdded.

    Tell the web client that an item has been added to the inventory
    """

    type: Required[Literal["ItemAdded"]]
    """


    Required property
    """

    slug: Required[str]
    """
    The id of the item

    Required property
    """

    amount: Required[int | float]
    """
    The amount of added items

    Required property
    """


class LoadingLevelEnd(TypedDict, total=False):
    """
    LoadingLevelEnd.

    Tell the we that the level loading is over and that any current LoadingLevelVideo ui can be hidden.

    deprecated: True
    """

    type: Required[Literal["LoadingLevelEnd"]]
    """


    Required property
    """

    levelId: Required[str]
    """
    The id of the loaded level

    Required property
    """


class LoadingLevelStart(TypedDict, total=False):
    """
    LoadingLevelStart.

    Tell the web that the game is loading a level. This also ask the web to show a LoadingLevelVideo panel to cover the load.

    deprecated: True
    """

    type: Required[Literal["LoadingLevelStart"]]
    """


    Required property
    """

    levelId: Required[str]
    """
    The id of the loading level as well as the slug for the LoadingLevelVideo to show while the level is loading

    Required property
    """


class MediaCaptureAction(TypedDict, total=False):
    """
    MediaCaptureAction.

    Control the media capture of the client.
    """

    type: Required[Literal["MediaCaptureAction"]]
    """


    Required property
    """

    mediaType: Required["_MediaCaptureActionmediaType"]
    """
    The type of media being captured

    Required property
    """

    action: Required["_MediaCaptureActionaction"]
    """
    The state of the capture

    Required property
    """


class MouseEnterClickableSpot(TypedDict, total=False):
    """
    MouseEnterClickableSpot.

    NOT IMPLEMENTED - Tell the web that the mouse is over a clickable element (so the cursor should be 'pointer').
    """

    type: Required[Literal["MouseEnterClickableSpot"]]
    """


    Required property
    """

    interactableType: Required[str]
    """


    Required property
    """


class MouseExitClickableSpot(TypedDict, total=False):
    """
    MouseExitClickableSpot.

    NOT IMPLEMENTED - Tell the web that the mouse not anymore over a clickable spot.
    """

    type: Required[Literal["MouseExitClickableSpot"]]
    """


    Required property
    """

    interactableType: Required[str]
    """


    Required property
    """


class MovementTypeChanged(TypedDict, total=False):
    """
    MovementTypeChanged.

    Tell web client which movement type is active at the moment
    """

    type: Required[Literal["MovementTypeChanged"]]
    """


    Required property
    """

    movementType: Required["_MovementTypeChangedmovementType"]
    """
    Can have the values 'Fly', 'Walk', 'Hover', although there might be new ones coming

    Required property
    """


class NearbyPlayer(TypedDict, total=False):
    """
    NearbyPlayer.

    A nearby player.
    """

    playerId: Required[int | float]
    """
    The player id (unique across the room)

    Required property
    """

    name: Required[str]
    """
    The player's name to display

    Required property
    """

    distance: Required[int | float]
    """
    Distance between the current player and the other player (in world meters?)

    Required property
    """

    avatarColor: Required["GameColor"]
    """
    GameColor.

    A representation of a color.

    Required property
    """


class NearbyPlayers(TypedDict, total=False):
    """
    NearbyPlayers.

    Tell the web about the current nearby players (nomrally on a regular interval).
    """

    type: Required[Literal["NearbyPlayers"]]
    """


    Required property
    """

    players: Required[list["NearbyPlayer"]]
    """
    An array of NearbyPlayer objects, sorted by distance

    Required property
    """


class OnChatMessageDeleted(TypedDict, total=False):
    """
    OnChatMessageDeleted.

    Tell the web to delete a chat message.
    """

    type: Required[Literal["OnChatMessageDeleted"]]
    """


    Required property
    """

    senderId: Required[int | float]
    """
    The user whose message to be deleted

    Required property
    """

    messageId: Required[int | float]
    """
    The id of the message to be deleted

    Required property
    """


class OpenBusinessCardEditor(TypedDict, total=False):
    """
    OpenBusinessCardEditor.

    NOT IMPLEMENTED - Ask the web to open the visitors business-card (profile panel) which is editable.

    deprecated: True
    """

    type: Required[Literal["OpenBusinessCardEditor"]]
    """


    Required property
    """


class PauseMode(TypedDict, total=False):
    """
    PauseMode.

    NOT IMPLEMENTED - Ask the web to open/close the pause UI.

    deprecated: True
    """

    type: Required[Literal["PauseMode"]]
    """


    Required property
    """

    pauseMode: Required[bool]
    """
    Open or close the pause ui

    Required property
    """


class PerformanceStats(TypedDict, total=False):
    """
    PerformanceStats.

    Forward to the web the performance stats (normally on a regular interval).
    """

    type: Required[Literal["PerformanceStats"]]
    """


    Required property
    """

    cpuUsage: Required[int | float]
    """
    Average CPU usage in a range of 0-100

    minimum: 0
    maximum: 100

    Required property
    """

    gpuUsage: Required[int | float]
    """
    Average GPU usage in a range of 0-100

    minimum: 0
    maximum: 100

    Required property
    """

    fps: int | float
    """ Average Frames Per Seconds """


class PhotonPlayerConnected(TypedDict, total=False):
    """
    PhotonPlayerConnected.

    Tell the web that the game has connected to a Photon Room.
    """

    type: Required[Literal["PhotonPlayerConnected"]]
    """


    Required property
    """

    playerId: Required[int | float]
    """
    Unique player id inside the connected room

    Required property
    """

    roomId: Required[str]
    """
    Unique id for the room

    Required property
    """


class PhotonPlayerDisconnected(TypedDict, total=False):
    """
    PhotonPlayerDisconnected.

    NOT IMPLEMENTED - Tell the web that the player disconnected from the current photon room.
    """

    type: Required[Literal["PhotonPlayerDisconnected"]]
    """


    Required property
    """


class Poll(TypedDict, total=False):
    """
    Poll.

    Ask the web to open/close a poll.

    deprecated: True
    """

    type: Required[Literal["Poll"]]
    """


    Required property
    """

    display: Required[bool]
    """
    Close the current poll or open a new one

    Required property
    """

    id: Required[str]
    """
    The CMS slug of the poll to be open

    Required property
    """


class ProductSelected(TypedDict, total=False):
    """
    ProductSelected.

    Tell the web client that a product has been selected
    """

    type: Required[Literal["ProductSelected"]]
    """


    Required property
    """

    slug: Required[str]
    """
    The id of the product

    Required property
    """

    variant: str
    """ The id of the variant of the product """


class QuestProgress(TypedDict, total=False):
    """
    QuestProgress.

    Tell the client the progress of a quest
    """

    type: Required[Literal["QuestProgress"]]
    """


    Required property
    """

    quest: Required["_QuestProgressquest"]
    """
    The quest

    Required property
    """

    hasProgressUI: Required[bool]
    """
    Whether the quest has a progress UI

    Required property
    """


class QuestsInfo(TypedDict, total=False):
    """
    QuestsInfo.

    Tell the client the status of the quests
    """

    type: Required[Literal["QuestsInfo"]]
    """


    Required property
    """

    quests: Required[list["_QuestsInfoquestsitem"]]
    """
    An array of quests

    Required property
    """


class Reaction(TypedDict, total=False):
    """
    Reaction.

    Broadcast a reaction to all users.
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


class ReceivedChatMessage(TypedDict, total=False):
    """
    ReceivedChatMessage.

    Tell the web that a new chat message should be displayed.
    """

    type: Required[Literal["ReceivedChatMessage"]]
    """


    Required property
    """

    content: Required[str]
    """
    The content of the message

    Required property
    """

    sender: Required[str]
    """
    The user name of the person that sent the message

    Required property
    """

    senderId: Required[int | float]
    """
    The id of the sender

    Required property
    """

    channelId: str
    """ The channel in which the message was received. The public channel ends with "Default" """

    messageId: int | float
    """ This is an always incrementing number - each sender has it's own message id that increments every time they broadcast a message """

    roomId: Required[str]
    """
    The room id

    Required property
    """


class RoomTeleportEnd(TypedDict, total=False):
    """
    RoomTeleportEnd.

    NOT IMPLEMENTED - Tell the we that the visitor has teleported to another room
    """

    type: Required[Literal["RoomTeleportEnd"]]
    """


    Required property
    """

    success: Required[bool]
    """
    Whether the teleport was executed successfully

    Required property
    """

    errorCode: Required[int | float]
    """
    If success is false this will have a none zero value (1=JoinRoomFailed, 2=PlayerNotFound)

    Required property
    """


class RoomTeleportStart(TypedDict, total=False):
    """
    RoomTeleportStart.

    NOT IMPLEMENTED - Called when Unreal receives the TeleportTo event
    """

    type: Required[Literal["RoomTeleportStart"]]
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


class SetIsPresenter(TypedDict, total=False):
    """
    SetIsPresenter.

    Notify the web that a user is now the presenter. Can be empty, represents that nobody is presenting
    """

    type: Required[Literal["SetIsPresenter"]]
    """


    Required property
    """

    userId: str
    """ Nakama id of the user """


class SetPointerScheme(TypedDict, total=False):
    """
    SetPointerScheme.

    NOT IMPLEMENTED - Ask the web to switch between mouse control schemes.

    deprecated: True
    """

    type: Required[Literal["SetPointerScheme"]]
    """


    Required property
    """

    scheme: Required["_SetPointerSchemescheme"]
    """
    `0` for a locked mouse capture via the Pointer Lock API, `1` for a hovering mouse

    Required property
    """


class ShareMedia(TypedDict, total=False):
    """
    ShareMedia.

    Ask the web to show some media file sharing options to the user.
    """

    type: Required[Literal["ShareMedia"]]
    """


    Required property
    """

    url: Required[str]
    """
    The URL to download the media from

    Required property
    """

    mediaType: Required["_ShareMediamediaType"]
    """
    The type of the media

    Required property
    """

    endSession: Required[bool]
    """
    Whether the session should end after the media has been shared

    Required property
    """

    onMobile: Required[bool]
    """
    Whether the media should be shareable on mobile

    Required property
    """

    onDesktop: Required[bool]
    """
    Whether the media should be shareable on desktop

    Required property
    """


class ShowBusinessCard(TypedDict, total=False):
    """
    ShowBusinessCard.

    Ask the web to display the business-card (profile information) of another visitor.
    """

    type: Required[Literal["ShowBusinessCard"]]
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

    avatarColor: Required["GameColor5265"]
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


class SmartChatAction(TypedDict, total=False):
    """
    SmartChatAction.

    Tell the web to perform actions related to smart-chats (GPT-avatars).
    """

    type: Required[Literal["SmartChatAction"]]
    """


    Required property
    """

    smartChatSlug: Required[str]
    """
    The slug to identify to which smart-chat the action should apply to

    Required property
    """

    action: Required["_SmartChatActionaction"]
    """
    The action to perform. `openChat` and `closeChat` simply open and close the chat panel (in which a smart-chat would take place). `npcTyping` is a ping to show a "i am typing..."-like message in the smart-chat (used while a chat bot is generating an answer).

    Required property
    """


class SmartChatEngineReply(TypedDict, total=False):
    """
    SmartChatEngineReply.

    Tell the web to display a new message in a smart-chat thread.
    """

    type: Required[Literal["SmartChatEngineReply"]]
    """


    Required property
    """

    smartChatSlug: Required[str]
    """
    The slug to identify to which smart-chat the message should ve added to

    Required property
    """

    message: Required[str]
    """
    The actual message

    Required property
    """


class SmartChatSubscriptionUpdate(TypedDict, total=False):
    """
    SmartChatSubscriptionUpdate.

    Tell the web what are the currently available smart-chat (norbally this is based on chat-bot proximity). Currently, if any is present, they override the global chat.
    """

    type: Required[Literal["SmartChatSubscriptionUpdate"]]
    """


    Required property
    """

    smartChatSlugs: Required[list[str]]
    """
    The list of available smart-chat slugs

    Required property
    """


class TakeScreenshot(TypedDict, total=False):
    """
    TakeScreenshot.

    NOT IMPLEMENTED - Ask web to take a screenshot and start the social media share flow.
    """

    type: Required[Literal["TakeScreenshot"]]
    """


    Required property
    """


class UiAction(TypedDict, total=False):
    """
    UiAction.

    Ask the web to open/close a UI panel.
    """

    type: Required[Literal["UiAction"]]
    """


    Required property
    """

    uiElement: Required["_UiActionuiElement"]
    """
    The panel to target

    Required property
    """

    uiActionType: "_UiActionuiActionType"
    """ The action to perform. """

    options: Required["_UiActionoptions"]
    """
    The options to pass to the UI element

    Required property
    """


class UnrealStateUpdate(TypedDict, total=False):
    """
    UnrealStateUpdate.

    ???
    """

    type: Required[Literal["UnrealStateUpdate"]]
    """


    Required property
    """


class Validator(TypedDict, total=False):
    """
    Validator.

    NOT IMPLEMENTED - Ask the web to diplay a validator dialog.
    """

    type: Required[Literal["Validator"]]
    """


    Required property
    """

    requestId: Required[str]
    """
    An id (generated by the game) to keep track of the current validator negotiation

    Required property
    """

    validatorId: Required[str]
    """
    The slug of the validator to open (CMS)

    Required property
    """


class _ActionElementStatusoptions(TypedDict, total=False):
    """Custom options of the action element"""

    items: list[str]
    """ An array of available item values for menu or select type elements """

    open: bool
    """ Whether the menu or select type element is open """


class _ActionElementsInfoelementsitem(TypedDict, total=False):
    actionElementId: Required[str]
    """
    The id of the action element

    Required property
    """

    value: Required[str]
    """
    The current value of the action element

    Required property
    """

    hidden: bool
    """ Whether the action element is hidden """

    options: "_ActionElementsInfoelementsitemoptions"
    """ Custom options of the action element """


class _ActionElementsInfoelementsitemoptions(TypedDict, total=False):
    """Custom options of the action element"""

    items: list[str]
    """ An array of available item values for menu or select type elements """

    open: bool
    """ Whether the menu or select type element is open """


_MediaCaptureActionaction = Literal["start"] | Literal["complete"] | Literal["cancel"]
""" The state of the capture """
_MEDIACAPTUREACTIONACTION_START: Literal["start"] = "start"
"""The values for the 'The state of the capture' enum"""
_MEDIACAPTUREACTIONACTION_COMPLETE: Literal["complete"] = "complete"
"""The values for the 'The state of the capture' enum"""
_MEDIACAPTUREACTIONACTION_CANCEL: Literal["cancel"] = "cancel"
"""The values for the 'The state of the capture' enum"""


_MediaCaptureActionmediaType = Literal["image"] | Literal["video"]
""" The type of media being captured """
_MEDIACAPTUREACTIONMEDIATYPE_IMAGE: Literal["image"] = "image"
"""The values for the 'The type of media being captured' enum"""
_MEDIACAPTUREACTIONMEDIATYPE_VIDEO: Literal["video"] = "video"
"""The values for the 'The type of media being captured' enum"""


_MovementTypeChangedmovementType = Literal["Fly"] | Literal["Walk"] | Literal["Hover"]
""" Can have the values 'Fly', 'Walk', 'Hover', although there might be new ones coming """
_MOVEMENTTYPECHANGEDMOVEMENTTYPE_FLY: Literal["Fly"] = "Fly"
"""The values for the 'Can have the values 'Fly', 'Walk', 'Hover', although there might be new ones coming' enum"""
_MOVEMENTTYPECHANGEDMOVEMENTTYPE_WALK: Literal["Walk"] = "Walk"
"""The values for the 'Can have the values 'Fly', 'Walk', 'Hover', although there might be new ones coming' enum"""
_MOVEMENTTYPECHANGEDMOVEMENTTYPE_HOVER: Literal["Hover"] = "Hover"
"""The values for the 'Can have the values 'Fly', 'Walk', 'Hover', although there might be new ones coming' enum"""


class _QuestProgressquest(TypedDict, total=False):
    """The quest"""

    slug: Required[str]
    """
    The id of the quest

    Required property
    """

    state: Required["_QuestProgressqueststate"]
    """
    The status of the quest

    Required property
    """

    currencyCollectedAmount: Required[int | float]
    """
    The amount of currency collected

    Required property
    """

    currencyNeededAmount: Required[int | float]
    """
    The amount of currency required

    Required property
    """


_QuestProgressqueststate = Literal["Active"] | Literal["Completed"] | Literal["NotStarted"]
""" The status of the quest """
_QUESTPROGRESSQUESTSTATE_ACTIVE: Literal["Active"] = "Active"
"""The values for the 'The status of the quest' enum"""
_QUESTPROGRESSQUESTSTATE_COMPLETED: Literal["Completed"] = "Completed"
"""The values for the 'The status of the quest' enum"""
_QUESTPROGRESSQUESTSTATE_NOTSTARTED: Literal["NotStarted"] = "NotStarted"
"""The values for the 'The status of the quest' enum"""


class _QuestsInfoquestsitem(TypedDict, total=False):
    slug: Required[str]
    """
    The id of the quest

    Required property
    """

    state: Required["_QuestsInfoquestsitemstate"]
    """
    The status of the quest

    Required property
    """

    currencyCollectedAmount: Required[int | float]
    """
    The amount of currency collected

    Required property
    """

    currencyNeededAmount: Required[int | float]
    """
    The amount of currency required

    Required property
    """


_QuestsInfoquestsitemstate = Literal["Active"] | Literal["Completed"] | Literal["NotStarted"]
""" The status of the quest """
_QUESTSINFOQUESTSITEMSTATE_ACTIVE: Literal["Active"] = "Active"
"""The values for the 'The status of the quest' enum"""
_QUESTSINFOQUESTSITEMSTATE_COMPLETED: Literal["Completed"] = "Completed"
"""The values for the 'The status of the quest' enum"""
_QUESTSINFOQUESTSITEMSTATE_NOTSTARTED: Literal["NotStarted"] = "NotStarted"
"""The values for the 'The status of the quest' enum"""


_SetPointerSchemescheme = Literal[0] | Literal[1] | Literal[2]
""" `0` for a locked mouse capture via the Pointer Lock API, `1` for a hovering mouse """
_SETPOINTERSCHEMESCHEME_0: Literal[0] = 0
"""The values for the '`0` for a locked mouse capture via the Pointer Lock API, `1` for a hovering mouse' enum"""
_SETPOINTERSCHEMESCHEME_1: Literal[1] = 1
"""The values for the '`0` for a locked mouse capture via the Pointer Lock API, `1` for a hovering mouse' enum"""
_SETPOINTERSCHEMESCHEME_2: Literal[2] = 2
"""The values for the '`0` for a locked mouse capture via the Pointer Lock API, `1` for a hovering mouse' enum"""


_ShareMediamediaType = Literal["video"] | Literal["image"]
""" The type of the media """
_SHAREMEDIAMEDIATYPE_VIDEO: Literal["video"] = "video"
"""The values for the 'The type of the media' enum"""
_SHAREMEDIAMEDIATYPE_IMAGE: Literal["image"] = "image"
"""The values for the 'The type of the media' enum"""


_SmartChatActionaction = Literal["openChat"] | Literal["closeChat"] | Literal["npcTyping"]
""" The action to perform. `openChat` and `closeChat` simply open and close the chat panel (in which a smart-chat would take place). `npcTyping` is a ping to show a "i am typing..."-like message in the smart-chat (used while a chat bot is generating an answer). """
_SMARTCHATACTIONACTION_OPENCHAT: Literal["openChat"] = "openChat"
"""The values for the 'The action to perform. `openChat` and `closeChat` simply open and close the chat panel (in which a smart-chat would take place). `npcTyping` is a ping to show a "i am typing..."-like message in the smart-chat (used while a chat bot is generating an answer)' enum"""
_SMARTCHATACTIONACTION_CLOSECHAT: Literal["closeChat"] = "closeChat"
"""The values for the 'The action to perform. `openChat` and `closeChat` simply open and close the chat panel (in which a smart-chat would take place). `npcTyping` is a ping to show a "i am typing..."-like message in the smart-chat (used while a chat bot is generating an answer)' enum"""
_SMARTCHATACTIONACTION_NPCTYPING: Literal["npcTyping"] = "npcTyping"
"""The values for the 'The action to perform. `openChat` and `closeChat` simply open and close the chat panel (in which a smart-chat would take place). `npcTyping` is a ping to show a "i am typing..."-like message in the smart-chat (used while a chat bot is generating an answer)' enum"""


class _UiActionoptions(TypedDict, total=False):
    """The options to pass to the UI element"""

    slug: str


_UiActionuiActionType = Literal["open"] | Literal["close"]
""" The action to perform. """
_UIACTIONUIACTIONTYPE_OPEN: Literal["open"] = "open"
"""The values for the 'The action to perform' enum"""
_UIACTIONUIACTIONTYPE_CLOSE: Literal["close"] = "close"
"""The values for the 'The action to perform' enum"""


_UiActionuiElement = (
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
    | Literal["actionBar/social"]
    | Literal["actionBar/emojis"]
    | Literal["actionBar/reactionsBar"]
    | Literal["actionBar/movements"]
    | Literal["actionBar/map"]
    | Literal["actionBar/settings"]
    | Literal["actionBar/photo"]
    | Literal["cinematicView/skip"]
    | Literal["fullscreenVideo/skip"]
    | Literal["social/assistant"]
    | Literal["social/chat"]
    | Literal["social/players"]
    | Literal["social/playerProfile/:playerId"]
    | Literal["settings/home"]
    | Literal["settings/about"]
    | Literal["settings/video"]
    | Literal["settings/controls"]
    | Literal["settings/streamDiffusion"]
    | Literal["settings/walletconnect"]
)
""" The panel to target """
_UIACTIONUIELEMENT_ACTIONBAR: Literal["actionBar"] = "actionBar"
"""The values for the 'The panel to target' enum"""
_UIACTIONUIELEMENT_LOGO: Literal["logo"] = "logo"
"""The values for the 'The panel to target' enum"""
_UIACTIONUIELEMENT_SOCIAL: Literal["social"] = "social"
"""The values for the 'The panel to target' enum"""
_UIACTIONUIELEMENT_INFOCARD: Literal["infocard"] = "infocard"
"""The values for the 'The panel to target' enum"""
_UIACTIONUIELEMENT_LANGUAGE: Literal["language"] = "language"
"""The values for the 'The panel to target' enum"""
_UIACTIONUIELEMENT_SETTINGS: Literal["settings"] = "settings"
"""The values for the 'The panel to target' enum"""
_UIACTIONUIELEMENT_MAP: Literal["map"] = "map"
"""The values for the 'The panel to target' enum"""
_UIACTIONUIELEMENT_POPUP: Literal["popup"] = "popup"
"""The values for the 'The panel to target' enum"""
_UIACTIONUIELEMENT_PROFILE: Literal["profile"] = "profile"
"""The values for the 'The panel to target' enum"""
_UIACTIONUIELEMENT_CINEMATICVIEW: Literal["cinematicView"] = "cinematicView"
"""The values for the 'The panel to target' enum"""
_UIACTIONUIELEMENT_PHOTO: Literal["photo"] = "photo"
"""The values for the 'The panel to target' enum"""
_UIACTIONUIELEMENT_VIDEOCAPTURE: Literal["videoCapture"] = "videoCapture"
"""The values for the 'The panel to target' enum"""
_UIACTIONUIELEMENT_MEDIASHARE: Literal["mediaShare"] = "mediaShare"
"""The values for the 'The panel to target' enum"""
_UIACTIONUIELEMENT_ENDING: Literal["ending"] = "ending"
"""The values for the 'The panel to target' enum"""
_UIACTIONUIELEMENT_SCREENSHARING: Literal["screenSharing"] = "screenSharing"
"""The values for the 'The panel to target' enum"""
_UIACTIONUIELEMENT_VIDEOAVATARS: Literal["videoAvatars"] = "videoAvatars"
"""The values for the 'The panel to target' enum"""
_UIACTIONUIELEMENT_HINT: Literal["hint"] = "hint"
"""The values for the 'The panel to target' enum"""
_UIACTIONUIELEMENT_QUESTHINT: Literal["questHint"] = "questHint"
"""The values for the 'The panel to target' enum"""
_UIACTIONUIELEMENT_STATS: Literal["stats"] = "stats"
"""The values for the 'The panel to target' enum"""
_UIACTIONUIELEMENT_REPORT: Literal["report"] = "report"
"""The values for the 'The panel to target' enum"""
_UIACTIONUIELEMENT_DEVOPTIONS: Literal["devOptions"] = "devOptions"
"""The values for the 'The panel to target' enum"""
_UIACTIONUIELEMENT_PRESENTATIONBAR: Literal["presentationBar"] = "presentationBar"
"""The values for the 'The panel to target' enum"""
_UIACTIONUIELEMENT_FULLSCREENVIDEO: Literal["fullscreenVideo"] = "fullscreenVideo"
"""The values for the 'The panel to target' enum"""
_UIACTIONUIELEMENT_FORCELANDSCAPE: Literal["forceLandscape"] = "forceLandscape"
"""The values for the 'The panel to target' enum"""
_UIACTIONUIELEMENT_STARTBUTTON: Literal["startButton"] = "startButton"
"""The values for the 'The panel to target' enum"""
_UIACTIONUIELEMENT_POLL: Literal["poll"] = "poll"
"""The values for the 'The panel to target' enum"""
_UIACTIONUIELEMENT_TEXTCHATPREVIEW: Literal["textChatPreview"] = "textChatPreview"
"""The values for the 'The panel to target' enum"""
_UIACTIONUIELEMENT_WALLETCONNECT: Literal["walletConnect"] = "walletConnect"
"""The values for the 'The panel to target' enum"""
_UIACTIONUIELEMENT_QUEST: Literal["quest"] = "quest"
"""The values for the 'The panel to target' enum"""
_UIACTIONUIELEMENT_MOBILECONTROLLER: Literal["mobileController"] = "mobileController"
"""The values for the 'The panel to target' enum"""
_UIACTIONUIELEMENT_ACTIONELEMENTS: Literal["actionElements"] = "actionElements"
"""The values for the 'The panel to target' enum"""
_UIACTIONUIELEMENT_ACTIONBAR_SOLIDUS_SOCIAL: Literal["actionBar/social"] = "actionBar/social"
"""The values for the 'The panel to target' enum"""
_UIACTIONUIELEMENT_ACTIONBAR_SOLIDUS_EMOJIS: Literal["actionBar/emojis"] = "actionBar/emojis"
"""The values for the 'The panel to target' enum"""
_UIACTIONUIELEMENT_ACTIONBAR_SOLIDUS_REACTIONSBAR: Literal["actionBar/reactionsBar"] = (
    "actionBar/reactionsBar"
)
"""The values for the 'The panel to target' enum"""
_UIACTIONUIELEMENT_ACTIONBAR_SOLIDUS_MOVEMENTS: Literal["actionBar/movements"] = (
    "actionBar/movements"
)
"""The values for the 'The panel to target' enum"""
_UIACTIONUIELEMENT_ACTIONBAR_SOLIDUS_MAP: Literal["actionBar/map"] = "actionBar/map"
"""The values for the 'The panel to target' enum"""
_UIACTIONUIELEMENT_ACTIONBAR_SOLIDUS_SETTINGS: Literal["actionBar/settings"] = "actionBar/settings"
"""The values for the 'The panel to target' enum"""
_UIACTIONUIELEMENT_ACTIONBAR_SOLIDUS_PHOTO: Literal["actionBar/photo"] = "actionBar/photo"
"""The values for the 'The panel to target' enum"""
_UIACTIONUIELEMENT_CINEMATICVIEW_SOLIDUS_SKIP: Literal["cinematicView/skip"] = "cinematicView/skip"
"""The values for the 'The panel to target' enum"""
_UIACTIONUIELEMENT_FULLSCREENVIDEO_SOLIDUS_SKIP: Literal["fullscreenVideo/skip"] = (
    "fullscreenVideo/skip"
)
"""The values for the 'The panel to target' enum"""
_UIACTIONUIELEMENT_SOCIAL_SOLIDUS_ASSISTANT: Literal["social/assistant"] = "social/assistant"
"""The values for the 'The panel to target' enum"""
_UIACTIONUIELEMENT_SOCIAL_SOLIDUS_CHAT: Literal["social/chat"] = "social/chat"
"""The values for the 'The panel to target' enum"""
_UIACTIONUIELEMENT_SOCIAL_SOLIDUS_PLAYERS: Literal["social/players"] = "social/players"
"""The values for the 'The panel to target' enum"""
_UIACTIONUIELEMENT_SOCIAL_SOLIDUS_PLAYERPROFILE_SOLIDUS__COLON_PLAYERID: Literal[
    "social/playerProfile/:playerId"
] = "social/playerProfile/:playerId"
"""The values for the 'The panel to target' enum"""
_UIACTIONUIELEMENT_SETTINGS_SOLIDUS_HOME: Literal["settings/home"] = "settings/home"
"""The values for the 'The panel to target' enum"""
_UIACTIONUIELEMENT_SETTINGS_SOLIDUS_ABOUT: Literal["settings/about"] = "settings/about"
"""The values for the 'The panel to target' enum"""
_UIACTIONUIELEMENT_SETTINGS_SOLIDUS_VIDEO: Literal["settings/video"] = "settings/video"
"""The values for the 'The panel to target' enum"""
_UIACTIONUIELEMENT_SETTINGS_SOLIDUS_CONTROLS: Literal["settings/controls"] = "settings/controls"
"""The values for the 'The panel to target' enum"""
_UIACTIONUIELEMENT_SETTINGS_SOLIDUS_STREAMDIFFUSION: Literal["settings/streamDiffusion"] = (
    "settings/streamDiffusion"
)
"""The values for the 'The panel to target' enum"""
_UIACTIONUIELEMENT_SETTINGS_SOLIDUS_WALLETCONNECT: Literal["settings/walletconnect"] = (
    "settings/walletconnect"
)
"""The values for the 'The panel to target' enum"""
