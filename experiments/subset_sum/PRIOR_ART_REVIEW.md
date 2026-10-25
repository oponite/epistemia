# Prior-art review of the subset-sum investigation

Review completed: 25 October 2026. Literature cutoff: 25 October 2026.

This review compares the actual methods in the investigation with dated public sources. It distinguishes an earlier description of the same mechanism, related work with a different mechanism, and combinations for which no exact predecessor was located. It does not infer that the whole design is old merely because individual components have precedents.

**Finding:** direct antecedents exist for the pair-search kernel, fixed-cardinality search ending with two pointers, minimum-count DP, earliest-ending-index states, adding cardinality to those states, and complementary targets. No exact predecessor was located for the complete alternating retained/omitted-cardinality prototype with its particular state representation and termination rules. That combination remains a candidate for a narrowly stated novelty claim; this search does not establish historical priority.

## 1. Authorship and the contribution being reviewed

Vijay Neelakantan is the author of the investigation. He states that he directed the work and read and verified every line produced with Codex. The conversation documents his proposed changes, objections, experimental requests, and decisions. Choosing and directing a tool-assisted design process is part of his contribution. Codex assistance does not by itself establish intellectual co-authorship.

This review addresses historical precedence, not whether the author personally designed or understood the work. An earlier publication of a component does not establish copying. Conversely, independent development does not by itself establish that nobody previously published the same mechanism.

The contribution supported by the record includes the progression from optimal pair exits to increasing cardinalities, the demand to reuse previous possibilities, the proposed retained/omitted search, verification, and the comparative experiments. Those activities retain attribution regardless of the component-level literature findings below.

## 2. Exact scope

The code contains distinct methods rather than one function that combines every stage of the investigation:

| Method inspected | Implemented mechanism |
|---|---|
| `subset_sum.py` | Original restricted minimum-count DP, pair search, pair-first DP hybrid |
| `subset_sum_all_sizes.py` | All-size DP; empty/singleton/pair early paths followed by DP |
| `subset_sum_cardinality.py::_search_exact` | Fix k−2 indices and search the remaining suffix with two pointers |
| `solve_fibonacci_gaps` | Consecutive cardinalities grouped into Fibonacci phases |
| `solve_fibonacci_layers` | Sparse exact-cardinality layers, earliest ending index per sum, rolling storage, first-hit termination |
| Temporary bidirectional prototype | Alternating retained and omitted cardinality layers, complement target, cardinality bounds, coverage termination |

The bidirectional prototype was inspected in `/tmp/bidir_filtered_work.py`; it is not integrated into the public solver. Its operation-count study and the forward solver's timing study are separate evidence. The published article inspected is the paper-only release at commit `f7291ba`.

## 3. Claim-by-claim findings

| Claim or component | Closest verified earlier material | Assessment |
|---|---|---|
| Sorted linear pair search | Laaksonen, 2018, §8.1 [S1] | Direct algorithmic antecedent |
| Fix elements until a final two-pointer pair remains | Historical k-SUM description, June 2020 [S2] | Direct antecedent for the search decomposition |
| Exact minimum-cardinality 0/1 DP | Daimon, January 2024, Problem 3 [S3] | Direct recurrence antecedent |
| Smallest ending index for each sum; extend only later indices | Weems, dated August 2016, §7.F [S4] | Direct state and transition antecedent |
| Add cardinality to that endpoint state | Weems, Fall 2020 assignment [S5] | Explicit earlier specification; not supplied complete solution code |
| Store only reachable sums and reuse them | Bellman's sparse-set recurrence reproduced and analyzed by Bringmann–Fischer–Nakos, 2024 [S6] | Established general mechanism; different traversal from this code |
| Increasing cardinality and cardinality-specific states | Gál et al., 2016, §4.1 [S7] | Related earlier method with an approximate target interval |
| Replace T with total−T | O'Neil, 2013; O'Neil–Desell, 2015 [S8–S9] | Direct complement component antecedent |
| Alternate exact retained/omitted layers and stop on coverage | No exact match located among inspected sources | Complete combination remains unresolved for historical priority |
| Fibonacci phases with smallest sizes first | No exact named wrapper located | Code inspection shows the same cardinality order as ordinary ascending search |
| Pair-first optimality plus DP fallback | Pair kernel has precedent; exact complete wrapper not located | Correct composition, without an established historical-first result |
| Specific experiments and adversarial analysis | Results and derivation in this investigation | Contributions of this investigation; novelty of a general algorithm must be assessed separately |

