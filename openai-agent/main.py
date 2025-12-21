from dotenv import load_dotenv
from experiments import ExperimentMetadata, Model, Intensity
from experiments.final_report2025.agent import run as run_agent
from experiments.final_report2025.workflow import run as run_workflow
from financial_agents.financial_analyst import IndicatorOutput

load_dotenv()

WRITE_FOLDER = "/Users/thiagocastroferreira/Desktop/kubernetes/results/final_report2025"

print("GPT-4.1 Mini (no reflection)")
experiment = ExperimentMetadata(
    model=Model.GPT_4_1_MINI,
    write_folder=WRITE_FOLDER,
    max_turns=30,
    structured_output=IndicatorOutput.model_json_schema(),
    reflection=False,
)
run_agent(experiment_metadata=experiment)
run_workflow(experiment_metadata=experiment)

print("\n\nGPT-4.1 Mini (with  reflection)")
experiment = ExperimentMetadata(
    model=Model.GPT_4_1_MINI,
    write_folder=WRITE_FOLDER,
    max_turns=30,
    structured_output=IndicatorOutput.model_json_schema(),
    reflection=True,
)
run_agent(experiment_metadata=experiment)
run_workflow(experiment_metadata=experiment)

print("GPT-4.1 Nano (no reflection)")
experiment = ExperimentMetadata(
    model=Model.GPT_4_1_NANO,
    write_folder=WRITE_FOLDER,
    max_turns=30,
    structured_output=IndicatorOutput.model_json_schema(),
    reflection=False,
)
run_agent(experiment_metadata=experiment)
run_workflow(experiment_metadata=experiment)

print("\n\nGPT-4.1 Nano (with  reflection)")
experiment = ExperimentMetadata(
    model=Model.GPT_4_1_NANO,
    write_folder=WRITE_FOLDER,
    max_turns=30,
    structured_output=IndicatorOutput.model_json_schema(),
    reflection=True,
)
run_agent(experiment_metadata=experiment)
run_workflow(experiment_metadata=experiment)

print("GPT-5 Mini (no reflection)")
experiment = ExperimentMetadata(
    model=Model.GPT_5_MINI,
    write_folder=WRITE_FOLDER,
    max_turns=30,
    structured_output=IndicatorOutput.model_json_schema(),
    reasoning=Intensity.MEDIUM,
    verbosity=Intensity.MEDIUM,
    reflection=False,
)
run_agent(experiment_metadata=experiment)
run_workflow(experiment_metadata=experiment)

print("\n\nGPT-5 Mini (with  reflection)")
experiment = ExperimentMetadata(
    model=Model.GPT_5_MINI,
    write_folder=WRITE_FOLDER,
    max_turns=30,
    structured_output=IndicatorOutput.model_json_schema(),
    reasoning=Intensity.MEDIUM,
    verbosity=Intensity.MEDIUM,
    reflection=True,
)
run_agent(experiment_metadata=experiment)
run_workflow(experiment_metadata=experiment)

print("GPT-5 Nano (no reflection)")
experiment = ExperimentMetadata(
    model=Model.GPT_5_NANO,
    write_folder=WRITE_FOLDER,
    max_turns=30,
    structured_output=IndicatorOutput.model_json_schema(),
    reasoning=Intensity.MEDIUM,
    verbosity=Intensity.MEDIUM,
    reflection=False,
)
run_agent(experiment_metadata=experiment)
run_workflow(experiment_metadata=experiment)

print("\n\nGPT-5 Nano (with  reflection)")
experiment = ExperimentMetadata(
    model=Model.GPT_5_NANO,
    write_folder=WRITE_FOLDER,
    max_turns=30,
    structured_output=IndicatorOutput.model_json_schema(),
    reasoning=Intensity.MEDIUM,
    verbosity=Intensity.MEDIUM,
    reflection=True,
)
run_agent(experiment_metadata=experiment)
run_workflow(experiment_metadata=experiment)
