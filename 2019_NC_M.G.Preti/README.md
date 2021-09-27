* Decoupling of brain function from structure reveals regional behavioral specialization in humans

---
## Data source

* All used data can be find in https://www.github.com/gpreti/GSP_StructuralDecouplingIndex
* the `database.txt` and `features.txt` can be downloaded from https://www.github.com/gpreti/GSP_StructuralDecouplingIndex or https://github.com/neurosynth/neurosynth



## Methods

### Notation

* $N = 360$: cortical atlas ($180\times 2$)

* $m = 10$: number of subjects

* $\rm T = 1190$: number of time points

* ${\rm nSurr} = 19$: number of surrogate to generate for each subjects

* $C \in \mathbb{R}$ : median-split cut-off of **average energy spectrum density**

  

* $A_{unnorm} \in \mathbb{R}^{N \times N}$: group-level Structural connectome

* $D \in \mathbb{N \times N}$: degree matrix

* $S_i = [s_{i1}, \cdots, s_{i\rm T}], s_{it} \in \mathbb{R}^{N}$: resting-state functional data for i-th individual

* $R \in \mathbb{R}^{N \times N}$: a diagonal matrix with random $+1/-1$

  

### 1. Structural-connectome harmonics

* Symmetric normalization: $A = D^{-1/2}A_{unnorm}D^{-1/2}$

* normalized Laplacian matrix: $L = I - A$
* Graph Fourier Transformation (GFT): $LU = U\Lambda$
  * frequencies: $\Lambda_{ii} = \lambda_i, \lambda_1 \leq \lambda_2 \leq \cdots \leq \lambda_N$
  * eigenmodes or structural connectome harmonics: $U = [u_1, \cdots, u_N], u_i \in \mathbb{R}^N$

### 2. Structural-decoupling index **

* review：

  * discrete Fourier transformation: 

    * $X[k] = \sum_\limits{n=0}^{N-1}x[n]\exp(-j\frac{2\pi}{N}n \cdot k )$

    * matrix representation ($w = \exp(j\frac{2\pi}{N})$): $Fx(n) = X(f)$
      $$
      \begin{bmatrix}
      1 & 1 & 1 & \cdots & 1 \\
      1 & w^{-1} & w^{-2} & \cdots & w^{-(N-1)} \\
      1 & w^{-2} & w^{-3} & \cdots & w^{-2(N-1)} \\
      \vdots & \vdots & \vdots & \ddots & \vdots \\
      1 & w^{-(N-1)} & w^{-2(N-1)} & \cdots & w^{-(N-1)^2}
      \end{bmatrix} 
      \begin{bmatrix}
      x[0] \\
      x[1] \\
      x[2] \\
      \vdots \\
      x[N-1]
      \end{bmatrix} =  
      \begin{bmatrix}
      X[0] \\
      X[1] \\
      X[2] \\
      \vdots \\
      X[N-1]
      \end{bmatrix}
      $$

  * energy spectrum density
    * $E = \int_{-\infty}^{+\infty}|x(t)|^2 {\rm d}t = \int_{-\infty}^{+\infty}|X(f)|^2 {\rm d}f$

* graph Fourier transform pair: $\begin{cases} \hat S_i = U^TS_i \\ S_i = U\hat S_i \end{cases}$

* split structural harmonics in high and low frequency

  * compute cut-off frequency $C$
    * energy spectrum density for each subject: $P_i = |\hat S_i|^2 \in \mathbb{R}^{N}$
    * group-level power spectrum: $P = \frac{1}{m}\sum_\limits{i=1}^mPi$
    * let $P = [p_1, \cdots, p_N]$, $C = \arg\min |\sum_\limits{i=0}^Cp_i - \sum_\limits{i=C+1}^Np_i|$
      * $\int$ for continuous, $\sum$ for discrete
  * graph signal filtering
    * design ideal high-pass or low-pass filtering: $\begin{cases} U^{(low)} &= [u_1, \cdots, u_C, 0, \cdots, 0] \\ U^{(high)} &= [0, \cdots, 0, u_{C+1}, \cdots, u_N] \end{cases}$
    * filtering: $\begin{cases} S_i^C = U^{(low)}\hat S_i = U^{(low)}U^TS_i \\ S_i^D = U^{(high)}\hat S_i = U^{(high)}U^TS_i \end{cases}$

