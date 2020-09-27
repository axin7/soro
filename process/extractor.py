"""
该模块进行实体提取
为 Rasa-nlu 中的自定义component
"""

import ast

from rasa.nlu.components import Component
from rasa.nlu import utils
from rasa.nlu.model import Metadata

from flashtext import KeywordProcessor
from process.model import InFo,App


class AppExtractor(Component):
    """A pre-trained sentiment component"""

    name = "appextractor"
    provides = ["entities"]
    requires = []
    defaults = {}
    language_list = ["zh"]

    # def __init__(self, component_config=None):
    #     pass

    # def train(self, training_data, cfg, **kwargs):
    #     """Not needed, because the the model is pretrained"""
    #     pass



    def save_to_app(self, app_name):
        """Convert model output into the Rasa NLU compatible output format."""
        
        entity = {"value": app_name,
                  "confidence": 1,
                  "entity": "app_name",
                  "extractor": "appextractor"}

        return entity


    def process(self, message, **kwargs):
        """Retrieve the text message, pass it to the classifier
            and append the prediction results to the message class."""

        # 提取应用实体
        app_keyword_processor = KeywordProcessor()
        query = InFo.select(InFo.content).where(InFo.name=="app_kw_dict")
        app_dict = ast.literal_eval(query[0].content)
        app_keyword_processor.add_keywords_from_dict(app_dict)
        # print(f'query为：{message.text}')

        try:
            app_name = app_keyword_processor.extract_keywords(message.text)[0]
            # print(f'app_name词槽为：{app_name}')
            entity = self.save_to_app(app_name)
            message.set("entities", [entity], add_to_output=True)
        except Exception as ex:
            print(ex)

    # def persist(self, model_dir):
    #     """Pass because a pre-trained model is already persisted"""

    #     pass