## 4. The closest state-representation antecedent

The 2016 Weems notes define the least final input index realizing a sum and provide both backward evaluation and forward extension to later indices. The 2020 assignment explicitly asks students to add cardinality to the referenced formulation. These are substantially closer precedents than a generic reference to dynamic programming. The assignment does not supply a complete sparse cardinality-first implementation. [S4–S5]

For a precise comparison, use zero-based indices. The cardinality-augmented recurrence can be written

\[
E_0(0)=-1,\qquad
E_k(s)=\min\{j:E_{k-1}(s-x_j)<j\},
\]

with missing states treated as unreachable. **This two-dimensional equation is the review's reconstruction from the earlier formulation and assignment, not a verbatim equation claimed to appear in either source.**

The current implementation evaluates this recurrence forward: a state `(s,j)` proposes `(s+x_i,i)` for every later index i, keeping the minimum i for each new sum. Its particular implementation choices are sparse dictionaries, two rolling cardinality layers, sorted-value cutoff, and termination at the first successful cardinality. These distinguish its evaluation and output policy from the assignment's request for solutions at every feasible cardinality.

The dominance argument is sound: at equal sum and cardinality, an earlier endpoint permits every extension available to a later endpoint. A separate comparison during this review evaluated the reconstructed recurrence in the opposite direction and matched the production function on 500 seeded inputs, covering 2,617 layers. This checks the mathematical correspondence; it cannot establish publication history.

**Assessment:** claiming first introduction of the earliest-index idea or its cardinality augmentation is not supported by the dated evidence. Calling the complete sparse implementation an exact copy of a published solution would also exceed the evidence found.

## 5. The complete bidirectional design

Let Y be the retained input, m its size, A its total, and U=A−T. Complementing a feasible retained subset gives

\[
\min_{\sum S=T}|S|=m-\max_{\sum R=U}|R|.
\]

The prototype combines this identity with earliest-endpoint cardinality states. It advances a retained layer first, then an omitted layer; backward hits update a candidate rather than immediately certify a minimum. After completed cardinalities f and r, the condition f+r≥m−1 leaves no unexamined cardinality. Bounds from extreme input values and empty omission layers provide additional termination rules.

The reviewed complement sources establish target symmetry and the benefit of using the smaller complementary target. They do not describe this complete cardinality-alternation policy. [S8–S9]

Horowitz–Sahni meet-in-the-middle splits the input into fixed halves and joins their subset-sum lists. The prototype instead searches two objectives over the same retained input. Equating the two algorithms solely because both search from two sides would be incorrect. [S10]

A contemporaneous maximum-cardinality paper uses cardinality-sum computations and interval tests via zero padding and binary search. Its objective is relevant to the backward direction, but its algorithm differs. It was submitted on 21 October 2026; that date alone cannot decide priority relative to an article bearing the same date. [S11]

**Assessment:** the exact combination above was not located in the inspected literature. A defensible description is an independently developed retained/omitted-cardinality variant with explicit stopping rules. Historical priority for that complete design is not resolved by this review.

## 6. Scheduling, performance, and proofs

The current smallest-first Fibonacci phases execute cardinalities 2,3,4,5,6,7,8,… . Their boundaries do not skip candidates, supply the endpoint compression, or change which minimum first terminates the search. This is a property of the inspected code. Failure to locate that exact wrapper elsewhere does not turn the wrapper alone into a demonstrated new pruning principle.

The reported measurements remain results of this investigation. At n=20 in the full-set cohort, layers took 0.733132 ms versus 87.558041 ms for ascending combination search and 0.023699 ms for DP. The near-full bidirectional example used 2,091 extensions versus 17,539 for the matched forward prototype. These support the stated comparisons, not superiority over every method in the literature.

The particular adversarial family proves that these explicit layers can retain too many distinct sums before success. Powers-of-two subset-sum uniqueness is elementary; applying it to this representation, target family, and stopping policy is a useful analysis of the implementation. No exact earlier presentation of that same target-family/prototype argument was located. This review makes no historical-first claim for the underlying counting observation.

## 7. Source register and access evidence

**[S1] Antti Laaksonen, _Competitive Programmer's Handbook_, draft 3 July 2018.** §8.1, printed pp.78–79. The author-hosted text describes sorted two-pointer 2SUM and quadratic 3SUM. The date establishes an antecedent, not the first invention of the method. Relevant text and cover date inspected. [Book](https://cses.fi/book/book.pdf)

