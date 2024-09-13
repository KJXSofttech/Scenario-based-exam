from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
import traceback

# Initialize the LLM
llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", verbose=False, temperature=0.5, google_api_key="AIzaSyC-rVIkqo29VSv3wWojloYqS8T4V2gP-NQ")

# Prompt template for generating scenario-based questions
scenario_prompt_template = PromptTemplate(
    input_variables=["profession"],
    template="""
    You are a professional scenario designer. Generate 2 scenario-based questions for a {profession}. Each scenario should present a practical situation requiring critical thinking and problem-solving skills relevant to the profession. 
    
    Please format the scenarios as follows:
    **Scenario 1:**
    [Describe the scenario]
    
    Question: [Ask a question related to the scenario]
    
    **Scenario 2:**
    [Describe the scenario]
    
    Question: [Ask a question related to the scenario]
    """
)

def generate_scenarios(profession):
    scenarios_prompt = scenario_prompt_template.format(profession=profession)
    response = llm.invoke(input=scenarios_prompt)

    if hasattr(response, "content"):
        scenarios_content = response.content
        scenarios = []

        current_scenario = None
        for line in scenarios_content.splitlines():
            line = line.strip()
            
            if line.startswith("**Scenario"):
                if current_scenario:
                    scenarios.append(current_scenario)
                current_scenario = {"scenario": "", "question": ""}
            elif current_scenario is not None:
                if line.startswith("Question:"):
                    current_scenario["question"] = line[9:].strip()
                else:
                    current_scenario["scenario"] += line + " "

        if current_scenario:
            scenarios.append(current_scenario)

        return scenarios

    else:
        raise ValueError("Unexpected response format from the language model")

def present_scenarios(scenarios):
    answers = []
    for i, scenario in enumerate(scenarios, 1):
        print(f"\n**Scenario {i}:**")
        print(scenario['scenario'].strip())
        print(f"\nQuestion: {scenario['question']}")
        answer = input("Your answer: ").strip()
        answers.append(answer)
    return answers

def generate_result(profession, scenarios, answers):
    result_prompt = f"""
    Analyze the following scenario-based responses for a {profession}:

    Scenario 1: {scenarios[0]['scenario']}
    Question: {scenarios[0]['question']}
    Answer: {answers[0]}

    Scenario 2: {scenarios[1]['scenario']}
    Question: {scenarios[1]['question']}
    Answer: {answers[1]}

    Please provide a brief analysis of the responses, considering the following:
    1. Critical thinking and problem-solving skills demonstrated
    2. Application of professional knowledge
    3. Areas of strength
    4. Areas for improvement

    Format the result as follows:
    **Analysis:**
    [Your analysis here]

    **Strengths:**
    - [Strength 1]
    - [Strength 2]

    **Areas for Improvement:**
    - [Area 1]
    - [Area 2]

    **Overall Assessment:**
    [Brief overall assessment]
    """

    response = llm.invoke(input=result_prompt)
    return response.content if hasattr(response, "content") else "Error generating result"

def main():
    try:
        name = input("Enter your name: ").strip()
        profession = input("Enter your profession: ").strip()

        print("Generating scenarios... This may take a moment.")
        scenarios = generate_scenarios(profession)
        
        print(f"\nGenerated {len(scenarios)} scenarios.")
        
        answers = present_scenarios(scenarios)

        print("\nGenerating result... This may take a moment.")
        result = generate_result(profession, scenarios, answers)

        print("\nScenario-Based Assessment Result")
        print("=================================")
        print(f"Name: {name}")
        print(f"Profession: {profession}")
        print("\n" + result)

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    main()