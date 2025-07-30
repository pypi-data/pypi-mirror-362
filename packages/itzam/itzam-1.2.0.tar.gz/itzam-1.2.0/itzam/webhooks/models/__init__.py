from pydantic import BaseModel, Field

class CallBack(BaseModel):
  url: str = Field(..., description="The URL to which the webhook will send POST requests.")
  #optional
  headers: dict| None = Field({}, description="Optional headers to include in the webhook request.")
  custom_properties: dict|None = Field({}, description="Optional custom properties to include in the webhook request.", alias="customProperties")

class WebhookResponse(BaseModel):
  message: str = Field(..., description="A message to indicate that the webhook was queued.")
  run_id :str = Field(..., description="The unique identifier for the webhook run.", alias="runId")