# CrewAI Memory Architecture

> A detailed look at **Short-Term**, **Long-Term**, and **Entity** memory in CrewAI – what they store, how they work under the hood, and how they fit into an agent workflow.

---

## 1. Why memory matters

Large-language-model agents are stateless by default – each prompt starts from scratch.  CrewAI layers several memory components on top of LLM calls so that:

* Agents can *recall* past results within the same run (RAG-style retrieval).
* Crews can *learn* across independent runs – e.g. store prior tasks & their quality scores.
* Structured facts about *entities* (people, files, APIs…) can be accumulated and reused.

The library therefore exposes three complementary memory classes:

| Class | Scope & Lifetime | Primary Use | Default Storage Backend |
|-------|------------------|-------------|-------------------------|
| `ShortTermMemory` | **Ephemeral** – only for the current run (process memory / local sqlite file). | RAG-style retrieval of recent messages, task outputs, or observations to condition the next tool/LLM call. | `RAGStorage` (SQLite + Chroma vector index); `Mem0Storage` optional. |
| `LongTermMemory` | **Persistent** across runs & restarts. | Store task descriptions, agent names, outputs, and quality scores so future crews can reflect on past work. | `LTMSQLiteStorage` (plain SQLite table, no embeddings). |
| `EntityMemory` | **Persistent** knowledge-graph of structured facts. | Track canonical information about domain entities (name, type, description) for grounding, disambiguation, and RAG. | `RAGStorage` (separate namespace in the same SQLite/Chroma database). |

All three inherit from the minimal `crewai.memory.memory.Memory` base class, which supplies a common API:

```python
save(value: Any, metadata: dict | None = None, agent: str | None = None) -> None
search(query: str, limit: int = 3, score_threshold: float = 0.35) -> list[Any]
reset() -> None
```

---

## 2. Storage back-ends

### 2.1 RAGStorage (default for Short-Term & Entity)

```
┌──────────────────────────────┐
│   RAGStorage (SQLite + Chroma)│
├──────────────────────────────┤
│ docs table   | text   | meta │
│ embeddings   | vector | ref  │
└──────────────────────────────┘
```

* **Schema** – text chunks + JSON metadata; an accompanying Chroma vector table holds embeddings.
* **Embedding config** – passed via `embedder_config`, defaulting to OpenAI `text-embedding-3-small`.
* **Retrieval** – cosine-similarity search in Chroma followed by SQL fetch of the text & metadata.
* **Namespaces** – `type="short_term"`, `type="entities"`, etc. keep each memory space isolated.

### 2.2 LTMSQLiteStorage (default for Long-Term)

```
┌─────────────────────────────────┐
│   ltm_items (SQLite)           │
├────────┬──────────┬───────────┤
│ id PK  │ task     │ score     │
│ agent  │ metadata │ datetime  │
└────────┴──────────┴───────────┘
```
* Focuses on *chronological* storage, not semantic search – you typically pull the **latest N** items for a task.
* `metadata` may hold `{"quality": 0-1, "expected_output": "…"}` allowing the crew to evaluate itself over time.

---

## 3. Class deep-dive

### 3.1 ShortTermMemory
```python
item = ShortTermMemoryItem(data="JSON spec for endpoint /users", metadata={"task_id": 42})
mem.save(item.data, item.metadata, agent="backend_engineer")
results = mem.search("endpoint users auth", limit=5)
```
* If the crew's `memory_config["provider"] == "mem0"`, it switches to `Mem0Storage` (hosted vector DB) – otherwise local.
* Adds an *agent tag* into the metadata so retrieval can be filtered by source if desired.
* Often used by the **Task-Breaker** or **Architect** agent to fetch earlier chunk outputs.

### 3.2 LongTermMemory
```python
mem.save(LongTermMemoryItem(
  task="Generate unit tests", agent="test_engineer",
  expected_output="pytest file with ≥90% coverage",
  metadata={"quality": 0.9}
))
recent = mem.search("Generate unit tests", latest_n=3)
```
* Implements `save()` overriding the base signature to unpack the strongly-typed `LongTermMemoryItem`.
* Retrieval is chronological, not similarity-based.
* Great for *reflection* strategies (e.g., "how did we score on similar tasks last week?").

### 3.3 EntityMemory
```python
mem.save(EntityMemoryItem(name="Stripe API", type="service",
          description="REST payments API", metadata={"url": "https://stripe.com"}))
info = mem.search("payments service", limit=5)
```
* Stores concise facts; retrieval is vector-based via `RAGStorage`.
* CrewAI uses it to ground follow-up questions ("What's the base URL for Stripe?") or to avoid hallucination.

---

## 4. How they work together in a Crew run

```mermaid
flowchart TD
  subgraph Run[Single Crew Run]
    direction TB
    T1[Task 1 – Design] -->|save()| STM[Short-Term Memory]
    T1 -->|save()| ENT[Entity Memory]
    STM -- search() --> T2[Task 2 – Implement]
    ENT -- search() --> T2
    T2 -->|save()| LTM[Long-Term Memory]
  end
  style LTM fill:#fbeeca
  style STM fill:#e0f7fa
  style ENT fill:#e8eaf6
```
1. **During** the run, each agent writes its outputs to Short-Term & Entity memory; subsequent tasks query them.  
2. **After** the run completes, the final artefacts & quality scores are appended to Long-Term memory for future runs.  
3. On the *next* invocation, Long-Term and Entity memory are pre-loaded; Short-Term starts empty.

---

## 5. Security & Telemetry considerations

* Only `RAGStorage` depends on **ChromaDB**, which by default enables anonymous telemetry.  
  • Set `CHROMA_TELEMETRY_ENABLED=false` *before* import (e.g. via `sitecustomize.py`) to keep all data local.
* All default back-ends store data **locally** in the project directory unless you configure `Mem0Storage` or a remote Chroma server.

---

## 6. Practical tips

| Goal | Recommended Memory | Why |
|------|--------------------|-----|
| Keep context within a long conversation or chain-of-thought | Short-Term | fast vector search across recent content. |
| Build institutional knowledge over days/weeks | Long-Term | timestamped log optimised for chronological lookup. |
| Maintain factual catalogue (APIs, people, projects) | Entity | semantically searchable + structured. |

---

### Example crew snippet
```python
crew = HierarchicalCrew(
    agents=all_agents,
    tasks=all_tasks,
    long_term_memory=LongTermMemory(path="./memory/long_term.db"),
    short_term_memory=ShortTermMemory(embedder_config={
        "provider": "openai",
        "config": {"model": "text-embedding-3-small"}
    }),
    entity_memory=EntityMemory()
)
```

---

### Further reading
* CrewAI docs – https://docs.crewai.com/memory  
* ChromaDB – https://docs.trychroma.com/  
* Retrieval-Augmented Generation (RAG) – https://research.ibm.com/blog/retrieval-augmented-generation 