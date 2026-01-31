
# GA-Tuned DE Optimized KAN-GAN for Audio-Visual Speech Synthesis (AVSS)

This repository contains the official implementation of our research work on **hierarchical evolutionary optimization for Audio-Visual Speech Synthesis (AVSS)**, where a **Genetic Algorithm (GA)** is used to tune **Differential Evolution (DE)** for automated hyperparameter optimization of a **Kolmogorov–Arnold Network enhanced Generative Adversarial Network (KAN-GAN)**.

The proposed framework integrates **evolutionary computation** and **generative AI** to improve the realism, synchronization, and training stability of multimodal audio-visual speech generation.

---

## 🔍 Key Contributions

* **KAN-based GAN (KAN-GAN):**
  Incorporation of Kolmogorov–Arnold Networks into the GAN discriminator for efficient modeling of high-dimensional nonlinear relationships with fewer parameters.

* **GA-Tuned Differential Evolution (GA–DE):**
  A hierarchical evolutionary optimization strategy where GA adaptively tunes DE control parameters for robust and automated hyperparameter optimization.

* **Application to AVSS:**
  Joint optimization of Voice Conversion (VC) and Audio-Visual Synthesis (AVS) for generating synchronized speech audio and facial video.

* **Improved Stability and Quality:**
  Enhanced adversarial balance, reduced training instability, and improved perceptual quality compared to conventional optimization approaches.

---

## 🧠 Method Overview

1. **KAN-GAN Architecture** for VC and AVS
2. **DE** optimizes KAN-GAN hyperparameters
3. **GA** adaptively tunes DE control parameters
4. **Loss-based fitness** guides evolutionary search
5. Final optimized model trained for AVSS generation

---

## 📊 Evaluation

The framework is evaluated using:

* **Objective metrics:** MCD, F0-RMSE
* **Subjective metric:** Mean Opinion Score (MOS)
* **Comparative analysis:** Fixed DE, Bayesian optimization, and baseline GAN models

Detailed results and discussion are provided in the associated paper.

---

## 🛠️ Code Status

⚠️ **Important Notice**

> The repository is currently under active development.
> **The complete and updated implementation will be released shortly**, including:
>
> * GA–DE optimization pipeline
> * KAN-GAN architecture
> * Training and evaluation scripts
> * Reproducibility instructions

Please stay tuned for updates.

---

## 📄 Paper

If you use this work, please cite our paper:

> *GA-Tuned Differential Evolution for Hyperparameter Optimization of KAN-GAN in Audio-Visual Speech Synthesis*,
> submitted to **WCCI (IEEE World Congress on Computational Intelligence)**.

(Citation details will be updated upon publication.)

---

## 📬 Contact

For questions, collaborations, or early access requests, feel free to open an issue or contact the authors.

---

### ⭐ If you find this work useful, consider starring the repository!


