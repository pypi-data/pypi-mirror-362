# smart-thinking-llm

Для установки виртуального окружения через poetry используйте команду:

```bash
curl -sSL https://install.python-poetry.org | python3 - --version=1.8.5
export PATH="$HOME/.local/bin:$PATH"
poetry shell
```

Для скачивания данных нужно запросить к dvc у @vasgreg в тг и положить их в окружение

Далее нужно сделать:
```bash
dvc remote modify smart_thinking_llm --local access_key_id $DVC_ACCESS_KEY_ID
dvc remote modify smart_thinking_llm --local secret_access_key $DVC_SECRET_ACCESS_KEY
```

Далее для скачивания данных нужно использовать команду:
```bash
dvc pull data/raw_data.zip.dvc
```

## How to создание и сравнение графов

Установить зависимости через poetry (как выше) или через файл requirements.txt

Далее нужно скачать алиасы и сам датасет со [страницы](https://deepgraphlearning.github.io/project/wikidata5m).
Оттуда качаем [Transductive split](https://www.dropbox.com/s/6sbhm0rwo4l73jq/wikidata5m_transductive.tar.gz?dl=1) и [Entity & relation aliases](https://www.dropbox.com/s/lnbhc8yuhit4wm5/wikidata5m_alias.tar.gz?dl=1).

Разархивируем, нам понадобятся файлы `wikidata5m_transductive_train.txt`, `wikidata5m_entity.txt` и `wikidata5m_relation.txt`.

Далее можно начинать пользоваться функционалом:

```python

import os

import openai
from pathlib import Path

from smart_thinking_llm.tools.graph_creation import GraphCreator

# Initialization ~3-4 minutes
graph_creator = GraphCreator(
    entity_aliases_filepath=Path("data/raw_data/wikidata5m_alias/wikidata5m_entity.txt"),
    relation_aliases_filepath=Path("data/raw_data/wikidata5m_alias/wikidata5m_relation.txt"),
    dataset_filepath=Path("data/raw_data/wikidata5m_transductive/wikidata5m_transductive_train.txt"),
    triplets_prompt_filepath=Path("smart_thinking_llm/prompts/generate_triplets_prompt.txt"),
    openai_client=openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY")),
    triplets_model="gpt-4.1-mini-2025-04-14",
    norm_lev_threshold=0.8,
)

question = "What is the top-level Internet domain for the country where Miyankuh-e Gharbi is located?"
# first model part
# ...
# ...
answer = "Miyankuh-e Gharbi is located in Iran. The Internet country-code top-level domain for Iran is .ir."

# Ground truth from dataset
ground_truth_answer_path = "Q6884371-P17-Q794-P78-Q41774"
ground_truth_graph = graph_creator.get_graph_from_path(ground_truth_answer_path)

# Graph from model answer
graph = graph_creator(answer)

print("*"*50, "Model answer", "*"*50)
print(graph)
print("*"*50, "Ground truth", "*"*50)
print(ground_truth_graph)
print("*"*50, "Comparison", "*"*50)
print(graph.compare_to(ground_truth_graph))

================================================================
[2025-07-17 15:30:16,736: DEBUG WikiDataset] Start parsing entities aliases file...
[2025-07-17 15:30:29,799: DEBUG WikiDataset] Start parsing relation aliases file...
[2025-07-17 15:30:31,816: DEBUG WikiDataset] Start parsing dataset file...
[2025-07-17 15:30:32,496: WARNING WikiDataset] Error using mmap, falling back to standard processing: Do not use mmap
Processing chunk 1 of dataset: 100%|███████████████████████████████████████████████████████████████████████████████████████| 20614279/20614279 [01:41<00:00, 202859.48it/s]
[2025-07-17 15:32:15,236: DEBUG WikiDataset] Start creating entity2entity graph...████████████████████████████████████████▉| 20590650/20614279 [01:41<00:00, 447166.90it/s]
Creating entity2entity graph: 100%|████████████████████████████████████████████████████████████████████████████████████████| 20599278/20599278 [01:01<00:00, 336052.14it/s]
[2025-07-17 15:33:21,930: DEBUG WikiDataset] Dataset creation done!
************************************************** Model answer **************************************************
[Miyankuh-e Gharbi (Q6884371)]
└── located in the administrative territorial entity (P131): [Persian State of Iran (Q794)]
    └── top-level Internet domain (P78): [.sch.ir (Q41774)]

************************************************** Ground truth **************************************************
[Miyankuh-e Gharbi (Q6884371)]
└── country (P17): [Persian State of Iran (Q794)]
    └── top-level Internet domain (P78): [.sch.ir (Q41774)]

************************************************** Comparison **************************************************
1.0
```