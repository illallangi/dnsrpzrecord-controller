dnsrpzrecord-controller
============

DNS Response Policy Zone Record Controller

Uses DNSRPZRecord CRD and Service objects to create a RPZ zone which can be transferred to a DNS server and advertise the services into DNS.

Install
-------

    kubectl apply -f https://github.com/illallangi/dnsrpzrecord-controller/releases/latest/download/crd.yaml
    kubectl apply -f https://github.com/illallangi/dnsrpzrecord-controller/releases/latest/download/deploy.yaml
