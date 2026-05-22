# 🚗 AlphaCare Insurance Solutions (ACIS) — Exhaustive Interim Analytical Report
### Advanced Portfolio Risk Optimization, Feature Engineering, and Data Governance Infrastructure

**Author:** Quantitative Marketing Analytics Engineering Unit  
**Submission Milestone:** Interim Evaluation — Sunday, 24 May 2026, 8:00 PM UTC  
**Academic Steering Panel:** Kerod, Mahbubah, Feven  
**Development Integrity Repository:** https://github.com/Benareyo/insurance-risk-analytics (Active Branch: main)

---

## 1. Comprehensive Executive & Strategic Business Understanding

### 1.1 Corporate Mission and Market Placement
AlphaCare Insurance Solutions (ACIS) is executing an aggressive market expansion program within the highly saturated South African automotive underwriting sector. Historically, underwriting operations in this territory have relied on rigid, flat-tariff schedules built upon high-level customer indicators. While historically simple to administer, this baseline approach creates systematic premium inefficiencies: it overcharges low-volatility, safe customer segments, driving them toward competitors, while underpricing high-risk segments, creating severe underwriting deficits.

To capture market share sustainably while ensuring long-term profitability, ACIS must transition from traditional intuition-based operations to an evidence-driven, risk-adjusted pricing system. This project investigates an 18-month historical dataset of policy transactions, customer demographics, geographic parameters, and financial claims outlays spanning February 2014 to August 2015. 

### 1.2 Core Analytical Insurance Metrics
Portfolio performance and premium adjustment parameters are guided by two fundamental derived mathematical anchors:

* **Loss Ratio (LR):** The primary operational metric evaluating systemic portfolio risk exposure and underwriting profitability. It reflects the fraction of incoming premium cash inflows consumed directly by outlays:
    $$Loss\ Ratio = \frac{\text{TotalClaims}}{\text{TotalPremium}}$$
* **Net Operating Margin:** The absolute financial cash contribution preserved per underwriting policy bound over a designated temporal frame:
    $$\text{Margin} = \text{TotalPremium} - \text{TotalClaims}$$

### 1.3 Strategic Segmentation Mechanics
The ultimate objective of this analytical track is to establish an automated optimization engine that evaluates these two metrics to:
1.  **Identify Low-Risk Segments:** Discover driver profiles and regional nodes where the Loss Ratio is consistently low, enabling ACIS to safely reduce premium barriers to maximize customer acquisition rates.
2.  **Mitigate Underwriting Leakage:** Ensure premium structures are accurately aligned with high-volatility segments, preserving a stable cash position.

---

## 2. Granular Data Ingestion, Profiling, & Cleaning Matrix

The underlying database covers comprehensive relational feature groups across five explicit operational dimensions.

### 2.1 Complete Relational Feature Group Taxonomy
* **Policy & Inception Attributes:** `CoverID`, `PolicyID`, `TransactionMonth`, `TermFrequency`, `CalculatedPremiumPerTerm`, `SumInsured`, `ExcessSelected`
* **Client Demographics:** `IsVATRegistered`, `Citizenship`, `LegalType`, `Title`, `Language`, `Bank`, `AccountType`, `MaritalStatus`, `Gender`
* **Geographic Telematics:** `Country`, `Province`, `PostalCode`, `MainCrestaZone`, `SubCrestaZone`
* **Vehicle Specifications:** `ItemType`, `Mmcode`, `VehicleType`, `RegistrationYear`, `Make`, `Model`, `Cylinders`, `Cubiccapacity`, `Kilowatts`, `Bodytype`, `NumberOfDoors`, `VehicleIntroDate`, `CustomValueEstimate`
* **Safety Risk Flags:** `AlarmImmobiliser`, `TrackingDevice`, `CapitalOutstanding`, `NewVehicle`, `WrittenOff`, `Rebuilt`, `Converted`, `CrossBorder`, `NumberOfVehiclesInFleet`

### 2.2 Advanced Data Quality Audit & Structural Imputation Strategy
A rigorous initial profiling scan of the tabular inputs revealed missing entries and data type discrepancies that could degrade downstream machine learning models. The following engineering strategies were implemented:

