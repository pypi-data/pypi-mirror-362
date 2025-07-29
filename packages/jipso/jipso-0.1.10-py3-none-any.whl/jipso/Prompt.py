from pydantic import BaseModel, ConfigDict


class Prompt(BaseModel):
  """Encapsulates instructions and methodology for AI execution.
  
  The Prompt component (P) defines HOW tasks should be performed - methodology,
  approach, and specific instructions. Provides systematic prompt engineering
  capabilities including decomposition for complex workflows and union operations
  for modular prompt construction.
  
  Enables natural language programming through conversational prompt development,
  iterative improvement cycles, and template-based prompt optimization. Supports
  role assignment, few-shot learning integration, and constraint specification
  for precise AI behavior control.
  """

  model_config = ConfigDict(extra='allow')
  
  def __str__(self) -> str: pass
  