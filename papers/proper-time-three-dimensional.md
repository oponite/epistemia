---
title: "Proper Time Is Three-Dimensional"
author: "Vijay Neelakantan"
date: "2026-11-08"
description: "A representation theorem: a clock's temporal state is (amplitude, phase, proper time); ordinary time is its projection. Three kinds of clock, sorted by how acceleration moves their phase origin."
---

*Draft 3.2, 8 November 2026. Not peer reviewed. Interactive figure: <https://claude.ai/artifact/RYkA6PmJEz9iZkVPkzfPnA>.*

## Abstract

We propose that the temporal state of a physical clock has three coordinates, not one: an amplitude $r$, a phase $\theta$, and proper time $t$. A clock is a cycle; $\theta$ is where it is in the cycle, $r$ is how strong the cycle is, and $t$ is the ordinary forward parameter. The cycle's state space is attached to each event of the clock's worldline as a fibre; with an orientation it is the complex plane, the cycle state is the single complex number $z=re^{i\theta}$, and the full temporal state space is $\mathbb{C}\times\mathbb{R}$. Ordinary linear time is the origin $z=0$: a clock with no cycle. We count dimension structurally, as the number of independent coordinates on the clock's state space, and we place no metric on time; the three directions therefore carry none of the pathologies of multi-time metric theories, and the number three has a reason: a one-mode cycle has a two-dimensional state space. The worldline sits in ordinary spacetime; its bending is proper acceleration and leaves the cycle untouched. For clocks whose cycle is a spatial rotation the fibre is carried by Fermi–Walker transport and an accelerated clock's phase origin precesses relative to a free clock's at the Thomas rate; for point oscillators the origin is unchanged; for wave clocks it shifts by a geometric phase. The model thus sorts clocks into three kinds by one coordinate, and each kind's behaviour is already measured, in flat and in curved spacetime. Phase and amplitude are already what metrology measures, classically by phase and envelope detection and for quantum clocks by homodyne detection of a coherent state $\alpha$, for which $(r,\theta)=(|\alpha|,\arg\alpha)$ exactly. We state a criterion for a quantity to be temporal and prove that amplitude and phase satisfy it for every physical clock. The orientation of the fibre is correlated with the arrow of proper time: it is the common direction in which every bounded-below system's phase advances, and reversing it is time reversal. The result is a representation theorem, not a new dynamics: under the stated conditions the temporal state of a clock is three-dimensional and ordinary time is its projection. No number is predicted that a one-dimensional account with clock-state variables does not also give; the single assumption that could carry empirical content, a tube in spacetime around the worldline, is identified and left open.

## 1. Introduction

Ordinary time is one number. A clock, however, is a cycle, and a cycle has two more numbers attached to every moment: where in the cycle it is, and how strong the cycle is. Metrology reads both routinely. This paper asks what follows from treating them as coordinates of time rather than as properties of the instrument that measures it.

The answer has to begin with a definition of "dimension of time", because the phrase has two readings that lead to different theories.

The **metric reading** counts the directions a spacetime metric treats as timelike. Three such directions give signature $(3,n)$. This reading is well explored and well constrained: in flat space any circle in a time–time plane is a closed timelike curve, so causality has to be imposed by hand; wave equations become ultrahyperbolic and the initial-value problem is ill-posed except under nonlocal constraints [Tegmark 1997; Craig and Weinstein 2009]; extra timelike directions bring ghost or tachyonic modes unless a gauge symmetry removes them [Bars 2001]. Dorling [1970] argued on kinematic grounds that with more than one time dimension timelike geodesics lose their extremal property, and that stable particles require it; Cole [1978] worked out six-dimensional transformations with three times; the recent proposal of Kletetschka [2025] is on this road. We do not take it.

The **structural reading**, which we adopt, counts the independent coordinates needed to say *when* an event is. No metric on time is assumed. Under this reading the question "is time three-dimensional?" becomes "does the set of temporal events a theory admits have dimension three?", and that is a question about families of histories, not about one trajectory. A single history is always one-dimensional, whatever its ambient space, exactly as a single worldline is one-dimensional inside four-dimensional spacetime.

Our thesis is then:

> Every clock carries a three-dimensional temporal state $(r,\theta,t)$: amplitude, phase, proper time. Ordinary linear time is the degenerate case $r=0$.

This is a representation result. It shows that a specific idea holds under specific, stated conditions and draws its consequences; it does not propose a new dynamics, and Section 6 says exactly what would have to be added for it to do so.

