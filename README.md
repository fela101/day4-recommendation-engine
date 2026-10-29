# Grocery Recommendation Engine

A Python-based collaborative filtering recommendation engine that processes customer purchase histories, cleans and validates raw CSV records, computes customer similarity using Jaccard indices, and generates explainable, scored product recommendations.

---

## Approach & Architecture

The recommendation engine uses a **neighborhood-based collaborative filtering** approach:
1. **Customer History Modeling**: Each customer is represented by a unique set of purchased product IDs.
2. **Similarity Metric (Jaccard Index)**: Measures overlap between two customers' product histories:
   $$J(A, B) = \frac{|A \cap B|}{|A \cup B|}$$
3. **Candidate Generation**: For a target customer, the engine finds the top-$k$ most similar customers (neighbors) and collects products bought by those neighbors that the target customer has not yet purchased.
4. **Weighted Scoring Formula**: Candidates are scored and ranked using a multi-component heuristic combining neighbor similarity, support count, and global product popularity.

---

## How to Run

### Prerequisites
* Python 3.8+
* Required libraries: standard library modules (`csv`, `pathlib`, `argparse`, `typing`).

### Execution via Command Line / Script
Run the script directly from your terminal or script runner:
```bash
python main.py --input data/purchases.csv --output output/recommendations.csv --count 3
```

### Execution via Jupyter Notebook
If running inside a Jupyter Notebook, ensure `argparse` ignores notebook runtime arguments by passing an empty list to `parse_args`:
```python
args = parser.parse_args([])
```
Then execute your `main()` function:
```python
if __name__ == "__main__":
    main()
```

### CLI Arguments
* `--input`: Path to the input purchase CSV file (default: `data/purchases.csv`).
* `--output`: Path to save the generated recommendations CSV (default: `output/recommendations.csv`).
* `--count`: Number of top recommendations to generate per customer (default: `3`).

---

## Data-Cleaning & Validation Rules

The `read_purchases()` function loads raw CSV files using `utf-8-sig` encoding and validates each row against strict data integrity rules. 

### Mandatory Headers
The CSV header row must include:
* `customer_id`
* `product_id`
* `product_name`

### Rejection Criteria (Rejected Rows)
A row is moved to the rejected list with an explicit reason if any of the following occur:
1. **Extra Columns**: Row contains more values than defined by the header.
2. **Blank IDs / Names**: `customer_id`, `product_id`, or `product_name` is blank or whitespace-only.
3. **Invalid Quantity**: If the optional `quantity` column is present, it must be a positive whole integer ($> 0$). Blank quantities or non-numeric values cause rejection. (If the `quantity` column is absent from the CSV, it defaults to `1`).

### Normalization
* All column headers are stripped and case-folded (`casefold()`).
* Customer IDs and Product IDs are stripped and case-folded to prevent duplicate tracking due to casing discrepancies.

---

## Ranking & Scoring Rules

For each candidate product, a composite score is computed using three weighted components:

**Composite Score Formula:**
```text
Score = (0.7 * Mean Neighbor Similarity) + (0.2 * Support Ratio) + (0.1 * Popularity Ratio)
```

1. **Mean Neighbor Similarity (70%)**: The average Jaccard similarity score of the neighboring customers who purchased the candidate product.
2. **Neighbor Support Ratio (20%)**: The number of unique neighbors who bought the product divided by total neighbor count ($k$).
3. **Global Popularity Ratio (10%)**: The total purchase frequency of the product across the entire dataset divided by the maximum popularity of any single product.

### Tie-Breaker Sorting Order
Candidates are sorted descending by:
1. Composite `score`
2. `support_count` (number of supporting neighbors)
3. `popularity` (global purchase count)
4. `product_id` (alphabetical ascending order for deterministic stability)

---

## Worked Example

Let’s walk through a concrete numerical example of how recommendations are generated for a customer.

### Step 1: Customer Purchase Histories
* **Customer C1** bought: `[Milk, Bread, Butter]` -> Set size = 3
* **Customer C2** bought: `[Milk, Bread, Eggs]` -> Set size = 3
* **Target Customer C3** bought: `[Milk, Bread]` -> Set size = 2

### Step 2: Compute Similarities to Customer C3
* **Similarity with C1**: 
  * Intersection = `{Milk, Bread}` (count = 2)
  * Union = `{Milk, Bread, Butter}` (count = 3)
  * $J(C3, C1) = \frac{2}{3} \approx 0.667$
* **Similarity with C2**: 
  * Intersection = `{Milk, Bread}` (count = 2)
  * Union = `{Milk, Bread, Eggs}` (count = 3)
  * $J(C3, C2) = \frac{2}{3} \approx 0.667$

### Step 3: Candidate Product Identification ($k=2$)
* C1 and C2 are our top 2 neighbors.
* Unseen products bought by neighbors (excluding what C3 already owns):
  * **Butter** (bought by C1, similarity = $0.667$)
  * **Eggs** (bought by C2, similarity = $0.667$)

### Step 4: Scoring Candidate "Butter"
Assume:
* Supporting neighbor: C1 (similarity = $0.667$)
* Support count = $1$, Neighbor count ($k$) = $2$ -> Support Ratio = $\frac{1}{2} = 0.5$
* Global product popularity for Butter = $5$, Max dataset popularity = $10$ -> Popularity Ratio = $\frac{5}{10} = 0.5$

```text
Score(Butter) = (0.7 * 0.667) + (0.2 * 0.5) + (0.1 * 0.5)
Score(Butter) = 0.4669 + 0.10 + 0.05 = 0.617
```

---

## Assumptions & Design Decisions
1. **Implicit Feedback Binary Interaction**: Purchase history tracks distinct item ownership per customer using mathematical sets (multiple purchases of the same item by the same customer collapse into a unique presence flag for Jaccard modeling).
2. **Cold Start Handling**: Customers with no purchase history or unknown IDs raise appropriate exceptions (`KeyError`), while customers with unique baskets that share zero overlap with others fall back to global popularity ranking.
3. **Deterministic Output**: Sorting keys always include ID tie-breakers to guarantee reproducible CSV exports across different machine environments.