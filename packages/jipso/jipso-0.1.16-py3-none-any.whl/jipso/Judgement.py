from pydantic import BaseModel, ConfigDict


class Judgement(BaseModel):
  """Represents the AI system or evaluator performing analysis.
  
  The Judgement component (J) encapsulates the reasoning entity - whether it's
  an AI model, human expert, or ensemble of evaluators. This class manages
  AI platform connections, evaluation methodologies, and consensus mechanisms
  for systematic AI evaluation workflows.
  
  Supports multiple AI platforms including Anthropic, OpenAI, Google, and local
  deployments. Enables ensemble operations with weighted voting and distributed
  consensus building for enhanced reliability and bias reduction.
  """
  
  model_config = ConfigDict(extra='allow')
  
  def __str__(self) -> str: pass
  