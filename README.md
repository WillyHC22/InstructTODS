# InstrucTODS: Large Language Models for End-to-End Task-Oriented Dialogue Systems

**Paper**: https://arxiv.org/pdf/2310.08885.pdf

**Abstract**: Large language models (LLMs) have been used for diverse tasks in natural language processing (NLP), yet remain under-explored for task-oriented dialogue systems (TODS), especially for end-to-end TODS. We present InstructTODS, a novel off-the-shelf framework for zero-shot end-to-end task-oriented dialogue systems that can adapt to diverse domains without fine-tuning. By leveraging LLMs, InstructTODS generates a proxy belief state that seamlessly translates user intentions into dynamic queries for efficient interaction with any KB. Our extensive experiments demonstrate that InstructTODS achieves comparable performance to fully fine-tuned TODS in guiding dialogues to successful completion without prior knowledge or task-specific data. Furthermore, a rigorous human evaluation of end-to-end TODS shows that InstructTODS produces dialogue responses that notably outperform both the gold responses and the state-of-the-art TODS in terms of helpfulness, informativeness, and humanness. Moreover, the effectiveness of LLMs in TODS is further supported by our comprehensive evaluations on TODS subtasks: dialogue state tracking, intent classification, and response generation.

Framework of the current system:
![Alt text](imgs/Framework.png?raw=true "Framework")

Here is a sample of interaction with a user asking random general knowledge question to the dialogue system mixed with some task-oriented questions. The system detects when it is appropriate to use the private knowledge base (for restaurant recommendation in this case), and when it should rely on its own general knowledge to answer the questions:
![Alt text](imgs/Demo.png?raw=true "Demo")

We have evaluated GPT-3.5 and GPT4 zero-shot capabilities in the three main task-oriented objectives, namely Intent Classification, Dialogue State Tracking and Response Generation:

Intent Classification results:
<p align="center">
<img width=1600  src="imgs/IC.png?raw=true">
</p>

Dialogue State Tracking results:
<p align="center">
<img src="imgs/DST.png?raw=true">
</p>

Responge Generation results:
<p align="center">
<img src="imgs/RG.png?raw=true">
</p>
