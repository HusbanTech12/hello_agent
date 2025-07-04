import os
from agents import Agent,Runner,OpenAIChatCompletionsModel,AsyncOpenAI,RunConfig,handoff,RunContextWrapper,HandoffInputData
from dotenv import load_dotenv

load_dotenv()

gemini_api_key = os.getenv('GEMINI_API_KEY')

provider = AsyncOpenAI(
    api_key = gemini_api_key,
    base_url= 'https://generativelanguage.googleapis.com/v1beta/openai',
    
    
)

model = OpenAIChatCompletionsModel(
  model = 'gemini-2.0-flash',
  openai_client = provider,  
)    


config = RunConfig(                    
   model = model,
   model_provider = provider,
   tracing_disabled = True                 
)                   

Nextjs_agent = Agent(
  name = 'Nextjs Assistant',
  instructions='you are a helpful assistant that provides information and answers questions to the best of your ability.',
)

Python_agent = Agent(
  name = 'Nextjs Assistant',
  instructions='you are a helpful assistant that provides information and answers questions to the best of your ability.',
)

async def on_handoff(ctx: RunContextWrapper[None]):
  print(f'Nextjs handoff triggered with contex')
  
  
def handoff_input_filter(inputData:HandoffInputData):
  return HandoffInputData(
    input_history= input.input_history,
    pre_handoff_items= input.pre_handoff_items,
    new_items= input.new_items
  )  
  

handoff_obj = handoff(
  agent = Nextjs_agent,
  on_handoff = on_handoff,
  input_filter=handoff_input_filter,
)

Triage_agent = Agent(
  name = 'Triage Assistant',
  instructions='you are a helpful assistant that navigate between nextjs and python the best response based on the query.',
  handoffs=[handoff_obj , Python_agent]
  
)

result = Runner.run_sync(Triage_agent , 'I want to get help regarding python decorators', run_config=config) # config directly render nh hoga because first parameter jo hota h positional argument hota h but jo second and soo on argument hoter h wo key , value arguments hote hn tu yahan key run_config and value config hogi.


# print('Final Output :',result.final_output)
# print('Current Agent :',result.last_agent)
