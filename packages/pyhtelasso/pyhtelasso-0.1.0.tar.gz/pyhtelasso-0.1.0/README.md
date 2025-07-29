# pyhtelasso

![](https://img.shields.io/badge/license-MIT-green)

A Python package for detecting treatment effect heterogeneity in randomized experiments using debiased lasso regression.

## Installation

You can install the package using pip:

```bash
pip install pyhtelasso
```

**Note**: This package requires `econml>=0.13.0` for the DebiasedLasso implementation. The package will automatically install this dependency.

## Features

* Detects covariates that moderate treatment effects
* Debiased Lasso regression for valid inference
* Simulation tools for benchmarking
* Visualization tools for interpreting results

## Quick Start

```python
import numpy as np
from pyhtelasso import HTELasso

# Simulate data with heterogeneous treatment effects
np.random.seed(1988)
n, p_features, p_het = 1000, 20, 3
X = np.random.randn(n, p_features)
t = np.random.binomial(1, 0.4, n)
y_base = X[:, :3].sum(axis=1) + np.random.normal(0, 1, n)
treatment_effect = 2.0 * (1 + X[:, :p_het].sum(axis=1))
y = y_base + t * treatment_effect

# Initialize and fit the detector
detector = HTELasso(
    alpha=None,              # Auto-select regularization via CV
    random_state=1988,         # Random seed
    fit_intercept=True       # Fit intercept term
)

# fit the model
detector.fit(X, y, t)

# Print detailed summary
print(detector.summary())
```

## Examples

You can find detailed usage examples in the `examples/` directory.

## Technical Details

### Motivation

When studying heterogeneous treatment effects (HTE) in randomized experiments, researchers often suspect that only a few covariates truly moderate the effect of the treatment. Identifying these *moderators* is critical — whether for targeting, personalization, or scientific discovery.

> Lasso is often the go-to method for selecting a small set of variables "that matter." This work aims to extend that idea to the context of selecting treatment effect modifiers. 

It performs automatic variable selection in high-dimensional settings in a simple and transparent way, it scales well, and comes with theoretical guarantees. 

However, naively applying Lasso directly to treatment effect heterogeneity estimation is problematic:

* **Regularization bias**: Lasso shrinks coefficients toward zero, distorting treatment effect estimates.
* **Invalid confidence intervals**: Standard errors and $p$-values after variable selection are not valid.
* **Hierarchical constraint violations**: Lasso may select interactions without main effects, which can be undesirable in many applications.

---

### Related Work

Researchers have developed several sophisticated methods to address these challenges and still employ the Lasso in this context:

* Imai and Ratkovic (2013) use a modified Lasso with structured penalties and group interactions.
* Nie and Wager (2020) propose the R-learner, a powerful meta-learning approach that relies on orthogonalized loss functions and cross-fitting which can employ lasso.
* Zhao et al. (2022) focus on FDR control by combining weighted outcomes lasso regression with a knockoff filter.
* Bien et al. (2013) propose an interaction lasso which selects treatment variable interactions only if the main term also enters the model.

While effective, these methods can be complex to communicate, implement, and tune.

---

### Method Overview

The `pyhtelasso` package proposes a simple and statistically rigorous alternative based on:

1. Outcome transformation via an inverse-probability weighted score.
2. Debiased Lasso regression for variable selection and valid inference.

This method is inspired by semiparametric theory and builds most closely on the idea of using weighted outcomes regression to isolate treatment effect variation, as in Zhao et al. (2022). However, unlike their approach, we do not rely on knockoff variables, and we replace standard Lasso with Debiased Lasso, which yields valid standard errors and $p$-values for each covariate.

---

### Notation

Suppose we observe a randomized experiment with $n$ units. For each unit $i = 1, \dots, n$, we observe:

* outcome $Y_i \in \mathbb{R}$
* treatment indicator $T_i \in \{0, 1\}$
* covariates $X_i \in \mathbb{R}^p$
* known or estimated treatment probability $p = \mathbb{P}(T = 1) \in (0, 1)$

We assume $T$ is randomly assigned, so potential outcomes are independent of treatment assignment. Our focus is on the Conditional Average Treatment Effect (CATE) function:

$$
\tau(x) = \mathbb{E}[Y(1) - Y(0) \mid X = x].
$$

We define the transformed outcome:

$$
Y_i^* = Y_i \cdot \frac{T_i - p}{p(1 - p)}
$$

This transformation is helpful as it has the following property:

$$
\mathbb{E}[Y^* \mid X = x] = \tau(x).
$$

---

### Estimation

We assume a linear model for $\tau(x)$:

$$
\tau(x) = x^\top \beta
$$

To estimate $\beta$, we regress $Y^*$ on $X$ using the Debiased Lasso (also known as the Desparsified Lasso or De-biased Square-root Lasso), as developed independently in van de Geer et al. (2014), Javanmard and Montanari (2014), Zhang and Zhang (2014). The debiased Lasso corrects the regularization bias of standard Lasso and enables valid confidence intervals and hypothesis testing in high-dimensional settings.


Let $\widehat{\beta}_j$ denote the estimated coefficient on covariate $j$, and $\widehat{\sigma}_j$ its standard error. Then under suitable sparsity and design assumptions:

* $\widehat{\beta}_j$ is asymptotically normal,
* the t-statistic $t_j = \widehat{\beta}_j / \widehat{\sigma}_j$ can be used to test for significance,
* and covariates with significant $t_j$ values are interpreted as moderators of the treatment effect.

---

### Interpretation

Let’s say you want to know whether age or income or gender moderate the effect of an intervention of interest. You apply methodology as above and estimate:

$$
\tau(x) = 0.3 \cdot \text{age} + 0 \cdot \text{income} + 1.1 \cdot \text{female}
$$
This tells you:

* The treatment effect is larger for women and older individuals
* But income is not a significant moderator.

---

### Advantages

The proposed approach overcomes the naive lasso limitations, while maintaining simplicity. It is:

* Simple: No residualization, cross-fitting, or nested learners.
* Valid inference: Debiased Lasso enables hypothesis testing with proper standard errors even when $p>n$.
* Sparse discovery: Naturally selects a small number of likely moderators.

---

### Limitations

* Noise: The method is inefficient because it does not fully utilize the information contained in the treatment indicator beyond its role in constructing the transformed outcome.
* Multiple testing: In settings with many covariates the method is vulnerable to inflated type-1 errors. Consider combining with some type of multiple testing adjustment.

---

## References

* Bien, J., Taylor, J., & Tibshirani, R. (2013). *A lasso for hierarchical interactions*. Annals of statistics, 41(3), 1111.
* Du, Y., Chen, H., & Varadhan, R. (2021). *Lasso estimation of hierarchical interactions for analyzing heterogeneity of treatment effect*. Statistics in Medicine, 40(25), 5417-5433.
* Imai, K., & Ratkovic, M. (2013). *Estimating treatment effect heterogeneity in randomized program evaluation*. Annals of Applied Statistics.
* Javanmard, A., & Montanari, A. (2014). *Confidence intervals and hypothesis testing for high-dimensional regression*. The Journal of Machine Learning Research, 15(1), 2869-2909.
* Nie, X., & Wager, S. (2020). *Quasi-oracle estimation of heterogeneous treatment effects*. Biometrika.
* van de Geer, S., et al. (2014). *On asymptotically optimal confidence regions and tests for high-dimensional models*. Annals of Statistics.
* Zhao, Y., Xu, Y., & Zhao, Q. (2022). *False discovery rate controlled heterogeneous treatment effect detection for online controlled experiments*.
* Zhang, C. H., & Zhang, S. S. (2014). *Confidence intervals for low dimensional parameters in high dimensional linear models.* Journal of the Royal Statistical Society Series B: Statistical Methodology, 76(1), 217-242.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Citation

To cite this package in publications, please use the following BibTeX entry:

```bibtex
@software{pyhtelasso,
  title={Pyhtelasso: Treatment Effect Heterogeneity Detection with Debiased Lasso},
  author={Vasco Yasenov},
  year={2024},
  url={https://github.com/yourusername/pyhtelasso}
}
```
