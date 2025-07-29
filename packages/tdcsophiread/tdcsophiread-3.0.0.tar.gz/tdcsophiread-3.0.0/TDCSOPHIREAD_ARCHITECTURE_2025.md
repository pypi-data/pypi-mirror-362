# TDCSophiread Architecture Guide 2025

**Date**: 2025-01-13  
**Status**: Active Development  
**Goal**: Achieve >120M hits/sec clustering throughput with iterator-based parallel architecture  
**Target Hardware**: M2 Max (development), AMD EPYC 9174F (production)

## Executive Summary

This document defines the refactored TDCSophiread architecture that addresses fundamental flaws in the previous implementation. The new design enables true parallel processing through iterator-based interfaces, proper worker pool management, and temporal batching that leverages TPX3 data characteristics.

**Key Changes**:
- Iterator-based clustering interface for zero-copy processing
- Configuration management at algorithm instantiation
- Proper worker pool with algorithm instances per worker
- Statistical temporal batching for all clustering algorithms
- Memory-efficient parallel architecture

---

## Architecture Overview

```
┌──────────────────────────────────────────────────────────────────────────┐
│                           TPX3 Raw Data Processing                        │
│                    (Existing TDCProcessor - Working Well)                 │
└────────────────────────────────────────────────────┬─────────────────────┘
                                                     │
                                    ┌────────────────────────────┐
                                    │  std::vector<TDCHit>       │
                                    │  Temporally ordered hits    │
                                    └────────────────┬───────────┘
                                                     │
┌──────────────────────────────────────────────────────────────────────────┐
│                        NEW: Temporal Neutron Processor                   │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │ Phase 1: Statistical Analysis                                    │    │
│  │  - Analyze hit distribution across temporal windows              │    │
│  │  - Calculate optimal batch sizes and overlaps                   │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │ Phase 2: Worker Pool Processing                                 │    │
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐│    │
│  │  │   Worker 0      │  │   Worker 1      │  │   Worker N      ││    │
│  │  │ ┌─────────────┐ │  │ ┌─────────────┐ │  │ ┌─────────────┐ ││    │
│  │  │ │IHitClustering│ │  │ │IHitClustering│ │  │ │IHitClustering││    │
│  │  │ │ cluster()   │ │  │ │ cluster()   │ │  │ │ cluster()   ││    │
│  │  │ └─────────────┘ │  │ └─────────────┘ │  │ └─────────────┘ ││    │
│  │  │ ┌─────────────┐ │  │ ┌─────────────┐ │  │ ┌─────────────┐ ││    │
│  │  │ │INeutronExtr │ │  │ │INeutronExtr │ │  │ │INeutronExtr ││    │
│  │  │ │ extract()   │ │  │ │ extract()   │ │  │ │ extract()   ││    │
│  │  │ └─────────────┘ │  │ └─────────────┘ │  │ └─────────────┘ ││    │
│  │  └─────────────────┘  └─────────────────┘  └─────────────────┘│    │
│  └─────────────────────────────────────────────────────────────────┘    │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │ Phase 3: Result Aggregation & Deduplication                     │    │
│  │  - Combine neutrons from all workers                            │    │
│  │  - Remove duplicates from overlap regions                       │    │
│  └─────────────────────────────────────────────────────────────────┘    │
└────────────────────────────────────────────────────┬─────────────────────┘
                                                     │
                                    ┌────────────────────────────┐
                                    │  std::vector<TDCNeutron>   │
                                    │  Final neutron events      │
                                    └────────────────────────────┘
```

---

## Core Interface Design

### 1. Hit Clustering Interface

```cpp
class IHitClustering {
public:
    // Configuration management
    virtual void configure(const HitClusteringConfig& config) = 0;
    virtual const HitClusteringConfig& getConfig() const = 0;
    
    // Iterator-based processing for zero-copy operation
    virtual size_t cluster(std::vector<TDCHit>::iterator begin,
                          std::vector<TDCHit>::iterator end) = 0;
    
    // State management - clear data, preserve configuration
    virtual void reset() = 0;
    
    // Results access
    virtual const std::vector<int>& getClusterLabels() const = 0;
    virtual std::string getName() const = 0;
    virtual size_t getLastHitCount() const = 0;
};
```

### 2. Neutron Extraction Interface

```cpp
class INeutronExtraction {
public:
    // Configuration management
    virtual void configure(const NeutronExtractionConfig& config) = 0;
    virtual const NeutronExtractionConfig& getConfig() const = 0;
    
    // Extract neutrons from clustered hits
    virtual std::vector<TDCNeutron> extract(
        std::vector<TDCHit>::iterator begin,
        std::vector<TDCHit>::iterator end,
        const std::vector<int>& cluster_labels) = 0;
    
    // State management
    virtual void reset() = 0;
    virtual std::string getName() const = 0;
};
```

