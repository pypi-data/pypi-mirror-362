The TPX3 raw data consists of sections of raw bytes, which is referred to packet

- The physical process of the neutron detection is as follows:
    * The neutron hits the MCP detector, generating lots of alpha particles.
    * The alpha particles traversing through the MCP channels, accelerated by the applied voltage.
    * The alpha particle could eventually hit the TPX3 sensors, each particle (with enough power) will trigger a hit registered by the TPX3 chip.
    * The TPX3 chip accumulating data, and send them to the Spider board, which handles translating the analog signals into the raw tpx3 data format, along with the TDC timestamp packet (and other many metadata packets) as fast as possible, which is achieved by forgo the temporal ordering of the packets.

- Each section starts with a special header packet, which contains information about which chip the section data comes from (for tpx3 at VENUS, we have four chips, but there are other system that only has one), and the estimated number of packets available in this section.

- Within the section, there is no guarantee that the later packet arrives late, instead, it has a somewhat long range temporal order, but short-range temporal disorder.

- There are many types of packets within a section, but for the analysis we are doing, we only cares two: TDC packet and data packet.

- TDC packet is inserted into the section for the four chips whenever the neutron target send a pulse, indicating the generation of neutrons. Subtracting the TDC timestamp from the data packet timestamp, we can get the time for the neutron to go from the neutron source to the detector, aka time of flight (TOF). This TOF will be the core of our analysis.

- In extremely rare occasion, the TDC packet can be corrupted and missing from section, in which case we can correct the TOF by subtract a full cycle from the calculated TOF, which is assuming that we at most will only miss one TDC.

- In some cases, due to the short range disordering, the TDC data packet is inserted late, resulting TOF calculated from data packet referencing the wrong TDC timestamp (previous one). The subtract one cycle trick also takes care of this issue as well.

- For the target beamline VENUS, we have high throughput requirement, i.e. 120m hits/sec. But we also have a very powerful computer, AMD EPYC 9174 with 32 cores and 739 GB memory. In previous implementation, FastSophiread, we used TBB at the outmost loop and achieved the speed. So technically we should be able to achieve the same speed with this implementation.

- The previous implementation used TBB at the outmost loop, which is okay for demonstration purpose, but difficult for integrating into our data acquisition system. In this implementation, we will use TBB at the inner loop, which is more suitable for integration into our data acquisition system.

- The current implementation, tdcsohpiread, has a solid raw data to hits calculation that leverages TBB at the inner loop, and we would like to do the same for the process where we convert hits into neutrons.

- Although the current code is developed with VENUS in mind, the library itself is tended to be generic so that it can be used for other beamlines at SNS as well, which is why we use configuration system to specify the specifics.

- Our offline analysis revealed that the spiderboard, although it is not doing any time sorting, is still pushing out data in sections following a certain order. In order words, we do have somewhat periodicity in the data, and this is something we can leverage for parallel processing. For example, the four neighboring sections (assuming four chip tpx3 detector at VENUS) often provide a full view of the detector for a rough given period of time.

- Converting hits into neutrons is a two-step process:
    * First, we need to group the hits into a group where we belive they are from the same neutron event. This is done by grouping hits that are within a certain time window and are spacially close to each other (or closely related to each other). Previously we are using a adaptive box search method, which is fast but not very accurate. We would like to retain the capability to add other clustering method in the future, such as our previously failed attempt of using graph clustering method.
    * Second, we need to convert the grouped hits into neutrons, which is done by calculating the position of tof of the neutron based on the informaiton from hits. Currently, we are mainly using weighted average (center of gravity) method as it is fast. We also have a fast Gaussian fitting method for this step. In the future, we may also implement a more accurate method based on the time of flight distribution of the neutrons.

- All of this means we need to develop a architecture that is
    * Has something similar to a factory pattern to allow users to specify the clustering method and the neutron conversion method (we call this fitting method).
    * Has a way to allow the users to specify the configuration for the clustering method and the fitting method.
    * The process itself should be parallelized.
    * Similar to the previous step (raw -> hits), we need to be mindful about memory usage and performance. Avoid copying data around and use efficient data structures should help.

- The paralleization of the hits to neutron part could leverage the periodicity of the data, just like the failed graph cluterting attempt. I think we were very close to getting teh right solution, but we are tied down due to the bad software architecutre. This time, we should try the parallization strategy for the simple ABS first. If we can get it working, then we can venture into getting the more complex graph clustering method, or even dbscanning method to work.
