class FaceDetectorEventListener:
    CENTER = 'center'
    RIGHT = 'right'
    LEFT = 'left'

    def on_valid_face_present(self, present):
        """
        Called when a face is being detected for a certain amount of time.
        """
        pass

    def on_face_position(self, position):
        """
        Called when a face <change> position in the camera window.
        <change> := if a face stay in a specified part of the screen the method is NOT called. It's called
        only if the face switch from a section to another.

        Arguments:
             position: Position of the face in the camera window
        """
        pass