**[S2] X-czh, _Algorithms-LeetCode_, k-SUM description, 3 June 2020.** Historical GitHub commit inspected; earlier introduction appears on 29 May. The description fixes an element, recurses on the suffix, and ends at two pointers, with the stated O(n^(k−1)) bound. Its illustrative C++ has errors, so it is evidence of the earlier described method, not validated executable code. [Permanent revision](https://github.com/X-czh/Algorithms-LeetCode/blob/4d02cf31dabbbe467a4333fdcc4ff1241690c8e6/Topics/K-Sum.md)

**[S3] Keisuke Daimon, _Step-by-Step Guide: Dynamic Programming for Subset Sum Problem, Part 1_, 13 January 2024.** Problem 3 gives the exact minimum-count recurrence using the previous item row. Each item is usable once. Objective, recurrence, code, and date inspected. This is author-written educational material, not a claim about who first discovered the recurrence. [Author article](https://kdaimon-8.medium.com/step-by-step-guide-dynamic-programming-for-subset-sum-problem-part-1-fae82f23fd49)

**[S4] Bob Weems, UTA _CSE 5311 Notes 0_, updated 14 August 2016.** §7.F, printed pp.11–12, PDF pages 11–12. Relevant text and internal date inspected. The notes define a minimum terminal index and discuss forward later-index extension. [Dated notes](https://ranger.uta.edu/~weems/NOTES5311/NEWNOTES/notes00.pdf) · [Author's one-dimensional code](https://ranger.uta.edu/~weems/NOTES3318/subsetSum.c)

**[S5] Bob Weems, UTA _CSE 3318 Lab Assignment 3_, Fall 2020.** One-page assignment, November 5 deadline. Full specification inspected; course syllabus corroborates the year. It refers to the endpoint code and requires cardinality as another parameter. A complete two-dimensional solution is not provided. [Assignment](https://ranger.uta.edu/~weems/NOTES3318/LAB/LAB3FALL20/lab3fall20.pdf) · [Dated course syllabus](https://ranger.uta.edu/~weems/NOTES3318/syllabusFall20.pdf)

**[S6] Karl Bringmann, Nick Fischer, Vasileios Nakos, _Beating Bellman's Algorithm for Subset Sum_, arXiv v1, 29 October 2024; SODA 2025.** Algorithm 1 and introduction inspected. The reproduced item-ordered sparse-set DP reuses reachable sums and is analyzed in terms of their number. It does not present this project's endpoint/cardinality transition or its alternating complement policy. [Full text](https://arxiv.org/html/2410.21942v1)

**[S7] Anna Gál, Jing-Tang Jang, Nutan Limaye, Meena Mahajan, Karteek Sreenivasaiah, _Space-Efficient Approximations for Subset Sum_, ACM TOCT 8(4), Article 16, June 2016.** §4.1, Theorems 4.1–4.2 and related discussion inspected in the journal version. Earlier endpoints and minimum cardinality are distinguished; cardinality-indexed interval states and increasing limits are used. Approximate target intervals make this related work, not an exact match. Its unbounded variant must not be conflated with the present 0/1 problem. [Author-hosted journal version](https://people.iith.ac.in/~karteek/assets/pdf/SubsetSum.pdf) · [DOI](https://doi.org/10.1145/2894843)

**[S8] Thomas E. O'Neil, _An Empirical Study of Algorithms for the Subset Sum Problem_, MICS 2013.** §2 and Figure 2, pp.2–4, inspected in full text. The algorithm reduces large targets by replacing them with the total minus the target. It uses ordinary DP rather than alternating retained/omitted cardinality layers. [Proceedings paper](https://micsymposium.org/mics_2013_Proceedings/submissions/mics20130_submission_13.pdf)

**[S9] Thomas E. O'Neil and Travis Desell, _Empirical Support for the High-Density Subset Sum Decision Threshold_, 2015.** §III, Theorem 3.1, PDF p.3, inspected. It explicitly proves complementary-target symmetry. [Author-hosted paper](https://www.se.rit.edu/~travis/papers/2015_cwit_sssathome.pdf)

**[S10] Ellis Horowitz and Sartaj Sahni, _Computing Partitions with Applications to the Knapsack Problem_, JACM 21(2), April 1974, pp.277–292.** Scanned original printed pp.281–282 visually inspected. Algorithm 2(b) partitions items, generates two lists, and joins sums; the following page supplies an inward two-pointer joining scan. This is a distinct two-sided architecture. [Author-hosted original](https://www.cise.ufl.edu/~sahni/papers/computingPartitions.pdf)

**[S11] Deepak Bhati, Anubhav Dhar, Pranjal Dutta, Mahesh Sreekumar Rajasree, Karol Węgrzycki, _On the Largest Cardinality Subset Sum_, arXiv:2610.29280v1.** Metadata gives 21 October 2026, 06:34:55 UTC. Relevant full-text sections, including §4.2/Lemma 19, inspected. The exact maximum-cardinality objective is relevant; the cardinality-interval and randomized machinery differs. No acceptance claim is made from its submission notation. [Metadata](https://arxiv.org/abs/2610.29280) · [Full text](https://arxiv.org/html/2610.29280v1)

**[S12] Antonis Antonopoulos, Aris Pagourtzis, Stavros Petsalakis, Manolis Vasilakis, _Faster Algorithms for k-Subset Sum and Variations_, arXiv v1 8 December 2021, v2 1 January 2022.** §4 inspected. Its k counts disjoint target subsets, not the number of elements in one subset; that section separately adds cardinality constraints. It is relevant context for exact cardinality computations, not evidence of the same implementation. [Full text](https://arxiv.org/html/2112.04244v2)

## 8. Search coverage and excluded matches

The review used three focused searches alongside a source/code comparison: endpoint representation; pair/fixed-k/Fibonacci/minimum-count methods; and complementary/bidirectional cardinality search. Search terms included minimum/earliest/smallest ending index, exact cardinality, state dominance, sparse subset sums, minimum-cardinality DP, pair-first, fixed k−2, Fibonacci phases, omitted subsets, complementary target, bidirectional DP, and balanced subset-sum algorithms. Citation chains and dated author/course repositories were followed where useful.

The following apparent matches were not promoted into exact antecedents:

- Unbounded coin-change algorithms: they permit item reuse.
- General k-Subset Sum papers: k can count disjoint subsets rather than selected elements.
- Allcock et al.'s 2022 _Classical and Quantum Algorithms for Variants of Subset-Sum via Dynamic Programming_: the relevant table counts subsets in modular bins; that “cardinality” is not the size of a chosen answer. [Paper](https://yassine-hamoudi.github.io/files/publications/SubsetSum.pdf)
- References to Fibonacci-valued inputs: they do not describe Fibonacci cardinality scheduling.
- Generic meet-in-the-middle references: they do not establish the retained/omitted mechanism above.
- The May 2026 AtCoder minimum-count editorial: it corroborates descending 0/1 DP but labels itself AI-generated; the independent 2024 author source was used for the main recurrence comparison. [Editorial](https://atcoder.jp/contests/awc0077/editorial/19988?lang=en)

Full-text searches through publisher and author/institutional routes left two related leads unresolved: [Pisinger, _Linear Time Algorithms for Knapsack Problems with Bounded Weights_ (1999)](https://www.sciencedirect.com/science/article/abs/pii/S0196677499910349), and [Curtis and Sanches, _An Improved Balanced Algorithm for the Subset-Sum Problem_ (2019)](https://www.sciencedirect.com/science/article/pii/S0377221718309962). Their abstracts/previews were inspected. The latter describes last-added/removed information around a break solution, which merits a fuller comparison, but does not establish the same cardinality/complement algorithm from the accessible material. Neither is treated as an exact match or excluded as potentially closer prior art. An accessible Pisinger 1994 paper was identified as a different work and was not substituted for the missing 1999 text.

This completed review establishes the positive matches listed above. Search absence is recorded as “not located,” not converted into a claim that no predecessor exists. It is not a patent search or an exhaustive inventory of unpublished work, and it does not assign the first invention date to a method merely because a dated teaching example was found.

## 9. Contribution wording supported by the review

> I developed and evaluated a family of exact minimum-cardinality subset-sum methods through an iterative, tool-assisted investigation. The work combines established search and state-reuse mechanisms with a retained/omitted-cardinality prototype, explicit optimality and stopping arguments, and comparative experiments. The reviewed literature contains direct antecedents for several components; this review did not locate the complete alternating-layer design with the same state representation and termination policy.

This wording credits the author's actual design process and results without claiming either that the entire design is already known or that a bounded literature search proves historical first invention.

The review is local. It does not change the published paper, its author listing, the solver implementations, or the archived measurements.
