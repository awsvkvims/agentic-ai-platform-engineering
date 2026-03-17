run:
	PYTHONPATH=. python -m scripts.agent_cli

eval:
	PYTHONPATH=. python -m scripts.eval_prompts

graph:
	PYTHONPATH=. python -m scripts.visualize_graph

test:
	PYTHONPATH=. pytest