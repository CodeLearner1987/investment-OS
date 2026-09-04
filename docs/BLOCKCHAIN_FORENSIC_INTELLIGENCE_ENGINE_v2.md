# Blockchain Forensic Intelligence Engine v2

## Purpose

Extend investment-OS into a multi-source blockchain forensic research layer that treats the blockchain ledger as primary evidence and market/data providers as independent corroborating layers.

The system must distinguish **addresses** from **economic actors** and **transfers** from verified economic purchases/sales.

## Evidence hierarchy

1. **Primary:** chain RPCs, explorers, contract events, transaction receipts, token Transfer/Mint/Burn events.
2. **On-chain analytics:** Dune, Coin Metrics, Nansen and comparable providers.
3. **Market data:** CoinGecko, CoinMarketCap, CEX APIs, DEX APIs.
4. **Protocol fundamentals:** DeFiLlama, Token Terminal, official tokenomics, governance, treasury disclosures.

A secondary provider must never silently override primary evidence.

## Core pipeline

```text
Asset / Contract
      |
      v
Chain Resolver -> Contract Verification
      |
      v
Raw Ledger / RPC / Explorer
      |
      +--> Transaction Decoder
      +--> Token Supply Engine
      +--> Wallet Graph
      +--> DEX/CEX Flow Engine
      |
      v
Transaction Classifier
      |
      +--> VERIFIED_BUY
      +--> VERIFIED_SELL
      +--> TRANSFER
      +--> MINT
      +--> BURN
      +--> STAKE/UNSTAKE
      +--> BRIDGE
      +--> LIQUIDITY
      +--> UNKNOWN
      |
      v
Wallet Cluster / Sybil Analysis
      |
      v
Economic Actor Reconstruction
      |
      v
Cross-Source Reconciliation
      |
      v
Evidence Locker
      |
      v
Bull / Bear / Contradiction Research
      |
      v
Accumulation / Distribution / Supply / Fundamental Scores
      |
      v
Final Forensic Report
```

## Wallet deception / clustering layer

Never equate holder count with independent ownership.

Detect probable wallet relationships using observable evidence such as:

- common funding sources
- common CEX withdrawal origins
- synchronized activation
- synchronized buying/selling
- repeated common counterparties
- common contract interaction sequences
- consolidation into shared destination wallets
- recurring timing patterns
- downstream exchange deposits
- repeated behavioral similarity across observation periods

Do not identify a human or organization unless independently verified. Label results as:

- `KNOWN_ENTITY`
- `PROBABLE_CLUSTER`
- `POSSIBLE_CLUSTER`
- `UNKNOWN`

Maintain both:

- **gross observed activity**
- **cluster-adjusted activity**

Never erase raw addresses after clustering.

## Purchase classification

A token movement is a `VERIFIED_BUY` only when the available transaction evidence demonstrates an exchange of the target token for another economic asset, such as a DEX swap.

A plain wallet-to-wallet transfer is never a purchase by default.

For each classified event retain:

- chain
- contract address
- wallet/address
- transaction hash
- block number
- timestamp
- token quantity
- counter-asset
- counter-asset quantity
- estimated USD value
- venue/protocol
- source
- classification
- confidence

## Required metrics

### Supply

- total supply
- circulating supply
- max supply
- minted
- burned
- locked
- staked
- treasury
- team/insider where verified
- unlocked
- circulating-supply growth
- dilution rate

### Ownership

- holder count
- top 10/25/50/100 concentration
- whale concentration
- concentration change
- probable wallet clusters
- exchange-held supply
- treasury-held supply

### Flow

- gross verified buys
- gross verified sells
- net verified buying
- transfers
- exchange inflows
- exchange outflows
- net exchange flow
- bridge flow
- staking flow
- liquidity-pool flow

### Market

- price
- market cap
- FDV
- volume
- volatility
- DEX liquidity
- CEX liquidity when available

### Fundamentals

- active addresses
- transaction activity
- TVL
- fees
- revenue
- protocol usage
- treasury activity

## Cross-examination rules

Every material thesis must have:

1. supporting evidence
2. contradictory evidence
3. unresolved evidence
4. data-quality assessment
5. confidence level

Use:

- `FACT` — directly verified
- `CALCULATED` — deterministic calculation from verified data
- `INFERRED` — interpretation based on observable evidence
- `UNKNOWN` — insufficient evidence

Never present inference as fact.

## Required investigation output

For each asset produce:

1. Executive summary
2. Contract and chain verification
3. Supply structure
4. Holder distribution
5. Verified buying
6. Verified selling
7. Wallet clusters
8. Whale behavior
9. Exchange flows
10. Liquidity
11. Protocol/network fundamentals
12. Price confirmation
13. Dilution/unlock risk
14. Anomalies
15. Contradictory evidence
16. Five scores
17. Final classification
18. Evidence ledger

Scores:

- Accumulation: 0-100
- Distribution: 0-100
- Supply risk: 0-100
- Fundamental strength: 0-100
- Market confirmation: 0-100

Do not collapse these into a single score until the underlying evidence is displayed.

## Model routing

Use the strongest reasoning model for:

- thesis formation
- conflict resolution
- forensic interpretation
- final report
- adversarial bull/bear review

Use lower-cost/high-throughput models for:

- transaction normalization
- address labeling
- preliminary classification
- metadata extraction
- repetitive calculations

The model is not the source of truth. The evidence store is.

## Minimum viable implementation

Phase 1:

- asset/contract registry
- RPC/explorer ingestion
- ERC-20/SPL-style transfer ingestion where supported
- DEX swap classification
- supply accounting
- wallet graph
- evidence records

Phase 2:

- Dune integration
- CoinGecko integration
- DeFiLlama integration
- exchange labeling
- wallet clustering
- time-series dashboards

Phase 3:

- automated contradiction detection
- anomaly detection
- cluster-adjusted accumulation
- multi-chain graph analysis
- scheduled monitoring
- alerting

Phase 4:

- integrate with investment-OS research agents
- bullish researcher
- bearish researcher
- risk manager
- portfolio/research decision layer

## Golden rule

**Do not ask whether wallets are buying. Reconstruct the economic event and prove whether the observable evidence supports a purchase.**

The system's goal is not to predict price directly. Its goal is to detect changes and divergences across:

**SUPPLY -> OWNERSHIP -> CAPITAL FLOW -> LIQUIDITY -> NETWORK ACTIVITY -> ECONOMICS -> PRICE**

and determine whether those variables confirm or contradict the investment thesis.