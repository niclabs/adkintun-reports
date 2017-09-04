from app import db1, application
from app.models_server.base_model import BaseModel


class VideoResult(BaseModel):
    '''
    Video Results model class
    '''
    __tablename__ = 'video_results'

    id = db1.Column(db1.Integer, primary_key=True)
    quality = db1.Column(db1.String(50))
    buffering_time = db1.Column(db1.BigInteger)
    loaded_fraction = db1.Column(db1.Float)
    downloaded_bytes = db1.Column(db1.BigInteger)

    # relationships
    media_test_report_id = db1.Column(db1.Integer, db1.ForeignKey("media_test_reports.id"))

    def __init__(self, quality=None, buffering_time=None, loaded_fraction=None, downloaded_bytes=None):
        self.quality = quality
        self.buffering_time = buffering_time
        self.loaded_fraction = loaded_fraction
        self.downloaded_bytes = downloaded_bytes

    def __repr__(self):
        return '<VideoResults, id: %r, downloaded bytes: %r, quality: %r>' % (
            self.id, self.downloaded_bytes, self.quality)

    @staticmethod
    def add_video_result(args: dict):
        """
        Create a new video result object from a dict
        :param args: dict with video result data
        :return: video result object
        """
        if "downloaded_bytes" in args and "quality" in args and "buffering_time" in args and "loaded_fraction" in args:
            vr = VideoResult(quality=args["quality"], buffering_time=args["buffering_time"],
                             downloaded_bytes=args["downloaded_bytes"], loaded_fraction=args["loaded_fraction"])
            db1.session.add(vr)
            try:
                db1.session.commit()
            except Exception as e:
                db1.session.rollback()
                application.logger.error("Error adding video result.")
                return None
            return vr
        else:
            return None
