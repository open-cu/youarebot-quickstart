# 💼 Lecture: Pre-trained Models in Data Scientist and MLE Work

**Format**: 2 hours  
**Tools**: Jupyter Notebooks (10–20 pieces)  
**Goal**: to show where and how to use pre-trained models for real tasks, in which cases they work "out of the box", when they require fine-tuning, and where they are useless.  

---

## 🧩 Lecture Structure

### 🔷 1. Introduction (10 min)

#### What are pre-trained models?
Pre-trained models are neural networks that have been trained on large, general datasets and then made available for reuse. Think of them as "smart building blocks" that already understand patterns in data.

**Key characteristics:**
- Trained on massive datasets (billions of tokens, millions of images)
- Learn general representations that transfer across tasks
- Available as downloadable checkpoints
- Can be used directly or fine-tuned for specific tasks

**Examples:**
- **BERT**: trained on 3.3B words from Wikipedia + BookCorpus
- **ResNet**: trained on ImageNet (1.2M images, 1000 classes)
- **GPT models**: trained on internet-scale text data

#### Why Pre‑trained Models?

**🚀 Speed to Market**
- Traditional approach: 3-6 months to train from scratch
- Pre-trained approach: Days to weeks for deployment

**💰 Cost Efficiency**
- Shifts cost from unpredictable training to predictable inference
- Training once, use everywhere principle
- Democratizes access to state-of-the-art models

**📈 Performance Benefits**
- Often outperform models trained from scratch on small datasets
- Benefit from transfer learning
- Built-in robustness from diverse training data

#### Economics vs Quality Analysis

| Scenario                     | Up‑front cost | Inference cost                    | Typical F1 gain | Time to deploy |
| ---------------------------- | ------------- |-----------------------------------| --------------- | -------------- |
| Train BERT‑base from scratch |  ≈  \$50k GPUs | ≈  \$0.001 /  req                 |  –              | 3-4 months     |
| **GPT‑4o  mini** API          |  \$0          | **\$0.40  /  M  input tokens**    |  +10‑15  pp      | Same day       |
| LoRA‑tuned open‑model        |  ≤  \$300      | ≈  \$0.0002 /  req                |  +8‑12  pp       | 1-2 weeks      |

**Key insights:**
- APIs are fastest but most expensive long-term
- Fine-tuning offers best cost/performance balance
- Training from scratch only makes sense for very specific domains

#### Where to Find Pre-trained Models

**🤗 Hugging Face Hub** (Primary source)
- 1.8M+ model checkpoints
- Advanced filtering: by task, license, language, size
- Model cards with usage examples and limitations
- Integration with `transformers`, `diffusers`, `timm`

**Framework-Native Sources**
- **TorchHub**: PyTorch models with `torch.hub.load()`
- **TensorFlow Hub**: TensorFlow models
- **timm**: 1000+ computer vision models
- **sklearn**: Traditional ML models

**Research Sources**
- **Papers with Code**: Latest research with code
- **GitHub repositories**: Direct from authors
- **arXiv**: Cutting-edge research (may need implementation)

#### Usage Modes (The Pre-trained Spectrum)

**🎯 Zero-shot** (No additional training)
- Use model directly out-of-the-box
- Best for: general tasks, proof-of-concepts
- Example: `pipeline("sentiment-analysis", "I love this product!")`

**📝 Few-shot** (In-context learning)
- Provide examples in the prompt
- Best for: GPT-style models, quick prototyping
- Example: "Translate English to French: Hello -> Bonjour, Goodbye -> ?"

**🔧 Fine-tuning** (Additional training)
- Train on your specific data
- Best for: domain-specific tasks, production systems
- Methods: full fine-tuning, LoRA, adapter layers

**💡 When to use which approach:**
- Start with zero-shot for validation
- Use few-shot for rapid prototyping
- Fine-tune for production and domain-specific needs

📌 _Demo 1_: Live demonstration of `transformers.pipeline("sentiment-analysis")`
```python
from transformers import pipeline
classifier = pipeline("sentiment-analysis")
result = classifier("I love using pre-trained models!")
# Output: [{'label': 'POSITIVE', 'score': 0.9998}]
```

