<!-- Title Image Placeholder -->
# AIRAS - an open-source project for research automation

![Airas Logo](https://i.imgur.com/BNFAt17.png)

<p align="center">
  <a href="https://pypi.org/project/airas/">
    <img src="https://img.shields.io/pypi/v/airas" alt="Documentation" />
  </a>
  <a href="https://airas-org.github.io/airas/">
    <img src="https://img.shields.io/badge/Documentation-%F0%9F%93%95-blue" alt="Documentation" />
  </a>
  <a href="https://github.com/airas-org/airas/blob/main/LICENSE">
    <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="MIT License" />
  </a>
  <a href="https://discord.gg/ktumZQP3Tp">
    <img src="https://img.shields.io/badge/Discord-Join%20Us-7289da?logo=discord&logoColor=white" alt="Discord" />
  </a>
  <a href="https://x.com/fuyu_quant">
    <img src="https://img.shields.io/twitter/follow/fuyu_quant?style=social" alt="Twitter Follow" />
  </a>
</p>


AIRAS is an open-source software framework for automated research, being developed to support the entire research workflow. It aims to integrate all of the necessary functions for automating research—from literature search and method generation to experimentation and paper writing—and is designed with the aim of enabling as many individuals and organizations as possible to contribute to open innovation in research automation. 

Currently, it focuses on the automation of machine learning research.

Unlike other automated research agents such as [AI Scientist](https://github.com/SakanaAI/AI-Scientist), AIRAS has the following key features:

Features
- Implemented by individual research processes
- Enables users to implement flexible and customized research workflows
- Allows users to add their own original research processes

## Quick Start

It can be easily used by simply installing it via pip as shown below.

**Note: The package is currently under preparation and will be available on PyPI soon.**

```bash
pip install airas
```

It is implemented by individual research processes, allowing users to design their own automated research workflows freely.

```python
from airas.preparation import PrepareRepository
from airas.retrieve import (
  RetrieveCodeSubgraph, 
  RetrievePaperFromQuerySubgraph, 
  RetrieveRelatedPaperSubgraph
)
from airas.create import (
  CreateExperimentalDesignSubgraph, 
  CreateMethodSubgraph
)
from airas.execution import (
  ExecutorSubgraph, 
  FixCodeSubgraph, 
  PushCodeSubgraph
)


retriever = RetrievePaperFromQuerySubgraph(llm_name=llm_name, save_dir=save_dir, scrape_urls=scrape_urls)
retriever2 = RetrieveRelatedPaperSubgraph(llm_name=llm_name, save_dir=save_dir, scrape_urls=scrape_urls)
retriever3 = RetrieveCodeSubgraph(llm_name=llm_name)
creator = CreateMethodSubgraph(llm_name=llm_name)
creator2 = CreateExperimentalDesignSubgraph(llm_name=llm_name)
coder = PushCodeSubgraph()
executor = ExecutorSubgraph()
fixer = FixCodeSubgraph(llm_name=llm_name)


state = {
    "base_queries": "diffusion model",
    "gpu_enabled": True,
    "experiment_iteration": 1
}

state = retriever.run(state)
state = retriever2.run(state)
state = retriever3.run(state)
state = creator.run(state)
state = creator2.run(state)
state = coder.run(state)
state = executor.run(state)
state = fixer.run(state)
```

## Roadmap

- [ ] Complete automation of machine learning research with code-based experimentation
- [ ] Autonomous research in robotics
- [ ] Autonomous research in various fields

## Contact

We are exploring best practices for human-AI collaboration in automated AI research. Together, we're investigating how new research workflows—powered by both human insight and AI agents—can accelerate discovery, improve reproducibility, and give organizations a competitive edge in the age of autonomous research.

If you are interested in this topic, please feel free to contact us at <a href="mailto:ulti4929@gmail.com">ulti4929@gmail.com</a>.

## About AutoRes

This OSS is developed as part of the [AutoRes](https://www.autores.one/english) project.

## Citation

If you use AIRAS in your research, please cite as follows:

```
@software{airas2025,
  author = {Toma Tanaka, Takumi Matsuzawa, Yuki Yoshino, Ilya Horiguchi, Shiro Takagi, Ryutaro Yamauchi, Wataru Kumagai},
  title = {AIRAS},
  year = {2025},
  publisher = {GitHub},
  url = {https://github.com/airas-org/airas}
}
```
