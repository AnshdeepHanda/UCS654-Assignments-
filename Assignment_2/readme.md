

# GAN-based Probability Density Estimation

This project implements a **Generative Adversarial Network (GAN)** to estimate the **probability density function (PDF)** of a transformed air pollution variable (`NO₂`). The GAN learns the underlying distribution of the data and generates new samples that follow the same distribution.

---

##  Project Overview

The goal of this project is to:

1. Load real-world NO₂ concentration data.
2. Apply a **roll-number–dependent nonlinear transformation**.
3. Train a **1D GAN** on the transformed data.
4. Generate synthetic samples.
5. Compare real vs generated distributions using **Kernel Density Estimation (KDE)**.

---

##  Dataset

* File: `data.csv`
* Column used: `no2`
* Encoding handled: `cp1252`, `ISO-8859-1`
* Only numeric values are used (non-numeric entries are removed).

If the dataset is large, it is **randomly subsampled to 10,000 points** for faster training.

---

##  Data Transformation

The transformation depends on the roll number:

```
z = x + a_r * sin(b_r * x)
```

Where:

```
a_r = 0.5 * (ROLL_NUMBER % 7)
b_r = 0.3 * ((ROLL_NUMBER % 5) + 1)
```

This ensures every student gets a **unique distribution**.

The transformed data is then **standardized**:

```
z_norm = (z - mean(z)) / std(z)
```

---

##  GAN Architecture

This is a **simple fully-connected GAN for 1D data**.

### Generator

* Input: 1D noise
* Layers:

  * Dense(16, ReLU)
  * Dense(16, ReLU)
  * Dense(1, Linear)

### Discriminator

* Input: 1D sample
* Layers:

  * Dense(16, ReLU)
  * Dense(16, ReLU)
  * Dense(1, Sigmoid)

---

##  Training Details

| Parameter        | Value                |
| ---------------- | -------------------- |
| Epochs           | 1000                 |
| Batch Size       | 64                   |
| Optimizer        | Adam (lr=0.001)      |
| Loss             | Binary Cross Entropy |
| Latent Dimension | 1                    |

At every epoch:

* Discriminator learns to distinguish real vs fake.
* Generator learns to fool the discriminator.

---

##  Output Visualization

After training:

1. 5000 new samples are generated.
2. Samples are **denormalized**.
3. KDE plots compare:

   * Real transformed data
   * GAN generated data

The plot is saved as:

```
GAN_PDF_Plot.png
```

---

##  File Structure

```
.
├── data.csv
├── gan_pdf.py
├── GAN_PDF_Plot.png
└── README.md
```

---

##  How to Run

### 1. Install dependencies

```bash
pip install pandas numpy matplotlib seaborn tensorflow keras
```

### 2. Run the script

```bash
python gan_pdf.py
```

---

##  Result

The final plot shows:

* **Blue curve** → Real data distribution
* **Red curve** → GAN learned distribution

A good model produces **high overlap**, meaning the GAN successfully learned the underlying PDF.

---

##  Key Concepts Demonstrated

* Data preprocessing
* Nonlinear transformation
* GAN training from scratch
* Density estimation
* Deep learning for unsupervised modeling
* Visualization using KDE

---

##  Learning Outcome

This project demonstrates how **GANs can be used for statistical modeling**, not just image generation. It shows practical usage of:

* TensorFlow training loops
* GradientTape
* Adversarial learning dynamics
* Real-world noisy data

---


##  Author

**Divyansh Sharma**
Roll Number: 102303964


