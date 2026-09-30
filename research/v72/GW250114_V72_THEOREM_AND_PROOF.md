# GW250114 HRF v72 — Theorems and proofs

**Scope:** exact or stipulated-model statistical results. No astrophysical detection claim follows from these theorems.

## Theorem 1 — Punctured continuous alternatives have zero uniform margin

Let `P_{lambda,eta}` be a fixed statistical experiment, continuous in total variation at `(lambda_0,eta_0)` along some sequence `(lambda_n,eta_n)` with `lambda_n!=lambda_0`, `lambda_n->lambda_0`, and `P_{lambda_n,eta_n}->P_{lambda_0,eta_0}`. Let the target contain `P_{lambda_0,eta_0}` and the alternative contain every `P_{lambda_n,eta_n}`. Tests may be randomized, with values in `[0,1]`; the loss below is the maximum of target type-I error and worst-alternative type-II error.

Then the target-to-alternative total-variation distance is zero, and the minimax maximum error for testing the target against the unrestricted punctured alternative is exactly `1/2`.

### Proof

For a test `phi` with rejection probability in `[0,1]`, total-variation continuity gives

\[
E_{\lambda_n,\eta_n}\phi\to E_{\lambda_0,\eta_0}\phi=\alpha.
\]

The type-I error at the target is `alpha`, while the type-II error along the approaching alternatives tends to `1-alpha`. Thus the worst error is at least

\[
\max(\alpha,1-\alpha)\ge\frac12.
\]

The randomized rule that chooses either conclusion with probability one half has both errors `1/2`, so the lower bound is attained. QED.

### Qualification

The result is uniform for the fixed experiment. For any fixed separated `lambda_1`, increasing information may make `P_{lambda_1}` distinguishable from `P_{lambda_0}`. The theorem also does not prohibit interval estimation or an explicitly prior-weighted Bayesian comparison. An interval/equivalence procedure has its own coverage or type-I semantics; it creates a positive uniform classification margin only if the target and alternative regions are separated by an indifference gap.

## Theorem 2 — Least-favorable Gaussian score for closed convex images

Let `X~N(mu,K)` with `K` positive definite. Let `A,C` be nonempty closed convex mean sets with an attained closest pair `(a_*,c_*)` in the Mahalanobis norm. Put `v=a_*-c_*`, `d^2=v^TK^{-1}v`, and

\[
L=v^TK^{-1}\left[X-\frac{a_*+c_*}{2}\right].
\]

Then

\[
\operatorname{Var}(L)=d^2,
\quad
\inf_{a\in A}E_aL\ge d^2/2,
\quad
\sup_{c\in C}E_cL\le-d^2/2.
\]

For `d>0`, therefore

\[
\inf_{a\in A}P_a(L>c_0)
\ge \Phi(d/2-c_0/d),
\]

\[
\sup_{c\in C}P_c(L>c_0)
\le \Phi(-d/2-c_0/d).
\]

### Proof

Transform to whitened coordinates with `K^{-1/2}`. The closest-pair property for convex sets implies the supporting-hyperplane inequalities

\[
v^TK^{-1}(a-a_*)\ge0 \quad(a\in A),
\]

\[
v^TK^{-1}(c-c_*)\le0 \quad(c\in C).
\]

Substitution into the expectation of `L` yields the mean bounds. Linear Gaussian propagation gives variance `v^TK^{-1}KK^{-1}v=d^2`. Standardization yields the probability bounds. QED.

For midpoint threshold zero, the maximum error is bounded by `Phi(-d/2)`. If `d=0`, the images have zero margin and the standardized formulas containing `1/d` are undefined; no positive least-favorable separation gate is available. For `d>0`, a score threshold `c_0=ln(10)` and desired target probability `0.90` solve

\[
d/2-\ln(10)/d=\Phi^{-1}(0.90),
\]

giving `d=3.7810604375308374`.

The score is the simple likelihood ratio for `(a_*,c_*)`. It should be called a least-favorable endpoint likelihood-ratio score, not a composite Bayes factor.

## Corollary 2.1 — Affine nuisance distance

Let `A=mu_p+Col(B_p)`, `C=mu_g+Col(B_g)`, `delta=mu_p-mu_g`, and `G=[B_p,-B_g]`. Then

\[
d^2=\min_x(\delta+Gx)^TK^{-1}(\delta+Gx)
\]

equals

\[
\boxed{
d^2=\delta^T[K^{-1}-K^{-1}G(G^TK^{-1}G)^+G^TK^{-1}]\delta .
}
\]

### Proof

This is generalized least squares. The bracketed matrix is the `K^{-1}`-orthogonal residual projector after removing the column space of `G`. The Moore–Penrose inverse covers rank-deficient nuisance matrices. QED.

## Corollary 2.2 — Conservative finite-composite intersection rule

For competitor sets `C_k`, construct least-favorable scores `L_k` with distances `d_k` and thresholds `c_k`. Claim the target only if every `L_k>c_k`. Then

