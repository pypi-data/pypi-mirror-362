from datetime import datetime

class MediaData:
    """
    Represents media data with various attributes such as type, IDs, 
    filenames, MIME type, alternate text, and timestamps.
    """

    # Static variable for tracking media data IDs
    mediaData_id = -1

    def __init__(self):
        """
        Initialize a MediaData instance with default attributes.

        Attributes:
            Type (str): The type of media data (e.g., 'image', 'video').
            Id (int): Unique identifier for the media data.
            ZoneId (str): Zone identifier.
            CameraId (str): Camera identifier.
            MotTrackerId (int): Motion tracker identifier.
            EdgeFilename (str): Filename for edge storage.
            MotEdgeFilename (str): Filename for motion edge storage.
            MIMEType (str): MIME type of the media.
            AltText (str): Alternate text description.
            RawData (str): Base64 encoded binary data.
            DetectedStart_tm (float): Start time of detection.
            DetectedEnd_tm (float): End time of detection.
        """

        self.Type: str = ""

        # MediaData ID logic
        if MediaData.mediaData_id == -1:
            MediaData.mediaData_id = self.__get_media_data_id()
        MediaData.mediaData_id = MediaData.mediaData_id + 1
        self.Id: int = MediaData.mediaData_id

        # Initialize other attributes
        self.ZoneId: str = ""
        self.CameraId: str = ""
        self.MotTrackerId: int = None
        self.EdgeFilename: str = ""
        self.MotEdgeFilename: str = ""
        self.MIMEType: str = ""
        self.AltText: str = ""
        self.RawData: str = ""  # Base64 encoded binary data
        self.DetectedStart_tm: float = 0
        self.DetectedEnd_tm: float = 0

    def __get_media_data_id(self) -> int:
        """
        Generate a media data ID based on the number of seconds from the start 
        of the year to the current moment, multiplied by 10.

        Returns:
            int: A unique media data ID based on the time elapsed from the start of the year.
        """

        utcnow = datetime.utcnow()
        beginning_of_year = datetime(utcnow.year, 1, 1)
        time_difference = utcnow - beginning_of_year
        return int(time_difference.total_seconds() * 10)
