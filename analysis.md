Analysis
---

At a high level the solution enumerates the items, doing a allocation based on source item preference, 
and when the partner item is already allocated an attempt to steal is made, before trying the next item's 
preference. The list of items to enumerate grows as steals are succeeded causing orphaned items.

For implemetation simplicity the two sets of items are stored and processed separately.

The algorithm also tracks each steal, to avoid infinite enumeration, meaning an unstable dataset. The 
assumption is that when a match is broken up for a specific steal and source source pairs and two target pairs 
of a steal, and all these 4 actors occur twice then loop has occurred. This assumption is based on the fact that
a pair broken by a stronger pair should not be reversable. In reality a unstable data set may not be possible
but I haven't mathmatically proven that.

### Time Complexity

The problem input data is items with preferences across all other items, so is n^2 in total, however iteration 
through all of these isn't a given for the solution.

The given solution isn't a finite iteration, and uses some unbounded enumeration of the items in both sets of items, 
and then further enumerates those freed up by swappings. The further enumeration is limited by quantity of
required steals to become stable, which could be as many as a full extra dimension of items.

Due to the dimension of preferences and the extra dimension of stealing, on top of the first pass through the items I 
would describe the worst case complexity as O(n^3) (where n is items). Best case complexity would be a single pass 
of first choices so Omega(n). Average case would consider both the average depth of preference required for a match, 
as well as the probability of steals. There is no reason to assume either the preference depth or steal probability 
are less than a fraction of a multiple of n each, so Theta(n^3).

### Space Complexity

Regarding input memory: The algorthm enumerates the input keys, and accesses indexed preferences per item when needed, so can easily stream the 
input. So: O(1).
Regarding auxiliary memory: Maintaining orphaned items (for re-allocation), does require memory, up to O(n). This could be queued and enumerated via a data store for
a larger data set, if frequent steals are experienced overflowing memory.

Note: The dataset is left as a string for names of items. Prior mapping of this to an integer identifier would improve memory utilisation, and in comparison operations throughout the algorithm, causing a constant multiplier reduction in space complexity.  

### Parallelisation and Processor utilisation

The algorithm could be parallelised to deal with separate items per thread, but would need a row level write lock to avoid race conditions.

There are no gains to be made by processor matrix operations.

### Potential improvements

Prior ordering of the input items based on a score of bidirectional preferences, could potentially reduce the average case to Theta(nlogn). This would depend on the
data set, but could be a practical improvement for data sets that can be sorted in memory.

Other Solutions
---

The Gale-Shapley algorithm solves this in O(n^2)
- Gale, D.; Shapley, L. S. (1962). "College Admissions and the Stability of Marriage". American Mathematical Monthly. 
69 (1): 9–14. https://web.archive.org/web/20170925172517/http://www.dtic.mil/get-tr-doc/pdf?AD=AD0251958
-  Iwama, Kazuo; Miyazaki, Shuichi (2008). "A Survey of the Stable Marriage Problem and Its Variants" (PDF). 
International Conference on Informatics Education and Research for Knowledge-Circulating Society (Icks 2008): 
131–136. doi:10.1109/ICKS.2008.7. hdl:2433/226940. ISBN 978-0-7695-3128-1. S2CID 10642344.

The fundemental difference in algorithms is that Gale-Shapley algorithm only enumerates one preference per allocation attempt
(and so doesn't iterate them), so the preferences are enumerated as part of the steal attempts, resulting in the two being entwinned, 
hence the reduction in time complexity from O(n^3) to O(n^2). 

To ensure the CanSteal function doesn't need to iterate the preferences, the preferences are pre-processed into ranks (dictionary of name to 
index). This pre-process step is itself time complexity O(n^2), so is only an addition of same complexity to the overal algorithm, which doesn't affect the overall
O(n^2). It does increase auxilliary memory utilisation as an additional and final space complexity of O(n^2).
Note: that the preference enumeration is achieved through queuing, thus adding no additional memory constraints or space complexity.

Also the Gale-Shapley algorithm focuses on attempt iterations over the first set, without iterating the second set, simplifying the 
solution without adding any increase in complexity class.