Section 2 gives the definitions, states which are postulates, and proves that amplitude and phase are temporal under a stated criterion. Section 3 proves seven elementary theorems: no loops, recurrence without repetition, dimension three, independence of bend from cycle and from rate, the behaviour of the phase origin under push for rotor, point-oscillator and wave clocks, and the equivalence of uniform rotation with a complex structure. Section 4 says how $r$ and $\theta$ are measured, fixes their units, and cites the metrology that verifies the conditions. Section 5 gives examples, including the negative ones. Section 6 draws the implications, fixes the scope, and places the proposal next to relativity and to the metric-reading literature. Section 7 names the one road not taken.

## 2. Definitions

Throughout, "clock" means a physical system that undergoes a cycle and follows a worldline. Labels: **Definition** marks a choice; **Postulate** marks a definition the paper depends on but does not derive.

**Definition 1 (temporal state space).** $\mathcal{T}=\mathbb{R}_{\ge0}\times S^{1}\times\mathbb{R}$, with coordinates $(r,\theta,t)$:

- $r\ge0$, the amplitude of the cycle, free to grow, fade or wander;
- $\theta\in S^{1}=\mathbb{R}/2\pi\mathbb{Z}$, the phase, a circle with a distinguished origin;
- $t\in\mathbb{R}$, proper time, with a declared origin.

The angle is a coordinate in its own right. Drawing the circle in a plane as $(r\cos\theta,r\sin\theta)$ adds a coordinate but not a dimension; $r$ counts as a dimension only because it varies. The origin of $\theta$ for a single clock is a convention, like the origin of a position coordinate; what is physical is a difference of phases, between two clocks or along one clock. At $r=0$ the phase is undefined, as the angle of the origin is.

**Definition 2 (history).** A continuous curve $\gamma(s)=(r(s),\theta(s),t(s))$ in $\mathcal{T}$ along which $t$ is strictly increasing. Nothing else is constrained. "Irreversible" means exactly this.

**Definition 3 (dimension of a theory's time).** The dimension of the set of temporal events reached by the theory's admissible histories. One history is one-dimensional; dimension belongs to the family.

**Definition 4 (independence).** The initial amplitude and phase $(r_0,\theta_0)$ are free initial data of the theory.

**Postulate 5 (room, spine and fibre).** Clocks follow worldlines in Minkowski spacetime, the **room**, where clocks are compared. A clock's worldline $c(t)$, parametrised by proper time, is its **spine**. The cycle's state space (the $(r,\theta)$ sheet) is attached to each event of the spine as a **fibre**: it is not a region of spacetime and has no spatial extent; $r$ is a pure number. Formally the temporal state space is a bundle over the spine with fibre $\mathbb{R}_{\ge0}\times S^{1}$; a history is a section along the spine. Fibres at different events are identified by a transport rule, which depends on what kind of cycle the clock performs:

- **(i) Rotor clocks.** The cycle is a spatial rotation: a hand, a wheel, a spin. The fibre's two directions are then identified with a 2-plane of spatial *directions* in the clock's rest space (directions only, not lengths), and fibres are identified by **Fermi–Walker transport**: the phase origin is carried along the experienced passage of time without twisting. In words: "up" on the sheet at a later moment is whatever "up" becomes when carried forward along the clock's own time with no rotation about the forward direction.
- **(ii) Point-oscillator clocks.** The cycle is internal and carries no spatial direction: an atomic coherence, a quantum $U(1)$ phase of a system with no propagation direction. The phase is a scalar under spatial rotations, so Fermi–Walker transport does not act on it. The fibre is an internal bundle, and we take its connection to be flat: the phase origin is carried along unchanged.
- **(iii) Wave clocks.** The cycle is a wave with propagation direction $\hat{\mathbf k}$ and a polarisation: phase $=\mathbf k\cdot\mathbf x-\omega t$, so the dial is laid along $\hat{\mathbf k}$ with one turn per wavelength. The fibre's directions are identified with the polarisation plane transverse to $\hat{\mathbf k}$, and the transport rule is supplied by the wave equation: parallel transport of $\hat{\mathbf k}$ on the sphere of directions, whose holonomy is the geometric (Berry) phase.

*Why Fermi–Walker for (i).* A frame built from the spine's curvature (the Frenet frame) is undefined where the curvature vanishes, which is exactly the free clock. Fermi–Walker transport is defined on every worldline, reduces to parallel transport on a straight one, and is the standard rule for carrying a gyroscope's axis along an accelerated worldline [Misner, Thorne and Wheeler 1973, §§6.5–6.6].

*On drawing.* Figures draw the fibre as a disc around the spine, as every phase-space diagram does. The drawing is not an embedding in spacetime; in case (i) only the directions of the disc are spatial, never its size. Section 6 states what would follow if the disc were a region of spacetime.

**Definition 6 (push).** The push on a clock at $t$ is the turning rate of its forward direction, $k(t)=\dot T(t)$ with $T=\dot c$ the unit tangent, of size $\kappa=|k|$: the curvature of the spine. In the room, $\kappa=a/c$ with $a$ the proper acceleration. $\kappa=0$ is a straight spine: a clock in free fall.

**Definition 7 (arrow angle).** The angle between two clocks' forward directions is their rapidity, i.e. their relative velocity. This is inherited from relativity and is not new.

**Definition 8 (clock).** A clock is a cycle; $\theta$ is its phase and $r$ its amplitude. A clock's temporal state is (amplitude, phase, proper time). A **one-mode** clock has a single cycle; an $m$-mode clock has $m$ independent cycles. In mechanical terms $(r,\theta)$ is the action–angle pair of the mode: for an oscillator or a wave mode the action is proportional to $r^{2}$, for a rotor it is the angular momentum, so "amplitude" covers every kind of clock in Postulate 5.

**Definition 9 (units).** $r=A/A_0$ is dimensionless: the cycle's amplitude $A$ over the clock's **noise-floor amplitude** $A_0$. Its temporal size is $r\,\tau_0$ with $\tau_0=2\pi/\omega$ the clock's own period. The floor is the amplitude the cycle has when nothing drives it: the zero-point amplitude for a quantum clock, the thermal amplitude $\sqrt{k_BT/\kappa}$ (with $\kappa$ the mode's stiffness) for a classical one at temperature $T$. In both cases
$$r^{2}=\frac{E_{\rm cycle}}{E_{\rm floor}},\qquad E_{\rm floor}=\max(\hbar\omega,\,k_BT),$$
so that $r=|\alpha|$ and $r^{2}$ is the mean quantum number for a coherent state, and $r^{2}$ is the energy in thermal units for a classical oscillator. No calibration convention remains.