\[
\inf_A P(\text{claim target})
\ge1-\sum_k\Phi(c_k/d_k-d_k/2).
\]

Under competitor `C_k`, the probability of wrongly claiming the target is at most

\[
\Phi(-d_k/2-c_k/d_k).
\]

### Proof

Apply Theorem 2 to each lane and use the union bound for any target-lane failure. The wrong-target statement uses the corresponding competitor bound. QED.

This is a conservative multiple-comparison guarantee. It is not posterior model probability and not a substitute for a normalized composite likelihood or prior.

For the symmetric exclusion alternative `|lambda-lambda_0|>=delta_0`, the lower and upper endpoints are two competitor lanes. Allocating a total target miss probability of `0.10` equally gives `d>=4.348686765309588` per endpoint. At the historical full log gap this requires `q_eff<=0.100155239115278%`. The one-competitor value `0.115190902132591%` does not provide 90% simultaneous two-sided target success.

## Theorem 3 — Optimal allocation for two observables and one shared nuisance

Suppose

\[
Y_i=q_i\lambda+b_i\eta+\epsilon_i,
\quad
\epsilon_i\sim N(0,\sigma_i^2/n_i),
\quad n_1+n_2=N.
\]

where the errors are independent, `n_i>0`, `sigma_i>0`, and at least one `b_i` is nonzero. Then the nuisance-profiled information for `lambda` is

\[
I_{\rm eff}
=
\frac{a_1a_2(q_1b_2-q_2b_1)^2}
{a_1b_1^2+a_2b_2^2},
\qquad a_i=n_i/\sigma_i^2.
\]

Within this stipulated one-shared-nuisance model it is positive exactly when `q_1b_2-q_2b_1!=0`. For nonzero `b_i` and a nonzero determinant, the interior allocation maximizing it is

\[
\frac{n_1}{N}
=
\frac{|b_2|/\sigma_2}{|b_1|/\sigma_1+|b_2|/\sigma_2},
\]

and

\[
I_{\rm eff,max}
=
N\frac{(q_1b_2-q_2b_1)^2}
{(|b_1|\sigma_2+|b_2|\sigma_1)^2}.
\]

### Proof

Independence makes the two-parameter Fisher matrix `sum_i a_i (q_i,b_i)^T(q_i,b_i)`. Taking the Schur complement of the nuisance block gives the stated information. The numerator is the squared determinant of the two response vectors, proving the rank condition. Differentiating with respect to `n_1` under `n_2=N-n_1`, or applying Cauchy–Schwarz, yields the optimum. QED.

If the determinant is zero, the efficient information is zero and the maximizing allocation is nonunique. If exactly one `b_i` is zero, the displayed boundary allocation is an open-domain supremum as the other channel's positive resource tends to zero; it is not attained under the theorem's `n_i>0` assumption. If `b_1=b_2=0`, nuisance profiling is unnecessary and the ordinary information is `sum_i a_i q_i^2`; the quotient expression should not be evaluated as `0/0`. Correlated errors or additional nuisances require the full covariance/tangent calculation and can change both the determinant rule and the optimal allocation.

## Theorem 4 — Common versus detector-specific nuisance aliases

For detector responses `q_d`, nuisance design matrices `B_d`, and covariances `K_d`, define

\[
I_{\rm common}=\min_a\sum_d\|q_d-B_da\|^2_{K_d^{-1}}
\]

and

\[
I_{\rm ds}=\sum_d\min_{a_d}\|q_d-B_da_d\|^2_{K_d^{-1}}.
\]

Then `I_common>=I_ds`.

### Proof

Every common coefficient `a` is a feasible choice in each detector-specific minimization, whereas the detector-specific problem optimizes over the larger Cartesian product of coefficients. Minimization over the smaller feasible set cannot produce a smaller residual. QED.

If every detector is individually locally aliased, `I_ds=0`. The common-nuisance network has positive tangent information only if no single coefficient realizes every detector's linear alias simultaneously. If the same coefficient works for all, `I_common=0`; this establishes local first-order failure. Exact global nonidentifiability still requires an explicit finite gauge or intersecting nuisance-image sets.

## Theorem 5 — Bounded adverse bias closes the margin at half-gap

For two scalar centers separated by `Delta>0`, let either center move adversarially by at most `U` toward the other. Their worst-case remaining separation is

\[
\boxed{(\Delta-2U)_+.}
\]

If the stochastic width is `q_eff`, the robust standardized distance is

\[
d_U=(\Delta-2U)_+/q_{\rm eff}.
\]

### Proof

The upper center can move downward by `U` and the lower center upward by `U`; the triangle inequality gives remaining separation at least `Delta-2U`, attained by aligned adverse moves. Separation cannot be negative. QED.

At `U>=Delta/2`, no uniform branch margin remains regardless of SNR.

## Scope boundary

These results provide necessary claim design and finite-model scoring tools. They do not show that GW250114 supplies a rank-completing observable, that the relevant nuisance images are convex, Gaussian, or separated, or that a physical branch exists. Those are empirical/modeling questions left locked by v72.
