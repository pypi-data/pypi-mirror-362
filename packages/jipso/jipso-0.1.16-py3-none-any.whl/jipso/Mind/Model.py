import os, ujson

class Model:
  def __init__(self, id):
    self.id = id
    models_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'models.json'))
    with open(models_path, 'r') as f: models = ujson.load(f)
    if self.id not in models:
      raise ValueError(f'Model {self.id} not exsits')
    
    self.platform = models[self.id]['platform']
    if self.platform == 'Openai':
      from jipso.Mind.Client import ClientOpenai
      self.client = ClientOpenai()
    elif self.platform == 'Anthropic':
      from jipso.Mind.Client import ClientAnthropic
      self.client = ClientAnthropic()
    elif self.platform == 'Gemini':
      from jipso.Mind.Client import ClientGemini
      self.client = ClientGemini()
    elif self.platform == 'Xai':
      from jipso.Mind.Client import ClientXai
      self.client = ClientXai()
    elif self.platform == 'Alibabacloud':
      from jipso.Mind.Client import ClientAlibabacloud
      self.client = ClientAlibabacloud()
    elif self.platform == 'Byteplus':
      from jipso.Mind.Client import ClientByteplus
      self.client = ClientByteplus()
    elif self.platform == 'Sberbank':
      from jipso.Mind.Client import ClientSberbank
      self.client = ClientSberbank()
