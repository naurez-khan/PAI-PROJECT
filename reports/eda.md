# Stage 1: Quality and Data Audit

## Executive Summary
This report evaluates the **2,299 clean Python solutions** across **500 competitive programming problems** stored in the SQLite database (`data/code_similarity.db`).

The objective is to verify that the data pipeline successfully ingested, cleaned, validated, and extracted features from untrusted code, and to prove that the resulting dataset is statistically sound and ready for **Stage 2 (Code Similarity & Clone Detection)**.

---

## Core Findings

### 1. Data Cleaning & Integrity (The Filter Succeeded)
* **What happened:** A total of **2,338 candidate solutions** were parsed and validated through Pydantic and Python's Abstract Syntax Tree (`ast`).
* **The Result:** **2,299 solutions** passed all checks and were accepted (**98.3% pass rate**).
* **Duplicates Purged:** Exactly **39 structural duplicates** were detected and removed using AST fingerprinting (`canonical_hash`). These were solutions with identical syntax trees (e.g., someone copied code and only changed comments, variable names, or spacing).
* **Safety:** Zero broken or invalid Python scripts entered the database.

### 2. Pair Formation Feasibility (Can We Train Code Similarity?)
* **The Question:** In Stage 2, machine learning models need **positive pairs** (two different Python scripts that solve the exact same problem) to learn similarity.
* **The Result:** **485 out of 500 problems (97.0%)** have **2 to 5 distinct, working solutions**.
* **Significance:** The Stage 1 acceptance gate required at least 50 problems with multiple solutions. With 485 eligible problems, the pipeline provides thousands of valid positive pairs for training and benchmarking.

### 3. Code Size & Structural Complexity
* **Lines of Code:** The median solution is **21.0 lines long**, and 95% of solutions are under **55.1 lines** (mean: 25.7 lines).
* **Token Count:** The median solution contains **135.0 tokens** (mean: 161.3). Tokens represent meaningful words and symbols, ignoring blank lines and comments.
* **AST Syntax Nodes:** The median solution contains **161.0 syntax nodes** (mean: 189.8). This measures the actual logic blocks (loops, if-statements, function calls).
* **Takeaway:** The dataset consists of concise, algorithmic problem-solving scripts, making them ideal for semantic comparison without excessive memory overhead.

### 4. Correlation Analysis (How Features Behave Together)
* **Tokens vs. AST Nodes (r = 0.917 — Very Strong):** As algorithmic logic increases, the token count and AST syntax tree grow in direct proportion.
* **Lines vs. AST Nodes (r = 0.564 — Moderate):** Physical line count is a noisier metric because code formatting varies between programmers. AST node count provides a far more objective measurement of true code complexity.

---

## Key Dataset Limitations
1. **Convenience Sample:** The first 500 problems were downloaded sequentially from the APPS dataset rather than via stratified random sampling. All retained problems currently represent the `interview` difficulty tier.
2. **Task Equivalence vs. Plagiarism:** Two solutions with the same `problem_id` both solve the same programming challenge, but they were independently authored. This represents **semantic / functional equivalence**, not necessarily academic plagiarism.

---

## Modeling Decisions for Stage 2
1. **Feature Redundancy:** Because `token_count` and `node_count` are highly correlated, simple line counts will be deprioritized.
2. **Similarity Metrics:** Stage 2 should pair lexical similarity (**Token Jaccard**) with structural tree similarity (**AST Cosine**) to accurately detect both exact clones and rewritten code.