* calculate structural decoupling index (SDI)

  * Let $S_i^C = \begin{bmatrix} a_{i1}^C \\ \vdots \\ a_{iN}^C \end{bmatrix}, S_i^D = \begin{bmatrix} a_{i1}^D \\ \vdots \\ a_{iN}^D \end{bmatrix}, a_{ik}^C, a_{ik}^D \in \mathbb{R}^{\rm T}$
  * individual-level SDI for region $r$: ${\rm iSDI}[r, i] = \frac{\parallel a_{ir}^C \parallel_2}{ \parallel a_{ir}^D \parallel_2}$ 
  * group-level SDI for region $r$: $\rm{gSDI}[r] = \frac{ \sum_\limits{i=1}^m\parallel a_{ir}^C \parallel_2 / m}{\sum_\limits{i=1}^m \parallel a_{ir}^D \parallel_2 / m}$

### 3. Significance

* configuration model was used to generate degree-preserving graph $A'$
  * let $\mathbb{1} = [1, \cdots, 1]^T \in {1}^N$, $A' = A\mathbb{1}(A\mathbb{1})^T/\parallel A \parallel_{m_1}$
* $L' = I - A', L'U' = U'\Lambda'$
* $\hat S_i' = U'^TS_i$
* $\begin{cases} \hat S_i^{(rand1)} = RS_i' & (\rm{SC-ignorant})\\ \hat S_i^{(rand2)} = RS_i & (\rm{SC-informed}) \end{cases}$
* generate two type of surrogate functional signals:
  * SC-ignorant: $S_i^{(rand1)} = U'\hat S_i^{(rand1)} = U'R\hat S_i' = U'RU'^TS_i$
  * SC-informed: $S_i^{(rand2)} = U\hat S_i^{(rand2)} = UR\hat S_i = URU^TS_i$

* compute SDI for each subject's surrogate

  * ${\rm SDI_{surr}} \in \mathbb{R}^{N \times {\rm nSurr} \times m }$: SDI for every subject and surrogates

  * ${\rm SDI_{surr\_avgsurr}} \in \mathbb{R}^{N \times m}$: mean from ${\rm SDI_{surr}}$

  * ${\rm SDI_{surr\_avgsurrsubjs}} \in \mathbb{R}^N$: mean from ${\rm SDI_{surr\_avgsurr}}$

    > __computational logic seems different from empirical data !!__

* compare between empirical data and surrogate data

  * ${\rm minSDI_{surr}} \in \mathbb{R}^{N \times m}$: min along the second axis of ${\rm SDI_{surr}}$
  * ${\rm maxSDI_{surr}} \in \mathbb{R}^{N \times m}$: max along the second axis of  ${\rm SDI_{surr}}$
  * ${\rm minDetect} = {\rm rowsum }({\rm SDI_{surr}} < {\rm minSDI_{surr}}) \in \mathbb{R}^N$
  * ${\rm maxDetect} = {\rm rowsum }({\rm SDI_{surr}}>{\rm maxSDI_{surr}}) \in \mathbb{R}^N$

* compute threshold for significant higher or lower

  * $P(x)$: binomial cumulative distribution with $n=100, p=0.05$
  * $\alpha = 0.05 = \frac{1}{1+{\rm nSurr}}$: significance level
    * $\alpha/N$: correcting for the number of tests (number of region)
  * ${\rm THRsubjects} = \lfloor \frac{m}{n} \arg\min_\limits{x \in \mathbb{N}} (P(x)-\alpha/N)\rfloor + 1$

* compute significant region

  * significant higher: ${\rm maxDetect} > {\rm THRsubjects}$
  * significant lower: ${\rm minDetect} > {\rm THRsubjects}$















