### 3. Main Neutron Processor Interface

```cpp
class INeutronProcessor {
public:
    virtual void configure(const NeutronProcessingConfig& config) = 0;
    virtual std::vector<TDCNeutron> processHits(const std::vector<TDCHit>& hits) = 0;
    virtual std::string getHitClusteringAlgorithm() const = 0;
    virtual std::string getNeutronExtractionAlgorithm() const = 0;
    virtual double getLastProcessingTimeMs() const = 0;
    virtual double getLastHitsPerSecond() const = 0;
};
```

### 4. Enhanced Factory Pattern

```cpp
class HitClusteringFactory {
public:
    static std::unique_ptr<IHitClustering> create(
        const std::string& algorithm_name,
        const HitClusteringConfig& config);
};

class NeutronExtractionFactory {
public:
    static std::unique_ptr<INeutronExtraction> create(
        const std::string& algorithm_name,
        const NeutronExtractionConfig& config);
};

class NeutronProcessorFactory {
public:
    static std::unique_ptr<INeutronProcessor> create(
        const NeutronProcessingConfig& config);
};
```

### 5. Temporal Neutron Processor Architecture

```cpp
class TemporalNeutronProcessor : public INeutronProcessor {
private:
    // Worker pool with owned instances
    struct Worker {
        std::unique_ptr<IHitClustering> clusterer;
        std::unique_ptr<INeutronExtraction> extractor;
        std::vector<TDCNeutron> results;
    };
    std::vector<Worker> workers_;
    
public:
    // Main processing interface
    std::vector<TDCNeutron> processHits(const std::vector<TDCHit>& hits) override;
    
    // Configuration management
    void configure(const NeutronProcessingConfig& config) override;
};
```

---

## Configuration Architecture

### Configuration Hierarchy

```cpp
struct NeutronProcessingConfig {
    // Hit clustering configuration
    HitClusteringConfig clustering;
    
    // Neutron extraction configuration  
    NeutronExtractionConfig extraction;
    
    // Temporal processing configuration
    TemporalProcessingConfig temporal;
    
    // Performance settings
    PerformanceConfig performance;
};

struct HitClusteringConfig {
    std::string algorithm;  // "abs", "graph", "dbscan"
    
    // Algorithm-specific configurations
    ABSConfig abs_config;
    GraphConfig graph_config;
    // ... other algorithm configs
};

struct NeutronExtractionConfig {
    std::string algorithm;  // "centroid", "gaussian", "ml"
    
    // Algorithm-specific configurations
    CentroidConfig centroid_config;
    GaussianConfig gaussian_config;
    // ... other extraction configs
};

struct TemporalProcessingConfig {
    size_t num_workers;              // 0 = auto-detect
    size_t min_batch_size;           // Minimum hits per batch
    size_t max_batch_size;           // Maximum hits per batch
    double overlap_factor;           // Overlap multiplier (3.0 for 3σ)
    bool enable_deduplication;       // Remove duplicate neutrons
    double deduplication_tolerance;  // Spatial tolerance for duplicates
};
```

---

## Implementation Strategy

### Phase 1: Core Interfaces (Week 1)
**Goal**: Implement clean interfaces from scratch

1. **Create New Interface Headers**:
   - `neutron_processing.h` - Main interfaces
   - `hit_clustering.h` - Clustering algorithm interface
   - `neutron_extraction.h` - Extraction algorithm interface
   - `neutron_config.h` - Configuration structures

2. **Implement Basic Framework**:
   - Factory pattern for algorithm creation
   - Configuration management system
   - Basic worker pool structure

3. **Create Simple Test Implementation**:
   - Simple ABS clustering algorithm
   - Simple centroid extraction
   - Basic processor that combines them

**Deliverables**:
- Clean interface headers
- Basic implementation framework
- Unit tests for interfaces

### Phase 2: ABS Implementation (Week 2)
**Goal**: Complete ABS clustering with temporal batching

1. **Implement ABSHitClustering**:
   - Iterator-based clustering algorithm
   - Proper reset() functionality
   - Configuration management

2. **Implement CentroidNeutronExtraction**:
   - Extract neutron properties from clusters
   - Sub-pixel position calculation
   - Amplitude and timing consolidation

3. **Create TemporalNeutronProcessor**:
   - Statistical hit distribution analysis
   - Temporal batch creation
   - Worker pool management

**Deliverables**:
- Working ABS implementation
- Temporal processing framework
- Integration tests

### Phase 3: Performance Optimization (Week 3)
**Goal**: Achieve >120M hits/sec throughput

1. **Memory Optimization**:
   - Zero-copy iterator processing
   - Pre-allocated worker memory
   - Cache-friendly data layouts

2. **Parallel Efficiency**:
   - Optimal batch sizing
   - Load balancing strategies
   - Minimize synchronization overhead

