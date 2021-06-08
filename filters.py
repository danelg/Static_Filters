#!/usr/bin/python

import sys, getopt
from jnpr.junos import Device
from jnpr.junos.utils.config import Config

def configure(destination, username, password):
   dev=Device(host=destination, user=username, password=password)
   dev.open()
   dev.bind(cfg=Config)

   config_text="""
   policy-options {
       as-path-group bogon-asns{
           as-path zero ".* 0 .*";
   	   as-path as_trans ".* 23456 .*";
	   as-path examples1 ".* [64496-64511] .*";
	   as-path examples2 ".* [65536-65551] .*";
	   as-path reserved1 ".* [64512-65534] .*";
	   as-path reserved2 ".* [4200000000-4294967294] .*";
	   as-path last16 ".* 65535 .*";
	   as-path last32 ".* 4294967295 .*";
	   as-path iana-reserved ".* [65552-131071] .*";
           }
           policy-statement import_from_ebgp{
               term bogon-asns {
                   from as-path-group bogon-asns;   
                   then reject;
               }   
           }
           prefix-list BOGONS_v4 {
                   0.0.0.0/8;
                   10.0.0.0/8;
                   100.64.0.0/10;
                   127.0.0.0/8;
                   169.254.0.0/16;
                   172.16.0.0/12;
                   192.0.2.0/24;
                   192.88.99.0/24;
                   192.168.0.0/16;
                   198.18.0.0/15;
                   198.51.100.0/24;
                   203.0.113.0/24;
                   224.0.0.0/4;
                   240.0.0.0/4;
           }
           policy-statement BGP_FILTER_IN {
               term IPv4 {
                   from {
                       prefix-list BOGONS_v4;
                   }
                   then reject;
               }
           }
           policy-statement bgp-import-policy1 {
               term reject_too_small_prefixes_v4 {
                   from {
                       route-filter 0.0.0.0/0 prefix-length-range /25-/32;
                   }
                   then {
                       reject;
                   }
               }
           }
           policy-statement bgp-import-policy2 {
               term no-long-paths {
                   from as-path too-many-hops;
                   then reject;
                   }
               }
           as-path too-many-hops ".{100,}";
        
           policy-statement bgp-import-policy {
               term no-transit-leaks {
                   from as-path no-transit-import-in;
                   then reject;
               }
              }

    as-path no-transit-import-in ".* (174|209|701|702|1239|1299|2914|3257|3320|3356|3549|3561|4134|5511|6453|6461|6762|7018).*";
    }
                
   """
   dev.cfg.load(config_text, format='text', merge=True)
   #COMMIT:
   dev.cfg.commit()
   dev.close()

def main(argv):
   destination = ''
   username = ''
   password = ''
   try:
      opts, args = getopt.getopt(argv,"hd:u:p:",["help","destination=","username=","password="])
   except getopt.GetoptError:
      print ('filters.py -d <destination IP> -u <username> -p <password>')
      sys.exit(2)
   if (opts[0][0] in ("-h", "--help") or len(opts) == 3 ):
     for opt, arg in opts:
        if opt in ("-h", '--help'):
           print ('filters.py -d <destination IP> -u <username> -p <password>')
           sys.exit()
        elif opt in ("-d", "--destination"):
           destination = arg
        elif opt in ("-u", "--username"):
           username = arg
        elif opt in ("-p", "--password"):
           password = arg
     configure (destination, username, password)
   else:
     print ('ERROR: you should use the following sintax:\nfilters.py -d <destination IP> -u <username> -p <password>\nfilters.py -h <help>')

if __name__ == "__main__":
   main(sys.argv[1:])