**Definition 10 (orientation).** The fibre carries a quarter-turn rule, a linear map $J$ with $J^{2}=-I$. The fibre is then the complex plane, the cycle state is $z=re^{i\theta}$, and the full temporal state space is $\mathbb{C}\times\mathbb{R}$. The origin $z=0$ is a clock with no cycle: ordinary linear time.

**Definition 11 (one orientation per room).** The room carries a single $J$; every clock's $z$ is read on that sheet. A clock whose phase runs the other way has $\omega<0$ and is the conjugate $\bar z$ of a normal one. Comparisons of phase between clocks are made where the clocks are together, or along a stated transport; for clocks at spacelike separation "a quarter turn ahead" depends on a synchronisation convention, as relativity requires.

**Definition 12 (the room's orientation).** $J$ is the common direction in which every clock's phase advances with proper time, where "clock" is any system whose energy is bounded below. In quantum terms: for energy eigencomponents $E_j>E_k$, the relative phase $e^{-i(E_j-E_k)t/\hbar}$ turns one fixed way as $t$ increases, and the same way for every such system. Reversing $J$ is complex conjugation, i.e. time reversal.

*What Definition 12 fixes.* Conjugating the whole theory together with reversing $t$ is a symmetry of quantum predictions, so $J$ is fixed *relative to the arrow of $t$*, not absolutely: the orientation of the fibre is correlated with the direction of proper time, and flipping both is invisible. The ingredients are forward $t$ (Definition 1) and energy bounded below (a stability postulate about systems); neither mentions $J$, so the definition is not circular, and it is consistent because Schrödinger evolution has one sign for all systems. Classical mechanics is time-reversal symmetric and supplies no orientation; for a purely classical clock $J$ is a convention, and Definitions 10–12 acquire physical content only through quantum mechanics.

**Definition 13 (temporal quantity).** A quantity attached to a clock is *temporal* if it is (a) a coordinate on the cycle's state space, as opposed to a parameter of the cycle such as its frequency or damping rate, (b) read by comparison with another clock, and (c) unchanged by translating the clock in space. A quantity is *dynamically temporal* if, in addition, (d) it is needed to predict the clock's future phase to a stated precision.

**Proposition 1 (amplitude and phase are temporal).** For every clock, $\theta$ and $r$ are temporal, and they are the only temporal quantities of a one-mode clock besides $t$. For every physical clock they are dynamically temporal. The only clock for which $r$ fails (d) is the exactly harmonic classical oscillator.

*Proof.* The state space of a one-mode cycle is two-dimensional (the action–angle pair of Definition 8: position and momentum for an oscillator, angle and angular momentum for a rotor), so (a) admits exactly two coordinates, and frequency and damping are excluded as parameters. (b): both are read by phase or envelope comparison against a reference clock (Section 4). (c): the cycle belongs to the system, so a spatial translation of the clock changes neither. (Rotation is where the kinds of clock part: a point oscillator's phase is a rotation scalar, a rotor's phase origin is a direction, a wave's is tied to its polarisation, which is exactly the distinction Postulate 5 draws.) (d) for $\theta$: the future phase depends on the present phase. (d) for $r$, on two independent grounds. First, no physical oscillator is exactly isochronous: amplitude shifts the rate in pendulums (circular error), in quartz (drive-level dependence) and in atomic clocks (power-dependent shifts, evaluated as systematics; Section 4), so $r$ enters $\dot\theta$ with a nonzero coefficient. Second, the phase of any physical clock is uncertain by an amount set by its amplitude: for a quantum clock $\Delta\theta\approx1/(2r)$ (number–phase uncertainty), and for a classical clock at temperature $T$ the phase diffuses with variance proportional to $k_BT/E_{\rm cycle}=1/r^{2}$ (Definition 9). So predicting $\theta$ to a stated precision requires $r$ regardless of isochronism. The exactly harmonic classical oscillator at zero temperature has $\dot\theta$ independent of $r$ and no grain, and fails (d). $\square$

**Corollary 2 (why three).** The temporal state space of an $m$-mode clock has dimension $2m+1$. For a one-mode clock it is three.

*Proof.* Each mode contributes a two-dimensional state space by Proposition 1's clause (a); proper time contributes one. $\square$

The first ground in Proposition 1 is qualitative: the coefficient can be made arbitrarily small, and in a good atomic clock $r$'s role in the rate is tiny. The second ground is exact and carries the weight for precision clocks. With Proposition 1 in hand, Theorem 3 below yields "the theory's time is three-dimensional" as a theorem relative to Definition 13, not as a reading; Corollary 2 says that "three" is the one-mode case.

## 3. Theorems

**Theorem 1 (no loops).** No history visits the same temporal event twice.

*Proof.* If $\gamma(s_1)=\gamma(s_2)$ then $t(s_1)=t(s_2)$; since $t$ is strictly increasing, $s_1=s_2$. $\square$

The proof uses only one strictly increasing coordinate. It holds in any number of dimensions, including one; the absence of loops is therefore not evidence for three dimensions and is not claimed as such.

**Theorem 2 (recurrence without repetition).** If $\theta$ is periodic with period $P$ along a history, then $\theta(s+P)=\theta(s)$ while $\gamma(s+P)\neq\gamma(s)$.

*Proof.* $t(s+P)>t(s)$. $\square$

**Theorem 3 (dimension three).** Let the admissible histories include $\gamma_{r_0,\varphi}(s)=\big(r(s),\,\varphi+\omega s,\,vs\big)$ for all $r_0=r(0)\ge0$, all $\varphi\in S^{1}$, with $\omega$ fixed and $v>0$, and with $r(\cdot)$ ranging over non-negative functions with $r(0)=r_0$. Then the reached set contains every event with $t>0$, so the theory's time has dimension three. If instead $r$ is held at one value along all histories, the reached set is the cylinder $\{r_0\}\times S^{1}\times\mathbb{R}$ and the dimension is two.

*Proof.* Given $(r,\theta,t)$ with $t>0$, take $s=t/v$, $\varphi=\theta-\omega s$, and any admissible $r(\cdot)$ with $r(s)=r$. For fixed $r$ the first coordinate of the reached set is fixed. $\square$

Theorem 3 is the whole content of "three-dimensional": two free initial numbers for the cycle plus one forward coordinate. A single locked history (a clock whose amplitude and phase are both functions of its own $t$, like the hands of a wall clock relative to the date) reaches a one-dimensional set however many coordinates one writes down. Note that free initial data suffice: the family of free clocks, each with constant $r$ (Theorem 7), already fills the space because $r_0$ varies across the family. Variation of $r$ along a single history requires driving or damping (Section 5).

**Theorem 4 (push ignores the cycle).** $\kappa$ depends on the spine $c(t)$ alone, not on $r$ or $\theta$.

*Proof.* $k=\dot T$ is built from $c$ only. $\square$

**Theorem 5 (bend is not rate).** With $t$ the arc length of the spine ($|\dot c|=1$), the spacing of successive cycles along the spine per unit $t$ is unchanged by any bend.

*Proof.* Spacing is $|\dot c|\,\Delta t=\Delta t$, independent of $\dot T$. $\square$

Direction (bend, $\kappa$) and rate (dilation, $|\dot c|$ relative to another clock) are independent quantities. A change of rate shows as cycles bunching along the spine; a bend shows as the spine turning.

**Theorem 6 (Thomas precession of the phase origin, rotor clocks).** Let a rotor clock (Postulate 5, case (i)) move with velocity $\mathbf v$ and proper acceleration $\mathbf a$ relative to an inertial frame of the room, with $\gamma=(1-v^{2}/c^{2})^{-1/2}$. Its Fermi–Walker-transported phase origin precesses, relative to the phase origin of a free clock carried by parallel transport in that frame, at the angular velocity
$$\boldsymbol\Omega_T=\frac{\gamma^{2}}{\gamma+1}\,\frac{\mathbf a\times\mathbf v}{c^{2}}.$$
For a clock in uniform circular motion at angular frequency $\omega_{\rm orb}$ the magnitude is $(\gamma-1)\,\omega_{\rm orb}$, opposite to the orbital sense.

*Proof.* Fermi–Walker transport along an accelerated worldline is the composition of infinitesimal boosts; boosts in different directions do not commute, and their commutator is a rotation at the rate displayed. This is Thomas's result [Thomas 1926, 1927], in the form given in standard texts [Misner, Thorne and Wheeler 1973, §§6.5–6.6 for Fermi–Walker transport, §41.4 for Thomas precession]. $\square$

**Theorem 6′ (point-oscillator clocks).** For a point-oscillator clock (Postulate 5, case (ii)) the phase origin is unchanged by any push: the connection is flat and the phase is a rotation scalar, so $\boldsymbol\Omega_T=0$.

*Proof.* Immediate from Postulate 5(ii). $\square$

**Theorem 6″ (wave clocks).** For a wave clock (Postulate 5, case (iii)) carried along a path on which $\hat{\mathbf k}$ sweeps a closed loop enclosing solid angle $\Omega$ on the sphere of directions, the phase origin returns shifted by the geometric phase $\gamma=-\sigma\,\Omega$, with $\sigma=\pm1$ the helicity, independently of the path's speed and of the wavelength.

*Proof.* Parallel transport of the polarisation along the loop traced by $\hat{\mathbf k}$ has holonomy equal to the enclosed solid angle; the two helicity states acquire opposite phases. This is Berry's phase for light, observed in a helically wound optical fibre by Tomita and Chiao [1986]. $\square$

Theorems 6, 6′ and 6″ are the one place where the push reaches the fibre, and they say it reaches it differently for three kinds of clock. By Theorem 4 the push does not change $r$ or the rate of $\theta$ for any clock. By Theorem 6 it turns the *origin* from which $\theta$ is read for a rotor clock at the Thomas rate; by Theorem 6′ it leaves the origin of a point oscillator alone; by Theorem 6″ it shifts the origin of a wave clock by a geometric phase that depends only on the directions swept. All three are standard physics: a gyroscope precesses, an atomic coherence does not, light in a coiled fibre picks up Berry's phase. What the representation adds is the statement that the three kinds of clock differ in exactly this one coordinate, and a test that separates them: carry one of each around the same loop and compare their zeros on return.

**Theorem 7 (uniform rotation is a complex structure).** A linear flow $\dot x=Ax$ on $\mathbb{R}^{2}$, $A\neq0$, has every orbit closed with the same period $2\pi/\omega$ iff $A^{2}=-\omega^{2}I$, i.e. iff $A=\omega J$ with $J^{2}=-I$.

*Proof.* Closed orbits with common period force the eigenvalues to be $\pm i\omega$; by Cayley–Hamilton, $A^{2}-(\operatorname{tr}A)A+(\det A)I=0$ with $\operatorname{tr}A=0$, $\det A=\omega^{2}$. Conversely $A^{2}=-\omega^{2}I$ gives eigenvalues $\pm i\omega$, so $A$ is diagonalisable over $\mathbb{C}$ and every orbit is an ellipse of period $2\pi/\omega$. $\square$

With Definition 10, Theorem 7 run forward is the law of a free clock: $\dot z=i\omega z$, with $|z|=r$ constant. Uniform rotation is not something the model has to force; it is what a cycle on an oriented fibre does when nothing pushes it.

## 4. Measurement and units

**Classical clocks.** The phase $\theta$ is read by a phase detector, or as the beat note against a reference oscillator. The amplitude $r$ is read by an envelope or power detector against the noise-floor amplitude $A_0$ of Definition 9. Both are standard metrology, and both are clock-to-clock comparisons. Under the structural reading that is what makes them temporal: they are measured the way time is measured, by comparing cycles.

**Quantum clocks.** For a coherent state $|\alpha\rangle$, $(r,\theta)=(|\alpha|,\arg\alpha)$ exactly, with $A_0$ the zero-point amplitude, and homodyne detection reads both quadratures. The fibre is the complex plane of amplitudes; Definition 10 is therefore not an extra assumption for a quantum clock but a description of it.

**Grain.** Number–phase uncertainty, $\Delta n\,\Delta\theta\gtrsim\tfrac12$ with $n=r^{2}$, means a quantum clock's $r$ and $\theta$ cannot both be sharp. A classical clock at temperature $T$ has the thermal analogue: phase diffusion with variance proportional to $1/r^{2}$ in the units of Definition 9. The fibre has a minimum grain in both cases, set by the floor. The idealised model of Sections 2–3 does not contain this; it is a feature of physical clocks the theory inherits.

**Amplitude is not inert.** In a pendulum the rate depends on amplitude (the circular error, $T\approx T_0(1+\theta_0^{2}/16)$). Amplitude and proper time are already coupled in real clocks; this supports treating $r$ as temporal and does not touch Theorem 5, which concerns the spine.

**Orientation is relational.** Interference intensity goes as $1+V\cos\Delta\theta$, which is even in $\Delta\theta$; a single phase-difference reading cannot reveal which way the fibre turns. Two clocks read in two quadratures can. Definition 12 therefore has observable content only as agreement between clocks, which is precisely what Definition 11 asserts.

**Evidence that the conditions hold.** Proposition 1's dynamical ground is not hypothetical. Amplitude-dependent frequency shifts are evaluated as systematics in every primary frequency standard. In the first accuracy evaluation of the NIST-F2 caesium fountain, the type B uncertainty was dominated by microwave-amplitude-dependent effects [Heavner et al. 2014; see also Gibble 2015]. In strontium optical lattice clocks the lattice light shift has a nonlinear intensity dependence (hyperpolarizability), measured and cancelled to the $10^{-19}$ level at an operational lattice depth [Ushijima, Takamoto and Katori 2018]. Phase precision scaling with amplitude is the quantum projection noise limit, observed in trapped-ion frequency standards by Itano et al. [1993], and spin squeezing moves clocks past it. These measurements confirm that $r$ enters both the rate and the resolution of real clocks. They do not, and cannot, prefer the present representation over a one-dimensional account with clock-state variables, because both give the same numbers.

## 5. Examples

**Atomic clock.** $\theta$ is the local oscillator's phase, $r$ its amplitude over the noise-floor amplitude, $t$ its proper time. All three are measured. That they are *coordinates of time* rather than properties of the instrument is the interpretive claim of this paper; the measurements themselves are not in dispute.

**Elevator.** With the cable cut the occupant is weightless: straight spine, $\kappa=0$, a free clock. Standing on the floor at rest, the floor pushes: bent spine, $\kappa=g/c$. Gravity does not bend the spine; it curves the room. The floor bends the spine.

**The helix.** Constant $r$ and a straight spine give $\gamma(s)=(r_0,\omega s,vs)$, the helix $(r_0\cos\omega s,\,r_0\sin\omega s,\,vs)$ when drawn in a plane. It is a free clock with a steady cycle, and by Theorem 3 a *family* of such helices with free $r_0$ fills the space while any one of them is a one-dimensional history. The helix is the free case of the model, not a different model.

**Damped clock.** An undriven clock with damping has $r(t)=r_0e^{-t/\tau}$: its history spirals inward to $z=0$. A dead clock is pure linear time. A driven clock has $r$ rising or wandering. Variation of $r$ along a history is the signature of a non-free clock; it is not required for Theorem 3.

**Clock face and calendar.** The same time of day recurs on a different date: recurrence without repetition in everyday form. But the hands are a fixed function of the date, so this is one locked history and reaches a one-dimensional set. It is the negative example for Theorem 3.

**Quantum phase.** A stationary state's phase $e^{-iEt/\hbar}$, plotted as $(\operatorname{Re},\operatorname{Im},t)$, is the helix again, with $r$ constant. A superposition of two energies has a free relative phase and a measurable one; a coherent state has free amplitude and phase. The latter is the nearest physical instance of the full $(r,\theta,t)$.

**Gyroscope, atom and light on a loop.** A gyroscope is a rotor clock: carried around a circular orbit it returns with its axis, its phase origin, turned by $2\pi(\gamma-1)$ relative to a free clock's (Theorem 6). An atomic clock on the same orbit is a point-oscillator clock: its phase origin returns unturned (Theorem 6′). Light sent along a helically coiled fibre is a wave clock: its propagation direction sweeps a cone, and its polarisation returns rotated by the enclosed solid angle (Theorem 6″) [Tomita and Chiao 1986]. For laboratory speeds $\gamma-1$ is of order $v^{2}/2c^{2}$ and the gyroscope's angle is minute; the fibre's angle, by contrast, is of order one and was seen directly.

## 6. Implications and relation to prior work

1. **Time is per system.** Each clock carries its own three-dimensional temporal state; there is no universal three-dimensional time. Relativity already makes proper time a property of the worldline. This proposal adds two coordinates to it, as a fibre over the worldline.
2. **Comparison between clocks is relativity's.** Arrow angle is relative velocity (Definition 7); push is proper acceleration (Definition 6); the transport of the fibre is Fermi–Walker. The model adds nothing there. All novelty is inside the fibre.
3. **Linear time is the origin.** With Definition 10, a clock with no cycle is the point $z=0$; the projection of any temporal event onto ordinary time is $z\mapsto0$. "Emergent linear time" is a one-symbol map.
4. **Why three.** Corollary 2: a one-mode cycle has a two-dimensional state space, plus proper time. A clock with $m$ independent cycles has $(2m+1)$-dimensional time. The number three is the number for the simplest clock, not a constant of nature.
5. **Space is in the room, not in time.** This is the reverse of proposals in which space is a byproduct of a three-dimensional time [Kletetschka 2025], and it is why none of the metric-reading obstructions [Tegmark 1997; Craig and Weinstein 2009; Bars 2001] apply: the fibre carries no metric and the room keeps its ordinary signature.
6. **One arrow, two guises.** By Definition 12, reversing the fibre's orientation is time reversal. The forward direction of $t$ and the turning direction of the cycle are correlated, and the pair is fixed once the arrow of $t$ is. No entropy enters anywhere in the construction.
7. **Push reaches the fibre only through its origin, and differently for three kinds of clock.** Theorems 4–6″: acceleration leaves $r$ and the rate alone for every clock; it turns the phase origin of a rotor clock at the Thomas rate, leaves the origin of a point oscillator alone, and shifts the origin of a wave clock by a geometric phase. The model thereby sorts clocks into three kinds by one coordinate.
8. **The curved room is already tested.** Fermi–Walker transport is defined on curved backgrounds, and in a gravitational field a rotor clock's phase origin acquires the geodetic and frame-dragging drifts in addition to Thomas precession. Gravity Probe B measured both on orbiting gyroscopes: a geodetic drift of $6601.8\pm18.3$ mas/yr against the predicted $6606.1$, and frame-dragging of $37.2\pm7.2$ mas/yr against $39.2$ [Everitt et al. 2011]. The spine's rate in a curved room is the gravitational redshift, seen between optical clocks 33 cm apart [Chou et al. 2010]. Neither measurement distinguishes this representation from standard physics; both confirm that the rotor's zero mark and the oscillator's rate behave in a curved room as Postulate 5 and Theorem 5 say.

The construction is compatible with relational programmes that derive spacetime from causal order and counting: those supply the room of Postulate 5, and the present proposal decorates each worldline with a phase map and an amplitude map.

**Scope.** This paper is a representation result. Theorems 1–7, Proposition 1 and Corollary 2 hold under Definitions 1–13 and Postulate 5, and every quantity in them is one that standard physics already computes for an oscillator carried along a worldline. No number is predicted that a one-dimensional proper time with clock-state variables does not also give. What the representation adds is a geometry: one object $(z,t)$, one free law $\dot z=i\omega z$, ordinary time as the origin, acceleration as bend, Thomas precession and Berry's phase as rotations of the temporal fibre, and an orientation that is time reversal's arrow. The scope is semiclassical: $t$ as a coordinate presupposes a worldline, so a quantum clock in a superposition of worldlines is outside it. The scope is also one-mode: Corollary 2 states the count for $m$ independent modes, but coupled modes in a single device, and how their fibres combine, are not treated here.

The single assumption that could carry empirical content is a *physical tube*: the claim that a clock's cycle occupies a region of spacetime around its worldline, with the fibre's two directions realised as spatial directions of extent $r\tau_0c$. Nothing in this paper depends on that reading, and nothing here supports it; Postulate 5 explicitly denies it. If it were adopted, two things would follow. First, the tube would stay unfolded only while $r\tau_0\kappa<1$, i.e. $r<c/(a\tau_0)$: the amplitude ratio below the number of periods that fit in the Rindler time $c/a$ [Rindler 1966]. This is the Born-rigidity bound for an accelerated extended body, and its scale is forced by dimensional analysis, $c/a$ being the only time that can be built from $a$ and $c$. For a 1 Hz clock at one $g$ the bound is $r<3.1\times10^{7}$; for a caesium clock, $r<2.8\times10^{17}$; no laboratory clock approaches either. Second, two clocks whose tubes overlap would be the place to look for a consequence. Both statements belong to the physical-tube reading, not to the representation. The wave clock of Postulate 5(iii) is the natural place to pursue that reading, since for a wave the dial is already laid out in space along $\hat{\mathbf k}$, one turn per wavelength.

## 7. Beyond this paper

**A physical tube.** Whether the fibre of Postulate 5 can be read as a region of spacetime (Section 6, Scope), and what overlapping tubes would imply. This is the only route from representation to prediction, and it is deliberately not taken here; the wave clock of Postulate 5(iii) is where it would start.

## References

- Bars, I. (2001). Survey of two-time physics. *Classical and Quantum Gravity* 18 (16), 3113–3130. arXiv:hep-th/0008164.
- Chou, C. W., Hume, D. B., Rosenband, T. and Wineland, D. J. (2010). Optical clocks and relativity. *Science* 329 (5999), 1630–1633. doi:10.1126/science.1192720.
- Cole, E. A. B. (1978). Subluminal and superluminal transformations in six-dimensional special relativity. *Il Nuovo Cimento B* 44, 157–166.
- Craig, W. and Weinstein, S. (2009). On determinism and well-posedness in multiple time dimensions. *Proceedings of the Royal Society A* 465 (2110), 3023–3046. arXiv:0812.0210.
- Dorling, J. (1970). The dimensionality of time. *American Journal of Physics* 38, 539–540.
- Everitt, C. W. F., et al. (2011). Gravity Probe B: final results of a space experiment to test general relativity. *Physical Review Letters* 106, 221101. arXiv:1105.3456.
- Gibble, K. (2015). Comment on "First accuracy evaluation of NIST-F2". *Metrologia* 52, 163–166.
- Heavner, T. P., Donley, E. A., Levi, F., Costanzo, G., Parker, T. E., Shirley, J. H., Ashby, N., Barlow, S. and Jefferts, S. R. (2014). First accuracy evaluation of NIST-F2. *Metrologia* 51 (3), 174–182. doi:10.1088/0026-1394/51/3/174.
- Itano, W. M., Bergquist, J. C., Bollinger, J. J., Gilligan, J. M., Heinzen, D. J., Moore, F. L., Raizen, M. G. and Wineland, D. J. (1993). Quantum projection noise: population fluctuations in two-level systems. *Physical Review A* 47 (5), 3554–3570. doi:10.1103/PhysRevA.47.3554.
- Kletetschka, G. (2025). Three-dimensional time: a mathematical framework for fundamental physics. *Reports in Advances of Physical Sciences*. doi:10.1142/S2424942425500045.
- Misner, C. W., Thorne, K. S. and Wheeler, J. A. (1973). *Gravitation*. W. H. Freeman. §6.5 (the tetrad Fermi–Walker transported by an observer with arbitrary acceleration), §6.6 (the local coordinate system of an accelerated observer), §41.4 (Thomas precession via spinor algebra).
- Rindler, W. (1966). Kruskal space and the uniformly accelerated frame. *American Journal of Physics* 34 (12), 1174–1178. doi:10.1119/1.1972547.
- Tegmark, M. (1997). On the dimensionality of spacetime. *Classical and Quantum Gravity* 14 (4), L69–L75. arXiv:gr-qc/9702052.
- Thomas, L. H. (1926). The motion of the spinning electron. *Nature* 117 (2945), 514. doi:10.1038/117514a0.
- Thomas, L. H. (1927). The kinematics of an electron with an axis. *Philosophical Magazine*, Series 7, 3 (13), 1–22. doi:10.1080/14786440108564170.
- Tomita, A. and Chiao, R. Y. (1986). Observation of Berry's topological phase by use of an optical fiber. *Physical Review Letters* 57, 937–940.
- Ushijima, I., Takamoto, M. and Katori, H. (2018). Operational magic intensity for Sr optical lattice clocks. *Physical Review Letters* 121, 263202. doi:10.1103/PhysRevLett.121.263202.
