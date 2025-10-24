import json
import requests
from openai import OpenAI

CONCIERGE_URL = "http://localhost:8081"

SYSTEM_PROMPT = """You are an AI assistant with access to a concierge service.

Available signals:

1. To initiate a concierge workflow:
   {"__signal__": "initiate_conversation", "prompt": "<N/A>"}

2. To call the concierge service:
   {"__signal__": "call_concierge", "message": <your_concierge_payload>}

3. To request user input:
   {"__signal__": "request_input", "prompt": "<your_message for the user>"}

4. To end the current concierge session (user conversation continues):
   {"__signal__": "terminate"}

Note: The user will type "exit" when they want to end the entire conversation.

You are only allowed to respond back in JSON with the above format. Any message MUST include the __signal__ key."""


class Client:
    def __init__(self, api_base: str, api_key: str):
        self.llm = OpenAI(base_url=api_base, api_key=api_key)
        self.messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        self.session_id = None
    
    def handshake(self) -> str:
        request_payload = {"action": "handshake"}
        print(f"\n[CLIENT → SERVER] {json.dumps(request_payload)}")
        
        response = requests.post(CONCIERGE_URL, json=request_payload)
        self.session_id = response.headers.get('X-Session-Id')
        
        print(f"[SERVER → CLIENT] {response.text}")
        return response.text

    def chat(self, user_input: str) -> str:
        self.messages.append({"role": "user", "content": user_input})
        
        print(f"\n[CLIENT → LLM] {json.dumps(self.messages[-1])}")
        
        response = self.llm.chat.completions.create(
            model="gpt-4",
            messages=self.messages
        )
        
        reply = response.choices[0].message.content
        self.messages.append({"role": "assistant", "content": reply})
        
        print(f"[LLM → CLIENT] {reply}")
        
        return reply

    def call_concierge(self, llm_message: str) -> str:
        try:
            envelope = json.loads(llm_message)
            payload = envelope.get("message", {})
            
            headers = {}
            if self.session_id:
                headers["X-Session-Id"] = self.session_id
            
            print(f"\n[CLIENT → SERVER] {json.dumps(payload)}")
            if headers:
                print(f"[HEADERS] {json.dumps(headers)}")
            
            response = requests.post(CONCIERGE_URL, json=payload, headers=headers)
            
            if 'X-Session-Id' in response.headers:
                self.session_id = response.headers['X-Session-Id']
            
            print(f"[SERVER → CLIENT] {response.text}")
            
            return response.text
        except Exception as e:
            return f"Error calling concierge: {e}"

    def process_response(self, reply: str) -> tuple[bool, str]:
        try:
            data = json.loads(reply)
            signal = data.get("__signal__")
            
            if signal == "call_concierge":
                result = self.call_concierge(reply)
                llm_response = self.chat(f"Concierge response: {result}")
                return self.process_response(llm_response)
            
            elif signal == "request_input":
                prompt = data.get("prompt", "Please provide input:")
                return False, prompt

            elif signal == "initiate_conversation":
                result = self.handshake()
                llm_response = self.chat(f"Concierge response: {result}")
                return self.process_response(llm_response)
                
            elif signal == "respond":
                self.session_id = None
                message = data.get("message", "Task completed.")
                return False, message
            else:
                return False, f"Unknown signal: {signal}"
        except json.JSONDecodeError:
            return False, f"Invalid JSON: {reply}"

    def run(self):
        while True:
            try:
                user_input = input("You: ").strip()
                if not user_input:
                    continue
                if user_input.lower() == "exit":
                    break
                    
                reply = self.chat(user_input)
                should_exit, output = self.process_response(reply)
                
                print(f"Assistant: {output}\n")
                
                if should_exit:
                    break
                    
            except KeyboardInterrupt:
                print("\nExiting...")
                break
            except Exception as e:
                print(f"Error: {e}\n")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 3:
        print("Usage: python client.py <api_base> <api_key>")
        sys.exit(1)
    
    api_base = sys.argv[1]
    api_key = sys.argv[2]
    
    client = Client(api_base, api_key)
    client.run()