* **Vehicle Valuation Imputation (`CustomValueEstimate`):** Missing values in asset valuations were identified. Rather than utilizing a generic global average—which would introduce severe structural bias—missing entries were handled via median value imputation stratified across specific `VehicleType`, `Make`, and `Bodytype` clusters.
* **Temporal Calibration (`RegistrationYear`):** Missing parameters in production timelines were resolved using median production years indexed by vehicle `Make`. This variable was then transformed into an active predictive feature reflecting physical depreciation:
    $$\text{VehicleAge} = 2016 - \text{RegistrationYear}$$
* **Safety Matrix Imputation (`AlarmImmobiliser`, `TrackingDevice`):** Missing entries within vehicle anti-theft fields were cross-referenced. These blanks represent an explicit structural absence ("No Device Installed") rather than a random data omission, and were encoded as distinct categorical groups to preserve their risk signaling value.

---

## 3. Explanatory Data Analysis (EDA) Insights & Portfolio Profiling

### 3.1 Resolving the Core Underwriting Inquiries

#### Q1: What is the overall Loss Ratio, and how does it vary by Province, VehicleType, and Gender?
The global portfolio displays a right-skewed, heavy-tailed claim footprint. The vast majority of policy terms generate consistent, zero-claim premium revenues, while a small percentage of high-severity incidents account for the bulk of total outlays. 
* **Provincial Variation:** Deep geographic mapping reveals that the dense metropolitan traffic networks of **Gauteng** present an elevated baseline Loss Ratio compared to the **Western Cape**. This disparity is driven by higher urban congestion and accident frequencies, justifying localized base premium weighting rules.
* **Vehicle Type Variation:** Commercial transit vehicles and high-performance passenger sedans reflect heightened claim frequencies, whereas consumer compact family models and SUVs generate stable, positive operating margins.
* **Gender Profiling:** Initial descriptive tracking indicates minor variations in historical claim distributions between gender groups, establishing a clear baseline for rigorous statistical testing in Task 3.

#### Q2: What are the distributions of key financial variables, and do extreme anomalies exist?
Continuous variables such as `TotalClaims`, `TotalPremium`, and `CustomValueEstimate` deviate sharply from normal Gaussian distributions, following log-normal, Pareto-like shapes instead. Box plot isolation identified extreme claims outlays reaching hundreds of thousands of Rand. These heavy-tailed variations can distort traditional parametric linear algorithms, highlighting the need for robust tree-based machine learning ensembles (Random Forest, XGBoost).

#### Q3: Are there clear temporal trends over the 18-month historical span?
Plotting historical transaction volumes against the `TransactionMonth` series reveals noticeable seasonal fluctuations. Claim severity spikes during major winter travel and December holiday windows. This variance confirms that risk exposure is dynamic, reinforcing the strategic business case for a pricing framework that accounts for seasonality rather than relying on fixed annual models.

#### Q4: Which vehicle makes/models are associated with the highest and lowest claim amounts?
Premium luxury import passenger models are heavily correlated with extreme claim severity structures. This pattern is directly tied to the high import costs of specialized replacement components and complex repair logistics in South Africa. Conversely, high-volume consumer baseline models track at lower claim severities, making them excellent targets for acquisition discounts.

---

## 4. Industry-Standard Data Version Control (DVC) Implementation

In highly regulated financial environments, reproducibility is a strict compliance requirement. Every data transformation, analysis, and model score must be fully auditable for compliance review, debugging, or pipeline refinement. 

### 4.1 Split-Tracking Infrastructure Architecture
To establish an enterprise-grade workflow, the repository decouples source code from large dataset files using **Data Version Control (DVC)**. Git tracks lightweight, cryptographic pointer metadata hashes (the `.dvc` tracking schema), while the heavy raw data payloads are safely synchronized to an external, isolated local remote caching storage hub. This setup ensures complete tracking of data history without bloating the main repository.

### 4.2 Pipeline Reproduction Blueprint for Technical Stakeholders
To safely reproduce the exact data state matching this Interim submission from any clean computer environment, engineers can run the following sequence:

```bash
# Fetch production branch infrastructure code
git clone [https://github.com/Benareyo/insurance-risk-analytics.git](https://github.com/Benareyo/insurance-risk-analytics.git)
cd insurance-risk-analytics
git checkout main

# Re-pull the verified cryptographic data payload snapshot
python -m dvc pull