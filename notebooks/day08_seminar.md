### 1  ―  Session  8 – Pre‑trained  Models  FTW

* Replace last week’s **random bot‑detector** with a pre‑trained model 
* Outcome today: know **where to find, how to pick  & adapt** a model

---

### 8  ―  Our Challenge: Detect Bots on youare.bot

* Input  =  full chat transcript (1‑200  messages)
* Output  =  *“human”* or *“bot”*
* **Baseline** rule‑set: heuristics on emoji count & response delay

---

### 9  ―  Zero‑shot with NLI

```text
Premise:  <dialogue>
Hypothesis: "This speaker is human."
Model:   facebook/bart‑large‑mnli
```

Classify by entailment probability   

---

### 10  ―  Few‑shot Prompt‑Tuning

* Add **3–5 labelled examples** inside the prompt
* Typical F1 jump: +8  pp over pure zero‑shot (internal test set)
* No extra training; latency ↑ only by prompt length

---

### 11  ―  Embedding Route (E5 / SBERT)

* Encode each turn → 384‑d vector; compute **cos  sim** to *human* centroid
* Fast ANN search: 0.6  ms per query on FAISS
* Sentence‑BERT reduces 10  k× pairwise comparisons → 5  s  

---

### 12  ―  Seq2Seq for NLG & QA

* BART / T5 can paraphrase or summarise dialogue style
* We score perplexity: bots often have **lower diversity** than humans
* Works well as auxiliary signal to classifier

---

 

### 14  ―  Multimodal Defence with CLIP

* CLIP maps avatar image ↔ text bio in same vector space   
* Inconsistent avatar/text pair → likely bot or catfish
* Plug‑in signal: (1–cos  sim) >  0.4 ⇒ flag

---

### 15  ―  PEFT Landscape

| Method                       | Trainable  params | Extra latency | Typical memory |
| ---------------------------- | ---------------- | ------------- | -------------- |
| Prompt‑tuning                | 0                | 0             | 0              |
| **LoRA**                     | 0.1  %            | 0             | +5  MB          |
| **QLoRA  4‑bit**              | 0.1  %            | 0             | +2  MB          |
| Adapters                     | 3–5  %            | +1  ms         | +30  MB         |
 

---

### 16  ―  LoRA Under the Hood

* Inject **rank‑r** matrices per weight (r  =  8)
* –10  000  × trainable parameters, +3  × throughput  
* No change in inference graph

---

### 17  ―  QLoRA 4‑bit Fine‑tune

* Quantise base model to **NF4 int4**; train LoRA on top
* Fits **65  B** params on a single 48  GB A6000  GPU  
* Matches 16‑bit full‑fine‑tune accuracy within ±0.2  pp

---

### 18  ―  Adapters & Prefix‑Tuning

* Pluggable MLP blocks (AdapterHub)
* Keeps vendor weights frozen; favoured by SaaS compliance teams
* 1–2  ms extra latency; fine on CPUs

---

### 19  ―  Distillation & Tiny LLM

* Teacher GPT‑J → Student DistilBERT (6 layers)
* 4  × smaller, 75  % latency drop; −1  pp F1 on our bot task

---

### 20  ―  Quantization in Practice

* fp32 →  int8: –75  % VRAM, –30  % BW
* int4  +  group‑wise scale (GPTQ) keeps <  3  % accuracy loss
* Combine **int4  +  LoRA** for best \$ 

---

### 21  ―  Model Selection Checklist

✔  Task alignment ✔  Language ✔  License ✔  VRAM budget ✔  Community activity ✔  Security (no malware weights)

---

### 22  ―  From Notebook to API

1. Load model in `model.py`
2. Wrap in FastAPI endpoint `app.py`
3. `docker-compose up --build` → local REST service
 

---

 
 

### 23 ―  Live Demo  

1️⃣ Zero‑shot with `intfloat/e5-small`
2️⃣ Train LoRA (r  =  8) –  3  min
3️⃣ Expose `/predict` in FastAPI
4️⃣ `docker-compose up` & test with `curl`

---

### 24  ―  Key Code Snippet

```python
from peft import LoraConfig, get_peft_model
base = AutoModelForSequenceClassification.from_pretrained("intfloat/e5-small")
config = LoraConfig(r=8, lora_alpha=32)
model = get_peft_model(base, config)
```

---
 