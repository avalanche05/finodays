import models
import data.__all_models as db_models


def create_cfa_image(user_id: int, create_cfo_image_dto: models.CreateCfaImageDTO):
    cfa_image = db_models.cfa_image.CfaImage()