---

### 🧠 2. NLP (30 min)
**Tasks**:
- Classification (sentiment and topic)
- NER (entity extraction)
- Translation
- Summarization
- Zero-shot classification

📌 _Demo 2_: text classification  
📌 _Demo 3_: NER  
📌 _Demo 4_: text translation  
📌 _Demo 5_: zero-shot (`facebook/bart-large-mnli`)  
📌 _Demo 6_: text generation (T5)

🧩 Limitations:
- Context < 512/1024 tokens
- Poor performance on domain-specific vocabulary
- Often require fine-tuning

📌 _Demo 7_: model fine-tuning via PEFT/LoRA

---

### 🧠 3. Computer Vision (30 min)

**Tasks**:
- Classification
- Object detection
- Segmentation
- OCR

📌 _Demo 8_: classification with `timm`  
📌 _Demo 9_: object detection (YOLOv8)  
📌 _Demo 10_: segmentation (`DeepLabV3`, `SAM`)  
📌 _Demo 11_: OCR (`TrOCR`, `pytesseract`)

🧩 Limitations:
- Poor performance on medical/satellite/custom images
- Class limitations

📌 _Demo 12_: fine-tuning classifier on custom data

---

### 🧠 4. Multimodal Models (15 min)

📌 _Demo 13_: CLIP — text and image matching  
📌 _Demo 14_: BLIP-2 — image captioning  
📌 _Demo 15_: DINOv2 + FAISS — similar image search

🧩 Limitations:
- Interpretability
- Applicability in narrow tasks

---

### 🧠 5. Audio and Time Series (15 min)

**Tasks**:
- Audio classification
- ASR (speech recognition)
- Forecasting

📌 _Demo 16_: audio classification (`speechbrain`, `torchaudio`)  
📌 _Demo 17_: Wav2Vec2 (speech-to-text)  
📌 _Demo 18_: time series (`nixtla`, `gluonts`)

🧩 Limitations:
- Noise, accents, frequency
- Few pre-trained models available

---

### 🧠 6. Graph ML (5 min)

📌 _Demo 19_: GCN on Cora (with PyG)  
🧩 Limitations: poor scalability, require graph preparation

---

### 🧠 7. Code models (5 min)

📌 _Demo 20_: auto-generation of SQL or code using StarCoder / CodeT5  
🧩 Limitations: licensing issues, require result validation

---

### ⚠️ 8. Where pre-trained models don't work (10 min)

🛑 Don't work:
- Tabular ML tasks (like XGBoost)  
- Specific metrics/formulas/business logic

🟡 Partially work:
- Tabular: `TabPFN`, `AutoGluon`  
📌 _Demo 21_: TabPFN on tabular task

---

### 🔐 9. Licenses and Legal Restrictions (10 min)

**License types**:
- Apache 2.0 / MIT — ✅ commercial use
- CC BY-NC — ❌ cannot use in production
- RAIL — ⚠️ usage restrictions (e.g., military)
- OpenRAIL-M / BigScience RAIL

📌 _Demo 22_: `model_info("bigscience/bloom").license`

**How to check**:
- HuggingFace → README / Model Card
- GitHub → LICENSE.md

🧠 Case study: can GPT-2 be used in a corporate assistant?

---

### ✅ 10. Wrap-up (10 min)

- Quick model selection checklist:
  1. Is there a suitable task in the repository?
  2. Does zero-shot work?
  3. Is fine-tuning needed?
  4. Is the license suitable?
- Resources:
  - [https://huggingface.co/models](https://huggingface.co/models)
  - [https://paperswithcode.com](https://paperswithcode.com)
  - [https://github.com/rwightman/pytorch-image-models](https://github.com/rwightman/pytorch-image-models)
- Homework:
  - choose 1 task
  - find 2–3 models
  - test "out of the box"
  - evaluate fine-tuning possibility
  - evaluate license
