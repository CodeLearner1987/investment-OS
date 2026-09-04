# Blockchain Forensic Intelligence Layer

This module turns blockchain activity into auditable investment evidence.

## First principle

**An address transfer is not automatically a buy or sell.** A `VERIFIED_BUY`
or `VERIFIED_SELL` requires evidence of an economic exchange, such as a
 decoded DEX swap. Transfers, mints, burns, staking, bridges, LP activity,
and treasury movements remain separately classified.

## Pipeline

`asset registry -> raw chain/RPC -> decoded events -> transaction classifier -> wallet clustering -> economic-actor reconstruction -> reconciliation -> evidence locker -> research agents`

## Wallet deception controls

The engine preserves every raw address and separately calculates candidate
clusters using operational fingerprints such as shared funding sources,
shared counterparties, synchronized activation, and common exchange
withdrawal/deposit destinations. A cluster is a hypothesis, not an identity.

Reports must show both:

- **Gross address activity** — what the ledger directly observed.
- **Cluster-adjusted activity** — activity after applying explicitly scored
  clustering hypotheses.

Never collapse these into one number.

## Evidence labels

- `FACT`: directly observed or sourced from a primary record.
- `CALCULATED`: deterministic calculation from facts.
- `INFERRED`: model/heuristic conclusion supported by evidence.
- `UNKNOWN`: insufficient evidence.

## Provider roles

- Blockchain RPC/explorer: primary ledger evidence.
- Dune: decoded/indexed SQL analytics and cross-wallet queries.
- CoinGecko: market, DEX, liquidity and holder context.
- Coin Metrics: network/fundamental metrics.
- DeFiLlama: protocol economics, TVL, fees, revenue and unlock context.

No provider is treated as the sole source of truth.

## Next implementation stage

Build chain adapters and fixture-backed tests for Ethereum first, then add
additional chains behind the same evidence interface. Required outputs are
verified buys, verified sells, transfers, mints/burns, holder distribution,
wallet clusters, exchange flows, supply changes, liquidity, price/volume,
contradictory evidence, and confidence.
