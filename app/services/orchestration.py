from app.flows.launch_strategy_flow import LaunchStrategyFlow
from app.schemas import LaunchRequest, LaunchResponse


def run_launch_strategy(request: LaunchRequest) -> LaunchResponse:
    flow = LaunchStrategyFlow()
    flow.state.request = request
    result = flow.kickoff()
    return result
