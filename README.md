# Static_Filters
This project has been developed with the aim of optimizing the performance of Juniper routers. For this, several static filters have been used, filtering common for all the neighbors. However, the idea behind these filters can be also applied to routers of other brands.

**Bogon ASN filtering**: private or reserved ASNs have no place in the public DFZ (Default Free Zone). The DFZ helps cushion accidental exposure from internal routing devices. In other words, a bogon can be any Internet resource that, according to the registration authority, should not appear on any network. A good behavior would be to reject all EBGP routes that contain an ASN Bogon anywhere in the AS_PATH.

**Bogon Prefix filtering**: there are prefixes that should be filtered as the IETF does not intend for these to be routed to the public network.

**No small prefix filtering**: Any BGP configuration must include a small prefix filter. This avoids hijacks targeting /32 networks or lesser prefixes. Most of the small prefixes seen in Internet communications are incorrect leaks due to misconfiguration or traffic engineering. By using these filters, no information will be lost as, in general, the largest prefixes advertised by the same IXP or transit source will be visible. It is true that there are small IP networks such as /29 or /28, but they are very few. It is important to note that these networks would also be filtered. However, the shortage of IPv4 address space is not a sufficient reason not to use these types of filters. Therefore, routes less than /24 for IPv4 or /48 for IPv6 should not be expected to have global routing capability.

**Filter Long AS Paths**: some networks greatly exceed the number of ASs that precede them. This enables the type of malicious attack that was discovered many years ago. At the time of doing this project, AS_PATHs of a maximum of 40 ASNs are known. Therefore, a safe number in the filter would be 100 AS in the AS_PATH.

**Filter Known transit Networks in AS Paths**: Through an IXP, Tier 2 and Tier 3 networks should not advertise prefixes with a transit network on the AS_PATH as it is probably they are not any of their clients. Also for the same reason, none of your clients should be accepted through one of your clients. In short, filter the list of Tier 1 ASs.