3. **Performance Validation**:
   - Benchmark on M2 Max
   - Scale testing on EPYC 9174F
   - Compare with existing implementation

**Deliverables**:
- Performance-optimized implementation
- Comprehensive benchmarks
- Scaling analysis

### Phase 4: Algorithm Extensions (Week 4)
**Goal**: Add graph clustering and prepare for future algorithms

1. **Graph Clustering Implementation**:
   - GraphHitClustering with iterator support
   - Spatial hash optimization
   - Union-Find algorithm

2. **Advanced Extraction Methods**:
   - Gaussian fitting extraction
   - ML-based extraction framework

3. **Documentation and Tools**:
   - Algorithm development guide
   - Performance analysis tools
   - Integration documentation

**Deliverables**:
- Multiple clustering algorithms
- Advanced extraction methods
- Complete documentation

---

## Critical Success Factors

### 1. Zero-Copy Processing
- Iterators eliminate data copying between workers
- Direct memory access to hit ranges
- Minimal memory bandwidth usage

### 2. Configuration Management
- Algorithms configured at creation
- Configuration preserved across resets
- Thread-safe configuration updates

### 3. Worker Pool Efficiency
- One algorithm instance per worker
- No shared state between workers
- Minimal synchronization overhead

### 4. Memory Efficiency
- Bounded memory per worker
- Pre-allocated data structures
- Memory pool reuse

### 5. **CRITICAL: TPX3 Data Structure Constraints**

**⚠️ FUNDAMENTAL PROHIBITION: NEVER SORT HITS BY TOF OR TIMESTAMP ⚠️**

The TPX3 data format imposes critical constraints that MUST be understood:

1. **TOF is Periodic (0-16.67ms)**: TOF represents time-of-flight calculation that resets every 16.67ms (60Hz pulse rate). Sorting by TOF destroys the inherent temporal structure and creates artificial boundaries.

2. **TOF ≠ Absolute Time**: TOF is calculated as `data_timestamp - TDC_timestamp`, representing the flight time within a pulse period, NOT a monotonic timeline.

3. **Long-Range Temporal Order**: Hits maintain natural temporal order from hardware acquisition, but short-range disorder exists within packets.

4. **Sequential Dependencies**: TDC state propagation requires processing in acquisition order to maintain correct timestamp corrections.

**VIOLATIONS OF THIS CONSTRAINT WILL:**
- Break neutron correlation across pulse boundaries
- Create incorrect temporal clustering
- Destroy performance due to cache misses
- Lead to fundamentally incorrect physics results

**LEGACY CODE VIOLATION**: The previous implementation contained `ClusterProcessingUtils::sortHitsByTimestamp()` which sorted by TOF - this was the source of clustering failures and has been disabled.

**CORRECT APPROACH**: Leverage the natural temporal order and periodic structure through statistical batching that respects pulse boundaries.

---

## Risk Mitigation

### Technical Risks

1. **Iterator Invalidation**
   - Risk: Modifying hits during processing
   - Mitigation: Const iterators or separate label storage

2. **Load Imbalance**
   - Risk: Uneven batch sizes
   - Mitigation: Dynamic work stealing or adaptive batching

3. **Memory Fragmentation**
   - Risk: Frequent allocations/deallocations
   - Mitigation: Memory pools and pre-allocation

### Implementation Risks

1. **Backward Compatibility**
   - Risk: Breaking existing code
   - Mitigation: Maintain old interfaces alongside new

2. **Performance Regression**
   - Risk: New architecture slower than expected
   - Mitigation: Continuous benchmarking and profiling

---

## Validation Strategy

### Correctness Testing
1. Unit tests for each algorithm with iterators
2. Integration tests for temporal processor
3. Physics validation against known datasets
4. Comparison with existing implementation

### Performance Testing
1. Micro-benchmarks for algorithm components
2. End-to-end throughput measurements
3. Scaling tests across core counts
4. Memory usage profiling

### Production Validation
1. Test with real VENUS data
2. Validate 120M hits/sec requirement
3. Long-running stability tests
4. Integration with DAQ system

---

## Development Principles

### Code Quality
- Clear separation of concerns
- Comprehensive documentation
- Extensive unit testing
- Performance regression tests

### Architecture Principles
- Favor composition over inheritance
- Minimize shared state
- Design for testability
- Optimize for common case

### Performance Guidelines
- Profile before optimizing
- Measure, don't guess
- Cache-conscious design
- Minimize allocations

---

## Future Extensions

### Algorithm Support
- DBSCAN clustering
- ML-based clustering
- Advanced peak fitting methods

### Hardware Support
- GPU acceleration readiness
- SIMD optimizations
- NUMA-aware processing

### Integration Features
- Streaming processing support
- Online/offline mode switching
- Dynamic configuration updates

---

**Document Status**: Living document - will be updated throughout implementation  
**Next Update**: After Phase 1 completion  
**Approval**: Required before implementation begins